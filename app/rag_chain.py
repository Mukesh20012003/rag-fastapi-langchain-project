from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from app.config import GROQ_API_KEY
from app.vector_store import load_vector_store


def get_llm():
    return ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.1-8b-instant"
    )


def get_rag_response(question: str):
    vector_store = load_vector_store()

    if vector_store is None:
        return {
            "answer": "Vector store not found. Please create the vector store first.",
            "context_used": []
        }

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    relevant_docs = retriever.invoke(question)

    if not relevant_docs:
        return {
            "answer": "No relevant documents found.",
            "context_used": []
        }

    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are a helpful AI assistant.
Answer the question only using the provided context.
If the answer is not in the context, say: "I could not find the answer in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""
    )

    prompt = prompt_template.format(context=context, question=question)

    llm = get_llm()
    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "context_used": [doc.page_content for doc in relevant_docs]
    }