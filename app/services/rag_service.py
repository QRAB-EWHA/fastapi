from typing import List, Dict
from langchain_chroma import Chroma
from app.utils.embeddings import get_embeddings
from app.config.openai_config import chat
import os
import json
from langchain.prompts import ChatPromptTemplate
from app.utils.config_manager import ConfigManager

# 프롬프트 템플릿 생성
PROMPT_TEMPLATE = """"{category_name}" 주제와 관련된 영어 텍스트입니다. 한국어로 번역하고, 대학생의 학습 자료로 가공해주세요.

원문:
{context}

요구사항:
- 전문 용어는 영어 원어를 괄호로 표시
- 내용을 구조화하여 설명
- 예시나 구현 내용 반드시 포함
- 페이지 정보 표시"""

class RAGService:
    def __init__(self):
        self.embeddings = get_embeddings()
        self.persist_directory = "vector_store"
        os.makedirs(self.persist_directory, exist_ok=True)
        self.db = Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)
        self.rag_prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        self.config_manager = ConfigManager()

    def add_documents(self, texts):
        try:
            print(f"임베딩 시작: {len(texts)}개의 텍스트 청크")
            self.db.add_documents(texts)
            print("임베딩 완료 및 저장됨")
            return len(texts)
        except Exception as e:
            print(f"임베딩 중 에러 발생: {str(e)}")
            raise e

    def search_documents(self, query: str, k: int = 2):
        try:
            print(f"검색 시작: {query}")
            docs = self.db.similarity_search(query, k=k)
            print(f"검색 완료: {len(docs)}개의 관련 문서 발견")
            return docs
        except Exception as e:
            print(f"검색 중 에러 발생: {str(e)}")
            return []

    def generate_rag_references(self, category_name: str, content: str, relevant_docs: List) -> List[Dict]:
        try:
            references = []
            seen_pages = set()

            # 최대 2개의 reference만 생성
            for doc in relevant_docs[:2]:
                page = doc.metadata.get('page', 0)
                if page in seen_pages:
                    continue
                seen_pages.add(page)

                file_name = doc.metadata.get('source', '').split('\\')[-1]
                print(f"Exact file_name being searched: '{file_name}'")  # 정확한 파일명 출력
                
                # 설정에서 문서 메타데이터 가져오기
                metadata = self.config_manager.get_document_metadata(file_name)
                print(f"File name being matched: {file_name}")
                print(f"Metadata fetched: {metadata}")
                
                # metadata에서 url을 가져와서 link로 매핑
                doc_link = metadata.url if metadata else ""
                print(f"Using link: {doc_link}")
                    
                messages = self.rag_prompt.format_messages(
                    category_name=category_name,
                    context=doc.page_content
                )
                response = (chat(messages)
                            .content
                            .replace('#', '')
                            .replace('**', '')
                            .replace('```', '')
                            .split('---')[0]
                            .strip())

                references.append({
                    "title": f"{file_name} (Page {page})",
                    "link": doc_link,
                    "content": response
                })
                print(f"Sending reference with link: {doc_link}") 

            return references[:2]  # 최대 2개만 반환

        except Exception as e:
            print(f"참고자료 생성 실패: {e}")
            raise e