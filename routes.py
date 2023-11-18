from fastapi import APIRouter, Depends, HTTPException, status

from models import DynamicModel, FieldsDataTypesGetter
from db import form_finder, form_embedder


router = APIRouter()

@router.post('/get_form')
async def get_form(fields: DynamicModel):
    data = await form_finder.get_form_by_fields(fields.fields)
    return data if data is not None else FieldsDataTypesGetter.check(fields)

@router.post('/add_form')
async def get_form(form_name : str, fields: DynamicModel):
    return await form_embedder.add_form(form_name=form_name, 
                                        fields=fields.fields)