import tkinter as tk
from tkinter import ttk

from ..games.memory import MemoryGame
from ..games.matching import MatchingGame


class MainWindow(tk.Frame):
    """Main application frame. Hosts navigation and game containers."""

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass
        self.create_widgets()

    def create_widgets(self):
        header = ttk.Label(self, text="Dementia Games", font=("Helvetica", 18))
        header.pack(pady=10)

        self.container = ttk.Frame(self, relief="flat")
        self.container.pack(fill="both", expand=True)

        self.home()

    def clear_container(self):
        for child in self.container.winfo_children():
            child.destroy()

    def home(self):
        """Show home screen with game choices."""
        self.clear_container()
        frm = ttk.Frame(self.container)
        frm.pack(fill="both", expand=True, padx=10, pady=10)

        btn1 = ttk.Button(frm, text="Memory Sequence", command=self.show_memory)
        btn1.pack(fill="x", padx=20, pady=10)

        btn2 = ttk.Button(frm, text="Matching Pairs", command=self.show_matching)
        btn2.pack(fill="x", padx=20, pady=10)

        # Helpful large-exit button for caregivers
        btn_quit = ttk.Button(self.container, text="Quit", command=self.master.quit)
        btn_quit.pack(side="bottom", pady=20)

    def show_memory(self):
        self.clear_container()
        frame = MemoryGame(self.container, on_exit=self.home)
        frame.pack(fill="both", expand=True)

    def show_matching(self):
        self.clear_container()
        frame = MatchingGame(self.container, on_exit=self.home)
        frame.pack(fill="both", expand=True)
