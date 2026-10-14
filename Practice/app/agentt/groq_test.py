from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)


response = model.invoke(
    "What is 25% of 200?"
)


print(response.content)