from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader
import os
import streamlit as st

def load_file(folder, f):
    """
    Load a single file from the specified folder based on its extension.
    
    Args:
        folder (str): The directory where the file is located.
        f (str): The filename to load.
    
    Returns:
        list: A list of documents loaded from the file.
    """
    # Separate files by their extension
    pdf_files = [f for f in [f] if f.endswith('.pdf')]
    txt_files = [f for f in [f] if f.endswith('.txt')]
    docx_files = [f for f in [f] if f.endswith('.docx')]
    
    # Return an empty list if no files are found
    if not pdf_files and not txt_files and not docx_files:
        return []

    # Create loaders for the files based on their type
    loaders = [
        PyPDFLoader(os.path.join(folder, f)) for f in pdf_files
    ] + [
        TextLoader(os.path.join(folder, f)) for f in txt_files
    ] + [
        UnstructuredWordDocumentLoader(os.path.join(folder, f)) for f in docx_files
    ]

    docs = []
    for loader in loaders:
        try:
            # Load documents using the appropriate loader
            loaded_docs = loader.load()
            docs.extend(loaded_docs)
        except Exception as e:
            # Handle errors during document loading
            st.error(f"Error loading documents with {loader.__class__.__name__}: {e}, File corrupted", icon='❌')
            print(f"Error loading documents with {loader.__class__.__name__}: {e}")

    return docs

def load_directory(dir):
    """
    Load all files from the specified directory and aggregate their content.
    
    Args:
        dir (str): The directory containing the files to load.
    
    Returns:
        dict: A dictionary where keys are filenames (without extension) and values are aggregated content of the files.
    """
    file_data = {}
    
    # Iterate over each file in the directory
    for file in os.listdir(dir):
        file_name, ext = os.path.splitext(file)
        ext = ext.lstrip('.').lower()  # Get the file extension
        
        # Continue if the file extension is not supported
        if ext not in ['pdf', 'txt', 'docx']:
            continue
        
        # Load the file and aggregate content
        pages = load_file(dir, file)
        content = ''.join(page.page_content for page in pages)
        file_data[file_name] = content
    
    return file_data
