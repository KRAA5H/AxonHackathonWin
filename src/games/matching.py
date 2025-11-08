"""Simple Matching Pairs game.

This is a gentle, low-friction matching pairs demo suitable for touchscreen.
"""
import random
import tkinter as tk
from tkinter import ttk
from typing import Callable


class MatchingGame(ttk.Frame):
    """Very small matching game with a configurable grid size."""

    def __init__(self, master, on_exit: Callable = None, rows: int = 2, cols: int = 2):
        super().__init__(master)
        self.on_exit = on_exit
        self.rows = rows
        self.cols = cols
        self.pairs = (rows * cols) // 2
        self._build_ui()
        self.reset()

    def _build_ui(self):
        title = ttk.Label(self, text="Matching Pairs", font=("Helvetica", 14))
        title.pack(pady=6)

        self.grid_frame = ttk.Frame(self)
        self.grid_frame.pack(padx=6, pady=6)

        ctrl = ttk.Frame(self)
        ctrl.pack(fill="x", pady=8)

        restart = ttk.Button(ctrl, text="Restart", command=self.reset)
        restart.pack(side="right", padx=6)

        back = ttk.Button(ctrl, text="Back", command=self._on_back)
        back.pack(side="right")

        self.status = ttk.Label(self, text="Find all pairs")
        self.status.pack()

    def _on_back(self):
        if callable(self.on_exit):
            self.on_exit()

    def reset(self):
        values = list(range(1, self.pairs + 1)) * 2
        random.shuffle(values)
        self.values = values
        self.buttons = []
        self.revealed = [False] * (self.rows * self.cols)
        self.first_idx = None

        # Clear frame
        for child in self.grid_frame.winfo_children():
            child.destroy()

        idx = 0
        for r in range(self.rows):
            for c in range(self.cols):
                b = tk.Button(self.grid_frame, text=" ", width=8, height=4, command=lambda i=idx: self._on_click(i))
                b.grid(row=r, column=c, padx=4, pady=4)
                self.buttons.append(b)
                idx += 1

        self.status.config(text="Find all pairs")

    def _on_click(self, index: int):
        if self.revealed[index]:
            return
        # reveal
        self.buttons[index].config(text=str(self.values[index]))
        if self.first_idx is None:
            self.first_idx = index
            return

        # Second click
        second = index
        if self.values[second] == self.values[self.first_idx]:
            # match
            self.revealed[second] = True
            self.revealed[self.first_idx] = True
            self.first_idx = None
            if all(self.revealed):
                self.status.config(text="All pairs found — well done!")
        else:
            # temporary show then hide
            a, b = self.first_idx, second
            self.after(700, lambda: self._hide_pair(a, b))
            self.first_idx = None

    def _hide_pair(self, a: int, b: int):
        # only hide if not already matched
        if not self.revealed[a]:
            self.buttons[a].config(text=" ")
        if not self.revealed[b]:
            self.buttons[b].config(text=" ")
