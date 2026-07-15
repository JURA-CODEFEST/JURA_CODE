from fastapi import APIRouter, Depends
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.db.schemas.anonymous_report import CreateReport,ShowReport
from app.service.reportService import ReportService
from app.utils.protectroute import admin_check_for_privileged_endpoints

report = APIRouter()

@report.post("/add")
def add_report(report_details:CreateReport,session:Session=Depends(get_db)):
    try:
        return ReportService(session=session).CreateReport(report_details=report_details)
    except Exception as error:
        print(error)
        raise(error)
    
@report.get("/show",response_model=list[ShowReport])
def show_report(session:Session=Depends(get_db),admin = Depends(admin_check_for_privileged_endpoints)):
    return ReportService(session).show_reports()

@report.patch("/update-verified/{report_id}")
def update_verified(report_id:int,verified:bool,session:Session=Depends(get_db),admin=Depends(admin_check_for_privileged_endpoints)):
    return ReportService(session).update_report_verified(report_id,verified)