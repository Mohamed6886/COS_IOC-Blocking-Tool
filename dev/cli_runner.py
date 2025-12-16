"""
Helpful notes:
 - cd FMC-Core
 - (playwright inspector) $env:PWDEBUG=1
 - playwright codegen https://fmc5.ci.stockton.ca.us/ui/login
 - python -m dev.cli_runner --env FMC5 --max 50 --dry-run
 - python -m PyInstaller --onefile --windowed --name "FMC Tool" --add-data "src;src" --hidden-import playwright.sync_api --hidden-import dotenv gui_runner.py
"""
import argparse

from src.fmc_ioc_blocker import run_blocker, read_env_urls

def main():
    parser = argparse.ArgumentParser(description="FMC IOC blocker (developer CLI)")
    parser.add_argument("--env", choices=["FMC5", "FMC3"], default="FMC5")
    parser.add_argument("--max", type=int, required=True, help="Max IOCs to block this run")
    parser.add_argument("--dry-run", action="store_true", help="Simulate only; do not click Block")
    args = parser.parse_args()

    fmc5_url, fmc3_url = read_env_urls()
    base_url = fmc5_url if args.env == "FMC5" else fmc3_url

    if not base_url:
        print(f"[ERROR] {args.env}_BASE_URL not found in .env. Update the .env in the project root.")
        return

    print(f"Using {args.env} base URL: {base_url}")
    changed = run_blocker(
        base_url=base_url,
        max_count=args.max,
        dry_run=args.dry_run,
        gui_logger=None
    )
    print(f"\nCompleted. {'Would have blocked' if args.dry_run else 'Blocked'} {changed} IOCs.")


if __name__ == "__main__":
    main()
