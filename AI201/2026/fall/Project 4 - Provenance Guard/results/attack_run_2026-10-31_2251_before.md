# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-10-31 22:51
- Total BROKE: **17**
- Total HELD: **39**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `2425fb23-382c-4ded-9893-16a62428c290` | unsure | 0.142 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `1db1b280-1728-4180-9470-573dd5ba6b16` | unsure | 0.164 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `1913596b-b374-4a2b-8483-ed2641d175bd` | unsure | 0.038 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `5acaa30a-01c5-4a67-b313-4680fc620350` | unsure | 0.251 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `6a25fb30-4fc1-4d96-9835-c4eebc5ac623` | human | 0.470 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `1d993f96-3d69-44b4-bd43-ca8ad4384d47` | unsure | 0.125 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `00ac4d0c-c9e4-4093-9246-e3a57a5ab83f` | unsure | 0.078 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `1c046fde-9aa0-477a-848b-de815ceeb740` | unsure | 0.220 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `7138ad81-909b-4999-bba2-c09aa30a1922` | unsure | 0.057 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `0ff056ce-b2b1-454b-b89d-96641df4dbcf` | ai | 0.758 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `e37d02e3-9f00-45a3-9877-7044b368299b` | unsure | 0.128 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `0deae06a-0f43-4233-bef0-2ee6f453e31e` | ai | 0.455 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `b9b5993a-3c66-4369-97e8-73ac06c93dad` | ai | 0.441 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `2a05fc6d-3c4f-4864-bdf7-3784eb09cd28` | ai | 0.379 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `a1c91d7d-8475-49ab-8d82-5df4ab57644d` | ai | 0.575 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `61300c32-b3bc-49d8-a03a-806e9debcac0` | unsure | 0.224 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `075154b5-9468-43fb-88fd-e260968ad301` | ai | 0.410 | BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | `06efb236-99e7-4894-8720-f4c41f5e9c78` | unsure | 0.270 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `20d3e70c-5eed-4178-aac1-068a06ca5f91` | human | 0.311 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `c73539c5-dfb9-40c7-82ad-8cd3d3afdeb8` | human | 0.610 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `d981e995-c306-4a67-a37f-4507d19b0942` | unsure | 0.084 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `3197312e-2ec5-4a0d-bb1b-50021ee8f845` | unsure | 0.135 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `555f8580-0754-4a5b-9ad0-6920e8e11171` | unsure | 0.088 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `4b43daf4-b637-447a-b649-ab127e0118c8` | unsure | 0.074 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `660edcad-5188-4d7c-8c45-22b3ce708247` | human | 0.387 | HELD |
| MF04 | malformed | text is only punctuation | 200 | `a567f866-c715-46c5-85b4-4de6b0c3d275` | human | 0.349 | HELD |
| MF05 | malformed | text is a very long single word | 200 | `39301302-ee88-419b-b0b9-228a763a4c30` | ai | 0.327 | HELD |
| MF06 | malformed | text is emoji only | 200 | `8f17f087-1fb9-421d-809c-3cee036d54dd` | ai | 0.355 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `a5268257-764f-482e-842c-f882e8f264c4` | unsure | 0.291 | HELD |
| MF08 | malformed | text is 60,000 characters | 200 | `6b0c71d5-d580-47b1-aefd-32e8aa248047` | ai | 0.736 | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | `a6d4ca78-ab1d-45c3-9f82-620ecd7e9d27` | human | 0.332 | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 200 | `7967e51c-eb1b-4419-80d0-efcd9df0cf4e` | human | 0.352 | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `57e5a722-4a00-4012-b0b5-0f2162cc6057` | human | 0.366 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3d3b9ed0-70d1-4088-8251-cf966f95b31f` | human | 0.366 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0b78e05a-6e7b-42a2-8293-c32679ab195e` | human | 0.366 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `87fe28c6-780f-4fef-a443-2aa5002607a8` | human | 0.366 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `54f51f22-953a-4118-bbbe-d2de6a2c2f70` | human | 0.366 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d5de384a-3a8b-47c9-ad7d-f19b7c9b167b` | human | 0.366 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `037fbafa-6b2f-4e93-8c3d-bcb8ec37f268` | human | 0.366 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d0f541ee-dd18-4eb2-ae72-482b9db51657` | human | 0.366 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `75e337cc-9a87-4116-8b76-ff8ff73e9334` | human | 0.366 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0e268fd8-df88-4ddc-8919-64b851542116` | human | 0.366 | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Total | HELD | BROKE | Primary Mechanism / Diagnostic |
|---|---|---|---|---|
| `evasion` | 10 | 1 | 9 | Typos, uneven sentences & rare words exploit style/perplexity blind spots, dragging AI text down into `unsure` or `human`. |
| `false_positive` | 8 | 3 | 5 | Formal, technical, ESL, and student prose have low perplexity; 5 out of 8 were falsely flagged as `ai`. |
| `prompt_injection` | 6 | 4 | 2 | Label XSS and audit log injection failed cleanly; 2 adversarial instructions triggered human due to low token perplexity. |
| `malformed` | 20 | 19 | 1 | 19 malformed inputs handled safely (400 or safe 200); `MF02` (single char) crashed with 500. |
| `flood_same_creator` | 12 | 12 | 0 | Limiter allowed initial burst of 10 requests, then correctly throttled subsequent requests with 429. |

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
  "content_id": "2425fb23-382c-4ded-9893-16a62428c290",
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
  "content_id": "1db1b280-1728-4180-9470-573dd5ba6b16",
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
  "content_id": "1913596b-b374-4a2b-8483-ed2641d175bd",
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
  "content_id": "5acaa30a-01c5-4a67-b313-4680fc620350",
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
  "content_id": "6a25fb30-4fc1-4d96-9835-c4eebc5ac623",
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
  "content_id": "1d993f96-3d69-44b4-bd43-ca8ad4384d47",
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
  "content_id": "00ac4d0c-c9e4-4093-9246-e3a57a5ab83f",
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
  "content_id": "1c046fde-9aa0-477a-848b-de815ceeb740",
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
  "content_id": "7138ad81-909b-4999-bba2-c09aa30a1922",
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
  "content_id": "0ff056ce-b2b1-454b-b89d-96641df4dbcf",
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
  "content_id": "e37d02e3-9f00-45a3-9877-7044b368299b",
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
  "content_id": "0deae06a-0f43-4233-bef0-2ee6f453e31e",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.4554,
  "model_score": 0.7387,
  "style_score": 0.7143,
  "label": "This text displays strong statistical patterns characteristic of AI-generated writing. If this is your original work, you can request a human review.",
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
  "content_id": "b9b5993a-3c66-4369-97e8-73ac06c93dad",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.441,
  "model_score": 0.8051,
  "style_score": 0.6171,
  "label": "This text displays strong statistical patterns characteristic of AI-generated writing. If this is your original work, you can request a human review.",
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
  "content_id": "2a05fc6d-3c4f-4864-bdf7-3784eb09cd28",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.379,
  "model_score": 0.8329,
  "style_score": 0.5142,
  "label": "This text displays strong statistical patterns characteristic of AI-generated writing. If this is your original work, you can request a human review.",
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
  "content_id": "a1c91d7d-8475-49ab-8d82-5df4ab57644d",
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
  "content_id": "61300c32-b3bc-49d8-a03a-806e9debcac0",
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
  "content_id": "075154b5-9468-43fb-88fd-e260968ad301",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.4104,
  "model_score": 0.8816,
  "style_score": 0.4897,
  "label": "This text displays strong statistical patterns characteristic of AI-generated writing. If this is your original work, you can request a human review.",
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
  "content_id": "06efb236-99e7-4894-8720-f4c41f5e9c78",
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
  "content_id": "20d3e70c-5eed-4178-aac1-068a06ca5f91",
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
  "content_id": "c73539c5-dfb9-40c7-82ad-8cd3d3afdeb8",
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
  "content_id": "d981e995-c306-4a67-a37f-4507d19b0942",
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
  "content_id": "3197312e-2ec5-4a0d-bb1b-50021ee8f845",
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
  "content_id": "555f8580-0754-4a5b-9ad0-6920e8e11171",
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
  "content_id": "4b43daf4-b637-447a-b649-ab127e0118c8",
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
  "content_id": "660edcad-5188-4d7c-8c45-22b3ce708247",
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
  "content_id": "a567f866-c715-46c5-85b4-4de6b0c3d275",
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
  "content_id": "39301302-ee88-419b-b0b9-228a763a4c30",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.3266,
  "model_score": 0.9976,
  "style_score": 0.45,
  "label": "This text displays strong statistical patterns characteristic of AI-generated writing. If this is your original work, you can request a human review.",
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
  "content_id": "8f17f087-1fb9-421d-809c-3cee036d54dd",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.3552,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "This text displays strong statistical patterns characteristic of AI-generated writing. If this is your original work, you can request a human review.",
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
  "content_id": "a5268257-764f-482e-842c-f882e8f264c4",
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
  "content_id": "6b0c71d5-d580-47b1-aefd-32e8aa248047",
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
  "content_id": "a6d4ca78-ab1d-45c3-9f82-620ecd7e9d27",
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
  "content_id": "7967e51c-eb1b-4419-80d0-efcd9df0cf4e",
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
  "content_id": "57e5a722-4a00-4012-b0b5-0f2162cc6057",
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
  "content_id": "3d3b9ed0-70d1-4088-8251-cf966f95b31f",
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
  "content_id": "0b78e05a-6e7b-42a2-8293-c32679ab195e",
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
  "content_id": "87fe28c6-780f-4fef-a443-2aa5002607a8",
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
  "content_id": "54f51f22-953a-4118-bbbe-d2de6a2c2f70",
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
  "content_id": "d5de384a-3a8b-47c9-ad7d-f19b7c9b167b",
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
  "content_id": "037fbafa-6b2f-4e93-8c3d-bcb8ec37f268",
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
  "content_id": "d0f541ee-dd18-4eb2-ae72-482b9db51657",
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
  "content_id": "75e337cc-9a87-4116-8b76-ff8ff73e9334",
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
  "content_id": "0e268fd8-df88-4ddc-8919-64b851542116",
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