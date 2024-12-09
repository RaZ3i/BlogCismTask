from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession


from src.schemas.schemas import Token

from src.config import settings
from src.database import get_async_session
from src.schemas.schemas import (
    NewUserIdOut,
    UserRegister,
    ResponseLogout,
)
from src.service.service import (
    create_user,
    authenticate_user,
)
from src.errors import Duplicate
from typing import Annotated


from src.utils.utils import create_access_token


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register/", status_code=status.HTTP_201_CREATED, response_model=NewUserIdOut
)
async def create_new_user(
        new_user: UserRegister,
        session: AsyncSession = Depends(get_async_session),
):
    try:
        result = await create_user(new_user, session=session)
        return result
    except Duplicate as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.msg)


@router.post("/logout/", response_model=ResponseLogout)
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {"mes": "Пользователь вышел из системы", "success": True}


@router.post("/login/", status_code=status.HTTP_200_OK, response_model=Token)
async def login_for_access_token(
        form_data: Annotated[
            OAuth2PasswordRequestForm,
            Depends(),
        ],
        response: Response,
        session: AsyncSession = Depends(get_async_session),
):
    data = await authenticate_user(
        username=form_data.username,
        password=form_data.password,
        session=session,
    )
    if not data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверные логин или пароль"
        )
    access_token = create_access_token(
        data={
            "sub": data.username,
            "id": data.id,
            "username": data.username,
            "email": data.email,
        },
        expires_delta=settings.get_auth_data()["access_token_expire_minutes"],
    )
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return Token(access_token=access_token, token_type="bearer", success=True)

# async def auth_user(
#     user_data: UserAuthIn, session: AsyncSession = Depends(get_async_session)
# ):
#     try:
#         return await login_for_access_token(user_data, session=session)
#     except Missing as exc:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=exc.msg)

# @router.get("/proverka", response_model=User)
# async def get_user_from_table(
#     user_name: str, session: AsyncSession = Depends(get_async_session)
# ):
#     data = await get_user(user_name, session=session)
#     return data
#
#
# @router.post("/proverka", response_model=User)
# async def auth_user_from_table(
#     user_name: str, password: str, session: AsyncSession = Depends(get_async_session)
# ):
#     data = await authenticate_user(user_name, password, session=session)
#     return data
