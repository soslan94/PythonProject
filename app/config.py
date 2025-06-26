from decouple import config

class Settings:
    DB_USER: str = config('DB_USER')
    DB_PASSWORD: str = config('DB_PASSWORD')
    DB_HOST: str = config('DB_HOST', default='localhost')
    DB_PORT: str = config('DB_PORT', default='5432')
    DB_NAME: str = config('DB_NAME', default='store')

    @property
    def db_url(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()