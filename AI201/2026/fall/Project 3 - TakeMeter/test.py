#!/usr/bin/env python3
"""
AI201 environment check.

Run this before every class:

    python test.py

It checks the things that actually break: your Python version, your virtual
environment, your pinned packages, whether your machine has the disk and
memory a training run needs, and whether the baseline model has been
downloaded. It is the same file in every unit's starter repo — the checks
adapt to whatever that unit's requirements.txt pins.

This pair needs no API key. Nothing here calls a hosted service.

Nothing here touches your project code, and nothing here is graded.
"""

import importlib
import importlib.metadata as md
import os
import platform
import re
import shutil
import sys
from pathlib import Path

# Windows consoles default to a codepage that can't encode the characters this
# file prints, and Python only notices when the output is redirected — so
# `python test.py > log.txt` would crash where the same command on screen is
# fine. Ask for UTF-8 on the way out.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, OSError, ValueError):
        pass


# --- Course-wide pins -------------------------------------------------------
# This pair has no hosted model and no API key. Both models it uses — the
# fine-tune and the zero-shot baseline — run on your machine and are named in
# the notebook and in baseline.py.

MIN_PYTHON = (3, 11)
MAX_PYTHON = (3, 14)  # exclusive — 3.14 breaks the pinned stack
MIN_DISK_GB = 9   # pair 3 steps up: the local baseline model is ~1.6 GB
# 6, not 4. Two things on this machine are memory-hungry: baseline.py peaks
# around 1.8 GB loading the zero-shot model, and the unit 5 training run peaks
# around 2.1 GB. Neither fits comfortably beside an editor and a browser on a
# 4 GB machine.
MIN_RAM_GB = 6

# Distribution name on PyPI -> module name you actually import.
IMPORT_NAMES = {
    "python-dotenv": "dotenv",
    "google-genai": "google.genai",
    "sentence-transformers": "sentence_transformers",
    "rank-bm25": "rank_bm25",
    "rank_bm25": "rank_bm25",
    "scikit-learn": "sklearn",
    "opencv-python": "cv2",
    "pyyaml": "yaml",
    "pillow": "PIL",
    "beautifulsoup4": "bs4",
}

ROOT = Path(__file__).resolve().parent

passed, failed, warned, skipped = [], [], [], []


def report(status, name, detail=""):
    line = f"[{status:<4}] {name}"
    if detail:
        line += f"\n         {detail}"
    print(line)
    {"PASS": passed, "FAIL": failed, "WARN": warned, "SKIP": skipped}[status].append(name)


# --- 1. Python --------------------------------------------------------------

def check_python():
    v = sys.version_info
    actual = f"{v.major}.{v.minor}.{v.micro}"
    if (v.major, v.minor) < MIN_PYTHON:
        return report("FAIL", "Python version", f"Found {actual}. This course needs 3.11 or newer.")
    if (v.major, v.minor) >= MAX_PYTHON:
        return report(
            "FAIL",
            "Python version",
            f"Found {actual}. The pinned packages do not support 3.14 yet — "
            f"install 3.13 and rebuild your virtual environment.",
        )
    report("PASS", "Python version", f"{actual} on {platform.system()}")


def check_venv():
    active = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    if not active:
        return report(
            "FAIL",
            "Virtual environment",
            "Not active. Run the activate command for your OS, then try again. "
            "Installing into your system Python is the most common cause of "
            "'it worked yesterday'.",
        )
    report("PASS", "Virtual environment", sys.prefix)


# --- 2. Packages ------------------------------------------------------------

def parse_requirements(path):
    """Yield (distribution_name, raw_specifier) for each real requirement line."""
    reqs = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#")[0].strip()
        if not line or line.startswith("-"):
            continue
        name = re.split(r"[<>=!~\[;]", line, maxsplit=1)[0].strip()
        if name:
            reqs.append((name, line))
    return reqs


def check_packages():
    req_file = ROOT / "requirements.txt"
    if not req_file.exists():
        return report(
            "FAIL",
            "requirements.txt",
            f"Not found next to test.py. Run this from inside the starter repo folder.",
        )

    missing, wrong = [], []
    for dist, spec in parse_requirements(req_file):
        module = IMPORT_NAMES.get(dist.lower(), dist.replace("-", "_"))
        try:
            importlib.import_module(module)
        except Exception as e:
            missing.append(f"{dist} ({type(e).__name__})")
            continue
        try:
            installed = md.version(dist)
        except md.PackageNotFoundError:
            continue
        if "==" in spec:
            want = spec.split("==")[1].split(",")[0].strip()
            if installed != want:
                wrong.append(f"{dist}: pinned {want}, installed {installed}")

    if missing:
        return report(
            "FAIL",
            "Pinned packages",
            "Could not import: " + ", ".join(missing)
            + "\n         Fix: pip install -r requirements.txt",
        )
    if wrong:
        return report("WARN", "Pinned packages", "; ".join(wrong))
    report("PASS", "Pinned packages", f"all {len(parse_requirements(req_file))} import cleanly")


# --- 3. Machine -------------------------------------------------------------

def total_ram_gb():
    try:
        if hasattr(os, "sysconf") and "SC_PAGE_SIZE" in os.sysconf_names:
            return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 1024**3
        if sys.platform == "win32":
            import ctypes

            class MemStatus(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]

            stat = MemStatus()
            stat.dwLength = ctypes.sizeof(MemStatus)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
            return stat.ullTotalPhys / 1024**3
    except Exception:
        pass
    return None


def check_machine():
    free_gb = shutil.disk_usage(ROOT).free / 1024**3
    if free_gb < MIN_DISK_GB:
        report("FAIL", "Free disk space",
               f"{free_gb:.1f} GB free, need about {MIN_DISK_GB} GB. "
               f"The embedding model and its cache are most of it.")
    else:
        report("PASS", "Free disk space", f"{free_gb:.1f} GB")

    ram = total_ram_gb()
    if ram is None:
        report("SKIP", "Memory", "Could not read total RAM on this OS — check manually.")
    elif ram < MIN_RAM_GB:
        report("WARN", "Memory",
               f"{ram:.1f} GB total, {MIN_RAM_GB} GB recommended. Things will run, "
               f"but close other apps while indexing.")
    else:
        report("PASS", "Memory", f"{ram:.1f} GB")


# --- 4. Secrets -------------------------------------------------------------

def check_torch():
    """Both the baseline and the training run need a backend, on this machine."""
    try:
        import torch
    except ImportError:
        return report("FAIL", "PyTorch",
                      "Not installed. Run: pip install -r requirements.txt")

    if torch.cuda.is_available():
        device = f"NVIDIA GPU ({torch.cuda.get_device_name(0)}) — training will be quick"
    elif getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        device = "Apple Silicon GPU (MPS) — training will use it"
    else:
        device = "CPU only — fine, a three-seed run is minutes not hours"
    report("PASS", "PyTorch", f"{torch.__version__}, {device}")


def check_transformers():
    """The zero-shot baseline and the fine-tune. Models download on first use."""
    try:
        import transformers  # noqa: F401
        from transformers import pipeline  # noqa: F401
    except ImportError as exc:
        return report("FAIL", "Transformers", f"Could not import: {exc}")
    report("PASS", "Transformers", "imports cleanly")


def check_training_deps():
    """What the notebook needs beyond transformers, now that it runs here."""
    missing = []
    for name in ("datasets", "accelerate"):
        try:
            __import__(name)
        except ImportError:
            missing.append(name)
    if missing:
        return report("FAIL", "Training packages",
                      f"Missing: {', '.join(missing)}. "
                      f"Run: pip install -r requirements.txt")
    report("PASS", "Training packages", "datasets and accelerate both import")


def check_baseline_model():
    """Is the ~1.6 GB baseline model already downloaded?"""
    from pathlib import Path as _P

    cache = _P.home() / ".cache" / "huggingface" / "hub"
    if cache.exists() and any("bart-large-mnli" in p.name for p in cache.iterdir()):
        return report("PASS", "Baseline model", "already downloaded")
    report(
        "WARN",
        "Baseline model",
        "Not downloaded yet (~1.6 GB). It downloads on your first run of\n"
        "         baseline.py. Do that BEFORE the unit 6 session, not during it.",
    )


def check_project_files():
    """The notebook and the practice data."""
    missing = [
        name for name in ("takemeter.ipynb", "baseline.py", "agreement.py",
                          "criteria.md", "data/practice_labels.csv")
        if not (ROOT / name).exists()
    ]
    if missing:
        return report("FAIL", "Project files", f"Missing: {', '.join(missing)}")

    try:
        import json
        json.loads((ROOT / "takemeter.ipynb").read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return report("FAIL", "Project files", f"takemeter.ipynb is not readable: {exc}")

    report("PASS", "Project files", "notebook, scripts and practice data all present")


def main():
    print("\nAI201 environment check\n" + "-" * 60)
    check_python()
    check_venv()
    check_packages()
    check_machine()
    check_torch()
    check_training_deps()
    check_transformers()
    check_baseline_model()
    check_project_files()

    print("-" * 60)
    print(f"{len(passed)} passed, {len(failed)} failed, "
          f"{len(warned)} to look at, {len(skipped)} skipped\n")
    if failed:
        print("Not ready yet. Fix the FAIL lines above, then run test.py again.")
        print("Still stuck after one honest attempt? Post the whole output in the")
        print("help channel — the day before class, not the morning of.\n")
        return 1
    if skipped:
        print("You're set for what's installed. The skipped checks are packages")
        print("this unit's requirements.txt doesn't pin yet — that's expected.\n")
        return 0
    print("You're set. See you in class.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
