import threading
import tkinter as tk
from tkinter import ttk, messagebox

from src.fmc_ioc_blocker import run_blocker, read_env_urls


class GuiApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("FMC IOC Blocking Tool")
        self.fmc5_url, self.fmc3_url = read_env_urls()

        # ------------- Layout -------------

        main = ttk.Frame(root, padding=12)
        main.grid(row=0, column=0, sticky="nsew")

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        # Title
        ttk.Label(main, text="FMC IOC Blocking Tool", font=("Segoe UI", 12, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 8)
        )

        # Environment
        ttk.Label(main, text="Environment:").grid(row=1, column=0, sticky="e", padx=(0, 8))
        self.env_var = tk.StringVar(value="FMC5")
        env_combo = ttk.Combobox(
            main,
            textvariable=self.env_var,
            values=["FMC5", "FMC3"],
            state="readonly",
            width=10,
        )
        env_combo.grid(row=1, column=1, sticky="w")

        # IOC count
        ttk.Label(main, text="Number of IOCs to block:").grid(
            row=2, column=0, sticky="e", padx=(0, 8), pady=(6, 0)
        )
        self.max_var = tk.StringVar(value="0")
        max_entry = ttk.Entry(main, textvariable=self.max_var, width=10)
        max_entry.grid(row=2, column=1, sticky="w", pady=(6, 0))

        # Log output
        ttk.Label(main, text="Log:").grid(row=3, column=0, sticky="ne", padx=(0, 8), pady=(8, 0))
        self.log_widget = tk.Text(main, width=70, height=15, state="disabled", wrap="word")
        self.log_widget.grid(row=3, column=1, sticky="nsew", pady=(8, 0))

        # Scrollbar
        scroll = ttk.Scrollbar(main, command=self.log_widget.yview)
        self.log_widget["yscrollcommand"] = scroll.set
        scroll.grid(row=3, column=2, sticky="ns", pady=(8, 0))

        # Buttons
        btn_frame = ttk.Frame(main)
        btn_frame.grid(row=4, column=0, columnspan=3, pady=(10, 0), sticky="e")

        self.start_btn = ttk.Button(btn_frame, text="Start", command=self.on_start)
        self.start_btn.grid(row=0, column=0, padx=(0, 8))

        ttk.Button(btn_frame, text="Exit", command=root.destroy).grid(row=0, column=1)

        # Grid weights
        main.rowconfigure(3, weight=1)
        main.columnconfigure(1, weight=1)

    # ------------- Logging -------------

    def log(self, msg: str):
        self.log_widget.configure(state="normal")
        self.log_widget.insert("end", msg + "\n")
        self.log_widget.see("end")
        self.log_widget.configure(state="disabled")
        self.root.update_idletasks()

    # ------------- Events -------------

    def on_start(self):
        # Validate IOC count
        try:
            max_count = int(self.max_var.get().strip())
            if max_count <= 0:
                raise ValueError
        except Exception:
            messagebox.showerror("Invalid input", "Please enter a positive integer for number of IOCs.")
            return

        env = self.env_var.get()
        base_url = self.fmc5_url if env == "FMC5" else self.fmc3_url

        if not base_url:
            messagebox.showerror(
                "Missing URL",
                f"{env}_BASE_URL not found in .env.\nPlease update the .env file next to the EXE."
            )
            return

        # Disable Start while running
        self.start_btn.configure(state="disabled")
        self.log_widget.configure(state="normal")
        self.log_widget.delete("1.0", "end")
        self.log_widget.configure(state="disabled")

        self.log(f"Starting run for {env} – base URL: {base_url}")
        self.log(f"Target IOCs: {max_count}")
        self.log("A browser window will open. Please sign in to FMC manually, then the tool will continue.\n")

        t = threading.Thread(
            target=self.worker,
            args=(base_url, max_count),
            daemon=True,
        )
        t.start()

    def worker(self, base_url: str, max_count: int):
        try:
            run_blocker(
                base_url=base_url,
                max_count=max_count,
                dry_run=False,
                gui_logger=self.log,
            )
        except Exception as e:
            self.log(f"[ERROR] {e}")
        finally:
            self.start_btn.configure(state="normal")
            self.log("Run finished.")


if __name__ == "__main__":
    root = tk.Tk()
    app = GuiApp(root)
    root.mainloop()
