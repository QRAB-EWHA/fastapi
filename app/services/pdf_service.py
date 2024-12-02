from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from app.utils.config_manager import ConfigManager

class PDFService:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )
        self.config_manager = ConfigManager()
    
    async def save_pdf(self, file: UploadFile, title: str, url: str) -> str:
        # PDF 파일 저장
        file_path = os.path.join("data", file.filename)
        os.makedirs("data", exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 메타데이터 저장
        self.config_manager.add_document(file.filename, title, url)
        
        return file_path
    
    def process_pdf(self, file_path: str):
        # PDF 로드
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        
        # 텍스트 분할
        texts = self.text_splitter.split_documents(pages)
        
        print(f"PDF를 {len(texts)}개의 청크로 분할했습니다.")
        return texts