# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-11 13:09
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `d8a85cf5-d3be-4d6d-9d3a-a43df89f3557` | unsure | 0.486 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `60ef5e78-cda3-4449-a88f-12c27d05223f` | unsure | 0.509 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `c67e6217-7e69-4f1d-a501-9e97a301588a` | unsure | 0.510 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `8f01f75e-dd04-4f47-bd23-37ad394f5d75` | unsure | 0.682 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `d721b0d7-ecb5-48ff-b039-fcd1c94af709` | human | 0.325 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `1da31773-9f5b-4c66-b9b3-772f90693596` | unsure | 0.539 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `0e170f56-654f-4725-be2a-1b9b230d5b2c` | unsure | 0.472 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `6ae6b37a-9ae3-4858-ac27-306edfe595b5` | unsure | 0.448 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `ef5a2bf8-d4b8-4ac7-a768-aabbb15ddb76` | unsure | 0.519 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `9b047b52-5163-4451-b5df-e264a9cb860e` | ai | 0.852 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `4d077654-6087-437c-b66e-7b32cf6808c1` | unsure | 0.632 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `d11bcf8a-4011-4b26-baa0-5acd037cb4d0` | ai | 0.814 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `7357f8dd-8b5d-42be-aac9-ce7992ad66a2` | unsure | 0.792 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `50b63f9a-2e56-456c-b959-9d78188adda5` | unsure | 0.745 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `58c7c539-471c-4e94-a354-244ab3c6c0b2` | ai | 0.829 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `341a04ed-1390-422d-829c-8c56c76aa112` | unsure | 0.717 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `4d0af956-2b41-4b41-9caa-4bba22205a65` | unsure | 0.716 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `e030fd1c-beb4-4bfa-9b58-f4227d2c7496` | unsure | 0.402 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `2b47d9d9-13f9-4a1e-ab6a-3db0655261d3` | unsure | 0.406 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `2982f6a0-0eab-4fee-8bb3-fcc904aaadff` | human | 0.270 | HELD |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `1f9f18f4-3ee8-4a3c-bb30-916bf5253482` | unsure | 0.568 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `69781faa-3209-4cde-aebb-6981c495e580` | unsure | 0.401 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `3068af88-14f5-4a62-a8d3-7e93aad0999e` | unsure | 0.364 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `9e40fa99-c018-4429-b35b-c23a16180adb` | unsure | 0.609 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `66db6658-ab49-418d-becc-44963e4355c4` | human | 0.287 | HELD |
| MF04 | malformed | text is only punctuation | 200 | `8744f3d9-312b-4d71-a32a-59f22f136c61` | human | 0.256 | HELD |
| MF05 | malformed | text is a very long single word | 200 | `08608b5c-b152-4327-8b75-79c0ab4d55e7` | unsure | 0.786 | HELD |
| MF06 | malformed | text is emoji only | 200 | `c9640497-3b6b-4309-86cf-896e84b6996b` | unsure | 0.749 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `13a6a609-a33b-4093-9273-fe9677935b96` | unsure | 0.703 | HELD |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | `4d7ec217-24ce-4ec0-9586-d5e6c3a9938a` | unsure | 0.407 | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 200 | `2691ba1a-be8c-4354-a23c-9b45c864ce12` | human | 0.312 | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8e5b9d88-16e4-4fc6-80b4-35a9266f1175` | human | 0.302 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e7ecc670-61d1-4540-8e96-15a9398547eb` | human | 0.302 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `72bd8e00-3be0-47a9-84c7-430ebee898df` | human | 0.302 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `088bcdc5-d4dd-492d-8d02-a8fe166e5aed` | human | 0.302 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `84134fc2-df16-4299-adb1-1460c80e6b32` | human | 0.302 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3c62cc27-f9fe-432e-b358-693cefcf6618` | human | 0.302 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0b0f2af8-6547-4051-a09d-f8a19f1df398` | human | 0.302 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3f38442e-498c-4314-84c1-dd3e24d6af18` | human | 0.302 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d4af9f64-b9b4-43f2-ac40-9931203dc746` | human | 0.302 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `82a370d6-f1cc-4bec-bcbf-697360f6fa5a` | human | 0.302 | HELD |
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
  "content_id": "d8a85cf5-d3be-4d6d-9d3a-a43df89f3557",
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
  "content_id": "60ef5e78-cda3-4449-a88f-12c27d05223f",
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
  "content_id": "c67e6217-7e69-4f1d-a501-9e97a301588a",
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
  "content_id": "8f01f75e-dd04-4f47-bd23-37ad394f5d75",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6823,
  "model_score": 0.6114,
  "style_score": 0.7532,
  "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
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
  "content_id": "d721b0d7-ecb5-48ff-b039-fcd1c94af709",
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
  "content_id": "1da31773-9f5b-4c66-b9b3-772f90693596",
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
  "content_id": "0e170f56-654f-4725-be2a-1b9b230d5b2c",
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
  "content_id": "6ae6b37a-9ae3-4858-ac27-306edfe595b5",
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
  "content_id": "ef5a2bf8-d4b8-4ac7-a768-aabbb15ddb76",
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
  "content_id": "9b047b52-5163-4451-b5df-e264a9cb860e",
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
  "content_id": "4d077654-6087-437c-b66e-7b32cf6808c1",
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
  "content_id": "d11bcf8a-4011-4b26-baa0-5acd037cb4d0",
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
  "content_id": "7357f8dd-8b5d-42be-aac9-ce7992ad66a2",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.7919,
  "model_score": 0.8051,
  "style_score": 0.7787,
  "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
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
  "content_id": "50b63f9a-2e56-456c-b959-9d78188adda5",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.7451,
  "model_score": 0.8329,
  "style_score": 0.6573,
  "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
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
  "content_id": "58c7c539-471c-4e94-a354-244ab3c6c0b2",
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
  "content_id": "341a04ed-1390-422d-829c-8c56c76aa112",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.7174,
  "model_score": 0.8814,
  "style_score": 0.5534,
  "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
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
  "content_id": "4d0af956-2b41-4b41-9caa-4bba22205a65",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.7158,
  "model_score": 0.8816,
  "style_score": 0.55,
  "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
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
  "content_id": "e030fd1c-beb4-4bfa-9b58-f4227d2c7496",
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
  "content_id": "2b47d9d9-13f9-4a1e-ab6a-3db0655261d3",
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
  "content_id": "2982f6a0-0eab-4fee-8bb3-fcc904aaadff",
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
  "content_id": "1f9f18f4-3ee8-4a3c-bb30-916bf5253482",
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
  "content_id": "69781faa-3209-4cde-aebb-6981c495e580",
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
  "content_id": "3068af88-14f5-4a62-a8d3-7e93aad0999e",
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
  "content_id": "9e40fa99-c018-4429-b35b-c23a16180adb",
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
  "content_id": "66db6658-ab49-418d-becc-44963e4355c4",
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
  "content_id": "8744f3d9-312b-4d71-a32a-59f22f136c61",
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
  "content_id": "08608b5c-b152-4327-8b75-79c0ab4d55e7",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.7863,
  "model_score": 0.9976,
  "style_score": 0.575,
  "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
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
  "content_id": "c9640497-3b6b-4309-86cf-896e84b6996b",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.7485,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
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
  "content_id": "13a6a609-a33b-4093-9273-fe9677935b96",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.7032,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
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
  "content_id": "4d7ec217-24ce-4ec0-9586-d5e6c3a9938a",
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
  "content_id": "2691ba1a-be8c-4354-a23c-9b45c864ce12",
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
  "content_id": "8e5b9d88-16e4-4fc6-80b4-35a9266f1175",
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
  "content_id": "e7ecc670-61d1-4540-8e96-15a9398547eb",
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
  "content_id": "72bd8e00-3be0-47a9-84c7-430ebee898df",
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
  "content_id": "088bcdc5-d4dd-492d-8d02-a8fe166e5aed",
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
  "content_id": "84134fc2-df16-4299-adb1-1460c80e6b32",
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
  "content_id": "3c62cc27-f9fe-432e-b358-693cefcf6618",
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
  "content_id": "0b0f2af8-6547-4051-a09d-f8a19f1df398",
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
  "content_id": "3f38442e-498c-4314-84c1-dd3e24d6af18",
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
  "content_id": "d4af9f64-b9b4-43f2-ac40-9931203dc746",
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
  "content_id": "82a370d6-f1cc-4bec-bcbf-697360f6fa5a",
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