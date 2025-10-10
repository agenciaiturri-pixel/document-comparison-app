from fastapi import Body, FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Optional
import os
import uuid
from datetime import datetime

# Import our custom modules
from app.core.config import settings
from app.schemas.comparison import (
    ComparisonRequest,
    ComparisonResponse,
    DocumentData,
    ComparisonSummary,
    ExportFormat
)
from app.services.document_processor import DocumentProcessor
from app.services.comparison_engine import ComparisonEngine
from app.services.report_generator import ReportGenerator
from app.services.file_handler import FileHandler
from app.services.session_manager import session_manager
from app.utils.logger import setup_logger, log_api_request, log_error_with_context

# Initialize FastAPI app
app = FastAPI(
    title="Document Comparison API",
    description="API for comparing commercial invoices and bills of lading",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
logger = setup_logger("main")
document_processor = DocumentProcessor()
comparison_engine = ComparisonEngine()
report_generator = ReportGenerator()
file_handler = FileHandler()

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("Starting Document Comparison API")
    
    # Create upload directory if it doesn't exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.REPORTS_DIR, exist_ok=True)
    
    logger.info(f"Upload directory: {settings.UPLOAD_DIR}")
    logger.info(f"Reports directory: {settings.REPORTS_DIR}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Document Comparison API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check_alt():
    """Alternative health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/upload", response_model=dict)
async def upload_files(
    commercial_invoice: UploadFile = File(...),
    bill_of_lading: UploadFile = File(...)
):
    """Upload and process two documents for comparison"""
    try:
        log_api_request(
            "upload_files",
            {
                "commercial_invoice": commercial_invoice.filename,
                "bill_of_lading": bill_of_lading.filename,
            },
        )
        logger.info(f"Processing upload request - Commercial Invoice: {commercial_invoice.filename}, Bill of Lading: {bill_of_lading.filename}")

        # Validate file types
        allowed_types = ["application/pdf", "image/jpeg", "image/png", "image/jpg"]

        if commercial_invoice.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail=f"Invalid file type for commercial invoice: {commercial_invoice.content_type}")
        
        if bill_of_lading.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail=f"Invalid file type for bill of lading: {bill_of_lading.content_type}")
        
        # Generate job ID for this upload session
        job_id = str(uuid.uuid4())
        
        # Save uploaded files
        from app.schemas.comparison import DocumentType
        ci_path = await file_handler.save_uploaded_file(commercial_invoice, DocumentType.INVOICE, job_id)
        bol_path = await file_handler.save_uploaded_file(bill_of_lading, DocumentType.BILL_OF_LADING, job_id)
        
        # Process documents
        logger.info("Processing commercial invoice...")
        ci_data = await document_processor.extract_data(ci_path, DocumentType.INVOICE)
        
        logger.info("Processing bill of lading...")
        bol_data = await document_processor.extract_data(bol_path, DocumentType.BILL_OF_LADING)
        
        # Perform comparison
        logger.info("Comparing documents...")
        comparison_result = await comparison_engine.compare_documents(ci_data, bol_data)

        # Generate session ID for this comparison
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        await session_manager.create_session(job_id, session_id)
        await session_manager.store_results(job_id, ci_data, bol_data, comparison_result)

        return {
            "job_id": job_id,
            "session_id": session_id,
            "commercial_invoice": ci_data.model_dump(),
            "bill_of_lading": bol_data.model_dump(),
            "comparison_result": comparison_result.model_dump(),
            "message": "Documents processed and compared successfully"
        }
        
    except Exception as e:
        log_error_with_context(e, {"endpoint": "upload_files"})
        raise HTTPException(status_code=500, detail=f"Error processing documents: {str(e)}")

@app.post("/api/compare", response_model=ComparisonResponse)
async def compare_documents(request: ComparisonRequest):
    """Compare two document data objects"""
    try:
        log_api_request("compare_documents", request.model_dump())
        logger.info(f"Starting document comparison for session: {request.session_id}")

        # Perform comparison
        comparison_result = await comparison_engine.compare_documents(
            request.commercial_invoice,
            request.bill_of_lading
        )

        job_id = await session_manager.get_job_id_for_session(request.session_id)
        if job_id:
            await session_manager.store_results(
                job_id=job_id,
                invoice=request.commercial_invoice,
                bill_of_lading=request.bill_of_lading,
                comparison=comparison_result,
            )

        return ComparisonResponse(
            session_id=request.session_id,
            comparison_result=comparison_result,
            timestamp=datetime.now()
        )

    except Exception as e:
        log_error_with_context(e, {"endpoint": "compare_documents"})
        raise HTTPException(status_code=500, detail=f"Error comparing documents: {str(e)}")

@app.post("/api/export/{session_id}")
async def export_report(
    session_id: str,
    format: ExportFormat,
    comparison_data: Optional[ComparisonSummary] = Body(default=None)
):
    """Export comparison report in specified format"""
    try:
        log_api_request("export_report", {"session_id": session_id, "format": format.value})
        logger.info(f"Exporting report for session {session_id} in {format} format")

        if comparison_data is None:
            comparison_result = await session_manager.get_session_summary(session_id)
            comparison_data = comparison_result.summary

        # Generate report
        if format == ExportFormat.PDF:
            report_path = report_generator.generate_pdf_report(comparison_data, session_id)
            media_type = "application/pdf"
        elif format == ExportFormat.CSV:
            report_path = report_generator.generate_csv_report(comparison_data, session_id)
            media_type = "text/csv"
        elif format == ExportFormat.JSON:
            report_path = report_generator.generate_json_report(comparison_data, session_id)
            media_type = "application/json"
        else:
            raise HTTPException(status_code=400, detail="Invalid export format")
        
        # Return file
        filename = os.path.basename(report_path)
        return FileResponse(
            path=report_path,
            media_type=media_type,
            filename=filename
        )
        
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        log_error_with_context(e, {"endpoint": "export_report"})
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@app.get("/api/sessions/{session_id}")
async def get_session_info(session_id: str):
    """Get information about a comparison session"""
    try:
        log_api_request("get_session_info", {"session_id": session_id})
        return await session_manager.get_session(session_id)

    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        log_error_with_context(e, {"endpoint": "get_session_info"})
        raise HTTPException(status_code=500, detail=f"Error retrieving session info: {str(e)}")

@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a comparison session and its files"""
    try:
        logger.info(f"Deleting session: {session_id}")
        log_api_request("delete_session", {"session_id": session_id})
        job_id = await session_manager.delete_session(session_id)
        if job_id is None:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        await file_handler.cleanup_job(job_id)
        return {
            "message": f"Session {session_id} deleted successfully",
            "job_id": job_id
        }

    except Exception as e:
        log_error_with_context(e, {"endpoint": "delete_session"})
        raise HTTPException(status_code=500, detail=f"Error deleting session: {str(e)}")

@app.post("/api/compare/{job_id}")
async def start_comparison(job_id: str):
    """Start document comparison process (already handled in upload)"""
    try:
        log_api_request("start_comparison", {"job_id": job_id})
        return await session_manager.get_job_status(job_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error in comparison endpoint for job {job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status/{job_id}")
async def get_job_status(job_id: str):
    """Get job processing status (processing completed in upload)"""
    try:
        log_api_request("get_job_status", {"job_id": job_id})
        return await session_manager.get_job_status(job_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting status for job {job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/result/{job_id}.json")
async def get_job_result(job_id: str):
    """Get job processing results"""
    try:
        log_api_request("get_job_result", {"job_id": job_id})
        return await session_manager.get_job_result(job_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting result for job {job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )