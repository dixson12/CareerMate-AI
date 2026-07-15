from google import genai
from app.config import settings

client = genai.Client(api_key=settings.gemini_api_key)


def generate_response(query: str, context_chunks: list[dict]) -> str:
    context_text = "\n\n".join(
        f"[Source: {chunk['source']}]\n{chunk['text']}" for chunk in context_chunks
    )

    prompt = f"""You are a helpful assistant answering questions based on the provided document context.

Context:
{context_text}

Question: {query}

Answer based only on the context above. If the context doesn't contain relevant information, say so clearly."""

    response = client.models.generate_content(
        model=settings.llm_model,
        contents=prompt,
    )

    return response.text