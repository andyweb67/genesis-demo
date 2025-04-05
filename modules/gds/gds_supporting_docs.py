# Placeholder for GDS Supporting Documents functionality
def manage_supporting_docs():
    print("Managing GDS supporting documents...")
# Module: GDS Supporting Documents

class GDSSupportingDocs:
    """
    Handles the management of supporting documents in the Genesis Demand Summary.
    """

    def __init__(self):
        self.documents = []

    def add_document(self, name, page_range, description):
        """
        Add a new supporting document to the GDS.

        Args:
            name (str): Name of the document.
            page_range (str): Page range where the document is located.
            description (str): Description of the document.
        """
        document = {
            "name": name,
            "page_range": page_range,
            "description": description
        }
        self.documents.append(document)

    def list_documents(self):
        """
        List all supporting documents in the GDS.

        Returns:
            list: A list of all supporting documents.
        """
        return self.documents