from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "InfluencersPlace AI Lead Agent"
    debug: bool = False
    database_url: str = "sqlite:///./lead_agent.db"
    jwt_secret: str = "change-me-in-prod"
    jwt_algorithm: str = "HS256"
    access_token_expiry_minutes: int = 60 * 24
    llm_api_key: str | None = None
    llm_provider: str = "heuristic"
    serpapi_key: str | None = None
    redis_url: str | None = None
    agent_schedule_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
