from app.db.repository.base_repo import BaseRepository
from app.db.models.anonymous_report import AnonymousReport

from sqlalchemy import func
from geoalchemy2 import Geometry

class ReportRepository(BaseRepository):
    def createreport(self,report:AnonymousReport):

        self.session.add(report)
        self.session.commit()
        self.session.refresh(report)
        return report
    
    def showreport(self):
        # reports = self.session.query(AnonymousReport).all()
        # return reports
        ## THE ABOVE WONT WORK CAUSE WE ARE USING POSTGIS AND FASTAPI CANT SERIALIZE THOSE FIELDS


        reports = (self.session.query(
            AnonymousReport.id,
            AnonymousReport.title,
            AnonymousReport.description,
            func.ST_Y(AnonymousReport.location.cast(Geometry)).label("latitude"),
            func.ST_X(AnonymousReport.location.cast(Geometry)).label("longitude"),
            AnonymousReport.verified
        ))
        return reports
    
    def get_report_by_id(self,report_id:int):
        report = self.session.query(AnonymousReport).filter_by(id=report_id).first()
        return report
    
    def update_report(self,report:AnonymousReport):
        self.session.commit()
        self.session.refresh(report)

        

        return report
