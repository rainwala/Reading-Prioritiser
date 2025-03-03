import argparse
import chromadb
from parser import PDFParser


parser = argparse.ArgumentParser(description="Create a persistent index of PDF files")
parser.add_argument("pdfs_path", help="Path to the directory containing PDF files")
parser.add_argument("index_path", help="Path to store the index")
args = parser.parse_args()

pp = PDFParser(args.pdfs_path)
texts = pp.get_all_first_page_texts()
client = chromadb.PersistentClient(path=args.index_path)
collection = client.create_collection(name="pdf_index")
collection.add(
    documents=texts,
    ids=[f"abstract_{i}" for i in range(len(texts))]
)

