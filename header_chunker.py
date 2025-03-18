from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain import hub
from langchain_openai import AzureChatOpenAI
from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
import os

# Utility Functions
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_chunk(file_path, chunk, index):
    chunk_file_path = f"{file_path}_chunk_{index + 1}.md"
    with open(chunk_file_path, 'w') as file:
        file.write(chunk)

def split_into_markdown_chunks(content, headers_to_split_on):
    text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on,
                                               strip_headers=False)
    splits = text_splitter.split_text(content)

    print("Length of splits: " + str(len(splits)))
    return splits


markdown_directory = '<input directory for markdown files>'
chunk_directory = '<output directory for chunks>'

# Ensure the output directory exists
if not os.path.exists(chunk_directory):
    os.makedirs(chunk_directory)

# Split the document into chunks base on markdown headers.
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

# List all files in the directory
files = os.listdir(markdown_directory)

SHORT_CHUNK_THRESHOLD = 200  

# Filter out Markdown files
markdown_files = [f for f in files if f.endswith('.md') ] # and ('chapter' in f)  ]
# Iterate over each Markdown file
for markdown_file in markdown_files:
    print(f"Processing file {markdown_file}")
    markdown_path = os.path.join(markdown_directory, markdown_file)
    content = read_file(markdown_path)
    chunks = split_into_markdown_chunks(content,headers_to_split_on)
    
    large_file_name = os.path.splitext(os.path.basename(markdown_path))[0]
    for i, chunk_page in enumerate(chunks):
        chunk_name = f"{large_file_name}_chunk_{i + 1}.md"
        chunk_file_path = os.path.join(chunk_directory, chunk_name)
        print(f"Writing chunk to {chunk_file_path}")
        write_chunk(chunk_file_path, chunk_page.page_content, i)