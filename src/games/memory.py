"""Simple Memory Sequence game.

This file exposes a small, testable generator `generate_sequence` and a
`MemoryGame` GUI Frame that displays a short color sequence which the user
then tries to reproduce by tapping color buttons.
"""
import random
import tkinter as tk
from tkinter import ttk
from typing import List, Sequence, Callable


def generate_sequence(length: int, choices: Sequence[str] = ("red", "green", "blue", "yellow")) -> List[str]:
    """Return a random sequence of colors from choices with given length.

    Pure function useful for unit testing.
    """
    if length < 0:
        raise ValueError("length must be non-negative")
    return [random.choice(list(choices)) for _ in range(length)]


class MemoryGame(ttk.Frame):
    """A small memory game implemented as a Frame.

    Behavior:
    - Start a sequence (default length grows slowly)
    - Show sequence by highlighting the color label briefly
    - Let user reproduce by pressing color buttons
    - On success show a message and increase difficulty
    - on_exit callback returns to home
    """

    def __init__(self, master, on_exit: Callable = None):
        super().__init__(master)
        self.on_exit = on_exit
        self.sequence_length = 3
        self.choices = ["red", "green", "blue", "yellow"]
        self.sequence = []
        self.user_index = 0

        self._build_ui()

    def _build_ui(self):
        lbl = ttk.Label(self, text="Memory Sequence", font=("Helvetica", 14))
        lbl.pack(pady=6)

        self.display = tk.Label(self, text=" ", width=20, height=6, relief="ridge", bg="lightgray")
        self.display.pack(pady=6)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=6)

        for color in self.choices:
            b = tk.Button(btn_frame, text=color.capitalize(), bg=color, fg="white", width=8, command=lambda c=color: self._on_color(c))
            b.pack(side="left", padx=4, pady=4)

        ctrl = ttk.Frame(self)
        ctrl.pack(fill="x", pady=8)

        self.status = ttk.Label(ctrl, text="Press Start to begin")
        self.status.pack(side="left", padx=8)

        start = ttk.Button(ctrl, text="Start", command=self.start_round)
        start.pack(side="right", padx=8)

        back = ttk.Button(ctrl, text="Back", command=self._on_back)
        back.pack(side="right")

    def _on_back(self):
        if callable(self.on_exit):
            self.on_exit()

    def start_round(self):
        self.sequence = generate_sequence(self.sequence_length, self.choices)
        self.user_index = 0
        self.status.config(text=f"Watch the sequence ({self.sequence_length})")
        self.after(500, lambda: self._show_sequence(0))

    def _show_sequence(self, i: int):
        if i >= len(self.sequence):
            self.status.config(text="Now reproduce the sequence")
            self.display.config(bg="lightgray", text="Your turn")
            return

        color = self.sequence[i]
        # highlight
        self.display.config(bg=color, text=color.capitalize())
        # show briefly then clear and show next
        self.after(700, lambda: self._clear_then_next(i))

    def _clear_then_next(self, i: int):
        self.display.config(bg="lightgray", text=" ")
        self.after(300, lambda: self._show_sequence(i + 1))

    def _on_color(self, color: str):
        # Only accept input when sequence exists
        if not self.sequence:
            self.status.config(text="Press Start first")
            return

        expected = self.sequence[self.user_index]
        if color == expected:
            self.user_index += 1
            self.status.config(text=f"Good: {self.user_index}/{len(self.sequence)}")
            if self.user_index >= len(self.sequence):
                self.status.config(text="Well done! Next round will be harder.")
                self.sequence = []
                self.sequence_length = min(self.sequence_length + 1, 8)
        else:
            self.status.config(text=f"Incorrect (expected {expected}). Try again.")
            # give a small hint by resetting current round
            self.sequence = []
