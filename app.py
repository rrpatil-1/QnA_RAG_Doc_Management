from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from backend.driver_services.ingestion_service import IngestionService
from backend.driver_services.qa_service import QAService

app = FastAPI()

qna_service = QAService()
ingestion_service =IngestionService()

class IngestDocument(BaseModel):
    filepath:str

class QARequest(BaseModel):
    message: str
    filter: str|None

@app.post("/ingest_documents")
async def ingest_documents(request: IngestDocument):
    """
    Ingest a list of documents into the database
    """
    try:
        
        file = request.filepath
        if not file:
            raise HTTPException(status_code=400, detail="File path is required")
        
        result = ingestion_service.process_and_insert(file)
        if str(result).lower() == "success":
            return {"message": "Documents ingested successfully","status":200}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/qa_service")
async def qa_service(request: QARequest):
    try:
        message = request.message
        filter = request.filter
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        if filter:
            result = await qna_service.get_answer(message,{'source':filter})
        else: 
            result = await qna_service.get_answer(message)

        if result.lower().startswith('error'):
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
        return {"message": "success","status":200,"response":result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,reload=True)