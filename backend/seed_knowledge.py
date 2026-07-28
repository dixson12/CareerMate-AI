"""
One-time script to seed the visa_knowledge collection with sample content.
Run with: python seed_knowledge.py (from inside the backend container or venv)
"""
from app.services.rag_service import add_document_to_store

SAMPLE_VISA_INFO = """
Stamp 1G Overview:
The Stamp 1G is a permission granted to non-EEA students who have completed a qualifying course in Ireland, 
allowing them to remain in the country to seek employment. Graduates of a Level 8 (honours bachelor) degree 
receive 12 months of Stamp 1G, while graduates of a Level 9 (master's) or Level 10 (PhD) degree receive 24 months.

During the Stamp 1G period, graduates can work full-time without needing a separate employment permit, 
and can use this time to search for a job that would qualify them for a Critical Skills Employment Permit 
or General Employment Permit.

Critical Skills Employment Permit:
This permit is for occupations on Ireland's Critical Skills Occupations List, generally requiring a 
salary of at least €38,000 per year (or €32,000 for certain STEM occupations), and is designed to 
attract highly skilled workers in areas of skills shortages.
"""

if __name__ == "__main__":
    chunks_added = add_document_to_store(
        filename="visa_overview.txt",
        text=SAMPLE_VISA_INFO,
        collection_name="visa_knowledge"
    )
    print(f"Seeded visa_knowledge collection with {chunks_added} chunks.")