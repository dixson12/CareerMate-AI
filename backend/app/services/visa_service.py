from google import genai
from app.config import settings
from app.services.rag_service import query_documents

client = genai.Client(api_key=settings.gemini_api_key)


def answer_visa_question(question: str) -> dict:
    retrieved_chunks = query_documents(question, top_k=4, collection_name="visa_knowledge")

    if not retrieved_chunks:
        return {
            "answer": "I don't have information on that yet. The visa knowledge base may need more content added.",
            "sources": []
        }

    context_text = "\n\n".join(chunk["text"] for chunk in retrieved_chunks)

    prompt = f"""You are a visa and immigration assistant for international students in Ireland.
Answer the question using ONLY the context provided below. If the context doesn't fully answer the question, say so clearly and recommend the person verify with official sources (INIS / Irish Immigration Service).

IMPORTANT: Do not invent visa rules, numbers, or requirements not stated in the context. Immigration information must be accurate — when in doubt, say you're not certain rather than guessing.

Context:
{context_text}

Question: {question}

Answer:"""

    response = client.models.generate_content(
        model=settings.llm_model,
        contents=prompt,
    )

    sources = list(set(chunk["source"] for chunk in retrieved_chunks))

    return {
        "answer": response.text,
        "sources": sources
    }