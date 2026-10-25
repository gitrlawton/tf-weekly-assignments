"""
Hybrid Retrieval Engine for The Unofficial Guide (Shape C).

Combines:
  1. Lexical BM25 keyword matching (BM25Okapi)
  2. Dense vector cosine embedding search (ChromaDB)
Fuses candidate ranks using Reciprocal Rank Fusion (RRF):
  RRF(d) = 1 / (60 + rank_dense) + 1 / (60 + rank_bm25)
"""

from dataclasses import dataclass
import re
import time
from rank_bm25 import BM25Okapi

import config
from chunker import Chunk
from store import Result, search as dense_search


@dataclass
class HybridResult(Result):
    """Retrieved chunk augmented with hybrid scoring metadata."""

    rrf_score: float = 0.0
    bm25_score: float = 0.0
    dense_rank: int | None = None
    bm25_rank: int | None = None


# Cached in-memory BM25 index: corpus_name -> (BM25Okapi, list[Chunk])
_bm25_cache: dict[str, tuple[BM25Okapi, list[Chunk]]] = {}


def tokenize(text: str) -> list[str]:
    """Tokenize text into lowercase alphanumeric tokens."""
    return [token for token in re.findall(r"\w+", text.lower()) if len(token) > 1]


def get_bm25_index(corpus: str | None = None) -> tuple[BM25Okapi, list[Chunk]]:
    """Build or retrieve cached in-memory BM25 index for a corpus."""
    corpus_name = corpus or config.CORPUS
    if corpus_name in _bm25_cache:
        return _bm25_cache[corpus_name]

    from chunker import split_documents
    from ingest import load_documents

    docs = load_documents(corpus_name)
    chunks = split_documents(docs)

    tokenized_corpus = [tokenize(c.text) for c in chunks]
    bm25 = BM25Okapi(tokenized_corpus)

    _bm25_cache[corpus_name] = (bm25, chunks)
    return bm25, chunks


def bm25_search(
    query: str,
    corpus: str | None = None,
    top_k: int = 15,
) -> list[tuple[Chunk, float, int]]:
    """Search corpus using BM25 lexical keyword matching.

    Returns list of (Chunk, bm25_score, rank_1_indexed).
    """
    bm25, chunks = get_bm25_index(corpus)
    query_tokens = tokenize(query)

    if not query_tokens:
        return []

    doc_scores = bm25.get_scores(query_tokens)

    # Sort descending by score
    scored_indices = sorted(
        range(len(doc_scores)),
        key=lambda i: doc_scores[i],
        reverse=True,
    )

    results: list[tuple[Chunk, float, int]] = []
    for rank_idx, idx in enumerate(scored_indices[:top_k], start=1):
        score = float(doc_scores[idx])
        if score > 0.0:  # only include non-zero keyword matches
            results.append((chunks[idx], score, rank_idx))

    return results


def reciprocal_rank_fusion(
    dense_results: list[Result],
    bm25_results: list[tuple[Chunk, float, int]],
    k: int = 60,
    top_k: int = 5,
) -> list[HybridResult]:
    """Fuse dense vector rankings and BM25 lexical rankings using RRF.

    RRF formula: RRF(d) = sum(1 / (k + rank)) across available ranks.
    """
    # Keyed by chunk label: "filename#index"
    candidates: dict[str, dict] = {}

    # 1. Ingest dense results
    for rank, d_res in enumerate(dense_results, start=1):
        candidates[d_res.label] = {
            "text": d_res.text,
            "source": d_res.source,
            "label": d_res.label,
            "distance": d_res.distance,
            "produced_by": f"{d_res.produced_by}+hybrid",
            "dense_rank": rank,
            "bm25_rank": None,
            "bm25_score": 0.0,
            "rrf_score": 1.0 / (k + rank),
        }

    # 2. Ingest BM25 results
    for chunk, bm25_score, rank in bm25_results:
        label = chunk.label
        if label in candidates:
            candidates[label]["bm25_rank"] = rank
            candidates[label]["bm25_score"] = bm25_score
            candidates[label]["rrf_score"] += 1.0 / (k + rank)
        else:
            # Appeared only in BM25 (not in dense top_k)
            candidates[label] = {
                "text": chunk.text,
                "source": chunk.source,
                "label": label,
                "distance": 0.55,  # default conservative distance below 0.60 gate
                "produced_by": f"{chunk.produced_by}+bm25",
                "dense_rank": None,
                "bm25_rank": rank,
                "bm25_score": bm25_score,
                "rrf_score": 1.0 / (k + rank),
            }

    # Sort descending by fused RRF score
    ranked = sorted(
        candidates.values(),
        key=lambda item: item["rrf_score"],
        reverse=True,
    )

    fused_results: list[HybridResult] = []
    for item in ranked[:top_k]:
        fused_results.append(
            HybridResult(
                text=item["text"],
                source=item["source"],
                label=item["label"],
                distance=round(item["distance"], 4),
                produced_by=item["produced_by"],
                rrf_score=round(item["rrf_score"], 5),
                bm25_score=round(item["bm25_score"], 3),
                dense_rank=item["dense_rank"],
                bm25_rank=item["bm25_rank"],
            )
        )

    return fused_results


def hybrid_search(
    question: str,
    top_k: int | None = None,
    corpus: str | None = None,
    variant: str = "default",
    pool_k: int = 15,
    rrf_k: int = 60,
) -> tuple[list[HybridResult], dict[str, float]]:
    """Execute hybrid search combining Chroma vector search and BM25 search.

    Returns (list[HybridResult], timing_breakdown).
    """
    final_top_k = top_k or config.TOP_K

    t0 = time.perf_counter()
    dense_res = dense_search(question, top_k=pool_k, corpus=corpus, variant=variant)
    dense_ms = (time.perf_counter() - t0) * 1000.0

    t1 = time.perf_counter()
    bm25_res = bm25_search(question, corpus=corpus, top_k=pool_k)
    bm25_ms = (time.perf_counter() - t1) * 1000.0

    t2 = time.perf_counter()
    fused = reciprocal_rank_fusion(dense_res, bm25_res, k=rrf_k, top_k=final_top_k)
    fusion_ms = (time.perf_counter() - t2) * 1000.0

    timings = {
        "dense_ms": round(dense_ms, 2),
        "bm25_ms": round(bm25_ms, 2),
        "fusion_ms": round(fusion_ms, 2),
    }

    return fused, timings
