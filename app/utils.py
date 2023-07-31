from decouple import config

from PyPDF2 import PdfReader
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from app.logger import logger

OPENAI_API_KEY = config("OPENAI_API_KEY")
PDF_FILE_NAME = config("PDF_FILE_NAME")


def load_pdf() -> str:
    try:
        doc_reader = PdfReader(PDF_FILE_NAME)
    except FileNotFoundError:
        logger.warning("Wrong pdf file name.")
        return ''
    raw_text = ''
    for page in doc_reader.pages:
        text = page.extract_text()
        if text:
            raw_text += text
    return raw_text


def split_text(text: str) -> list:
    if len(text) % 3 == 0:
        chunk_size = len(text) / 3
    else:
        chunk_size = len(text) // 3 + 1
    if chunk_size > 4096:
        chunk_size = 4096

    text_splitter = CharacterTextSplitter(
        separator=' ',
        chunk_size=chunk_size,
        chunk_overlap=0,
        length_function=len,
    )
    return text_splitter.split_text(text)


def get_answer(message: str) -> str:
    raw_text = load_pdf()
    if len(raw_text) < 10:
        logger.warning("There are few symbols in source pdf file.")
        return "I don't know please contact with support by email support@nifty-bridge.com"
    logger.info("Pdf file loaded.")

    chunks = split_text(raw_text)
    logger.info("Text split.")

    llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo")
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    db = FAISS.from_texts(chunks, embeddings)
    chain = load_qa_chain(llm, chain_type="stuff")
    prompt = "{context}{question}"
    search = db.similarity_search(query=prompt)

    q = message
    return chain.run(input_documents=search, question=q)
