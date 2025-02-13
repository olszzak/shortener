from fastapi import Depends, Request, Body
from pydantic import BaseModel, Field


def get_user_ip(request: Request):
    return request.client.host


def get_user_agent(request: Request):
    return request.headers["user-agent"]


class CreateUrlSchema(BaseModel):
    url: str = Field(Body(embed=True))
    created_by_ip: str = Field(Depends(get_user_ip))
    created_by_agent: str = Field(Depends(get_user_agent))


class UrlSchema(BaseModel):
    id: str
    url: str


class StatSchema(BaseModel):
    count: int
    url: str
    created_by_ip: str
    created_by_agent: str
