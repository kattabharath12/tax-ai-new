from fastapi import APIRouter
from .endpoints import auth, users, tax_forms, documents, payments

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tax_forms.router, prefix="/tax-forms", tags=["tax-forms"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])
