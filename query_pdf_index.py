import argparse
import chromadb
from parser import PDFParser
from pprint import pprint

def main():
    parser = argparse.ArgumentParser(description="Query a persistent index of PDF files")
    parser.add_argument("pdfs_path", help="Path to the directory containing PDF files")
    parser.add_argument("index_path", help="Path where the index is stored")
    parser.add_argument("collection_name", help="Name of the collection to query")
    args = parser.parse_args()

    pp = PDFParser(args.pdfs_path)
    texts = pp.get_all_first_page_texts()
    client = chromadb.PersistentClient(path=args.index_path)
    collection = client.get_collection(name=args.collection_name)
    results = collection.query(
        query_texts=texts[0], # Chroma will embed this for you
        n_results=2 # how many results to return
    )
    print(texts[0])
    print("")
    pprint(results)

if __name__ == "__main__":
    main()