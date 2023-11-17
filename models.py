import re
from abc import ABC, abstractmethod
from typing import Any, Dict
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ValidationError, validator

class Validator(ABC):
    @abstractmethod
    def validate(cls, v):
        pass

class StringValidator(Validator):
    @classmethod
    def validate(cls, v):
        if isinstance(v, str):
            return v

class PhoneNumberValidator(Validator):
    @classmethod
    def validate(cls, v):
        if re.fullmatch(r'\+7 \d{3} \d{3} \d{2} \d{2}', v):
            return v

class DateValidator(Validator):
    @classmethod
    def validate(cls, v):
        formats = ['%d.%m.%Y', '%Y.%m.%d']
        for format in formats:
            try:
                return datetime.strptime(v, format)
            except ValueError:
                continue

class EmailValidator(Validator):
    @classmethod
    def validate(cls, v):
        try:
            return EmailStr._validate(v)
        except ValueError:
            pass

datatypes = [PhoneNumberValidator, DateValidator, EmailValidator]

class DynamicModel(BaseModel):
    fields: Dict[str, Any] = Field(...)

    @validator('fields', each_item=True)
    def validate_fields(cls, value, **kwargs):
        if StringValidator.validate(value):
            for custom_type in datatypes:
                if v:=custom_type.validate(value):
                    return v
            else:
                raise ValueError
