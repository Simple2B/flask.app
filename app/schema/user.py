from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    id: int
    username: str
    email: str
    activated: bool

    model_config: ConfigDict = {
        "from_attributes": True,
    }
