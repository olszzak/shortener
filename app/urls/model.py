import random
import string

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import validates

from app.misc.db import Base
from app.settings import get_settings

settings = get_settings()


class Url(Base):
    __tablename__ = "url"

    @staticmethod
    def generate_id():
        return "".join(
            random.choices(
                string.ascii_letters + string.digits, k=settings.short_id_length
            )
        )

    id = Column(String, primary_key=True, default=generate_id)
    url = Column(String, nullable=False, unique=True)
    count = Column(Integer, default=0)
    created_by_ip = Column(String, nullable=False)
    created_by_agent = Column(String, nullable=False)

    @validates("id")
    def validate_id_length(self, _, id_):
        if len(id_) != settings.short_id_length:
            raise ValueError("failed simple email validation")
        return id_
