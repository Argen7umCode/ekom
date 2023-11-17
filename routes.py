from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter()

@router.post('get_form')
async def get_form()