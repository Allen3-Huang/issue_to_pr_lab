import re

from fastapi import FastAPI

from app.routers import products, reports

app = FastAPI()

app.include_router(products.router)
app.include_router(reports.router)



@app.get("/")
def read_root():
    return {"message": "Hello from issue-to-pr-lab!"}
