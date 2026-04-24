"""Edinburgh Postnatal Depression Scale (EPDS) screening.

Implements the 10-question EPDS screening tool with English, Shona,
and Ndebele translations. Includes scoring, interpretation, self-harm
detection, and Friendship Bench referral integration.
"""

from __future__ import annotations


EPDS_QUESTIONS: list[dict] = [
    {
        "q": 1,
        "en": "I have been able to laugh and see the funny side of things",
        "sn": "Ndaikwanisa kuseka uye kuona zvinhu zvinosekesa",
        "nd": "Bengikwazi ukuhleka lokubona okulotshisayo",
        "scoring": "reverse",
        "options": {
            "en": [
                "As much as I always could (0)",
                "Not quite so much now (1)",
                "Definitely not so much now (2)",
                "Not at all (3)",
            ],
            "sn": [
                "Zvakafanana nezvandaigara ndichiita (0)",
                "Hazvichaiti zvakadai sezvaimbova (1)",
                "Chokwadi hazvichaiti sezvaimbova (2)",
                "Kwete, hapana (3)",
            ],
            "nd": [
                "Njengoba bengisenza njalo (0)",
                "Akusenjalo kangako manje (1)",
                "Isibili akusenjalo kangako manje (2)",
                "Akunjalo langanini (3)",
            ],
        },
    },
    {
        "q": 2,
        "en": "I have looked forward with enjoyment to things",
        "sn": "Ndaitarisira zvinhu nemufaro",
        "nd": "Bengibheka phambili ngokuthokoza ezintweni",
        "scoring": "reverse",
        "options": {
            "en": [
                "As much as I ever did (0)",
                "Rather less than I used to (1)",
                "Definitely less than I used to (2)",
                "Hardly at all (3)",
            ],
            "sn": [
                "Zvakafanana nezvandaigara ndichiita (0)",
                "Zvishoma kupfuura zvandaigara ndichiita (1)",
                "Chokwadi zvishoma kupfuura zvandaigara ndichiita (2)",
                "Hazvichaiti zvachose (3)",
            ],
            "nd": [
                "Njengoba bengisenza njalo (0)",
                "Sekuncane kulalokho engangikhangela kukho (1)",
                "Isibili ngokuncane kulalokho engangikhangela kukho (2)",
                "Ngeze ngitsho (3)",
            ],
        },
    },
    {
        "q": 3,
        "en": "I have blamed myself unnecessarily when things went wrong",
        "sn": "Ndaizvipa mhosva zvisina musoro kana zvinhu zvaisafamba zvakanaka",
        "nd": "Bengizisola kungekho isizathu nxa izinto zingahambi kuhle",
        "scoring": "direct",
        "options": {
            "en": [
                "No, never (0)",
                "Not very often (1)",
                "Yes, some of the time (2)",
                "Yes, most of the time (3)",
            ],
            "sn": [
                "Kwete, hapana (0)",
                "Kwete, kazhinji kwete (1)",
                "Hongu, dzimwe nguva (2)",
                "Hongu, nguva zhinji (3)",
            ],
            "nd": [
                "Hatshi, akuzange kwenzeke (0)",
                "Akusikangaki (1)",
                "Yebo, ngezinye izikhathi (2)",
                "Yebo, isikhathi esinengi (3)",
            ],
        },
    },
    {
        "q": 4,
        "en": "I have been anxious or worried for no good reason",
        "sn": "Ndainetseka kana kuzvidya mwoyo pasina chikonzero chakanaka",
        "nd": "Bengikhathalekile kumbe bengikhathazekile kungekho isizathu",
        "scoring": "direct",
        "options": {
            "en": [
                "No, not at all (0)",
                "Hardly ever (1)",
                "Yes, sometimes (2)",
                "Yes, very often (3)",
            ],
            "sn": [
                "Kwete, hapana (0)",
                "Hazvina kumbobvira zvakaitika (1)",
                "Hongu, dzimwe nguva (2)",
                "Hongu, kazhinji (3)",
            ],
            "nd": [
                "Hatshi, akunjalo (0)",
                "Isikhathi esincinyane nje (1)",
                "Yebo, ngezinye izikhathi (2)",
                "Yebo, kanengi kakhulu (3)",
            ],
        },
    },
    {
        "q": 5,
        "en": "I have felt scared or panicky for no very good reason",
        "sn": "Ndainzwa kutya kana kushushikana pasina chikonzero chakanaka",
        "nd": "Bengisesaba kumbe bengiphatheka kubi kungekho isizathu",
        "scoring": "direct",
        "options": {
            "en": [
                "No, not at all (0)",
                "No, not much (1)",
                "Yes, sometimes (2)",
                "Yes, quite a lot (3)",
            ],
            "sn": [
                "Kwete, hapana (0)",
                "Kwete, kwete zvakanyanya (1)",
                "Hongu, dzimwe nguva (2)",
                "Hongu, zvakanyanya (3)",
            ],
            "nd": [
                "Hatshi, akunjalo (0)",
                "Hatshi, akukubi kangako (1)",
                "Yebo, ngezinye izikhathi (2)",
                "Yebo, kakhulu (3)",
            ],
        },
    },
    {
        "q": 6,
        "en": "Things have been getting on top of me",
        "sn": "Zvinhu zvanga zvichindiremera",
        "nd": "Izinto bezisiba nzima kimi",
        "scoring": "direct",
        "options": {
            "en": [
                "No, I have been coping as well as ever (0)",
                "No, most of the time I have coped quite well (1)",
                "Yes, sometimes I haven't been coping as well as usual (2)",
                "Yes, most of the time I haven't been able to cope at all (3)",
            ],
            "sn": [
                "Kwete, ndanga ndichikwanisa kugadzirisa sezvandinogara ndichiita (0)",
                "Kwete, nguva zhinji ndanga ndichikwanisa kugadzirisa zvakanaka (1)",
                "Hongu, dzimwe nguva handina kukwanisa kugadzirisa sezvandinogara (2)",
                "Hongu, nguva zhinji handina kukwanisa kugadzirisa zvachose (3)",
            ],
            "nd": [
                "Hatshi, bengisenza kuhle njengenjayelo (0)",
                "Hatshi, isikhathi esinengi bengisenelisa kuhle (1)",
                "Yebo, ngezinye izikhathi bengingenelisi njengenjayelo (2)",
                "Yebo, isikhathi esinengi bengingenelisi ukwenza lutho (3)",
            ],
        },
    },
    {
        "q": 7,
        "en": "I have been so unhappy that I have had difficulty sleeping",
        "sn": "Ndanga ndisina mufaro zvokuti ndaishaya hope",
        "nd": "Bengingathokozi kakhulu okokuthi bengibuthathela ukulala",
        "scoring": "direct",
        "options": {
            "en": [
                "No, not at all (0)",
                "Not very often (1)",
                "Yes, sometimes (2)",
                "Yes, most of the time (3)",
            ],
            "sn": [
                "Kwete, hapana (0)",
                "Kwete, kazhinji kwete (1)",
                "Hongu, dzimwe nguva (2)",
                "Hongu, nguva zhinji (3)",
            ],
            "nd": [
                "Hatshi, akunjalo (0)",
                "Akusikangaki (1)",
                "Yebo, ngezinye izikhathi (2)",
                "Yebo, isikhathi esinengi (3)",
            ],
        },
    },
    {
        "q": 8,
        "en": "I have felt sad or miserable",
        "sn": "Ndanga ndichisuwa kana kusuruvara",
        "nd": "Bengizwa ngidanile kumbe ngihluphekile",
        "scoring": "direct",
        "options": {
            "en": [
                "No, not at all (0)",
                "Not very often (1)",
                "Yes, quite often (2)",
                "Yes, most of the time (3)",
            ],
            "sn": [
                "Kwete, hapana (0)",
                "Kwete, kazhinji kwete (1)",
                "Hongu, kakawanda (2)",
                "Hongu, nguva zhinji (3)",
            ],
            "nd": [
                "Hatshi, akunjalo (0)",
                "Akusikangaki (1)",
                "Yebo, kanengi (2)",
                "Yebo, isikhathi esinengi (3)",
            ],
        },
    },
    {
        "q": 9,
        "en": "I have been so unhappy that I have been crying",
        "sn": "Ndanga ndisina mufaro zvokuti ndaichema",
        "nd": "Bengingathokozi kakhulu okokuthi bengikhala",
        "scoring": "direct",
        "options": {
            "en": [
                "No, never (0)",
                "Only occasionally (1)",
                "Yes, quite often (2)",
                "Yes, most of the time (3)",
            ],
            "sn": [
                "Kwete, hapana (0)",
                "Dzimwe nguva chete (1)",
                "Hongu, kakawanda (2)",
                "Hongu, nguva zhinji (3)",
            ],
            "nd": [
                "Hatshi, akuzange kwenzeke (0)",
                "Ngezinye izikhathi kuphela (1)",
                "Yebo, kanengi (2)",
                "Yebo, isikhathi esinengi (3)",
            ],
        },
    },
    {
        "q": 10,
        "en": "The thought of harming myself has occurred to me",
        "sn": "Pfungwa yokuzviitira pabhinya yakauya kwandiri",
        "nd": "Umcabango wokuzilimaza wafika kimi",
        "scoring": "direct",
        "options": {
            "en": [
                "Never (0)",
                "Hardly ever (1)",
                "Sometimes (2)",
                "Yes, quite often (3)",
            ],
            "sn": [
                "Hapana (0)",
                "Hazvina kumbobvira zvakaitika (1)",
                "Dzimwe nguva (2)",
                "Hongu, kakawanda (3)",
            ],
            "nd": [
                "Akuzange kwenzeke (0)",
                "Isikhathi esincinyane nje (1)",
                "Ngezinye izikhathi (2)",
                "Yebo, kanengi (3)",
            ],
        },
    },
]


class EPDSScreening:
    """Edinburgh Postnatal Depression Scale screening tool.

    Implements the validated 10-question EPDS with trilingual support
    (English, Shona, Ndebele), scoring, interpretation, and referral
    pathways including Zimbabwe's Friendship Bench programme.

    Example:
        >>> epds = EPDSScreening()
        >>> questions = epds.get_questions("sn")
        >>> len(questions)
        10
        >>> score = epds.calculate_score([0, 0, 1, 1, 0, 0, 1, 1, 0, 0])
        >>> epds.interpret_score(score)["level"]
        'low'
    """

    @staticmethod
    def get_questions(language: str = "en") -> list[dict]:
        """Get the EPDS questions in the specified language.

        Args:
            language: Language code ("en" for English, "sn" for Shona,
                     "nd" for Ndebele). Defaults to English.

        Returns:
            List of question dictionaries with q (number), text,
            and options.

        Example:
            >>> questions = EPDSScreening.get_questions("en")
            >>> questions[0]["text"]
            'I have been able to laugh and see the funny side of things'
        """
        lang = language.lower().strip()
        if lang not in ("en", "sn", "nd"):
            lang = "en"

        result: list[dict] = []
        for q in EPDS_QUESTIONS:
            result.append({
                "q": q["q"],
                "text": q[lang],
                "options": q["options"].get(lang, q["options"]["en"]),
                "scoring": q["scoring"],
            })
        return result

    @staticmethod
    def calculate_score(answers: list[int]) -> int:
        """Calculate the total EPDS score from answer values.

        Each answer should be 0-3. The total score ranges from 0-30.
        For reverse-scored items (questions 1 and 2), the raw answer
        value is used directly as the scores are already ordered
        0, 1, 2, 3 in the options.

        Args:
            answers: List of 10 integer values (0-3), one per question.

        Returns:
            Total EPDS score (0-30).

        Raises:
            ValueError: If answers list is not exactly 10 items, or if
                       any value is outside 0-3 range.

        Example:
            >>> EPDSScreening.calculate_score([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            0
            >>> EPDSScreening.calculate_score([3, 3, 3, 3, 3, 3, 3, 3, 3, 3])
            30
            >>> EPDSScreening.calculate_score([0, 1, 1, 0, 0, 1, 1, 0, 0, 0])
            4
        """
        if len(answers) != 10:
            raise ValueError(
                f"EPDS requires exactly 10 answers, got {len(answers)}"
            )

        for i, a in enumerate(answers):
            if not 0 <= a <= 3:
                raise ValueError(
                    f"Answer for question {i + 1} must be 0-3, got {a}"
                )

        return sum(answers)

    @staticmethod
    def interpret_score(score: int) -> dict:
        """Interpret the EPDS total score.

        Thresholds:
        - 0-9: Low risk. Monitor at routine visits.
        - 10-12: Moderate risk. Suggest Friendship Bench or community support.
        - 13+: High risk. Recommend clinical assessment and professional support.

        Special rule: If question 10 (self-harm) score >= 1,
        immediate referral is recommended regardless of total score.

        Args:
            score: Total EPDS score (0-30).

        Returns:
            Dictionary with level, referral, guidance, and score.

        Example:
            >>> EPDSScreening.interpret_score(5)
            {'level': 'low', 'referral': 'none', ...}
            >>> EPDSScreening.interpret_score(11)
            {'level': 'moderate', 'referral': 'friendship_bench', ...}
            >>> EPDSScreening.interpret_score(15)
            {'level': 'high', 'referral': 'clinical', ...}
        """
        if score <= 9:
            return {
                "level": "low",
                "referral": "none",
                "guidance": (
                    "Your score suggests you are coping well. It is normal "
                    "to feel tired or stressed with a new baby. Continue to "
                    "take care of yourself: rest when you can, eat well, and "
                    "accept help from family and friends. If you start to feel "
                    "more down, talk to your health worker at your next visit."
                ),
                "score": score,
            }

        if score <= 12:
            return {
                "level": "moderate",
                "referral": "friendship_bench",
                "guidance": (
                    "Your score suggests you may be experiencing some "
                    "emotional difficulties. This is not uncommon after having "
                    "a baby, and support is available. We recommend visiting a "
                    "Friendship Bench at your local clinic, where trained "
                    "grandmother counsellors can provide free, confidential "
                    "support. Talking about how you feel can make a big "
                    "difference."
                ),
                "score": score,
            }

        return {
            "level": "high",
            "referral": "clinical",
            "guidance": (
                "Your score suggests you may be experiencing significant "
                "emotional difficulties. This is not your fault, and effective "
                "help is available. We strongly recommend speaking with a "
                "health professional as soon as possible. Visit your clinic "
                "and ask to speak with a nurse or counsellor about how you "
                "are feeling. You can also visit a Friendship Bench for "
                "immediate support."
            ),
            "score": score,
        }

    @staticmethod
    def interpret_with_self_harm_check(
        score: int, answers: list[int]
    ) -> dict:
        """Interpret the EPDS score with special self-harm question check.

        If question 10 (self-harm ideation) has a score of 1 or more,
        the result always includes an immediate referral flag regardless
        of the total score.

        Args:
            score: Total EPDS score (0-30).
            answers: List of 10 integer values (0-3), one per question.

        Returns:
            Dictionary with level, referral, guidance, score,
            and self_harm_flag.

        Example:
            >>> EPDSScreening.interpret_with_self_harm_check(5, [0,0,1,0,0,0,1,0,0,3])
            {'level': 'low', 'referral': 'clinical', 'self_harm_flag': True, ...}
        """
        base_result = EPDSScreening.interpret_score(score)

        self_harm_score = answers[9] if len(answers) == 10 else 0
        if self_harm_score >= 1:
            base_result["self_harm_flag"] = True
            base_result["referral"] = "clinical"
            base_result["guidance"] = (
                "You mentioned having thoughts of harming yourself. "
                "This is a sign that you need support right away. "
                "Please speak with a health worker, counsellor, or trusted "
                "person today. You can visit your nearest clinic, call the "
                "Friendship Bench helpline, or go to your nearest hospital. "
                "You are not alone, and help is available. "
                "If you are in immediate danger, please go to your nearest "
                "hospital emergency department."
            )
        else:
            base_result["self_harm_flag"] = False

        return base_result

    @staticmethod
    def get_friendship_bench_info() -> dict:
        """Get information about Zimbabwe's Friendship Bench programme.

        The Friendship Bench is an evidence-based intervention where trained
        grandmother health workers (known as 'grandmothers') provide problem-
        solving therapy on wooden benches at primary health clinics.

        Returns:
            Dictionary with description, how_it_works, availability,
            evidence, and contact information.

        Example:
            >>> info = EPDSScreening.get_friendship_bench_info()
            >>> print(info["description"])
            'The Friendship Bench is ...'
        """
        return {
            "description": (
                "The Friendship Bench is a free, evidence-based mental health "
                "programme in Zimbabwe where trained community health workers "
                "(known as 'grandmothers' or ambuya utano) provide talk therapy "
                "on benches at primary health care clinics."
            ),
            "how_it_works": (
                "You visit your local clinic and ask for the Friendship Bench. "
                "A trained grandmother counsellor will sit with you on the bench "
                "and use a structured problem-solving approach called 'kuvhura "
                "pfungwa' (opening the mind). Sessions are free, confidential, "
                "and usually take 30-45 minutes. Most people have 6 sessions."
            ),
            "availability": (
                "The Friendship Bench is available at over 70 primary health "
                "care clinics across Zimbabwe, including in Harare, Bulawayo, "
                "Gweru, Mutare, Masvingo, and rural clinics. Ask at your local "
                "clinic if the programme is available there."
            ),
            "evidence": (
                "The Friendship Bench has been scientifically validated in "
                "randomised controlled trials published in the Journal of the "
                "American Medical Association (JAMA). It has been shown to "
                "significantly reduce symptoms of depression and anxiety. "
                "The programme was developed by Professor Dixon Chibanda at "
                "the University of Zimbabwe."
            ),
            "what_to_expect": [
                "Free and confidential sessions",
                "No medication - this is talk therapy",
                "Sessions are in Shona, Ndebele, or English",
                "The grandmother will help you identify problems and find solutions",
                "You may also join a peer support group called 'circle kubatana tose' (holding hands together)",
                "You can bring your baby - it is a family-friendly space",
            ],
            "contact": {
                "website": "https://www.friendshipbenchzimbabwe.org",
                "note": "Ask at your local primary health care clinic for availability",
            },
        }
