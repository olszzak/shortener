from pydantic import computed_field, Field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBConfig(BaseModel):
    user: str = "user"
    password: str = "pass"
    host: str = "localhost"
    port: int = 5432
    name: str = "url_db"

    @computed_field
    @property
    def connection_string(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    app_name: str = "URLShortener"
    debug: bool = False
    port: int = 8080
    api_prefix: str = ""

    short_id_length: int = 6

    db_config: DBConfig = Field(default_factory=DBConfig)


def get_settings() -> Settings:
    return Settings()
