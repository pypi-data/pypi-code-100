import datetime
from typing import Optional, List

from .. import fields
from ..core import AlfaObject


class Customer(AlfaObject):
    id = fields.Integer()
    name = fields.String()
    branch_ids = fields.ListField(fields.Integer())
    teacher_ids = fields.ListField(fields.Integer())
    is_study = fields.Bool()
    study_status_id = fields.Integer()
    lead_status_id = fields.Integer()
    lead_source_id = fields.Integer()
    assigned_id = fields.Integer()
    legal_type = fields.Integer()
    legal_name = fields.String()
    company_id = fields.Integer()
    dob = fields.DateField()
    balance = fields.Float()
    paid_lesson_count = fields.Integer()
    phone = fields.ListField(fields.String())
    email = fields.ListField(fields.String())
    web = fields.ListField(fields.String())
    addr = fields.ListField(fields.String())
    note = fields.String(fields.String())

    def __init__(
            self,
            id_: Optional[int] = None,
            name: Optional[str] = None,
            branch_ids: Optional[List[int]] = None,
            teacher_ids: Optional[List[int]] = None,
            is_study: Optional[bool] = None,
            study_status_id: Optional[int] = None,
            lead_status_id: Optional[int] = None,
            assigned_id: Optional[int] = None,
            legal_type: Optional[int] = None,
            legal_name: Optional[str] = None,
            company_id: Optional[int] = None,
            dob: Optional[datetime.date] = None,
            balance: Optional[float] = None,
            paid_lesson_count: Optional[int] = None,
            phone: Optional[List[str]] = None,
            email: Optional[List[str]] = None,
            web: Optional[List[str]] = None,
            addr: Optional[List[str]] = None,
            note: Optional[str] = None,
            **kwargs,
    ):
        super(Customer, self).__init__(
            id=id_,
            name=name,
            branch_ids=branch_ids,
            teacher_ids=teacher_ids,
            is_study=is_study,
            study_status_id=study_status_id,
            lead_status_id=lead_status_id,
            assigned_id=assigned_id,
            legal_type=legal_type,
            legal_name=legal_name,
            company_id=company_id,
            dob=dob,
            balance=balance,
            paid_lesson_count=paid_lesson_count,
            phone=phone,
            email=email,
            web=web,
            addr=addr,
            note=note,
            **kwargs,
        )
