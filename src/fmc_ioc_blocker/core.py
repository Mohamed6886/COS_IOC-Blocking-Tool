import time
from playwright.sync_api import sync_playwright, ViewportSize
from .utils import (
    _log,
    screenshot,
    count_visible_monitors,
    reload_grid,
)
from .config import make_artifacts_dir
from .navigation import (
    manual_login_and_wait,
    goto_ioc_page,
    apply_monitor_filter, change_batch,
)
"""
    Main public entry point.

    - base_url: FMC base URL (e.g. 'https://fmc5.example.gov')
    - max_count: maximum number of IOCs to block in this run
    - dry_run: if True, only simulates the flips (for CLI debugging)
    - gui_logger: optional logging callback used by the GUI
    - throttle: pacing between UI actions
    - refresh_every: periodic reload after this many changes

    Returns:
        total_changed (int)
    """
# -------------------- Public API --------------------
def run_blocker(base_url: str,
                max_count: int,
                dry_run: bool = False,
                gui_logger=None) -> int:

    out_dir = make_artifacts_dir()
    _log(f"Artifacts → {out_dir}", gui_logger)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            ignore_https_errors=True,
            viewport= ViewportSize(width = 1400, height = 900)
        )
        page = context.new_page()

        try:
            _log("Open login page; please sign in manually…", gui_logger)
            manual_login_and_wait(page, base_url)

            _log("Navigating to Indicators and applying Action=Monitor filter…", gui_logger)
            goto_ioc_page(page, out_dir)
            apply_monitor_filter(page, out_dir)

            initial_monitors = count_visible_monitors(page)
            _log(f"Initial visible 'Monitor' rows: {initial_monitors}", gui_logger)

            if initial_monitors == 0:
                screenshot(page, out_dir, "final")
                _log("No Monitor IOCs found. Nothing to do.", gui_logger)
                return 0

            total_changed = 0
            while total_changed < max_count:

                visible = count_visible_monitors(page)
                if visible == 0:
                    reload_grid(page)
                    visible = count_visible_monitors(page)

                    if visible == 0:
                        _log("No more Monitor IOCs detected.", gui_logger)
                        break

                batch_target = min(visible, max_count - total_changed)

                changed, had_err = change_batch(
                    page, out_dir, batch_target, dry_run=dry_run
                )

                total_changed += changed

                _log(f"Changed this batch: {changed} | Total: {total_changed} | Error? {had_err}", gui_logger)

                if total_changed >= max_count:
                    break

                # If something failed → reload early
                if changed < batch_target or had_err:
                    reload_grid(page)
                    continue

                # Finished a clean batch → reload for next page of rows
                reload_grid(page)

            # Final screenshot
            screenshot(page, out_dir, "final")

            _log(
                f"Done. Total IOCs {'(dry-run) ' if dry_run else ''}blocked: "
                f"{total_changed} (target {max_count})",
                gui_logger,
            )
            return total_changed

        finally:
            context.close()
            browser.close()