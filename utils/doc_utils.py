from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader
import os
import streamlit as st

def load_file(folder, f):
    pdf_files = [f for f in [f] if f.endswith('.pdf')]
    txt_files = [f for f in [f] if f.endswith('.txt')]
    docx_files = [f for f in [f] if f.endswith('.docx')]
    if pdf_files == [] and txt_files == [] and docx_files == []:
        return []
    loaders = [
        PyPDFLoader(os.path.join(folder, f'{f}')) for f in pdf_files] + [
        TextLoader(os.path.join(folder, f)) for f in txt_files] + [
        UnstructuredWordDocumentLoader(os.path.join(folder, f'{f}')) for f in docx_files
    ]

    docs = []
    for loader in loaders:
        try:
            loaded_docs = loader.load()
            docs.extend(loaded_docs)
        except Exception as e:
            st.error(f"Error loading documents with {loader.__class__.__name__}: {e}, File corrupted", icon='❌')
            print(f"Error loading documents with {loader.__class__.__name__}: {e}")
    return docs


def load_directory(dir):
    file_data = {}
    for file in os.listdir(dir):
        file_name = file.split('.')[0]
        try:
            ext = file.split('.')[1]
            if ext not in ['pdf', 'txt', 'docx']:
                continue
        except:
            print('')
        pages = load_file(dir, file)
        content = ''
        for page in pages:
            content += page.page_content
        file_data[file_name] = content
    return file_data

