import os
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

os.environ["GROQ_API_KEY"] = "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"
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

# Try with 'ISO-8859-1' or 'cp1252' encoding
document = TextLoader("new_data.txt", encoding="utf-8").load()

text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=2000,
    chunk_overlap=900
)

print(len(document),type(document))
texts = text_splitter.split_documents(document)
print(len(texts))
print(len(texts[2].page_content))
embeddings = HuggingFaceEmbeddings()
persist_directory = "chatbot_db"
collection_name="remedies_chatbot_v2"
vectordb = Chroma.from_documents(
    documents=texts,
    embedding=embeddings,
    persist_directory=persist_directory,
    collection_name=collection_name
)

print("Done")