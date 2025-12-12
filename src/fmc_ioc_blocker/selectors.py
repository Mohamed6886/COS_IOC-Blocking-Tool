import re

SELECTORS = {
    # --- Nav / tabs ---
    "nav_integration": {"role": "link", "name": "Integration"},
    "nav_sources": {"role": "link", "name": "Sources"},
    "nav_indicators": {"role": "link", "name": "Indicators"},

    # --- Filter bar & actions ---
    "filter_bar": "#filterBar",
    "filter_clear_initial": '[data-test="removeSearch"]',
    "filter_add_container": '[data-test="addFilter"]',
    "filter_bubble": '[data-test="filterBubble"]',

    # --- Grid ---
    "grid": 'table[role="grid"], [role="grid"]',
    "grid_rows": '[role="rowgroup"] [role="row"]',
    "grid_cells": '[role="cell"]',

    # --- Action cell interaction ---
    # Some rows show "Monitor ▾", others just "Monitor"
    "action_cell_monitor_variants": ["Monitor ▾", "Monitor"],
    "action_menu_container": "#action-options",
    "action_menu_option_block_text": "Block",

    # --- Interstitials ---
    "banner_accept": '[data-test-id="bannerAccept"]',
    "carousel_iframe": 'iframe[title^="Carousel slide"]',
    "carousel_close_btn_role": {
        "role": "button",
        "name": "Click on Close Icon to close"
    },

}

ERROR_PAT = re.compile(r"failed to (fetch|update)", re.I)
