from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from src.service.service import get_posts, get_current_user_from_cookies

router = APIRouter(prefix="/pages", tags=["Frontend"])
templates = Jinja2Templates(directory="src/templates")


@router.get("/registration")
async def get_registration_html(request: Request):
    return templates.TemplateResponse(
        name="registration_page.html", context={"request": request}
    )


@router.get("/authenticate")
async def get_authenticate_html(request: Request):
    return templates.TemplateResponse(
        name="authentication_page.html", context={"request": request}
    )


@router.get("/home_page")
async def get_home_page_html(
    request: Request,
    posts_info=Depends(get_posts),
    user_info=Depends(get_current_user_from_cookies),
):
    return templates.TemplateResponse(
        name="home_page.html",
        context={"request": request, "posts_info": posts_info, "user_info": user_info},
    )


@router.get("/create_post_window")
async def get_home_page_html(
    request: Request,
    posts_info=Depends(get_posts),
    user_info=Depends(get_current_user_from_cookies),
):
    return templates.TemplateResponse(
        name="create_post_window.html",
        context={"request": request, "posts_info": posts_info, "user_info": user_info},
    )
