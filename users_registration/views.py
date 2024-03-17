
from fastapi import Request, Response, Depends, HTTPException, Header, UploadFile
from pydantic import BaseModel
from datetime import datetime
import typing
from http import HTTPStatus
from users_registration import app
from users_registration.controller import Controller

class ItemsResponse(BaseModel):
    items: list

class User(BaseModel):
    email: str
    password:str
    products_bucket_list: list
    last_product_date: datetime
    geometry: object



controller = Controller()

@app.post("/users/{user_name}",status_code=HTTPStatus.OK,)
async def create_user(
    user: User,
):

    _create_new_user(
        content=user,
    )
    return Response()



def _create_new_user(content):
    controller.login(content)

@app.get("/users")
async def get_users():
    emails= controller.get_users()
    return ItemsResponse(
        items=emails,
    )