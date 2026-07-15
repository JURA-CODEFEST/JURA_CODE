from app.db.schemas.anonymous_report import CreateReport
from app.db.models.anonymous_report import AnonymousReport
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from sqlalchemy.orm import Session
from app.db.repository.report_repo import ReportRepository


class ReportService:

    def __init__(self,session:Session):
        self.__ReportRepo = ReportRepository(session=session)


    def CreateReport(self,report_details:CreateReport):

        location = from_shape(
            Point(report_details.longitude,report_details.latitude),
            srid=4326
        )

        new_report = AnonymousReport(
            title = report_details.title,
            description = report_details.description,
            location = location

        )
        self.__ReportRepo.createreport(new_report)
        return{"Success":"Your report was added"}
    
    def show_reports(self):
        return self.__ReportRepo.showreport()
    
    def update_report_verified(self,report_id:int,verified):
        report = self.__ReportRepo.get_report_by_id(report_id=report_id)

        report.verified = verified
        self.__ReportRepo.update_report(report)

        return {
            "message":"Report verification updated"
        }