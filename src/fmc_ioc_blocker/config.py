import os
import sys
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv


def get_app_dir() -> Path:
    """
    Application root directory.

    - If running as a PyInstaller EXE: folder containing the executable.
    - If running from source: project root (one level above this file).
    """
    if getattr(sys, "frozen", False) and hasattr(sys, "executable"):
        return Path(sys.executable).parent
    # src/fmc_ioc_blocker/config.py -> go up two levels to project root
    return Path(__file__).resolve().parents[2]


def configure_playwright_browsers():
    """
    If a 'browsers' folder exists next to the EXE / project root,
    tell Playwright to use it via PLAYWRIGHT_BROWSERS_PATH.
    """
    if BROWSERS_DIR.exists():
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(BROWSERS_DIR)


def load_env():
    """
    Load .env from the app directory only.
    No fallback search. This keeps behavior simple and predictable.
    """
    if ENV_PATH.exists():
        load_dotenv(ENV_PATH, override=True)


def read_env_urls():
    """
    Returns (fmc5_url, fmc3_url) trimmed and without trailing slashes.
    These values come ONLY from .env in the app directory.
    """
    def val(key: str) -> str:
        v = os.getenv(key, "").strip()
        return v.rstrip("/")

    fmc5 = val("FMC5_BASE_URL")
    fmc3 = val("FMC3_BASE_URL")
    return fmc5, fmc3


def make_artifacts_dir() -> Path:
    """
    Create and return a timestamped run_artifacts directory in APP_DIR.
    Example: APP_DIR/run_artifacts/20251205_134530
    """
    d = APP_DIR / "run_artifacts" / datetime.now().strftime("%Y%m%d_%H%M%S")
    d.mkdir(parents=True, exist_ok=True)
    return d


# One-time initialization when module is imported
APP_DIR: Path = get_app_dir()
BROWSERS_DIR: Path = APP_DIR / "browsers"
ENV_PATH: Path = APP_DIR / ".env"
configure_playwright_browsers()
load_env()