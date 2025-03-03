from pathlib import Path
import pdfplumber
from litellm import completion
import sys


class PDFParser:

    def __init__(self, path):
        self.pdf_library_path = path
        self.pdf_files = self._get_pdf_files()
        self.pdf_dirs = self._get_pdf_directories()
   
    def _get_pdf_files(self):
        return [str(p) for p in list(Path(self.pdf_library_path).rglob("*.pdf")) if p.is_file()]

    def _get_pdf_directories(self):
        return [str(p) for p in list(Path(self.pdf_library_path).rglob("*/")) if p.is_dir()]
    
    def _extract_pdf_first_page_text(self, pdf_filepath):
        with pdfplumber.open(pdf_filepath) as pdf:
            return pdf.pages[0].extract_text()

    def get_all_first_page_texts(self):
        return [self._extract_pdf_first_page_text(pdf) for pdf in self.pdf_files]
    

class LLMAbstractExtractor:

    def __init__(self, model):
        self.model = model

    def extract_abstract(self, text):
        reponse = completion(
            model=self.model,
            messages=[{"content": f"""
                      You are a postdoctoral scientist. Please return just the abstract from the following text. Don't output anything except the abstract:
                      {text}
                      """, "role": "system"
                      }],
                      api_base="http://localhost:11434",
                                 
        )
        return reponse.choices[0]['message']['content']
    
if __name__ == "__main__":
    pp = PDFParser(sys.argv[1])
    texts = pp.get_all_first_page_texts()
    #print (texts)
    model = "ollama/llama3.3"
    extractor = LLMAbstractExtractor(model)
    abstracts = [extractor.extract_abstract(text) for text in texts]
    for a in abstracts:
        #print(a[:100])
        #print(a)
        print(extractor.extract_abstract(a))
