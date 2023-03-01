from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, Document

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class DocumentObj(BaseModel):
    title: str
    content: str


@app.post("/documents/")
async def create_document(doc: DocumentObj, db: Session = Depends(get_db)):
    document = DocumentObj(title=doc.title, content=doc.content)
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


@app.get("/documents/{document_id}")
async def read_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    return document


@app.get("/documents/")
async def read_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    documents = db.query(Document).offset(skip).limit(limit).all()
    return documents


@app.get("/__health")
async def check_health():
    return
