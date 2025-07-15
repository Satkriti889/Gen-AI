from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
import os

def load_db_query(query_text):
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    FAISS_PATH = "faiss_gemini"
    db = FAISS.load_local(embeddings=GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-exp-03-07"),folder_path=FAISS_PATH, allow_dangerous_deserialization=True)
    llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    prompt= ChatPromptTemplate.from_template(
        """Anser the question only based on the provided context.
        Think step by step before providing a detailed answer.
        Context: {context}
        Question: {input}
        """
    )
    retriver=db.as_retriever(search_kwargs={"k": 7})

    document_chain = create_stuff_documents_chain(llm,prompt)
    retrival_chain = create_retrieval_chain(retriver,document_chain)
    response = retrival_chain.invoke({"input":query_text})
    return response['answer'].strip()
if __name__ == "__main__":
    res = load_db_query("What is the things sacrificed in dakshinkali temple and where is it located?")
    print(res)
       