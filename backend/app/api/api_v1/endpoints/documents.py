from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.document import Document
import os
import uuid

router = APIRouter()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = "general",
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    """Upload a document"""
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"

    # In production: save to S3 or local storage
    file_path = f"/uploads/{unique_filename}"

    # Save document record
    new_document = Document(
        user_id=user_id,
        filename=file.filename,
        file_path=file_path,
        file_type=file.content_type,
        file_size=0,  # In production: get actual file size
        document_type=document_type,
        extracted_data="{}"  # In production: run OCR
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return {
        "message": "Document uploaded successfully",
        "document_id": new_document.id,
        "extracted_data": {}  # In production: return OCR results
    }

@router.get("/")
async def get_documents(user_id: int = 1, db: Session = Depends(get_db)):
    """Get all documents for user"""
    documents = db.query(Document).filter(Document.user_id == user_id).all()
    return [
        {
            "id": doc.id,
            "filename": doc.filename,
            "document_type": doc.document_type,
            "file_size": doc.file_size,
            "created_at": doc.created_at
        }
        for doc in documents
    ]

@router.delete("/{document_id}")
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    """Delete a document"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    db.delete(document)
    db.commit()

    return {"message": "Document deleted successfully"}
