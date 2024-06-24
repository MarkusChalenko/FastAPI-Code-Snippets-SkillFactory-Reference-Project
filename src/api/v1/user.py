from time import sleep

import httpx
from fastapi import APIRouter, Depends
from fastapi import BackgroundTasks

from auth.auth import has_role

# Создаем APIRouter с префиксом "/user" и тегом 'user' для отображения в документации
user_router = APIRouter(prefix="/user", tags=['user'])


@user_router.get("/{user_id}")
async def get_user(user_id: int):
    async with httpx.AsyncClient(base_url='https://jsonplaceholder.typicode.com') as client:
        response = await client.get(f'/users/{user_id}')
        return response.json()


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        sleep(3)
        content = f"notification for {email}: {message}"
        email_file.write(content)


@user_router.post("/send-notification/{email}", dependencies=[Depends(has_role(["admin"]))])
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
