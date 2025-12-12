from pathlib import Path
from playwright.sync_api import Page
from .selectors import SELECTORS, ERROR_PAT
from .utils import wait_visible, screenshot, count_visible_monitors, error_banner_present, reload_grid


# ============================================================
# SMALL INTERNAL HELPERS
# ============================================================

def _dismiss_cookie_banner(page: Page) -> None:
    """Close cookie/consent banner if present."""
    try:
        wait_visible(page, SELECTORS["banner_accept"])
        page.locator(SELECTORS["banner_accept"]).click()
    except Exception:
        pass


def _dismiss_carousel(page: Page) -> None:
    """Optionally close the carousel if it happens to appear."""
    try:
        wait_visible(page, SELECTORS["carousel_iframe"], timeout=1000)
        page.get_by_role("button", name=SELECTORS["carousel_close_btn_role"]["name"]).click()
    except Exception:
        pass


# ============================================================
# PUBLIC NAVIGATION HELPERS
# ============================================================

def manual_login_and_wait(page: Page, base_url: str) -> None:
    """
    Navigate to the login page, let the user log in manually,
    and wait for the Integration link to appear.
    """
    page.goto(base_url, wait_until="domcontentloaded")
    _dismiss_cookie_banner(page)
    wait_visible(page, SELECTORS["nav_integration"])
    _dismiss_carousel(page)


def goto_ioc_page(page: Page, out_dir: Path) -> None:
    """
    Navigate FMC UI to Integration → Sources → Indicators.
    Screenshot the page when Indicators grid is ready.
    """
    page.get_by_role("link", name="Integration").click()
    page.get_by_test_id("menuNavigation").get_by_role("link", name="Sources").click()
    page.get_by_role("link", name="Indicators").click()

    # When Indicators loads, filter bar should be visible
    wait_visible(page, SELECTORS["filter_bar"])
    wait_visible(page, SELECTORS["grid"])
    screenshot(page, out_dir, "before_monitor_filter")


def apply_monitor_filter(page: Page, out_dir: Path) -> None:
    """
    Apply filter Action = Monitor.
    """
    # Clear filters
    page.locator(SELECTORS["filter_clear_initial"]).click()

    # Open Add Filter menu
    page.locator(SELECTORS["filter_add_container"]).click()

    # Choose "Action"
    page.locator(SELECTORS["filter_add_container"]).get_by_text("Action", exact=True).click()

    # Choose "Monitor"
    page.locator(SELECTORS["filter_bubble"]).get_by_text("Monitor", exact=True).click()

    # Apply
    page.get_by_role("button", name="Apply").click()

    wait_visible(page, SELECTORS["grid"])
    screenshot(page, out_dir, "after_monitor_filter")


def change_batch(page: Page,
                 out_dir: Path,
                 batch_target: int,
                 dry_run: bool = False) -> tuple[int, bool]:
    """
    Attempt to block up to batch_target Monitor rows.
    Returns (changed, had_error).
    """
    changed = 0
    had_error = False

    while changed < batch_target:
        visible = count_visible_monitors(page)

        if visible == 0:
            break  # no more monitors visible this batch

        # Scroll to topmost "Monitor" IOC
        monitor_cell = page.locator(SELECTORS["grid"]).get_by_text("Monitor", exact=True).first
        monitor_cell.scroll_into_view_if_needed()

        if dry_run:
            monitor_cell.highlight()
            changed += 1
            continue

        # Click monitor cell → opens menu → click Block
        monitor_cell.click()

        menu = page.locator(SELECTORS["action_menu_container"])
        block_btn = menu.get_by_text(SELECTORS["action_menu_option_block_text"], exact=True)
        block_btn.click()

        # Error?
        if error_banner_present(page):
            had_error = True
            screenshot(page, out_dir, "Failed_Update_Or_Fetch")
            break

        changed += 1

    return changed, had_error
