import json
import os
from typing import Dict
from app.models.document_metadata import DocumentMetadata, DocumentsConfig

class ConfigManager:
    def __init__(self, config_file: str = "documents_config.json"):
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self) -> DocumentsConfig:
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()  # 파일 내용 읽기
                    if content:  # 내용이 있는 경우
                        data = json.loads(content)
                        return DocumentsConfig(documents=data)
                    else:  # 파일이 비어있는 경우
                        return DocumentsConfig(documents={})
            else:  # 파일이 없는 경우
                # 빈 설정으로 새 파일 생성
                empty_config = DocumentsConfig(documents={})
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump({}, f, ensure_ascii=False, indent=2)
                return empty_config
        except json.JSONDecodeError:
            # JSON 파싱 에러가 발생한 경우 빈 설정으로 초기화
            empty_config = DocumentsConfig(documents={})
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
            return empty_config

    def save_config(self):
        try:
            # 기존 설정 먼저 읽기
            existing_config = {}
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        existing_config = json.loads(content)
            
            # 새로운 설정과 병합
            documents_dict = {
                filename: {
                    "title": metadata.title,
                    "url": metadata.url
                }
                for filename, metadata in self.config.documents.items()
            }
            
            existing_config.update(documents_dict)
            
            # 병합된 설정 저장
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(existing_config, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"설정 저장 중 오류 발생: {str(e)}")

    def add_document(self, filename: str, title: str, url: str):
        self.config.documents[filename] = DocumentMetadata(
            title=title,
            url=url
        )
        self.save_config()

    def get_document_metadata(self, filename: str) -> DocumentMetadata:
        # 모든 키를 소문자로 변환하여 비교
        normalized_keys = {key.lower(): key for key in self.config.documents.keys()}
        normalized_filename = filename.lower()

        # 키가 존재하면 해당 메타데이터 반환
        if normalized_filename in normalized_keys:
            actual_key = normalized_keys[normalized_filename]
            return self.config.documents[actual_key]
        
        # 키가 없으면 None 반환
        return None