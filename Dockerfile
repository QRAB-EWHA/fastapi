# 1. 기본 이미지 (Python이 설치된 최소한의 환경)
FROM python:3.9-slim

# 2. 컨테이너 안에서 작업할 디렉터리 설정
WORKDIR /app

# 3. 로컬에서 필요한 파일을 컨테이너로 복사
COPY requirements.txt requirements.txt
COPY ./data /app/data
COPY ./vector_store /app/vector_store
COPY . .

# 4. 환경 변수 파일 복사
COPY .env /app/.env

# 5. 필요한 Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 6. 서버가 열릴 포트 (FastAPI 기본 포트: 8000)
EXPOSE 8000

# 7. 컨테이너가 실행될 때 실행할 명령어
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
