import re
from abc import ABC, abstractmethod
from typing import Any, Dict
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ValidationError, validator

class Validator(ABC):
    @abstractmethod
    def validate(cls, v):
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

class StringValidator(Validator):
    @classmethod
    def validate(cls, v: str):
        if isinstance(v, str):
            return v

    @classmethod
    def __str__(cls) -> str:
        return 'string'

class PhoneNumberValidator(Validator):
    @classmethod
    def validate(cls, v: str):
        if re.fullmatch(r'\+7 \d{3} \d{3} \d{2} \d{2}', v):
            return v
    @classmethod
    def __str__(cls) -> str:
        return 'phone number'

class DateValidator(Validator):
    formats = ['%d.%m.%Y', '%Y.%m.%d']
    @classmethod
    def validate(cls, v: str):
        for format in cls.formats:
            try:
                return datetime.strptime(v, format)
            except ValueError:
                continue

    @classmethod
    def __str__(cls) -> str:
        return 'date'

class EmailValidator(Validator):
    @classmethod
    def validate(cls, v: str):  # sourcery skip: use-contextlib-suppress
        try:
            return EmailStr._validate(v)
        except ValueError:
            pass
    @classmethod
    def __str__(cls) -> str:
        return 'email'


datatypes = [PhoneNumberValidator, DateValidator, EmailValidator]


class DynamicModel(BaseModel):
    fields: Dict[str, Any] = Field(...)

    @validator('fields', each_item=True)
    def validate_fields(cls, value, **kwargs):
        if StringValidator.validate(value):
            return cls.__check_datatypes(value)
        else:
            raise ValueError

    @classmethod
    def __check_datatypes(cls, value):
        for custom_type in datatypes:
            if v := custom_type.validate(value):
                return v
        return value


class FieldsDataTypesGetter:

    @classmethod
    def get_datatype(cls, value):
        if isinstance(value, datetime):
            return DateValidator.__str__()

        for custom_type in datatypes:
            if custom_type.validate(value):
                return(custom_type.__str__())
            
        if not StringValidator.validate(value):
            return 'invalid datatype'
        return StringValidator.__str__()

    @classmethod
    def check(cls, fields):
        return {item: cls.get_datatype(value) for item, value in fields.fields.items()}