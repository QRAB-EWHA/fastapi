from langchain_huggingface import HuggingFaceEmbeddings

def get_embeddings():
    # 다국어 지원되는 모델 선택
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_kwargs = {'device': 'cpu'}
    
    # Sentence Transformers 임베딩 모델 초기화
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
    )