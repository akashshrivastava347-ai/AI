"""Runtime configuration.

Every secret is read from the environment. Nothing sensitive is ever hard-coded,
committed, or logged — see docs/03-INDUSTRY-READINESS.md section 3.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="LOGSENSE_",
        extra="ignore",
    )

    # --- storage -------------------------------------------------------------------
    database_url: str = Field(
        default="sqlite+pysqlite:///./logsense.db",
        description="SQLAlchemy URL. SQLite for local dev; PostgreSQL in any shared env.",
    )
    sql_echo: bool = False

    # --- LLM provider --------------------------------------------------------------
    # The API key is NEVER stored in code or committed. Export it, or put it in a
    # .env file that is git-ignored:  LOGSENSE_LLM_API_KEY=sk-...
    llm_provider: str = Field(default="openai", description="openai | fake")
    llm_api_key: str | None = Field(default=None, repr=False)
    llm_base_url: str | None = None

    # Cheap, fast model for bulk row and message extraction. Quality model is used
    # later for planning and answer composition (Story 3+).
    llm_model_extract: str = "gpt-4o-mini"
    llm_model_reason: str = "gpt-4o"

    llm_timeout_seconds: float = 30.0
    llm_max_retries: int = 2

    # Cost tracking, USD per 1M tokens. Update when provider pricing changes; recorded
    # costs are never recomputed retroactively (docs/03 section 6).
    llm_cost_input_per_mtok_usd: float = 0.15
    llm_cost_output_per_mtok_usd: float = 0.60
    usd_to_inr: float = 88.0

    # --- extraction / routing ------------------------------------------------------
    default_auto_approve_threshold: float = Field(
        default=0.80,
        ge=0.0,
        le=1.0,
        description="Overall confidence at or above which a record skips human review. "
        "Overridable per plant.",
    )
    fuzzy_match_floor: float = Field(
        default=0.60,
        ge=0.0,
        le=1.0,
        description="Below this, the resolver reports no candidate rather than guessing.",
    )

    # --- app -----------------------------------------------------------------------
    app_env: str = "dev"
    log_level: str = "INFO"

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() in {"prod", "production"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
