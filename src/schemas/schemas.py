import re
from pydantic import BaseModel, EmailStr, field_validator, Field, ConfigDict
from datetime import datetime
from typing import Annotated
from typing_extensions import TypedDict
from annotated_types import MaxLen, MinLen


class PostData(TypedDict):
    author: str
    author_id: int
    post_theme: str
    post_text: str
    created_at: datetime


class UserRegister(BaseModel):
    model_config = ConfigDict(regex_engine="python-re")
    username: str
    email: EmailStr
    hash_password: Annotated[
        str,
        Field(
            ...,
            pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{4,}$",
        ),
    ]

    # @classmethod
    # def validate_password(cls, value: str) -> bool:
    #     if not re.fullmatch(r"[A-Za-z0-9@#$%^&+=]{8,}", value):
    #         raise ValueError(
    #             "Пароль должен содержать минмум:\n",
    #             "1 маленькую латинскую букву\n",
    #             "1 большую латинскую букву\n",
    #             "1 цифру\n",
    #             "1 специальный символ (@#$%^&+=)",
    #         )
    #     return True


class SimplEReg(BaseModel):
    name: str
    email: EmailStr
    password: str


class User(UserRegister):
    id: int


class UserAuthIn(BaseModel):
    username: str
    hash_password: str


class ModifyData(BaseModel):
    post_id: int
    new_text: str


class NewUserIdOut(BaseModel):
    id: int
    success: bool


class Token(BaseModel):
    access_token: str
    token_type: str
    success: bool


class TokenData(BaseModel):
    username: str | None = None


class PostCreate(BaseModel):
    article_theme: str
    article_text: str


class ResponseLogout(BaseModel):
    success: bool
    mes: str


class ResponseDelete(BaseModel):
    success: bool
    mes: str


class ResponseLike(BaseModel):
    success: bool
    mes: str


class ResponseModify(BaseModel):
    success: bool
    mes: str
    date_change: datetime


class ResponseCreate(BaseModel):
    post_data: PostData
    success: bool
