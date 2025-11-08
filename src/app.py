"""Entry point for the phone-sized dementia-friendly games demo.

Run via: python run.py

This builds a fixed-size window that mimics a phone and hosts small games.
"""
from tkinter import Tk
from ui.main_window import MainWindow


def main():
    root = Tk()
    root.title("Dementia Care — Phone Demo")
    # Typical phone-ish demo size; will look like a portrait phone on desktop
    root.geometry("360x720")
    root.resizable(False, False)

    app = MainWindow(root)
    app.pack(fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()
