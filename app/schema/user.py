from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    id: int
    username: str
    email: str
    activated: bool = True

    model_config = ConfigDict(
        from_attributes=True,
    )
