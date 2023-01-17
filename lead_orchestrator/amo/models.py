from typing import Optional, Any
from pydantic import BaseModel, Field


class CustomField(BaseModel):
    id: int
    name: str
    values: list[Any]


class LeadField0(BaseModel):
    id: int
    name: str | None
    status_id: int | None
    old_status_id: Optional[int]
    price: str | None
    responsible_user_id: Optional[str]
    last_modified: int | str | None
    modified_user_id: Optional[int]
    created_user_id: Optional[int]
    date_create: int | str | None
    created_at: Optional[int]
    updated_at: Optional[int]

    pipeline_id: Optional[int]
    tags: Optional[dict]
    account_id: Optional[int]
    custom_fields: Optional[list[CustomField]]


class LeadHookStatus(BaseModel):
    field_0: LeadField0 = Field(..., alias='0')


class Action(BaseModel):
    __root__: dict[str, list[LeadHookStatus]] | dict[str, LeadHookStatus]
    # update: list[Field0] = None
    # add: list[Field0] = None

    # delete: Optional[HookStatus] = None
    # status: list[Field0] = None

    class Config:
        smart_union = True


class LeadAction(BaseModel):
    delete: LeadField0 | None = None
    add: list[LeadHookStatus] | None = None
    update: list[LeadHookStatus] | None = None
    status: list[LeadField0] | None = None


class _Links(BaseModel):
    self: str


class Account(BaseModel):
    subdomain: str
    id: str | None
    _links: _Links | None


class WebHook(BaseModel):
    task: Action | None
    leads: LeadAction | None
    unsorted: Action | None
    message: Action | None
    account: Account | None

    # class Config:
    # allow_population_by_field_name = True
