from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...core.database import get_db
from ...models.tax_form import TaxForm

router = APIRouter()

@router.get("/")
async def get_tax_forms(user_id: int = 1, db: Session = Depends(get_db)):
    """Get all tax forms for user"""
    forms = db.query(TaxForm).filter(TaxForm.user_id == user_id).all()
    return [
        {
            "id": form.id,
            "form_type": form.form_type,
            "tax_year": form.tax_year,
            "status": form.status,
            "created_at": form.created_at
        }
        for form in forms
    ]

@router.post("/")
async def create_tax_form(
    form_type: str,
    tax_year: int,
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    """Create a new tax form"""
    new_form = TaxForm(
        user_id=user_id,
        form_type=form_type,
        tax_year=tax_year,
        form_data={}
    )
    db.add(new_form)
    db.commit()
    db.refresh(new_form)

    return {"message": "Tax form created", "form_id": new_form.id}

@router.get("/{form_id}")
async def get_tax_form(form_id: int, db: Session = Depends(get_db)):
    """Get specific tax form"""
    form = db.query(TaxForm).filter(TaxForm.id == form_id).first()
    if not form:
        raise HTTPException(status_code=404, detail="Tax form not found")

    return {
        "id": form.id,
        "form_type": form.form_type,
        "tax_year": form.tax_year,
        "status": form.status,
        "form_data": form.form_data,
        "calculated_tax": form.calculated_tax
    }

@router.put("/{form_id}")
async def update_tax_form(
    form_id: int,
    form_data: dict,
    db: Session = Depends(get_db)
):
    """Update tax form data"""
    form = db.query(TaxForm).filter(TaxForm.id == form_id).first()
    if not form:
        raise HTTPException(status_code=404, detail="Tax form not found")

    form.form_data = form_data
    # Simple tax calculation (replace with real logic)
    form.calculated_tax = "1000.00"

    db.commit()

    return {"message": "Tax form updated", "calculated_tax": form.calculated_tax}
