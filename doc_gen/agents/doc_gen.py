from people import models as people_models
from doc_gen.agents import tools as doc_gen_tools

class DocGenAgentController:
    def __init__(self, intends_dict, user: people_models.Person):
        self.intends_dict = intends_dict
        self.user = user

    def use_tool(self):
        """
        Determine the tool to use based on the intent.
        """
        intent = self.__get_intent()
        if not intent:
            print("No valid intent found.", flush=True)
            return None
        
        # Call function to use the tool based on the intent
        if intent == "has_laboral_contract_intent":
            doc_gen_tools.send_laboral_contract(self.user)
        elif intent == "has_laboral_letter_intent":
            print("Using labor letter tool...", flush=True)
        elif intent == "has_vacation_query_intend":
            doc_gen_tools.send_available_vacation_days(self.user)
        else:
            print(f"Unknown intent: {intent}", flush=True)
            return None

    def __get_intent(self):
        """
        Get the intent from the intents dictionary.
        """
        intents = self.intends_dict.get("intents", {})
        if not intents:
            print("No intents found.", flush=True)
            return None
        
        intent = None
        for key, value in intents.items():
            if value:
                intent = key
                break

        if not intent:
            print("No valid intent found.", flush=True)
            return None
        
        print(f"Identified intent: {intent}", flush=True)
        return intent
