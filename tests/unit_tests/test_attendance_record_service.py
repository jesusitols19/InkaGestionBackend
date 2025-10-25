import pytest
from unittest.mock import MagicMock
from datetime import date, datetime
from app.application.attendancerecord.attendance_record_service import AttendanceRecordService
from app.application.attendancerecord.attendance_record_dto import AttendanceStartDTO
from app.helpers.jsend_response import jsend_fail, jsend_success

@pytest.fixture
def setup_service():
    # Creamos mocks para los repositorios
    repo = MagicMock()
    employee_repo = MagicMock()
    employee_shift_repo = MagicMock()
    shift_repo = MagicMock()
    service = AttendanceRecordService(repo, employee_repo, employee_shift_repo, shift_repo)
    return service, repo, employee_repo, employee_shift_repo, shift_repo


# Escenario 1 — El empleado no existe

def test_get_attendance_employee_not_found(setup_service):
    service, repo, employee_repo, *_ = setup_service

    # Mockeamos que no se encuentre el empleado
    employee_repo.find_by_employee_id.return_value = None

    result = service.get_attendance(employee_id=1)

    assert result == jsend_fail({"message": "Empleado no encontrado"})
    employee_repo.find_by_employee_id.assert_called_once_with(1)

# Escenario 2 — Empleado existe, y hay datos

def test_get_attendance_success(setup_service):
    service, repo, employee_repo, *_ = setup_service

    # Mockeamos el empleado
    employee_repo.find_by_employee_id.return_value = {"id": 1, "name": "Juan"}

    # Mockeamos la asistencia activa y el historial
    active_record = MagicMock(
        id=1,
        record_date=date.today(),
        time_in="08:00",
        time_out=None,
        work_hours=None,
        overtime_hours=None,
        status="A_TIEMPO",
        justification=None
    )

    history_record = MagicMock(
        id=2,
        record_date=date.today(),
        time_in="08:10",
        time_out="16:00",
        work_hours=7.5,
        overtime_hours=0.0,
        status="TARDANZA",
        justification=None
    )

    repo.get_active_attendance.return_value = active_record
    repo.list_history.return_value = [history_record]

    result = service.get_attendance(employee_id=1)

    assert "data" in result
    assert "active_record" in result["data"]
    assert "records" in result["data"]
    assert result["status"] == "success"




def test_start_attendance_employee_not_found(setup_service):
    service, repo, employee_repo, employee_shift_repo, shift_repo = setup_service

    # Mock: el empleado no existe
    employee_repo.find_by_employee_id.return_value = None

    dto = AttendanceStartDTO(
        employee_id=1,
        supervisor_user_id=2,
        timestamp=None,
        justification=None
    )

    result = service.start_attendance(dto)

    assert result == jsend_fail({"message": "Empleado no encontrado"}) 
    employee_repo.find_by_employee_id.assert_called_once_with(1)



def test_start_attendance_success(setup_service):
    service, repo, employee_repo, employee_shift_repo, shift_repo = setup_service

    # 1️⃣ Mock: el empleado existe
    employee_repo.find_by_employee_id.return_value = {"id": 1, "name": "Juan"}

    # 2️⃣ Mock: el empleado tiene un turno asignado
    employee_shift_repo.get_active_employee_shift.return_value = MagicMock(
        shift_id=10,
        start_date=date.today(),
        end_date=date.today()
    )

    # 3️⃣ Mock: el turno existe
    shift_repo.get_shift_by_id.return_value = MagicMock(
        name="Mañana",
        start_time=datetime.strptime("08:00", "%H:%M").time(),
        end_time=datetime.strptime("16:00", "%H:%M").time(),
        tolerance_minutes=10
    )

    # 4️⃣ Mock: no hay asistencia activa ni registro previo
    repo.get_active_attendance.return_value = None
    repo.exists_record_today.return_value = False

    # 5️⃣ Mock: crear asistencia devuelve un objeto simulado
    created_record = MagicMock(
        id=99,
        time_in=datetime.now(),
        status="A_TIEMPO"
    )
    repo.create_start.return_value = created_record

    # 6️⃣ Creamos el DTO
    dto = AttendanceStartDTO(
        employee_id=1,
        supervisor_user_id=2,
        timestamp=datetime.now(),
        justification=None
    )

    # 7️⃣ Ejecutamos
    result = service.start_attendance(dto)

    # 8️⃣ Aserciones
    assert result["status"] == "success"
    assert result["data"]["message"] == "Asistencia iniciada"
    assert result["data"]["attendance"]["id"] == 99
    assert result["data"]["attendance"]["status"] == "A_TIEMPO"

    # 9️⃣ Verificamos llamadas a repositorios
    employee_repo.find_by_employee_id.assert_called_once_with(1)
    employee_shift_repo.get_active_employee_shift.assert_called_once()
    shift_repo.get_shift_by_id.assert_called_once_with(10)
    repo.create_start.assert_called_once()
