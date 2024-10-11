#Importing necessary libraries:
from typing import AnyStr
from gentopia.tools.basetool import *  
#Importing for making HTTP requests:
import urllib.request
#Reading text from PDF files:
import PyPDF2
import io

class PDFReaderArgs(BaseModel):
    query: str = Field(..., description="a URL of the PDF document to be read")

class PDFReader(BaseTool):
    """A tool to read text from a PDF document present at the given URL."""

    name = "pdf_reader"
    description = "Input URL of PDF document for the pdf reader to read."

    args_schema: Optional[Type[BaseModel]] = PDFReaderArgs

    def _run(self, query: AnyStr) -> str:
        try:
            #Web request to fetch the PDF:
            req = urllib.request.Request(query, headers={'User-Agent': "Magic Browser"})
            #Open the URL to read the PDF file:
            remote_file = urllib.request.urlopen(req).read()
            #Converting the bytes read file like object:
            remote_file_bytes = io.BytesIO(remote_file)
            #Initializing the PDF reader with the file-like object:
            pdf_reader = PyPDF2.PdfReader(remote_file_bytes)
            #Fetching text from the pages of PDF putting them into a single string:
            return "\n\n".join(pdf_reader.pages[i].extract_text() for i in range(len(pdf_reader.pages)))
        except Exception as e:
            #Rasing an exception for any file not found error:
            raise ValueError("Failed to read the PDF, Please ensure the URL is correct or points to a valid PDF or the pdf might not be publicly accessible.") from e

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    #Creating an instance of the PDFReader, running it and printing for a sample PDF URL:
    ans = PDFReader()._run("https://arxiv.org/pdf/2201.05966.pdf")
    print(ans)