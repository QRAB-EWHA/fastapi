from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

chat = ChatOpenAI(
    openai_api_key=api_key,
    model_name="gpt-4o-mini",
    temperature=0
)