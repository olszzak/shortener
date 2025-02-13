import sqlalchemy

from app.misc.db_base_service import BaseService
from app.misc.deps import get_db
from app.urls.model import Url
from app.urls.schema import CreateUrlSchema, UrlSchema
from sqlalchemy.orm import Session
from fastapi import Depends


class UrlService(BaseService[Url, CreateUrlSchema]):
    def __init__(self, db_session: Session):
        super(UrlService, self).__init__(Url, db_session)

    def get_url(self, id_: str):
        obj = self.get_by_id(id_)
        if obj:
            obj.count += 1

            self.db_session.flush()
            self.db_session.commit()
            self.db_session.refresh(obj)
        return obj

    def create(self, obj: CreateUrlSchema) -> Url:
        try:
            db_obj = super().create(obj)
        except sqlalchemy.exc.IntegrityError:
            self.db_session.rollback()
            db_obj = self.get_by_details(url=obj.url)
        return db_obj


def get_urls_service(db_session: Session = Depends(get_db)) -> UrlService:
    return UrlService(db_session)
