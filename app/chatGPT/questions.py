class Query:
    class Question:
        def __init__(self, question: str):
            self.question = question

        def builder(self, db_details: str, lang: str):
            language = Query.Lang.map_to_full_name(lang)
            return self.question % (db_details, language)

    class Lang:
        PL = "PL"
        EN = "EN"

        @staticmethod
        def create_from(lang: str):
            if lang.lower() == Query.Lang.PL.lower():
                return Query.Lang.PL
            elif lang.lower() == Query.Lang.EN.lower():
                return Query.Lang.EN
            else:
                raise Exception("Invalid language")

        @staticmethod
        def map_to_full_name(lang: str):
            if lang.lower() == Query.Lang.PL.lower():
                return "Polish"
            elif lang.lower() == Query.Lang.EN.lower():
                return "English"
            else:
                raise Exception("Invalid language")

    GENERATE_TABLE = Question(
        "I will provide you with outputs from smart contract frameworks Securify, SmartCheck, Slither and Solhint. Based on the provided information, generate JSON in that will group the errors by the frameworks. You should return only JSON in format: {error1: [Securify, Solhint], error2: [Slihter, Solhint, Securify, Smartcheck]}")
