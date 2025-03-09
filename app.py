import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
import requests
from backend.driver_services.ingestion_service import IngestionService
from backend.driver_services.list_available_doc import ListDocuments
from backend.driver_services.qa_service import QAService
from backend.utils.logger import CustomLogger
from backend.utils.request_param_check import check_url
from dotenv import load_dotenv
from httpx import AsyncClient
from contextlib import asynccontextmanager
load_dotenv()
ollam_url = os.getenv("ollama_url")
logger = CustomLogger()
# app = FastAPI()


# Create a startup context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize services with their own connection pools
    app.state.qna_service = QAService()
    app.state.list_doc = ListDocuments()
    app.state.ingestion_service = IngestionService()
    yield
    # Cleanup
    await app.state.qna_service.cleanup()
    await app.state.list_doc.cleanup()
    await app.state.ingestion_service.cleanup()

# Initialize FastAPI with lifespan
app = FastAPI(lifespan=lifespan)


class IngestDocument(BaseModel):
    filepath:str
    class Config:
        json_schema_extra = {
            "example": {
                "filepath": "https://raw.githubusercontent.com/rrpatil-1/QnA_RAG_Doc_Management/dev/sample_doc/Attension_Is_All_You_Need.pdf"
            }
        }

class QARequest(BaseModel):
    message: str = Field(
        description="The question or message to be processed",
        example="what is encoder decoder stack explain in details?"
    )
    filter: str = Field(
        default="",
        description="Optional filter parameter for the query",
        example="Attension_Is_All_You_Need.pdf"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "message": "what is encoder decoder stack explain in details?",
                "filter": ""
            }
        }

@app.get("/ollamahealth")
def health_check():
    """
    Health check endpoint to ensure the service is running and model is available for serving.
    

    """
    try:
        logger.log("Health check called", level="info")
        response = requests.get(f"{ollam_url}/api/tags")
        if response.status_code == 200:
            models = response.json().get("models")
            if models:
                return JSONResponse(status_code=200, content={"status": "model ready to accept response"})
        else:
            return JSONResponse(status_code=503, content={"status": "model is not ready"})
    except Exception as e:
        logger.log(f"Error checking model status: {e}", level="error")
        raise HTTPException(status_code=500, detail=f"Error checking model status: {e}")

@app.post("/ingest_documents")
async def ingest_documents(request: IngestDocument):
    """
    Ingest a list of documents into the database
    """
    try:
        
        file = request.filepath
        if file.strip()=="":
            return JSONResponse(status_code=400, content={"message":"File path is required"})
        
        if not check_url(file):
            return JSONResponse(status_code=400, content={"message":"Invalid URL"})
        
        result = await app.state.ingestion_service.process_and_insert(file)

        if result.lower() == "success":
            return JSONResponse(status_code=200,content={"message": "Documents ingested successfully"})
        else:
            logger.log(f"Error ingesting documents: {result}", level="error")
            raise e
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/qa_service")
async def qa_service(request: QARequest):
    try:
        message = request.message
        filter = request.filter

        if not message:
            return JSONResponse(status_code=400, content={"Msg":"Message is required"})
        
        async with AsyncClient() as client:
            if filter.strip():
                result = await app.state.qna_service.get_answer(message,{'source':filter})
            else: 
                result = await app.state.qna_service.get_answer(message)

        if result.lower().startswith('error'):
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
        return JSONResponse(status_code=200,content={"response":result})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    

@app.get("/list_documents")
async def list_documents():
    """
    List all documents available in the database
    """
    try:
        result = await app.state.list_doc.get_doc_list()

        if type(result)== str and result.lower().startswith('error'):
            raise HTTPException(
                status_code=500, 
                detail="Internal Server Error"
            )
        
        if result == []:
            return JSONResponse(
                status_code=200, 
                content={"message":"No documents found"}
            )
        
        source = [doc[0] for doc in result]
        logger.log(f"Documents found: {source}", level="info")
        return JSONResponse(status_code=200, content={"message":source})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        workers=2,  # Number of worker processes
        limit_concurrency=100,  # Max concurrent connections
        loop="uvloop" # Faster event loop implementation
    )