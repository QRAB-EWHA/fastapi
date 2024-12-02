from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from app.services.pdf_service import PDFService
from app.services.rag_service import RAGService
import uvicorn
import os

# 요청/응답 모델 정의
class RAGRequest(BaseModel):
   category_name: str
   content: str

class ReferenceDTO(BaseModel):
   title: str
   link: str = Field(default='')
   content: str

class RAGResponse(BaseModel):
   no_relevant_docs: bool
   references: Optional[List[ReferenceDTO]] = None

app = FastAPI()
pdf_service = PDFService()
rag_service = RAGService()

app.add_middleware(
   CORSMiddleware,
   allow_origins=["http://localhost:8080"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

@app.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    title: str = Form(...),
    url: str = Form(...)
):
    try:
        if not file.filename.endswith('.pdf'):
            return {"error": "PDF 파일만 업로드 가능합니다."}
       
        print(f"PDF 파일 처리 시작: {file.filename}")
        file_path = await pdf_service.save_pdf(file, title, url)
        texts = pdf_service.process_pdf(file_path)
        
        print("벡터 DB에 문서 추가 시작")
        chunks_count = rag_service.add_documents(texts)
        print(f"벡터 DB에 {chunks_count}개의 청크 추가 완료")
        
        return {
            "filename": file.filename,
            "title": title,
            "url": url,
            "chunks": chunks_count,
            "message": "PDF 파일이 성공적으로 처리되고 임베딩되었습니다."
        }
    except Exception as e:
        print(f"에러 발생: {str(e)}")
        return {"error": str(e)}

@app.post("/generate-references", response_model=RAGResponse)
async def generate_references(request: RAGRequest):
    try:
        print(f"Searching for content related to: {request.content}")
        relevant_docs = rag_service.search_documents(request.content)
        
        if not relevant_docs:
            print("No relevant documents found")
            return RAGResponse(no_relevant_docs=True, references=[])
        
        references = rag_service.generate_rag_references(
            request.category_name,
            request.content,
            relevant_docs
        )
        
        # link 필드 포함
        return RAGResponse(
            no_relevant_docs=False,
            references=[
                ReferenceDTO(
                    title=ref["title"],
                    content=ref["content"],
                    link=ref["link"]  # link 필드 추가
                )
                for ref in references
            ]
        )       
    except Exception as e:
        print(f"Error in generate_references: {str(e)}")
        return RAGResponse(no_relevant_docs=True, references=[])

@app.post("/update-document-metadata")
async def update_document_metadata(
    filename: str = Form(...),
    title: str = Form(...),
    url: str = Form(...)
):
    try:
        # 파일이 실제로 존재하는지 확인
        file_path = os.path.join("data", filename)
        if not os.path.exists(file_path):
            return {"error": "파일이 존재하지 않습니다."}
        
        # 메타데이터 저장
        pdf_service.config_manager.add_document(filename, title, url)
        
        return {
            "message": f"{filename}의 메타데이터가 성공적으로 업데이트되었습니다.",
            "title": title,
            "url": url
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
   uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)