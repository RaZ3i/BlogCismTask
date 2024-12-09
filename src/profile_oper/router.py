from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from src.service.service import (
    create_post,
    modify_post,
    get_current_user_from_cookies,
    delete_post,
    like_or_dislike,
    get_posts,
    get_current_user,
)
from src.schemas.schemas import (
    PostCreate,
    User,
    ModifyData,
    ResponseLike,
    ResponseDelete,
    ResponseModify,
    ResponseCreate,
)
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session


router = APIRouter(prefix="/profile", tags=["Profile"])


@router.post(
    "/create_post/", status_code=status.HTTP_201_CREATED, response_model=ResponseCreate
)
async def create_new_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user_from_cookies),
    session: AsyncSession = Depends(get_async_session),
):
    return await create_post(
        current_user=current_user,
        post_theme=post_data.article_theme,
        post_text=post_data.article_text,
        session=session,
    )


@router.patch(
    "/modify_post/", status_code=status.HTTP_200_OK, response_model=ResponseModify
)
async def modify_the_post(
    new_data: ModifyData,
    current_user: User = Depends(get_current_user_from_cookies),
    session: AsyncSession = Depends(get_async_session),
):
    return await modify_post(
        current_user=current_user,
        post_id=new_data.post_id,
        new_post_text=new_data.new_text,
        session=session,
    )


@router.delete(
    "/delete_post/", status_code=status.HTTP_200_OK, response_model=ResponseDelete
)
async def delete_current_post(
    post_id: int,
    current_user: User = Depends(get_current_user_from_cookies),
    session: AsyncSession = Depends(get_async_session),
):
    return await delete_post(
        current_user=current_user, post_id=post_id, session=session
    )


@router.patch("/like_post", status_code=status.HTTP_200_OK, response_model=ResponseLike)
async def like_dislike(
    post_id: int,
    current_user: User = Depends(get_current_user_from_cookies),
    session: AsyncSession = Depends(get_async_session),
):
    return await like_or_dislike(
        post_id=post_id, user_id=current_user["id"], session=session
    )


@router.get("/get_all_posts")
async def get_all_post():
    return await get_posts()
