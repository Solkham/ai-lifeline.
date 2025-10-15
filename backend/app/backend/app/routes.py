from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .db import get_db
from .models import User, Base
from passlib.hash import bcrypt
from fastapi import status

router = APIRouter()

@router.post("/register")
async def register(email: str, password: str, full_name: str = "", db: AsyncSession = Depends(get_db)):
    # Проверка на существование пользователя
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # Создаём пользователя
    hashed_pw = bcrypt.hash(password)
    new_user = User(email=email, hashed_password=hashed_pw, full_name=full_name)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"id": new_user.id, "email": new_user.email}
