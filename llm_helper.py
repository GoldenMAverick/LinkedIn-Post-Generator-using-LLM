from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

# Utility function to clean invalid surrogate characters
def clean_text(text):
    return text.encode("utf-8", "ignore").decode("utf-8")

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)

if __name__ == "__main__":
    # Clean the text before invoking
    query = "Two most important ingradient in samosa are "
    query = clean_text(query)

    response = llm.invoke(query)
    print(response.content)
