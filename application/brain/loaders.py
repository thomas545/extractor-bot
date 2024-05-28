from typing import Optional, Union
from langchain.text_splitter import TextSplitter
from langchain_community.document_loaders import (
    UnstructuredURLLoader,
    PyPDFLoader,
    JSONLoader,
)
from core.files import save_url_to_local_file


class DocumentProcessor:
    def __init__(self, doc_type: str, splitter: Optional[TextSplitter] = None):
        self._doc_type = doc_type
        self._text_spliter = splitter
        self.local_files = []

    def url_loader(self, urls, *args, **kwargs):
        loader = UnstructuredURLLoader(urls=urls)
        return loader

    def pdf_loader(self, pdf_url, *args, **kwargs):
        loader = PyPDFLoader(file_path=pdf_url)
        return loader

    def json_loader(self, file_url, *args, **kwargs):
        file_type, local_path = save_url_to_local_file(file_url)
        loader = JSONLoader(local_path, jq_schema=kwargs.get("jq_schema"))
        self.local_files.append(local_path)
        return loader

    def run_loader(self, url: Union[str, list], *args, **kwargs):
        if self._doc_type.upper() == "PDF":
            loader = self.pdf_loader(url, *args, **kwargs)
        elif self._doc_type.upper() == "JSON":
            loader = self.json_loader(url, *args, **kwargs)
        elif self._doc_type.upper() == "URL":
            loader = self.url_loader(url, *args, **kwargs)
        else:
            raise ValueError("Invalid document type.")

        if self._text_spliter is not None:
            data = loader.load_and_split(self._text_spliter)
        else:
            data = loader.load()

        return data
