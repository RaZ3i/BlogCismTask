from datetime import datetime
from typing import Annotated
from fastapi import Depends, HTTPException, status
from jose import JWTError

from src.config import settings
from sqlalchemy import select, update, delete, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.utils.utils import (
    verify_password,
    get_password_hash,
    get_token_from_cookies,
    decode_token,
)
from src.database import get_async_session, async_session_factory
from src.models.models import User as User_table, Article as Article_table
from src.schemas.schemas import UserRegister, TokenData, User, PostCreate
from src.errors import Duplicate
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_user(user_name: str, session: AsyncSession):
    stmt = select(User_table).filter_by(username=user_name)
    user = await session.execute(stmt)
    return user.scalar()


async def authenticate_user(
    username: str,
    password: str,
    session: AsyncSession,
):
    stmt = select(User_table).filter_by(username=username)
    user = await session.execute(stmt)
    user = user.scalar()
    if not user:
        return False
    if not verify_password(password, user.hash_password):
        return False
    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_async_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверные логин или пароль",
    )
    try:
        payload = jwt.decode(
            token,
            key=settings.get_auth_data()["secret_key"],
            algorithms=settings.get_auth_data()["algorithm"],
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(user_name=token_data.username, session=session)
    if user is None:
        raise credentials_exception
    return user


async def get_current_user_from_cookies(token: str = Depends(get_token_from_cookies)):
    try:
        payload = decode_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не найден"
        )
    return payload


async def create_user(
    new_user: UserRegister,
    session: AsyncSession,
):
    try:
        data = new_user.model_dump()
        data["hash_password"] = get_password_hash(new_user.hash_password)
        stmt = User_table(**data)
        session.add(stmt)
        await session.flush()
        await session.commit()
        return {"id": stmt.id, "success": True}
    # except IntegrityError:
    #     return IntegrityError
    except IntegrityError:
        raise Duplicate(msg=f"Пользователь с указанными данными уже существует")
        # return IntegrityError
    # except IntegrityError:
    #     raise Duplicate(msg=f"Field {new_user.username} already exist"


async def create_post(
    current_user, post_theme: str, post_text: str, session: AsyncSession
):
    # try
    article_author = current_user["username"]
    article_author_id = current_user["id"]
    post_data = {
        "article_theme": post_theme,
        "article_text": post_text,
        "article_author_id": article_author_id,
        "article_author": article_author,
    }
    stmt = Article_table(**post_data)
    session.add(stmt)
    await session.flush()
    await session.commit()
    return {
        "post_data": {
            "author": article_author,
            "author_id": article_author_id,
            "post_theme": post_theme,
            "post_text": post_text,
            "created_at": datetime.now(),
        },
        "success": True,
    }


async def modify_post(
    current_user, post_id: int, new_post_text: str, session: AsyncSession
):
    stmt_3 = select(Article_table).filter_by(id=post_id)
    res = await session.execute(stmt_3)
    author_id = res.scalar().article_author_id
    if author_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Пользователь не авторизован: пользователь с id {current_user["id"]} хочет отредактировать пост, "
            f"который создал пользователь с id {author_id}",
        )
    else:
        stmt_1 = (
            update(Article_table)
            .filter_by(id=post_id, article_author_id=current_user["id"])
            .values(article_text=new_post_text)
        )
        await session.execute(stmt_1)
        await session.flush()
        stmt_2 = select(Article_table).filter_by(id=post_id)
        result = await session.execute(stmt_2)
        await session.flush()
        await session.commit()
        return {
            "mes": "Пост успешно отредактирован",
            "date_change": result.scalar().updated_at,
            "success": True,
        }


async def delete_post(current_user, post_id: int, session: AsyncSession):
    stmt = delete(Article_table).filter_by(
        id=post_id, article_author_id=current_user["id"]
    )
    await session.execute(stmt)
    await session.commit()
    return {"mes": "Пост успешно удален", "success": True}


async def like_or_dislike(user_id: int, post_id: int, session: AsyncSession):
    stmt_1 = select(Article_table).filter_by(id=post_id)
    res = await session.execute(stmt_1)
    res = res.scalar()
    if res.likes_id_users is None or str(user_id) not in res.likes_id_users:
        stmt_2 = (
            update(Article_table)
            .filter_by(id=post_id)
            .values(
                likes_id_users=func.array_append(
                    Article_table.likes_id_users, str(user_id)
                )
            )
        )
        await session.execute(stmt_2)
        await session.flush()
        await session.commit()
        return {"success": True, "mes": "like"}
    else:
        stmt_3 = (
            update(Article_table)
            .filter_by(id=post_id)
            .values(
                likes_id_users=func.array_remove(
                    Article_table.likes_id_users, str(user_id)
                )
            )
        )
        await session.execute(stmt_3)
        await session.flush()
        await session.commit()
        return {"success": True, "mes": "dislike"}


async def get_posts():
    async with async_session_factory() as session:
        stmt = select(Article_table).order_by(Article_table.id.desc())
        res = await session.execute(stmt)
        data = res.scalars().all()
        await session.commit()
        return data
    # stmt = select(Article_table)
    # res = await session.execute(stmt)
    # data = res.scalars().all()
    # await session.commit()
    # return data


# except:
#     return {"mes": "Error"}


# try:
#     stmt = select(User_table).where(User_table.username == user_data.username)
#     data = await session.execute(stmt)
#     pass_ver = verify_password(
#         user_data.hash_password,
#         data.scalar_one().hash_password,
#     )
#     if pass_ver is True:
#         return True
#     else:
#         raise Missing(msg="Неверные логин и(или) пароль")
# except NoResultFound:
#     raise Missing(msg="Неверные логин и(или) пароль")
