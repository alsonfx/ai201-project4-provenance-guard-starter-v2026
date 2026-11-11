# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-11 12:39
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `88112a26-1133-4d8b-b76c-7b2289c34a58` | unsure | 0.486 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `3951be86-3d00-4154-8f6e-7437a618aa8a` | unsure | 0.509 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `c92738a2-64d7-4c0b-8afc-f31ef2b94c01` | unsure | 0.510 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `0331ee25-1df1-430a-8a2f-57213224dd89` | ai | 0.682 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `9da0839d-6939-47ed-bd1c-94931ff63135` | human | 0.325 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `be4b4624-f9f7-40f3-a3c1-5668799c99c2` | unsure | 0.539 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `891f6b59-77b6-46c9-8f49-2d02a5890c77` | unsure | 0.472 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `18b269d6-1bd7-40bd-80e7-566121e13cd8` | unsure | 0.448 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `e95640d9-cd54-4280-8c26-fb71506e1a8b` | unsure | 0.519 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `94e3d7b6-2ae1-40bd-954d-6bac3cf3d669` | ai | 0.852 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `be07ef34-ab48-4b2d-bc81-b8f7550f7e6d` | unsure | 0.632 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `c48462d1-1fa7-4f1b-a7b8-ffc53201df5d` | ai | 0.814 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `3e484177-a020-46b1-80c6-b269af00fb1b` | ai | 0.792 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `e20301a8-65f1-4383-97b4-7f5dfabecc8d` | ai | 0.745 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `2275aba4-95cf-4449-a2bd-d096fc186689` | ai | 0.829 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `9ad4f32b-be77-4077-a337-c77844897fab` | ai | 0.717 | BROKE |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `c66ffeb1-fd79-4d8f-965f-27e39d890def` | ai | 0.716 | BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | `d0b817cf-a2f7-4b9b-8e70-86f5f3eec0de` | unsure | 0.402 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `677cec0c-5a04-47b3-8826-224e22d3f26b` | unsure | 0.406 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `d2c23bcb-bedf-4663-9a43-3c754801a0d2` | human | 0.270 | HELD |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `be091092-a268-4355-acb6-6843d4cedab4` | unsure | 0.568 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `3b322649-91d2-4ad6-a0cd-969ddce85c5a` | unsure | 0.401 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `4118b825-b743-4cde-a964-f85015b0a360` | unsure | 0.364 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `6b1d090d-07c5-4a0b-96bb-bbc65b7a340d` | unsure | 0.609 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `3ca6c1b9-d2ed-40e5-b834-ffc81f32d016` | human | 0.287 | HELD |
| MF04 | malformed | text is only punctuation | 200 | `493c0a0a-b345-44f5-bdc4-d02792291c63` | human | 0.256 | HELD |
| MF05 | malformed | text is a very long single word | 200 | `914ebcf6-e4f0-4ded-8b5d-b516a3ec718e` | ai | 0.786 | HELD |
| MF06 | malformed | text is emoji only | 200 | `02765323-4aca-48b3-8804-5f71d339ca0a` | ai | 0.749 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `f8702d7b-3d83-40b1-87bd-18be170190e5` | ai | 0.703 | HELD |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | `aab0f218-4807-476d-85f5-a7da9a36ba12` | unsure | 0.407 | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 200 | `4ad2be7c-f6fb-4b31-aece-2229ad4be8e8` | human | 0.312 | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a3d549c9-57e5-4c32-807d-b241f9f636e8` | human | 0.302 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e6e3ceb1-c202-411c-a78e-09ee916fe3a4` | human | 0.302 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b90735a3-f3ec-48b1-b312-261a04947c0f` | human | 0.302 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `dbf37f77-f675-4902-908e-fdd01ad6a0b4` | human | 0.302 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `46935585-f3ad-4262-9daf-f02a47a302ee` | human | 0.302 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `85d82d47-bdd4-4b94-9666-58761afc3f5e` | human | 0.302 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `65f1daf4-44f6-47cf-a5d7-52b235d850d4` | human | 0.302 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `588b5304-342a-45ed-a7ba-002a1c587902` | human | 0.302 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `eb7b00bd-083d-4361-b02a-ea7b05ddfc0a` | human | 0.302 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e33f49c4-d647-42b9-a889-b9d2a9df1cfa` | human | 0.302 | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
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
  "content_id": "88112a26-1133-4d8b-b76c-7b2289c34a58",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.4858,
  "model_score": 0.1635,
  "style_score": 0.808,
  "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
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
  "content_id": "3951be86-3d00-4154-8f6e-7437a618aa8a",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5087,
  "model_score": 0.5943,
  "style_score": 0.4231,
  "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
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
  "content_id": "c92738a2-64d7-4c0b-8afc-f31ef2b94c01",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5096,
  "model_score": 0.6662,
  "style_score": 0.353,
  "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
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
  "content_id": "0331ee25-1df1-430a-8a2f-57213224dd89",
  "creator_id": "attacker_EV04",
  "guess": "ai",
  "confidence": 0.6823,
  "model_score": 0.6114,
  "style_score": 0.7532,
  "label": "This text shows strong patterns typical of AI-generated writing. If you wrote this yourself, you can submit an appeal using your content ID.",
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
  "content_id": "9da0839d-6939-47ed-bd1c-94931ff63135",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3251,
  "model_score": 0.3212,
  "style_score": 0.329,
  "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression.",
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
  "content_id": "be4b4624-f9f7-40f3-a3c1-5668799c99c2",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.5386,
  "model_score": 0.5727,
  "style_score": 0.5045,
  "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
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
  "content_id": "891f6b59-77b6-46c9-8f49-2d02a5890c77",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4724,
  "model_score": 0.5862,
  "style_score": 0.3585,
  "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
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
  "content_id": "18b269d6-1bd7-40bd-80e7-566121e13cd8",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.4479,
  "model_score": 0.2452,
  "style_score": 0.6506,
  "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
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
  "content_id": "e95640d9-cd54-4280-8c26-fb71506e1a8b",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5191,
  "model_score": 0.7042,
  "style_score": 0.334,
  "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
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
  "content_id": "94e3d7b6-2ae1-40bd-954d-6bac3cf3d669",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8524,
  "model_score": 0.9792,
  "style_score": 0.7256,
  "label": "This text shows strong patterns typical of AI-generated writing. If you wrote this yourself, you can submit an appeal using your content ID.",
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
  "content_id": "be07ef34-ab48-4b2d-bc81-b8f7550f7e6d",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.6319,
  "model_score": 0.6175,
  "style_score": 0.6462,
  "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
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
  "content_id": "c48462d1-1fa7-4f1b-a7b8-ffc53201df5d",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.8138,
  "model_score": 0.7387,
  "style_score": 0.8889,
  "label": "This text shows strong patterns typical of AI-generated writing. If you wrote this yourself, you can submit an appeal using your content ID.",
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
  "content_id": "3e484177-a020-46b1-80c6-b269af00fb1b",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7919,
  "model_score": 0.8051,
  "style_score": 0.7787,
  "label": "This text shows strong patterns typical of AI-generated writing. If you wrote this yourself, you can submit an appeal using your content ID.",
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
  "content_id": "e20301a8-65f1-4383-97b4-7f5dfabecc8d",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.7451,
  "model_score": 0.8329,
  "style_score": 0.6573,
  "label": "This text shows strong patterns typical of AI-generated writing. If you wrote this yourself, you can submit an appeal using your content ID.",
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
  "content_id": "2275aba4-95cf-4449-a2bd-d096fc186689",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.8288,
  "model_score": 0.8005,
  "style_score": 0.8572,
  "label": "This text shows strong patterns typical of AI-generated writing. If you wrote this yourself, you can submit an appeal using your content ID.",
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
  "content_id": "9ad4f32b-be77-4077-a337-c77844897fab",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.7174,
  "model_score": 0.8814,
  "style_score": 0.5534,
  "label": "This text shows strong patterns typical of AI-generated writing. If you wrote this yourself, you can submit an appeal using your content ID.",
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
  "content_id": "c66ffeb1-fd79-4d8f-965f-27e39d890def",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7158,
  "model_score": 0.8816,
  "style_score": 0.55,
  "label": "This text shows strong patterns typical of AI-generated writing. If you wrote this yourself, you can submit an appeal using your content ID.",
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
  "content_id": "d0b817cf-a2f7-4b9b-8e70-86f5f3eec0de",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.4019,
  "model_score": 0.3223,
  "style_score": 0.4816,
  "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
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
  "content_id": "677cec0c-5a04-47b3-8826-224e22d3f26b",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4062,
  "model_score": 0.4625,
  "style_score": 0.35,
  "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
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
  "content_id": "d2c23bcb-bedf-4663-9a43-3c754801a0d2",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2695,
  "model_score": 0.2044,
  "style_score": 0.3346,
  "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression.",
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
  "content_id": "be091092-a268-4355-acb6-6843d4cedab4",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5681,
  "model_score": 0.5943,
  "style_score": 0.5419,
  "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
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
  "content_id": "3b322649-91d2-4ad6-a0cd-969ddce85c5a",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4014,
  "model_score": 0.4998,
  "style_score": 0.303,
  "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
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
  "content_id": "4118b825-b743-4cde-a964-f85015b0a360",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.3643,
  "model_score": 0.6401,
  "style_score": 0.0884,
  "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
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
  "content_id": "6b1d090d-07c5-4a0b-96bb-bbc65b7a340d",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.6094,
  "model_score": 0.5583,
  "style_score": 0.6604,
  "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
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
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "3ca6c1b9-d2ed-40e5-b834-ffc81f32d016",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.2875,
  "model_score": 0.0,
  "style_score": 0.575,
  "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression.",
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
  "content_id": "493c0a0a-b345-44f5-bdc4-d02792291c63",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.2556,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression.",
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
  "content_id": "914ebcf6-e4f0-4ded-8b5d-b516a3ec718e",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.7863,
  "model_score": 0.9976,
  "style_score": 0.575,
  "label": "This text shows strong patterns typical of AI-generated writing. If you wrote this yourself, you can submit an appeal using your content ID.",
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
  "content_id": "02765323-4aca-48b3-8804-5f71d339ca0a",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.7485,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "This text shows strong patterns typical of AI-generated writing. If you wrote this yourself, you can submit an appeal using your content ID.",
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
  "content_id": "f8702d7b-3d83-40b1-87bd-18be170190e5",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.7032,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "This text shows strong patterns typical of AI-generated writing. If you wrote this yourself, you can submit an appeal using your content ID.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
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
  "content_id": "aab0f218-4807-476d-85f5-a7da9a36ba12",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.4073,
  "model_score": 0.2395,
  "style_score": 0.575,
  "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
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
  "content_id": "4ad2be7c-f6fb-4b31-aece-2229ad4be8e8",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.3121,
  "model_score": 0.0492,
  "style_score": 0.575,
  "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression.",
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
  "content_id": "a3d549c9-57e5-4c32-807d-b241f9f636e8",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3018,
  "model_score": 0.0287,
  "style_score": 0.575,
  "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression.",
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
  "content_id": "e6e3ceb1-c202-411c-a78e-09ee916fe3a4",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3018,
  "model_score": 0.0287,
  "style_score": 0.575,
  "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression.",
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
  "content_id": "b90735a3-f3ec-48b1-b312-261a04947c0f",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3018,
  "model_score": 0.0287,
  "style_score": 0.575,
  "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression.",
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
  "content_id": "dbf37f77-f675-4902-908e-fdd01ad6a0b4",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3018,
  "model_score": 0.0287,
  "style_score": 0.575,
  "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression.",
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
  "content_id": "46935585-f3ad-4262-9daf-f02a47a302ee",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3018,
  "model_score": 0.0287,
  "style_score": 0.575,
  "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression.",
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
  "content_id": "85d82d47-bdd4-4b94-9666-58761afc3f5e",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3018,
  "model_score": 0.0287,
  "style_score": 0.575,
  "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression.",
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
  "content_id": "65f1daf4-44f6-47cf-a5d7-52b235d850d4",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3018,
  "model_score": 0.0287,
  "style_score": 0.575,
  "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression.",
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
  "content_id": "588b5304-342a-45ed-a7ba-002a1c587902",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3018,
  "model_score": 0.0287,
  "style_score": 0.575,
  "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression.",
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
  "content_id": "eb7b00bd-083d-4361-b02a-ea7b05ddfc0a",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3018,
  "model_score": 0.0287,
  "style_score": 0.575,
  "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression.",
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
  "content_id": "e33f49c4-d647-42b9-a889-b9d2a9df1cfa",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3018,
  "model_score": 0.0287,
  "style_score": 0.575,
  "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression.",
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