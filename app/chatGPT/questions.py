class Query:
    class Question:
        def __init__(self, question: str):
            self.question = question

        def builder(self, slither: str, solhint: str, securify: str, smartcheck: str):
            return self.question % (securify, solhint, slither, smartcheck)

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
        "I will provide you with outputs from smart contract frameworks Securify, SmartCheck, Slither and Solhint. Based on the provided information, generate JSON that will group the errors by the frameworks. Sometimes errors have different names but mean the same, handle it, especially smartcheck - try to rename them. Errors should be in human readable format. Take into considerations all errors. You should return only JSON in format: {error_name: list_of_frameworks_names}. securify: %s, solhint: %s, slither: %s, smartcheck: %s"
    )
