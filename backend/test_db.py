import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import Company, engine, SessionLocal
from starlette.middleware.cors import CORSMiddleware 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)

def get_db(): # リクエスト時にSessionLocalを作成し完了したら終了する
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# 銘柄一覧
@app.get("/companys/")
def read_todos(db: Session = Depends(get_db)):
    companys = db.query(Company).all()
    names = [c.name for c in companys]
    return names

# 銘柄の株価を取得
@app.get("/companys/{code}")
def read_todos_only(code: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.code == code).first()
    prices = [price.close for price in company.prices]
    return prices

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
