from fastapi import FastAPI, Depends, HTTPException
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, Document

Base.metadata.create_all(bind=engine)

app = FastAPI()

resource = Resource(attributes={
    SERVICE_NAME: "documents-service"
})

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

SQLAlchemyInstrumentor().instrument()

FastAPIInstrumentor.instrument_app(app)

Instrumentator().instrument(app).expose(app)


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
    document = Document(title=doc.title, content=doc.content)
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


@app.get("/documents/{document_id}")
async def read_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if document:
        return document
    raise HTTPException(status_code=404, detail="Document not found")


@app.get("/documents/")
async def read_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    documents = db.query(Document).offset(skip).limit(limit).all()
    return documents


@app.get("/__health")
async def check_health():
    return
