from modules.gds.gds_supporting_docs import GDSSupportingDocs

# Create an instance of GDSSupportingDocs
gds_docs = GDSSupportingDocs()

# Add documents
gds_docs.add_document("Medical Report", "Pages 1-5", "Details of medical treatments")
gds_docs.add_document("Police Report", "Page 6", "Summary of the accident")

# List documents
print("List of GDS Supporting Documents:")
for doc in gds_docs.list_documents():
    print(f"- {doc['name']} ({doc['page_range']}): {doc['description']}")