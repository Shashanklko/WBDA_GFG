
class Settings:
    PROJECT_NAME: str = "Water Quality Risk Assessment"
    # Using the credentials provided by the user
    DATABASE_URL: str = "mysql+pymysql://root:123456789@localhost:3306/wbda"
    SECRET_KEY: str = "supersecretkeyneedschange"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
