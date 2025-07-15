from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate  # Changed import path to langchain.prompts
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
import os

def load_db_query(query_text):
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    # If your LangChain Google GenAI classes require the API key explicitly, pass it here.
    # For example:
    # embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-exp-03-07", api_key=GOOGLE_API_KEY)
    # llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY)

    FAISS_PATH = "faiss_gemini"

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-exp-03-07")
    db = FAISS.load_local(
        embeddings=embeddings,
        folder_path=FAISS_PATH,
        allow_dangerous_deserialization=True
    )
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    prompt = ChatPromptTemplate.from_template(
        """Answer the question only based on the provided context.
        Think step by step before providing a detailed answer.
        Context: {context}
        Question: {input}
        """
    )

    retriever = db.as_retriever(search_kwargs={"k": 7})  # Fixed variable name

    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    response = retrieval_chain.invoke({"input": query_text})
    return response['answer'].strip()

if __name__ == "__main__":
    res = load_db_query("What is the things sacrificed in dakshinkali temple?")
    print(res)

