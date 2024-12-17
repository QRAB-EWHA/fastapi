# QRAB_FASTAPI

QRAB 프로젝트의 FastAPI 백엔드 레포지토리입니다. 이 서버는 RAG 기반 서비스 등 추가적인 AI 연동 기능을 제공하며, Chroma와 같은 Vector DB를 활용합니다.

## About Source Code

- **Framework**: FastAPI  
- **Server**: Uvicorn  
- **DB**: ChromaDB (Vector DB)
- **Key Libraries**: fastapi, uvicorn, chromadb, openai, pydantic 등

## Prerequisites

다음 환경이 필요합니다.

1. **Python 3.10+**  
   - Python 버전 확인:  
     ```bash
     python --version
     ```

2. **가상환경 권장**  
   - venv 또는 conda 등을 사용하여 격리된 가상환경에서 실행하는 것을 추천합니다.

3. **필요 라이브러리 설치**  
   - `requirements.txt` 파일에 필요한 라이브러리가 정의되어 있습니다.

## How to Build

1. **레포지토리 클론**  
   ```bash
   git clone https://github.com/QRAB-EWHA/fastapi.git
   cd fastapi
   ```

2. **가상환경 샟성 및 활성화**
   - Mac/Linux:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```
   - Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
     
3. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```
   
4. **환경변수 설정(.env 파일 생성)**
   프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 다음 내용을 추가합니다.
   .env 파일을 받은 경우, 해당 파일의 내용을 그대로 붙여넣기 해 주세요.
   ```bash
   OPENAI_API_KEY=YOUR_OPENAI_API_KEY
   ```

## How to Run
