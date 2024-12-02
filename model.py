from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv


load_env()
llm = ChatGoogleGenerativeAI(model = "gemini-pro", temperature = 0.3)