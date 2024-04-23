from src.schemas import MyBaseModel


class Token(MyBaseModel):
    access_token: str
    token_type: str


class TokenData(MyBaseModel):
    username: str
