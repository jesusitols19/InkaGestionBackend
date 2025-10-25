from app.domain.paymentruns import PaymentRun
from app.domain.paymentrunitems import PaymentRunItem
from app.application.paymentruns.payment_runs_dto import PaymentRunsCreateDTO
from app.application.paymentrunitem.payment_run_items_dto import PaymentRunItemCreateDTO
from app.infrastructure.payment_runs_repository import PaymentRunRepository
from app.infrastructure.payment_runs_item_repository import PaymentRunItemRepository
from app.helpers.jsend_response import jsend_success, jsend_fail
from datetime import datetime

class PaymentRunService:
    def __init__(self, repo: PaymentRunRepository, paymentRunItemRepo : PaymentRunItemRepository):
        self.repo = repo
        self.paymentRunItemRepo = paymentRunItemRepo


    def create_payment_run(self, created_by : int):
        run = PaymentRun(created_by=created_by)

        return jsend_success(self.repo.create_payment_runs(run))
    
    def add_item(self, paymentRunItem:PaymentRunItemCreateDTO):
        runItem = PaymentRunItem(**paymentRunItem.__dict__)
        return jsend_success(self.paymentRunItemRepo.create_payment_run_item(runItem))
    
    def generate_file_bank(self, run_id: int, file_path : str):
        items = self.paymentRunItemRepo.find_by_id(run_id)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("Empleado,Banco,Monto\n")
            for i in items:
                f.write(f"{i.employee_id},{i.bank_account},{i.amount}\n")
        
        run = self.repo.find_by_id(run_id)
        run.file_name = file_path.split("/")[-1]
        self.repo.update(run)
        return file_path
    

    def close_run(self, run_id: int):

        run = self.repo.find_by_id(run_id)

        if not run:
            return jsend_fail("No existe una corrida de pago para este id")
        
        run.status = "PROCESSED"

        run.total_amount = sum([i.amount for i in self.paymentRunItemRepo.find_by_id(run_id)])
        run.created_at = datetime.now()
        return self.repo.update(run)



