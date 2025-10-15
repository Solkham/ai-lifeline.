from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

# Заглушки для будущих роутов
@app.get("/")
def root():
    return {"message": "Welcome to AI Lifeline backend!"}
