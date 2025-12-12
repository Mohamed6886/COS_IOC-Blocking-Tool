import time
from pathlib import Path
from typing import Callable, Optional, Union
from playwright.sync_api import Page
from .selectors import SELECTORS, ERROR_PAT

GuiLogger = Optional[Callable[[str], None]]
SelectorRef = Union[str, dict]


# ============================================================
#  GUI Utility Functions
# ============================================================

def _log(msg: str, gui_logger: GuiLogger = None) -> None:
    """
    Log either to the GUI callback (if provided) or stdout.
    """
    if gui_logger:
        gui_logger(msg)
    print(msg)


# ============================================================
#  Playwright Utility Functions
# ============================================================

def screenshot(page: Page, out_dir: Path, label: str) -> Path:
    """
    Best-effort screenshot with a timestamped filename.
    """
    p = out_dir / f"snap_{label}_{int(time.time())}.png"
    page.screenshot(path=str(p), full_page=False)
    return p


def wait_visible(page: Page, locator_or_role: SelectorRef, timeout: int | None = None):
    """
    Wait for either a CSS locator or a role-based locator to become visible.
    If timeout=None, Playwright will wait indefinitely.
    Returns the Locator instance.
    """
    if isinstance(locator_or_role, dict):
        loc = page.get_by_role(
            locator_or_role["role"],
            name=locator_or_role["name"]
        )
    else:
        loc = page.locator(locator_or_role)

    loc.first.wait_for(state="visible", timeout=timeout)
    return loc


# ============================================================
#  FMC Specialized Utility Functions
# ============================================================

def reload_grid(page: Page) -> bool:
    """
    Press the Reload button. Returns True on success.
    """
    reload_button = page.locator("#filterBar").get_by_role("button")
    reload_button.click()

    # Clear hover tooltips
    page.keyboard.press("Escape")
    return True


def error_banner_present(page: Page) -> bool:
    """
    Return True if 'failed to fetch/update' banner appears.
    """
    return page.get_by_text(ERROR_PAT).count() > 0


def count_visible_monitors(page: Page) -> int:
    """
    Count how many 'Monitor' action cells are visible in the grid.
    """
    loc = page.locator(SELECTORS["grid"]).get_by_text("Monitor", exact=True)
    return loc.count() if loc is not None else 0
