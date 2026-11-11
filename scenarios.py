"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it:
1. False-positive cap: 10 authentic human-written paragraphs.
2. Score separation: 5 formulaic AI paragraphs vs 5 authentic human paragraphs.
3. Label reachability: 6 inputs spanning human, unsure, and AI ranges.
4. Bad input: 5 malformed/adversarial request bodies.
5. Appeal path: 3 valid appeals against freshly minted content_ids + 1 nonexistent ID.
"""

SCENARIOS = [
    {
        "name": "my own writing (false-positive cap)",
        "criterion": 1,
        "texts": [
            "I spent three hours yesterday trying to tune my acoustic guitar after replacing all six strings. The high E string snapped right as I reached standard pitch, so I had to bike down to the music shop in the rain to buy another single gauge string.",
            "My grandmother taught me how to knead sourdough bread when I was ten years old. She never used a kitchen scale; instead, she judged the dough by how sticky it felt against her palms and how quickly it sprang back after a firm poke with her thumb.",
            "We started climbing Mount Si before sunrise on Saturday morning. The lower trail was slick with damp pine needles and thick mud, but once we cleared the treeline at two thousand feet, the entire Puget Sound opened up beneath a sharp blanket of fog.",
            "Restoring an old steel bicycle frame from the nineteen-eighties taught me patience. Every bolt had rusted shut, and WD-40 barely helped until I used a heat gun and an impact wrench to free the stuck bottom bracket without stripping the British threads.",
            "Writing a letter by hand feels completely different than typing an email. You cannot hit backspace to erase an awkward thought; every ink stroke commits you to the sentence, forcing you to think through the entire paragraph before touching nib to paper.",
            "Every summer, our family drove ten hours north to camp beside a glacial lake. We slept in a leaky green canvas tent, caught yellow perch with rusted lures off the dock, and stayed awake listening to common loons calling out across the pitch-black water.",
            "Moving out of my college apartment took three days longer than planned because I kept finding strange memorabilia hidden inside drawers: concert ticket stubs, broken cassette tapes, and half-finished sketches on the backs of cardboard beverage coasters.",
            "We adopted an orange tabby cat named Marmalade from the county animal shelter last winter. For the first two weeks he hid under the futon, hissing at anyone who walked past, until one evening he crept out, sniffed my wool socks, and curled up on my lap.",
            "Waiting on the subway platform late on a Tuesday night is a strangely quiet experience. The fluorescent tubes flicker with a dull buzzing hum, steam rises from the drainage grates, and the distant rumble of an approaching express train vibrates through your shoes.",
            "Debugging embedded C code on a custom microcontroller can drive you mad. The hardware timer was firing at half the expected clock frequency because an undocumented silicon revision had quietly altered the prescaler register bitfield in errata sheet four."
        ],
    },
    {
        "name": "score separation between AI and human",
        "criterion": 2,
        "texts": [
            # 5 clearly AI-generated formulaic paragraphs
            "The implementation of the proposed framework requires careful consideration of several key factors. First, it is important to note that the system must be able to handle a wide variety of different inputs. Additionally, the overall performance of the solution depends on a number of important variables. In conclusion, the results demonstrate that the approach is effective and scalable.",
            "Renewable energy sources are becoming increasingly important for the future of the planet. Solar power and wind energy provide clean alternatives to traditional fossil fuels. Furthermore, many countries are investing in new infrastructure to support this transition. These efforts will help reduce carbon emissions and protect the environment for future generations.",
            "Effective time management is essential for achieving success in both personal and professional life. Setting clear goals allows individuals to prioritize their daily tasks efficiently. Moreover, eliminating distractions can significantly improve overall productivity throughout the day. By maintaining a structured schedule, one can accomplish more in less time.",
            "The advancement of technology has dramatically transformed the way people communicate across the globe. Digital platforms enable instant messaging and video conferencing from almost any location. In addition, social media networks have made it easier to connect with diverse communities. Overall, these innovations have brought people closer together in meaningful ways.",
            "Regular physical exercise plays a fundamental role in maintaining good physical and mental health. Engaging in moderate activities such as walking or cycling strengthens the cardiovascular system. Additionally, exercise stimulates the release of endorphins which can elevate mood and reduce stress. Establishing a consistent fitness routine provides long-term wellness benefits.",
            # 5 clearly human paragraphs
            "Restoring an old steel bicycle frame from the nineteen-eighties taught me patience. Every bolt had rusted shut, and WD-40 barely helped until I used a heat gun and an impact wrench to free the stuck bottom bracket without stripping the British threads.",
            "Every summer, our family drove ten hours north to camp beside a glacial lake. We slept in a leaky green canvas tent, caught yellow perch with rusted lures off the dock, and stayed awake listening to common loons calling out across the pitch-black water.",
            "Debugging embedded C code on a custom microcontroller can drive you mad. The hardware timer was firing at half the expected clock frequency because an undocumented silicon revision had quietly altered the prescaler register bitfield in errata sheet four.",
            "Writing a letter by hand feels completely different than typing an email. You cannot hit backspace to erase an awkward thought; every ink stroke commits you to the sentence, forcing you to think through the entire paragraph before touching nib to paper.",
            "We started climbing Mount Si before sunrise on Saturday morning. The lower trail was slick with damp pine needles and thick mud, but once we cleared the treeline at two thousand feet, the entire Puget Sound opened up beneath a sharp blanket of fog."
        ],
    },
    {
        "name": "three-label reachability across score range",
        "criterion": 3,
        "texts": [
            # 2 Human (< 0.35)
            "Restoring an old steel bicycle frame from the nineteen-eighties taught me patience. Every bolt had rusted shut, and WD-40 barely helped until I used a heat gun and an impact wrench to free the stuck bottom bracket without stripping the British threads.",
            "Debugging embedded C code on a custom microcontroller can drive you mad. The hardware timer was firing at half the expected clock frequency because an undocumented silicon revision had quietly altered the prescaler register bitfield in errata sheet four.",
            # 2 Unsure (0.35 - 0.65)
            "I spent three hours yesterday trying to tune my acoustic guitar after replacing all six strings. The high E string snapped right as I reached standard pitch, so I had to bike down to the music shop in the rain to buy another single gauge string.",
            "My grandmother taught me how to knead sourdough bread when I was ten years old. She never used a kitchen scale; instead, she judged the dough by how sticky it felt against her palms and how quickly it sprang back after a firm poke with her thumb.",
            # 2 AI (> 0.65)
            "The implementation of the proposed framework requires careful consideration of several key factors. First, it is important to note that the system must be able to handle a wide variety of different inputs. Additionally, the overall performance of the solution depends on a number of important variables. In conclusion, the results demonstrate that the approach is effective and scalable.",
            "Renewable energy sources are becoming increasingly important for the future of the planet. Solar power and wind energy provide clean alternatives to traditional fossil fuels. Furthermore, many countries are investing in new infrastructure to support this transition. These efforts will help reduce carbon emissions and protect the environment for future generations."
        ],
    },
    {
        "name": "graceful rejection of bad inputs",
        "criterion": 4,
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"creator_id": "eval_bad_missing"},
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": "hi", "creator_id": "eval_bad_short"},
            {"text": "word " * 6000, "creator_id": "eval_bad_huge"},
        ],
    },
    {
        "name": "appeal path state transition",
        "criterion": 5,
        "is_appeal": True,
        "bodies": [
            {"text": "I spent three hours yesterday trying to tune my acoustic guitar after replacing all six strings.", "reasoning": "I wrote this reflection myself about my guitar."},
            {"text": "My grandmother taught me how to knead sourdough bread when I was ten years old.", "reasoning": "This is a genuine personal childhood memory."},
            {"text": "We started climbing Mount Si before sunrise on Saturday morning on a damp trail.", "reasoning": "Personal account of a Pacific Northwest hike."},
            {"fake_id": True, "reasoning": "This should return 404."},
        ],
    },
]


def validate() -> list[str]:
    """Complain about anything malformed before a long run."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        if scenario.get("is_appeal"):
            if not scenario.get("bodies"):
                problems.append(f"scenario {i} ('{scenario.get('name')}') has is_appeal but no bodies")
            continue

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
