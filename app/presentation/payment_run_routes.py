from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.dependencies import get_payment_run_service
from app.application.paymentrunitem.payment_run_items_dto import PaymentRunItemCreateDTO


router = APIRouter()


@router.get("/get-all-payment-runs")
def get_all_payment_run(db: Session = Depends(get_db)):
    service = get_payment_run_service(db)
    response = service.get_all_payment_run()
    return response

@router.post("/create-payment-run/{created_by}")
def create_payment_run(created_by: int, db: Session = Depends(get_db)):
    service = get_payment_run_service(db)
    response = service.create_payment_run(created_by)
    return response

@router.post("/add-item")
def create_payment_run(dto: PaymentRunItemCreateDTO, db: Session = Depends(get_db)):
    service = get_payment_run_service(db)
    response = service.add_item(dto)
    return response

@router.put("/generate-file_bank/{run_id}/{file_path}")
def generate_file_bank(run_id: int, file_path: str, db: Session = Depends(get_db)):
    service = get_payment_run_service(db)
    response = service.generate_file_bank(run_id, file_path)
    return response

@router.put("/close-run/{run_id}")
def close_run(run_id: int, db: Session = Depends(get_db)):
    service = get_payment_run_service(db)
    response = service.close_run(run_id)
    return response