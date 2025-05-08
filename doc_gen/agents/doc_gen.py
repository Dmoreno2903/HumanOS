from people import models as people_models

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
        
        tool = self.__determine_tool(intent)
        if not tool:
            print("No valid tool found.", flush=True)
            return None
        
        # Call function to use the tool based on the intent


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

    def __determine_tool(self, intent):
        """
        Determine the tool to use based on the intent.
        """
        if intent == "generate_document":
            print("Generating document...", flush=True)
        elif intent == "generate_email":
            print("Generating email...", flush=True)
        elif intent == "generate_report":
            print("Generating report...", flush=True)
        else:
            print(f"Unknown intent: {intent}", flush=True)
            return None