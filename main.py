from fastapi import FastAPI

app = FastAPI(title="StockAPI")

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "API is running"}