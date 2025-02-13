from typing import Generic, Optional, Type, TypeVar, Sequence
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from app.misc.db import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class BaseService(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType], db_session: Session):
        self.model = model
        self.db_session = db_session

    def get_by_id(self, id_: str) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id_)
        result = self.db_session.execute(stmt)
        obj: Optional[ModelType] = result.scalars().one()
        if obj is None:
            raise Exception(f"{self.model} with {id_=} not found")
        return obj

    def get_by_details(self, **kwargs) -> Optional[ModelType]:
        stmt = select(self.model).where(
            and_(*[getattr(self.model, k) == v for k, v in kwargs.items()])
        )
        result = self.db_session.execute(stmt)
        obj: Optional[ModelType] = result.scalars().one()
        if obj is None:
            raise Exception(f"{self.model} with {kwargs=} not found")
        return obj

    def list(self) -> Sequence[ModelType]:
        result = self.db_session.execute(select(self.model))
        objs: Sequence[ModelType] = result.scalars().all()
        return objs

    def create(self, obj: CreateSchemaType) -> ModelType:
        db_obj: ModelType = self.model(**obj.model_dump())
        self.db_session.add(db_obj)
        self.db_session.flush()
        self.db_session.commit()
        self.db_session.refresh(db_obj)
        return db_obj

    def delete(self, id_: UUID) -> None:
        obj = self.get_by_id(id_)
        self.db_session.delete(obj)
        self.db_session.commit()
