# QRAB_FASTAPI

QRAB 프로젝트의 FastAPI 백엔드 레포지토리입니다. 이 서버는 RAG 기반 서비스 등 추가적인 AI 연동 기능을 제공하며, Chroma와 같은 Vector DB를 활용합니다.

## 🎈About Source Code

- **Framework**: FastAPI  
- **Server**: Uvicorn  
- **Core Functionality**:  
  - RAG( Retrieval-Augmented Generation ) 기반 추천 및 컨텐츠 분석 서비스  
  - OpenAI API 연동 및 자연어 처리 기능 제공  
  - ChromaDB 등 Vector DB를 활용한 벡터 검색 및 임베딩 기반 정보 조회
- **Key Libraries**:
  - **fastapi**: 웹 서버 엔드포인트 정의 및 요청/응답 처리
  - **uvicorn**: ASGI 서버 실행
  - **openai**: OpenAI API 연동을 통한 LLM 활용
  - **langchain**: LLM 기반 워크플로우 및 체인 관리
  - **chromadb**: Vector DB 활용을 통한 유사도 검색 및 임베딩 저장
  - **transformers / sentence-transformers**: 임베딩 모델 및 NLP 모델 사용
  - **pydantic**: 데이터 검증 및 스키마 정의
  - **requests / httpx**: HTTP 요청을 통한 외부 API 연동

## 🎈Prerequisites

다음 소프트웨어 및 환경이 필요합니다.

1. **Python 3.10+**  
   - Python 버전 확인:  
     ```bash
     python --version
     ```

2. **Visual Studio Code (VSCode)**  
   - 편리한 개발 환경을 위해 권장합니다.
   - [VSCode 다운로드](https://code.visualstudio.com/)

3. **가상환경 권장**  
   - venv 또는 conda 등을 사용하여 격리된 가상환경에서 실행하는 것을 추천합니다. 가상환경을 생성하는 방법은 **How to Build**에서 구체적으로 안내하겠습니다.

4. **필요 라이브러리 설치**  
   - `requirements.txt` 파일에 필요한 라이브러리가 정의되어 있습니다.

## 🎈How to Build

1. **레포지토리 클론**  
   ```bash
   git clone https://github.com/QRAB-EWHA/fastapi.git
   cd fastapi
   ```

2. **가상환경 생성 및 활성화**
   가상환경을 생성하고 활성화합니다. 가상환경이 제대로 활성화되면 터미널 프롬프트 앞에 (venv)가 표시됩니다.
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
     
4. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```
   
5. **환경변수 설정(.env 파일 생성)**
   - 프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 다음 내용을 추가합니다.
   - .env 파일을 제공받은 경우, 해당 파일의 내용을 그대로 붙여넣기 해 주세요.
   - 이미 아래 내용을 담은 .env 파일이 존재한다면 추가 작업은 필요 없습니다.
   ```bash
   OPENAI_API_KEY=YOUR_OPENAI_API_KEY
   ```

## 🎈How to Run
다음 명령어로 FastAPI 서버를 실행할 수 있습니다.
```bash
python -m uvicorn app.main:app --reload
```

서버 실행 후 다음 URL에서 Swagger UI를 통해 API를 테스트할 수 있습니다.
http://localhost:8000/docs
