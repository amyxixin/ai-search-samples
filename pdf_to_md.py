import os
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentContentFormat, AnalyzeResult
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import re

load_dotenv("../frontapp-st/.env")


output_directory = '../data/tdd-mds'
pdf_directory = '../data/tdd-pdfs'

# Ensure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# List all files in the directory
files = os.listdir(pdf_directory)

# Create a DocumentAnalysisClient
document_intelligence_client = DocumentIntelligenceClient(
    endpoint=f"https://{os.getenv('AI_SERVICE_NAME')}.cognitiveservices.azure.com/",
    credential=AzureKeyCredential(os.getenv('AI_API_KEY'))
)


# Filter out PDF files
pdf_files = [f for f in files if f.endswith('.pdf') ]

# Iterate over each PDF file
for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_directory, pdf_file)
    print(f"File processing {pdf_path}:\n")
    # Convert PDF to text md
    with open(pdf_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout",
            body=f,
            output_content_format=DocumentContentFormat.MARKDOWN,
            content_type="application/octet-stream"
        )
         # Extract text from the result and format as Markdown
        result: AnalyzeResult = poller.result()

    print(f"Here's the full content in format {result.content_format}:\n")
    #print(result.content)

    # Convert the content to a string to remove unknown chars
    content = result.content.encode("ascii", errors="ignore").decode("utf-8")

    # Save extracted Markdown text to a file
    file_name = os.path.splitext(os.path.basename(pdf_path))[0]
 
    # Extract only the file name without the folder path
    markdown_file_name = f"{file_name}_text.md"
    markdown_file_path = os.path.join(output_directory, markdown_file_name)
    with open(markdown_file_path, 'w') as markdown_file:
        markdown_file.write(content)
        markdown_file.close
    print(f"Extracted text saved to {markdown_file_name}")
print("Image text extraction and Markdown conversion using Azure Document Intelligence completed.")