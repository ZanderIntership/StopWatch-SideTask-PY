import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stopwatch / Timer")
        self.resizable(False, False)

        # State
        self.mode = tk.StringVar(value="Stopwatch")
        self.running = False
        self.seconds = 0
        self.after_id = None  

  
        main = ttk.Frame(self, padding=12)
        main.grid()

        ttk.Label(main, text="Mode:").grid(row=0, column=0, sticky="w")
        ttk.OptionMenu(main, self.mode, self.mode.get(), "Stopwatch", "Timer").grid(
            row=0, column=1, sticky="ew", padx=(8, 0)
        )

        ttk.Label(main, text="Timer seconds:").grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.seconds_entry = ttk.Entry(main, width=12)
        self.seconds_entry.insert(0, "10")
        self.seconds_entry.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(8, 0))

        self.display = ttk.Label(main, text="0", font=("Segoe UI", 24))
        self.display.grid(row=2, column=0, columnspan=2, pady=(12, 12))

        btns = ttk.Frame(main)
        btns.grid(row=3, column=0, columnspan=2, sticky="ew")

        ttk.Button(btns, text="Start", command=self.start).grid(row=0, column=0, padx=4)
        ttk.Button(btns, text="Stop", command=self.stop).grid(row=0, column=1, padx=4)
        ttk.Button(btns, text="Reset", command=self.reset).grid(row=0, column=2, padx=4)

        main.columnconfigure(1, weight=1)

        self.update_display()

    def update_display(self):
        self.display.config(text=str(self.seconds))

    def tick(self):
        if not self.running:
            return

        if self.mode.get() == "Stopwatch":
            self.seconds += 1
            self.update_display()
            self.after_id = self.after(1000, self.tick)

        else:
            if self.seconds > 0:
                self.seconds -= 1
                self.update_display()
                self.after_id = self.after(1000, self.tick)
            else:
                self.running = False
                self.after_id = None
                self.display.config(text="Time's up!")

    def start(self):
        if self.running:
            return


        if self.mode.get() == "Timer" and self.seconds == 0:
            try:
                self.seconds = int(self.seconds_entry.get().strip())
                if self.seconds < 0:
                    self.seconds = 0
            except ValueError:
                self.seconds = 0

        self.running = True
        self.tick()

    def stop(self):
        self.running = False
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None

    def reset(self):
        self.stop()
        self.seconds = 0
        self.update_display()

if __name__ == "__main__":
    App().mainloop()
