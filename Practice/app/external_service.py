from fastapi import FastAPI

app = FastAPI()


@app.get("/user/{name}")
def get_user(name: str):
    return {
        "name": name,
        "role": "AI/ML Intern",
        "status": "active",
    }