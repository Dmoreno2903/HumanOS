class DocGenAgentController:
    def __init__(self, message: str, phone: str):
        self.message = message
        self.phone = phone
        
    def determine_document_to_generate(self) -> str:
        """
        Determine the type of document to generate based on the message content.
        """
        pass

    def generate_document(self) -> str:
        """
        Generate the document based on the determined type and user.
        """
        pass
