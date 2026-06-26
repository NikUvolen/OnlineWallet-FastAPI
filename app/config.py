from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    POSTGRES_PORT: int = 5432

    @property
    def database_url(self) -> str:
        return (
            'postgresql+asyncpg://'
            f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
            f'@localhost:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
        )
    
    model_config = SettingsConfigDict(
        env_file='app/.env', 
        env_file_encoding='utf-8',
        extra='ignore'
    )


settings = Settings()
