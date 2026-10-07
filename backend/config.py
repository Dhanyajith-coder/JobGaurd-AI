import os

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Application settings loaded from environment variables."""

    app_name: str = Field(default_factory=lambda: os.getenv("APP_NAME", "JobGuard AI"))
    frontend_origin: str = Field(
        default_factory=lambda: os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
    )

    @property
    def frontend_origins(self) -> list[str]:
        """Return a list of allowed frontend origins for CORS."""
        origins = [
            origin.strip()
            for origin in self.frontend_origin.split(",")
            if origin.strip()
        ]
        return origins or ["http://localhost:3000"]


settings = Settings()