"""Translation service for English, Shona, and Ndebele.

Provides health-related translations for UI text, clinical messages,
and patient-facing content across the three main languages of Zimbabwe.
"""

from __future__ import annotations


_TRANSLATIONS: dict[str, dict[str, str]] = {
    # Greetings
    "greeting_welcome": {
        "en": "Welcome to Mwana Health",
        "sn": "Titambire kuMwana Health",
        "nd": "Siyalemukela kuMwana Health",
    },
    "greeting_how_are_you": {
        "en": "How are you today?",
        "sn": "Makadii nhasi?",
        "nd": "Linjani lamuhla?",
    },
    "greeting_mother": {
        "en": "Hello, mother",
        "sn": "Makadii, amai",
        "nd": "Sawubona, mama",
    },

    # Menu items
    "menu_home": {
        "en": "Home",
        "sn": "Kumba",
        "nd": "Ekhaya",
    },
    "menu_health_check": {
        "en": "Health Check",
        "sn": "Kuchekwa Hutano",
        "nd": "Ukuhlolwa Kwempilakahle",
    },
    "menu_immunization": {
        "en": "Immunization",
        "sn": "Majekiseni",
        "nd": "Ukugoma",
    },
    "menu_growth": {
        "en": "Growth",
        "sn": "Kukura",
        "nd": "Ukukhula",
    },
    "menu_feeding": {
        "en": "Feeding",
        "sn": "Kudya",
        "nd": "Ukondla",
    },
    "menu_milestones": {
        "en": "Milestones",
        "sn": "Matanho eKukura",
        "nd": "Izikhathi Zokukhula",
    },
    "menu_danger_signs": {
        "en": "Danger Signs",
        "sn": "Zviratidzo Zvengozi",
        "nd": "Izimpawu Zengozi",
    },
    "menu_mental_health": {
        "en": "Mental Health",
        "sn": "Hutano Hwepfungwa",
        "nd": "Impilakahle Yengqondo",
    },
    "menu_family_planning": {
        "en": "Family Planning",
        "sn": "Kugadzirisa Mhuri",
        "nd": "Ukuhlela Imuli",
    },

    # Triage messages
    "triage_red": {
        "en": "URGENT: Go to the clinic or hospital immediately",
        "sn": "PAKAREPO: Endai kuchipatara kana kuclinic izvozvi",
        "nd": "NGOKUPHANGISA: Hamba esibhedlela kumbe ekliniki khathesi",
    },
    "triage_yellow": {
        "en": "Visit your clinic within 24-48 hours",
        "sn": "Endai kuclinic munguva ye24-48 maawa",
        "nd": "Hamba ekliniki phakathi kwamahora angu24-48",
    },
    "triage_green": {
        "en": "You can manage this at home. Monitor symptoms",
        "sn": "Munogona kuzvigadzirisa kumba. Tarisai zviratidzo",
        "nd": "Ungakwenza lokhu ekhaya. Qaphela izimpawu",
    },
    "triage_call_ambulance": {
        "en": "Call an ambulance or get transport to the hospital now",
        "sn": "Fonai ambulance kana kutsvaka chitendero kuchipatara izvozvi",
        "nd": "Fonela i-ambulance kumbe uthole isithuthi esibhedlela khathesi",
    },

    # Immunization names
    "vaccine_bcg": {
        "en": "BCG (Tuberculosis vaccine)",
        "sn": "BCG (Jeketera yeTB)",
        "nd": "BCG (Umgomo weTB)",
    },
    "vaccine_opv": {
        "en": "Oral Polio Vaccine",
        "sn": "Jeketera yePolio yekumwa",
        "nd": "Umgomo wePolio okunathwayo",
    },
    "vaccine_pentavalent": {
        "en": "Pentavalent (5-in-1 vaccine)",
        "sn": "Pentavalent (Jeketera 5-mu-1)",
        "nd": "Pentavalent (Umgomo 5-ku-1)",
    },
    "vaccine_pcv": {
        "en": "Pneumococcal Conjugate Vaccine",
        "sn": "Jeketera yePneumonia",
        "nd": "Umgomo wePneumonia",
    },
    "vaccine_rotavirus": {
        "en": "Rotavirus Vaccine",
        "sn": "Jeketera yeRotavirus",
        "nd": "Umgomo weRotavirus",
    },
    "vaccine_measles_rubella": {
        "en": "Measles-Rubella Vaccine",
        "sn": "Jeketera yeGate neRubella",
        "nd": "Umgomo weGate leRubella",
    },
    "vaccine_due": {
        "en": "Your child's next vaccine is due",
        "sn": "Jeketera inotevera yemwana wenyu yasvika",
        "nd": "Umgomo olandelayo womntwana wakho ufike",
    },
    "vaccine_overdue": {
        "en": "Your child has missed a vaccine. Please visit the clinic",
        "sn": "Mwana wenyu ashaya jeketera. Endai kuclinic",
        "nd": "Umntwana wakho uswele umgomo. Hamba ekliniki",
    },

    # Milestone descriptions
    "milestone_on_track": {
        "en": "Your child is developing well",
        "sn": "Mwana wenyu ari kukura zvakanaka",
        "nd": "Umntwana wakho ukhula kuhle",
    },
    "milestone_monitor": {
        "en": "Some milestones to watch. Keep encouraging through play",
        "sn": "Pane matanho ekutarisa. Rambai muchikurudzira nekutamba",
        "nd": "Kukhona izikhathi okumelwe uziqaphele. Qhubeka ukhuthaza ngokudlala",
    },
    "milestone_delayed": {
        "en": "Your child may need a developmental check at the clinic",
        "sn": "Mwana wenyu anogona kuda kuchekwa kukura kuclinic",
        "nd": "Umntwana wakho kungadingeka ahlolwe ukukhula ekliniki",
    },

    # Nutrition guidance
    "nutrition_exclusive_bf": {
        "en": "Breastfeed exclusively for the first 6 months. No water, no formula, no food needed",
        "sn": "Yamisai mwana mazamu chete kwemwedzi 6 yekutanga. Hapana mvura, formula, kana chikafu chinodiwa",
        "nd": "Munyise umntwana ibele kuphela okwezinyanga 6 zokuqala. Akulamanzi, i-formula, kumbe ukudla okudingekayo",
    },
    "nutrition_complementary": {
        "en": "Start soft foods at 6 months while continuing breastfeeding",
        "sn": "Tangai chikafu chakapfava pamwedzi 6 muchiramba muchiisa mazamu",
        "nd": "Qalisa ukudla okuthambileyo ezinyangeni ezingu-6 uqhubeke umunyisa",
    },
    "nutrition_diverse_diet": {
        "en": "Give your child foods from at least 4 food groups every day",
        "sn": "Ipai mwana wenyu chikafu kubva kumagrupu 4 ezvokudya zuva nezuva",
        "nd": "Nika umntwana wakho ukudla okuvela kumaqembu angu-4 wokudla nsuku zonke",
    },

    # Danger signs
    "danger_sign_convulsions": {
        "en": "Convulsions or fits",
        "sn": "Kupfanya kana kuita zvinoita semhepo",
        "nd": "Ukuthuthumela kumbe ukuwa",
    },
    "danger_sign_not_feeding": {
        "en": "Unable to breastfeed or refusing to eat",
        "sn": "Asingagoni kuyamwa kana kuramba kudya",
        "nd": "Angeke anathele kumbe angavumi ukudla",
    },
    "danger_sign_fever": {
        "en": "High fever (body feels very hot)",
        "sn": "Fivha yakakwira (muviri unopisa)",
        "nd": "Ukutshisa okukhulu (umzimba utshisa kakhulu)",
    },
    "danger_sign_fast_breathing": {
        "en": "Fast or difficult breathing",
        "sn": "Kufema zvakanyanya kana zvekuomerwa",
        "nd": "Ukuphefumula ngokuphangisa kumbe kunzima",
    },
    "danger_sign_bleeding": {
        "en": "Severe bleeding",
        "sn": "Kubuda ropa zvakanyanya",
        "nd": "Ukopha okukhulu",
    },
    "danger_sign_unconscious": {
        "en": "Unconscious or very sleepy",
        "sn": "Asingapengenuki kana kurara zvakanyanya",
        "nd": "Angavuki kumbe alala kakhulu",
    },

    # EPDS / Mental health
    "epds_intro": {
        "en": "We would like to ask you some questions about how you have been feeling. There are no right or wrong answers.",
        "sn": "Tinoda kukubvunzai mibvunzo pamusoro pemaonero amuri kuita. Hapana mhinduro dzakanaka kana dzakaipa.",
        "nd": "Sifuna ukukubuza imibuzo mayelana lokuthi uzizwa njani. Akulampendulo eziqondileyo kumbe ezingaqondanga.",
    },
    "epds_result_low": {
        "en": "Your responses suggest you are coping well. Take care of yourself",
        "sn": "Mhinduro dzenyu dzinoratidza kuti muri kugona kugadzirisa zvinhu zvakanaka. Zvichengetei",
        "nd": "Izimpendulo zakho zitshengisa ukuthi usenelisa kuhle. Zinakekele",
    },
    "epds_result_moderate": {
        "en": "You may benefit from talking to someone. Consider visiting a Friendship Bench",
        "sn": "Munogona kubatsirwa nekutaura nomunhu. Fungai nezvekuenda kuFriendship Bench",
        "nd": "Ungasizakala ngokukhuluma lomuntu. Cabanga ngokuhamba eFriendship Bench",
    },
    "epds_result_high": {
        "en": "We recommend you speak with a health worker soon about how you are feeling",
        "sn": "Tinokurudzirai kuti mutaure nemushandi wezvehutano nekukurumidza pamusoro pemaonero amuri kuita",
        "nd": "Sikhuthaza ukuthi ukhulume lomsebenzi wezempilakahle masinyane mayelana lokuthi uzizwa njani",
    },
    "epds_self_harm_alert": {
        "en": "You mentioned having thoughts of harming yourself. Please speak to a health worker today. You are not alone.",
        "sn": "Mataura kuti munopfunga nezvekuzvikuvadza. Taurai nemushandi wezvehutano nhasi. Hamusi mega.",
        "nd": "Utsho ukuthi ulemicabango yokuzilimaza. Khuluma lomsebenzi wezempilakahle lamuhla. Awuwedwa.",
    },

    # Stages
    "stage_pregnant": {
        "en": "Pregnancy",
        "sn": "Kupambana / Nhumbu",
        "nd": "Ukuzithwala / Isisu",
    },
    "stage_newborn": {
        "en": "Newborn",
        "sn": "Mwana Mudiki",
        "nd": "Usane",
    },
    "stage_infant": {
        "en": "Baby",
        "sn": "Mwana",
        "nd": "Umntwana",
    },
    "stage_toddler": {
        "en": "Toddler",
        "sn": "Mwana Ari Kutanga Kufamba",
        "nd": "Umntwana Oqalayo Ukuhamba",
    },
    "stage_early_childhood": {
        "en": "Young Child",
        "sn": "Mwana Mudiki Ari Kukura",
        "nd": "Umntwana Omncane Okhulayo",
    },

    # General health messages
    "wash_hands": {
        "en": "Wash your hands with soap and water",
        "sn": "Geza maoko enyu nesipo nemvura",
        "nd": "Geza izandla zakho ngesipho lamanzi",
    },
    "drink_water": {
        "en": "Drink plenty of clean water",
        "sn": "Inwai mvura yakachena yakawanda",
        "nd": "Natha amanzi amanengi ahlanzekileyo",
    },
    "clinic_visit": {
        "en": "Visit your clinic",
        "sn": "Endai kuclinic yenyu",
        "nd": "Hamba ekliniki yakho",
    },
    "continue_breastfeeding": {
        "en": "Continue breastfeeding",
        "sn": "Rambai muchiisa mazamu",
        "nd": "Qhubeka umunyisa",
    },
    "take_medicine": {
        "en": "Take all your medicine as prescribed",
        "sn": "Inwai mushonga wenyu wese sezvamarayirwa",
        "nd": "Thatha umuthi wakho wonke njengoba ulayiwe",
    },
    "emergency": {
        "en": "This is an emergency. Go to the hospital now",
        "sn": "Ino inguva yenhamo. Endai kuchipatara izvozvi",
        "nd": "Lesi yisimo esiphuthumayo. Hamba esibhedlela khathesi",
    },

    # Breastfeeding
    "bf_exclusive": {
        "en": "Exclusive breastfeeding",
        "sn": "Kuyamwisa mazamu chete",
        "nd": "Ukunathela ibele kuphela",
    },
    "bf_complementary": {
        "en": "Breastfeeding with complementary foods",
        "sn": "Kuyamwisa nechikafu chakawedzerwa",
        "nd": "Ukunathela ibele lokudla okwengezelelweyo",
    },
    "bf_weaned": {
        "en": "Weaned",
        "sn": "Arumurwa",
        "nd": "Umntwana usulunyuliwe",
    },

    # Growth monitoring
    "growth_normal": {
        "en": "Your child's growth is on track",
        "sn": "Kukura kwemwana wenyu kuri panzvimbo yakanaka",
        "nd": "Ukukhula komntwana wakho kusendleleni enhle",
    },
    "growth_concern": {
        "en": "There are some concerns about your child's growth",
        "sn": "Pane zvimwe zvinonetsa nezvekukura kwemwana wenyu",
        "nd": "Kukhona okukhathazayo ngokukhula komntwana wakho",
    },
    "growth_urgent": {
        "en": "Your child needs urgent nutritional support",
        "sn": "Mwana wenyu anoda rubatsiro rwekudya zvakakurumidza",
        "nd": "Umntwana wakho udinga usizo lokondla ngokuphangisa",
    },

    # Family planning
    "fp_spacing": {
        "en": "Wait at least 2 years between pregnancies for the best health outcomes",
        "sn": "Mirai kwemakore 2 pakati penhumbu kuti muve nehutano hwakanaka",
        "nd": "Linda okungenani iminyaka engu-2 phakathi kwezisu ukuze impilakahle ibe ngcono",
    },
    "fp_discuss": {
        "en": "Discuss family planning options with your health worker",
        "sn": "Kurukurai nezvekugadzirisa mhuri nemushandi wezvehutano wenyu",
        "nd": "Xoxa ngendlela zokuhlela imuli lomsebenzi wezempilakahle wakho",
    },

    # Common phrases
    "yes": {"en": "Yes", "sn": "Hongu", "nd": "Yebo"},
    "no": {"en": "No", "sn": "Kwete", "nd": "Hatshi"},
    "thank_you": {"en": "Thank you", "sn": "Maita basa", "nd": "Ngiyabonga"},
    "please": {"en": "Please", "sn": "Ndapota", "nd": "Ngiyacela"},
    "help": {"en": "Help", "sn": "Rubatsiro", "nd": "Usizo"},
    "next": {"en": "Next", "sn": "Tevera", "nd": "Okulandelayo"},
    "back": {"en": "Back", "sn": "Dzokera", "nd": "Buyela emuva"},
    "done": {"en": "Done", "sn": "Zvapera", "nd": "Kuqedile"},
    "cancel": {"en": "Cancel", "sn": "Kanzura", "nd": "Susa"},
}


class TranslationService:
    """Trilingual translation service for health content.

    Provides translations in English (en), Shona (sn), and Ndebele (nd)
    for all health-related user-facing text in the Mwana Health system.

    Falls back to English if the requested language or key is not found.

    Example:
        >>> ts = TranslationService()
        >>> ts.t("greeting_welcome", "sn")
        'Titambire kuMwana Health'
        >>> ts.t("triage_red", "nd")
        'NGOKUPHANGISA: Hamba esibhedlela kumbe ekliniki khathesi'
    """

    @staticmethod
    def t(key: str, language: str = "en", **kwargs: str) -> str:
        """Translate a key to the specified language.

        Args:
            key: Translation key (e.g. "greeting_welcome", "triage_red").
            language: Language code ("en", "sn", or "nd"). Defaults to "en".
            **kwargs: Optional format parameters for string interpolation.

        Returns:
            Translated string. Falls back to English if the language or
            key is not found. Returns the key itself if no translation exists.

        Example:
            >>> TranslationService.t("greeting_welcome", "sn")
            'Titambire kuMwana Health'
            >>> TranslationService.t("nonexistent_key")
            'nonexistent_key'
            >>> TranslationService.t("greeting_welcome", "xx")
            'Welcome to Mwana Health'
        """
        lang = language.lower().strip()

        translations = _TRANSLATIONS.get(key)
        if translations is None:
            return key

        # Try requested language, fall back to English
        text = translations.get(lang)
        if text is None:
            text = translations.get("en", key)

        if kwargs:
            try:
                text = text.format(**kwargs)
            except (KeyError, IndexError):
                pass

        return text

    @staticmethod
    def get_available_languages() -> list[dict]:
        """Get list of available languages.

        Returns:
            List of language dictionaries with code and name.

        Example:
            >>> langs = TranslationService.get_available_languages()
            >>> [l["code"] for l in langs]
            ['en', 'sn', 'nd']
        """
        return [
            {"code": "en", "name": "English", "native_name": "English"},
            {"code": "sn", "name": "Shona", "native_name": "chiShona"},
            {"code": "nd", "name": "Ndebele", "native_name": "isiNdebele"},
        ]

    @staticmethod
    def get_all_keys() -> list[str]:
        """Get all available translation keys.

        Returns:
            Sorted list of all translation key strings.

        Example:
            >>> keys = TranslationService.get_all_keys()
            >>> "greeting_welcome" in keys
            True
        """
        return sorted(_TRANSLATIONS.keys())

    @staticmethod
    def get_category_keys(category: str) -> list[str]:
        """Get translation keys for a specific category.

        Categories are determined by the key prefix (e.g. "greeting_",
        "triage_", "vaccine_", "danger_sign_").

        Args:
            category: Key prefix (e.g. "greeting", "triage", "vaccine").

        Returns:
            List of keys matching the category prefix.

        Example:
            >>> TranslationService.get_category_keys("greeting")
            ['greeting_how_are_you', 'greeting_mother', 'greeting_welcome']
        """
        prefix = category.lower().strip().rstrip("_") + "_"
        return sorted(k for k in _TRANSLATIONS if k.startswith(prefix))
