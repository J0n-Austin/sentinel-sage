""" Configuration loader/validator 

Loads settings from TOML config files
Priority: env variables > user config > config/default.toml

-- Notes --
Pydantic handles validation. For instance, if someone
enters max_per_run_usd = "banana", it would throw a clear
error instead of crashing farther down the pipeline

This code uses Pydantic "models", which are essentially
data classes that have automatic validation. Pydantic
automatically checks the type, range, and format for
assigned values. This functionality requires us to import
BaseModel
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from pydantic import BaseModel, Field

# resolve the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Pydantic models
# Each TOML section maps to a model 
""" Notes:
- gt=0 means greater than zero
- le=5.00 means less than or equal to 5 (forces budget caps, 
    so if you'd like to spend more, simply change this max)


"""
class AppSettings(BaseModel):
    name: str = "sent-and-sage"
    version: str = "0.1.0"
    debug: bool = False

class ModelSettings(BaseModel):
    primary: str = "claude-sonnet-4-5-20250929"
    fallback: str = "claude-haiku-4-5-20251001"

class BudgetSettings(BaseModel):
    max_per_run_usd: float = Field(default=1.00, gt=0, le=5.00)
    warn_at_percent: int = Field(default=75, ge=1, le=99)

class AgentSettings(BaseModel):
    enabled: bool = True
    system_prompt: str = ""
    allowed_tools: list[str] =[]
    max_turns: int = Field(default=30, ge=1, le=200)

class AgentSettings(BaseModel):
    analyst: AgentSettings = AgentSettings()
    pentester: AgentSettings = AgentSettings()

class TsharkSettings(BaseModel):
    binary: str = "tshark"
    default_interface: str = "eth0"
    capture_timeout: int = Field(default=30, ge=5, le=300)
    output_format: str = "json"

class PathSettings(BaseModel):
    pcap_dir: str = "data/pcaps"
    samples_dir: str = "data/samples"
    wordlists_dir: str = "data/wordlists"
    reports_dir: str = "reports"
    tmp_dir: str = "data/tmp"
    log_dir: str = "logs"

    def resolve(self, name: str) -> Path:
        # resolve to an absolute path from project root
        return PROJECT_ROOT / getattr(self, name)

class VirusTotalSettings(BaseModel):
    requests_per_minute: int = Field(default=4, ge=1, le=30)
    daily_limit: int = Field(default=500, ge=1)

class LoggingSettings(BaseModel):
    level: str = "INFO"
    format: str = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"

class Config(BaseModel):
    app: AppSettings = AppSettings()
    model: ModelSettings = ModelSettings()
    budget: BudgetSettings = BudgetSettings()
    agents: AgentSettings = AgentSettings()
    tshark: TsharkSettings = TsharkSettings()
    paths: PathSettings = PathSettings()
    virustotal: VirusTotalSettings = VirusTotalSettings()
    logging: LoggingSettings = LoggingSettings()

    @classmethod
    def load(cls, config_path: Path | None = None) -> Config:
        """ load config from TOML with env variable overrides

        Args:
            config_path: optional path to a user config file
            falls back to config/default.toml

        Returns:
            validated config instance

        Raises:
            FileNotFounderror if no config file found
            ValueError if config values fail validations
        """

        if config_path is None:
            config_path = PROJECT_ROOT / "config" / "default.toml"

        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        # open/parse TOML
        with open(config_path, "rb") as f:
            raw = tomllib.load(f)

        # apply env variable overrides
        raw = _apply_env_overrides(raw)

        return cls.model_validate(raw)
    
def _apply_env_overrides(raw: dict) -> dict:
    """ override config values with env vars where set.

    """

    log_level = os.environ.get("SENT_SAGE_LOG_LEVEL")
    if log_level is not None:
        raw.setdefault("logging", {})["level"] = log_level.upper()

    debug = os.environ.get("SENT_SAGE_DEBUG")
    if debug is not None:
        raw.setdefault("app", {})["debug"] = debug.lower() in ("1", "true", "yes")

    return raw