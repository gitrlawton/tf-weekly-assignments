# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-01 21:28
- Auto-marked BROKE (5xx, crash, no response): **1**
- Left for you to judge: **55**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `3a307018-8aa9-47e2-a7f3-c807a021c0f1` | unsure | 0.142 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `bbbed2dc-7d35-4e07-9987-e4df654c1b8c` | unsure | 0.164 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `e174a468-57be-4d75-a516-107dcf34d6d8` | unsure | 0.038 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `c9688260-7f23-43e2-a2d2-70b2dbd5968e` | unsure | 0.251 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `3db102b0-74c0-4210-b39c-090e9f87157e` | human | 0.470 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `6c3f0657-bcd8-46a9-bff0-c53bd36ddc1d` | unsure | 0.125 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `4ea86ddb-2223-43f2-9956-66fe54b3b5fc` | unsure | 0.078 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `b151672e-5a62-4a7d-91a2-0b1c8cf2efa8` | unsure | 0.220 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `7b06f362-5de3-45f0-b006-211de60df8ff` | unsure | 0.057 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `d1ebd8fc-676b-421a-b8c5-eb2b2baef859` | ai | 0.758 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `67fb4ff2-113c-4e00-9818-e261e6d974c7` | unsure | 0.128 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `738e147b-e130-415b-bbcf-1cf4d2190ec6` | unsure | 0.455 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `36ef5e7b-d5ed-42b7-892e-c221db6ccbe1` | unsure | 0.441 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `88226481-7387-4a0c-8177-a70aaec0264d` | unsure | 0.379 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `3caf658d-35bf-4335-92fb-51bfbc932f0f` | ai | 0.575 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `81a1f4fe-bd7e-42a2-883a-7b9f96a277cd` | unsure | 0.224 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `42824322-46db-4083-be57-b5938e74f47b` | unsure | 0.410 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `702dcd53-6193-4f1a-a6ff-02b1258a03b6` | unsure | 0.270 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `9bd7a3a4-aecf-4de5-aa67-052f64e95431` | human | 0.311 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `309fad01-a05b-47aa-9cbb-514b4a7d960b` | human | 0.610 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `2c3854c1-7bea-429d-a24d-c929df0f390d` | unsure | 0.084 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `82eafd4c-5eea-407c-930f-d489f3c0a144` | unsure | 0.135 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `53f6c37e-ac62-4fe5-9c01-d43822890bf2` | unsure | 0.088 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `1def9297-283b-482d-a205-33566f4fac67` | unsure | 0.074 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `09ac363c-20af-464f-9f73-9ea1da73281b` | human | 0.387 | HELD |
| MF04 | malformed | text is only punctuation | 200 | `c30d0c71-607a-4bf9-9217-2c190d15bad6` | human | 0.349 | HELD |
| MF05 | malformed | text is a very long single word | 200 | `2d899c6f-d007-4921-af42-c47c8d9f7622` | unsure | 0.327 | HELD |
| MF06 | malformed | text is emoji only | 200 | `db18f63e-eb94-49e8-82d5-d46d8421c73b` | unsure | 0.355 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `864a2e7e-fa0b-484d-b512-56e4dbce292f` | unsure | 0.291 | HELD |
| MF08 | malformed | text is 60,000 characters | 200 | `c533a687-fc13-477f-bfe1-cd44c500587f` | ai | 0.736 | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | `ac841607-ab5d-443e-bec9-a100ff4531f1` | human | 0.332 | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 200 | `a6672141-a7a6-402e-b6e7-43554f893d85` | human | 0.352 | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `63826605-bdb1-41d1-a462-fbd5b28dcf0f` | human | 0.366 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1e470ad8-bd63-4e2c-83e7-081521033580` | human | 0.366 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `dba20fbe-c9aa-4a82-9ab3-406c209836c1` | human | 0.366 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1e1ffd58-142c-476b-b514-cfc9d9f0f428` | human | 0.366 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e5b4895f-9bd7-4e1e-9081-6ee65e586565` | human | 0.366 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c7d5026d-a8a5-41f3-9cd4-d302e4ea09f1` | human | 0.366 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7450b013-8c08-4f87-816e-19004f553385` | human | 0.366 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d9ae2e97-7476-4865-b69a-cf0c6958907f` | human | 0.366 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e7eca22c-9c0e-4cea-8d1d-ba417e90e2ef` | human | 0.366 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ca82510b-b42b-4623-be21-48d85a6a551a` | human | 0.366 | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 1 | 19 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "3a307018-8aa9-47e2-a7f3-c807a021c0f1",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.1416,
  "model_score": 0.1635,
  "style_score": 0.6692,
  "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "bbbed2dc-7d35-4e07-9987-e4df654c1b8c",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.1636,
  "model_score": 0.5943,
  "style_score": 0.2029,
  "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "e174a468-57be-4d75-a516-107dcf34d6d8",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.0378,
  "model_score": 0.6662,
  "style_score": 0.3388,
  "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "c9688260-7f23-43e2-a2d2-70b2dbd5968e",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.2512,
  "model_score": 0.6114,
  "style_score": 0.6429,
  "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "3db102b0-74c0-4210-b39c-090e9f87157e",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.4702,
  "model_score": 0.3212,
  "style_score": 0.1961,
  "label": "We are confident this work was written by a human author.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "6c3f0657-bcd8-46a9-bff0-c53bd36ddc1d",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.1254,
  "model_score": 0.5727,
  "style_score": 0.2719,
  "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "4ea86ddb-2223-43f2-9956-66fe54b3b5fc",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.0784,
  "model_score": 0.5862,
  "style_score": 0.3076,
  "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "b151672e-5a62-4a7d-91a2-0b1c8cf2efa8",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.2198,
  "model_score": 0.2452,
  "style_score": 0.5672,
  "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "7b06f362-5de3-45f0-b006-211de60df8ff",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.0574,
  "model_score": 0.7042,
  "style_score": 0.3142,
  "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "d1ebd8fc-676b-421a-b8c5-eb2b2baef859",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.7576,
  "model_score": 0.9792,
  "style_score": 0.7561,
  "label": "This text displays strong statistical patterns characteristic of AI-generated writing. If this is your original work, you can request a human review.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "67fb4ff2-113c-4e00-9818-e261e6d974c7",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.128,
  "model_score": 0.6175,
  "style_score": 0.4985,
  "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "738e147b-e130-415b-bbcf-1cf4d2190ec6",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.4554,
  "model_score": 0.7387,
  "style_score": 0.7143,
  "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "36ef5e7b-d5ed-42b7-892e-c221db6ccbe1",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.441,
  "model_score": 0.8051,
  "style_score": 0.6171,
  "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "88226481-7387-4a0c-8177-a70aaec0264d",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.379,
  "model_score": 0.8329,
  "style_score": 0.5142,
  "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "3caf658d-35bf-4335-92fb-51bfbc932f0f",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.5748,
  "model_score": 0.8005,
  "style_score": 0.7713,
  "label": "This text displays strong statistical patterns characteristic of AI-generated writing. If this is your original work, you can request a human review.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "81a1f4fe-bd7e-42a2-883a-7b9f96a277cd",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.2244,
  "model_score": 0.8814,
  "style_score": 0.4175,
  "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "42824322-46db-4083-be57-b5938e74f47b",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.4104,
  "model_score": 0.8816,
  "style_score": 0.4897,
  "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "702dcd53-6193-4f1a-a6ff-02b1258a03b6",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.2702,
  "model_score": 0.3223,
  "style_score": 0.417,
  "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "9bd7a3a4-aecf-4de5-aa67-052f64e95431",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.3112,
  "model_score": 0.4625,
  "style_score": 0.2,
  "label": "We are confident this work was written by a human author.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "309fad01-a05b-47aa-9cbb-514b4a7d960b",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.6104,
  "model_score": 0.2044,
  "style_score": 0.1831,
  "label": "We are confident this work was written by a human author.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "2c3854c1-7bea-429d-a24d-c929df0f390d",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.084,
  "model_score": 0.5943,
  "style_score": 0.4781,
  "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "82eafd4c-5eea-407c-930f-d489f3c0a144",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.135,
  "model_score": 0.4998,
  "style_score": 0.3502,
  "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "53f6c37e-ac62-4fe5-9c01-d43822890bf2",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.0878,
  "model_score": 0.6401,
  "style_score": 0.1786,
  "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "1def9297-283b-482d-a205-33566f4fac67",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.0742,
  "model_score": 0.5583,
  "style_score": 0.5111,
  "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: Text is too short to score \u2014 a few sentences at least.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&a",
  "verdict": "BROKE"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "09ac363c-20af-464f-9f73-9ea1da73281b",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.3868,
  "model_score": 0.0,
  "style_score": 0.45,
  "label": "We are confident this work was written by a human author.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "c30d0c71-607a-4bf9-9217-2c190d15bad6",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.3494,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "We are confident this work was written by a human author.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "2d899c6f-d007-4921-af42-c47c8d9f7622",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.3266,
  "model_score": 0.9976,
  "style_score": 0.45,
  "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "db18f63e-eb94-49e8-82d5-d46d8421c73b",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.3552,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "864a2e7e-fa0b-484d-b512-56e4dbce292f",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.2906,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "c533a687-fc13-477f-bfe1-cd44c500587f",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.736,
  "model_score": 0.9876,
  "style_score": 0.7218,
  "label": "This text displays strong statistical patterns characteristic of AI-generated writing. If this is your original work, you can request a human review.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "ac841607-ab5d-443e-bec9-a100ff4531f1",
  "creator_id": null,
  "guess": "human",
  "confidence": 0.3316,
  "model_score": 0.2395,
  "style_score": 0.45,
  "label": "We are confident this work was written by a human author.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "a6672141-a7a6-402e-b6e7-43554f893d85",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.3516,
  "model_score": 0.0492,
  "style_score": 0.45,
  "label": "We are confident this work was written by a human author.",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "63826605-bdb1-41d1-a462-fbd5b28dcf0f",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3662,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We are confident this work was written by a human author.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "1e470ad8-bd63-4e2c-83e7-081521033580",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3662,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We are confident this work was written by a human author.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "dba20fbe-c9aa-4a82-9ab3-406c209836c1",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3662,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We are confident this work was written by a human author.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "1e1ffd58-142c-476b-b514-cfc9d9f0f428",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3662,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We are confident this work was written by a human author.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "e5b4895f-9bd7-4e1e-9081-6ee65e586565",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3662,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We are confident this work was written by a human author.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "c7d5026d-a8a5-41f3-9cd4-d302e4ea09f1",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3662,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We are confident this work was written by a human author.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "7450b013-8c08-4f87-816e-19004f553385",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3662,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We are confident this work was written by a human author.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "d9ae2e97-7476-4865-b69a-cf0c6958907f",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3662,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We are confident this work was written by a human author.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "e7eca22c-9c0e-4cea-8d1d-ba417e90e2ef",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3662,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We are confident this work was written by a human author.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "ca82510b-b42b-4623-be21-48d85a6a551a",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3662,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We are confident this work was written by a human author.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
