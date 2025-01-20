"""A simple application to practice squares and square roots."""

from __future__ import annotations

import contextlib
import random
import tkinter as tk
from pathlib import Path


class SquaresTester:
    """A simple application to practice squares and square roots."""

    def __init__(self, root: tk.Tk) -> None:
        """Initialize the application.

        Args:
            root (tk.Tk): The root window of the application.

        """
        self.questions = []
        self.current_question_index = 0
        self.game_started = False

        self.RANGE_MAX_VALUE = 10000

        self.submit_button_text_var = tk.StringVar(value="Start")

        self.question_label_var = tk.StringVar(
            value="Press the button, [Enter]\n or [Space] to start!",
        )

        self.high_score_title = "Best"

        try:
            self.high_score = self.read_high_score()
        except FileNotFoundError:
            self.high_score = 0
            self.high_score_title = "Session best"

        self.high_score_label_var = tk.StringVar(
            value=f"{self.high_score_title}: {self.high_score}",
        )

        self.current_score = 0
        self.score_label_var = tk.StringVar(value="")

        self.START_TIME = 30
        self.time_left = 0
        self.timer_label_var = tk.StringVar(value="")

        self.root = root
        self.root.title("Squares Practice")

        self.initialize_widgets()
        self.center_window()

    def initialize_widgets(self) -> None:
        """Initialize the widgets for the application."""
        self.high_score_label = tk.Label(
            root,
            textvariable=self.high_score_label_var,
            width=12,
            anchor="w",
        )
        self.high_score_label.grid(row=0, column=0, padx=(10, 20), pady=10, sticky="nw")

        self.end_button = tk.Button(root, text="End game", command=self.end_game)
        self.end_button.grid(row=5, column=0, padx=(10, 0), pady=10, sticky="w")
        self.end_button.config(state=tk.DISABLED)

        self.score_label = tk.Label(
            root,
            textvariable=self.score_label_var,
            width=15,
        )
        self.score_label.grid(row=0, column=1, padx=(10, 10), pady=10, sticky="ew")

        self.timer_label = tk.Label(root, textvariable=self.timer_label_var, width=10)
        self.timer_label.grid(row=0, column=2, padx=(0, 0), pady=10, sticky="ne")

        self.question_label = tk.Label(
            root,
            textvariable=self.question_label_var,
            height=2,
            width=20,
            anchor="w",
        )

        self.question_label.grid(
            row=1,
            column=1,
            columnspan=2,
            padx=0,
            pady=10,
            sticky="w",
        )

        self.answer_entry = tk.Entry(root, width=20)
        self.answer_entry.grid(row=2, column=1, padx=0, pady=(2, 0))
        self.answer_entry.bind("<Return>", self.submit_button_pressed)
        self.answer_entry.bind("<space>", self.submit_button_pressed)
        self.answer_entry.focus_set()

        self.submit_button = tk.Button(
            root,
            textvariable=self.submit_button_text_var,
            command=self.submit_button_pressed,
        )
        self.submit_button.grid(row=2, column=2, padx=(10, 0), pady=10, sticky="w")

        self.question_type_var = tk.StringVar(value="squares")
        self.squares_radio = tk.Radiobutton(
            root,
            text="Squares",
            variable=self.question_type_var,
            value="squares",
        )
        self.squares_radio.grid(
            row=0,
            column=3,
            padx=(10, 0),
            pady=(10, 0),
            sticky="nw",
        )

        self.roots_radio = tk.Radiobutton(
            root,
            text="Roots",
            variable=self.question_type_var,
            value="roots",
        )
        self.roots_radio.grid(row=1, column=3, padx=(10, 0), pady=(0, 0), sticky="nw")

        self.practice_mode_checkbox_var = tk.BooleanVar()
        self.practice_mode_checkbox = tk.Checkbutton(
            root,
            text="Practice mode",
            variable=self.practice_mode_checkbox_var,
            command=self.update_labels_visibility,
        )
        self.practice_mode_checkbox.grid(
            row=2,
            column=3,
            padx=(10, 10),
            pady=(0, 5),
            sticky="nw",
        )

        self.range_label = tk.Label(root, text="Number range:")
        self.range_label.grid(row=3, column=3, padx=(12, 10), pady=(5, 5), sticky="nw")

        self.min_label = tk.Label(root, text="Min")
        self.min_label.grid(row=4, column=3, padx=(12, 10), pady=(5, 5), sticky="nw")

        self.range_min_value = tk.IntVar(value=11)
        self.range_min_entry = tk.Entry(
            root,
            textvariable=self.range_min_value,
            width=10,
        )
        self.range_min_entry.grid(
            row=4,
            column=3,
            padx=(0, 20),
            pady=(5, 5),
            sticky="ne",
        )

        self.range_max_label = tk.Label(root, text="Max")
        self.range_max_label.grid(
            row=5,
            column=3,
            padx=(12, 10),
            pady=(5, 15),
            sticky="nw",
        )

        self.range_max_value = tk.IntVar(value=99)
        self.range_max_entry = tk.Entry(
            root,
            textvariable=self.range_max_value,
            width=10,
        )
        self.range_max_entry.grid(
            row=5,
            column=3,
            padx=(0, 20),
            pady=(5, 15),
            sticky="ne",
        )

    def center_window(self) -> None:
        """Centers the application window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def read_high_score(self) -> str:
        """Read the high score from the high_score.txt file.

        Returns:
            str: The high score read from the file.

        """
        with Path.open("files/high_score.txt") as f:
            return int(f.read())

    def update_high_score(self) -> None:
        """Update the high score label and in the file."""
        try:
            with Path.open("files/high_score.txt") as _:
                pass
            with Path.open("files/high_score.txt", "w") as f:
                f.write(str(self.current_score))
        except FileNotFoundError:
            pass

        self.high_score = self.current_score
        self.high_score_label_var.set(f"{self.high_score_title}: {self.high_score}")

    def update_labels_visibility(self) -> None:
        """Update label visibility based on game mode checkbox state.

        If practice mode is enabled, hide the high score label and timer label.
        """
        if self.practice_mode_checkbox_var.get():
            self.high_score_label_var.set("")
            self.timer_label_var.set("")
        else:
            self.high_score_label_var.set(f"{self.high_score_title}: {self.high_score}")

    def update_timer(self) -> None:
        """Update the timer label every second."""
        self.timer_label_var.set(f"Time left: {self.time_left}")
        if self.time_left > 0:
            self.root.after(1000, self.update_timer)
            self.time_left -= 1

        elif self.game_started:
            self.end_game()

    def shake_answer_entry(self) -> None:
        """Shake the answer entry widget to indicate a wrong answer."""
        x, y = self.answer_entry.winfo_x(), self.answer_entry.winfo_y()
        for _ in range(4):
            for dx in (-5, 5):
                self.answer_entry.place(x=x + dx, y=y)
                self.answer_entry.update()
                self.root.after(
                    20,
                )
        self.answer_entry.place(x=x, y=y)

    def submit_button_pressed(self, _: tk.Event | None = None) -> str:
        """Handle the button press event."""
        if self.game_started:
            self.submit_answer()
        else:
            self.start_game()

        return "break"

    def start_game(self, _: tk.Event | None = None) -> None:
        """Start the game."""
        try:
            self.generate_questions()
        except NumberRangeError as e:
            self.display_error(e)
            return

        self.answer_entry.delete(0, tk.END)

        self.practice_mode_checkbox.config(state=tk.DISABLED)
        self.end_button.config(state=tk.NORMAL)

        self.answer_entry.focus_set()

        self.game_started = True
        self.submit_button_text_var.set("Submit")
        self.question_label_var.set(
            self.questions[self.current_question_index]["question"],
        )

        self.current_score = 0
        self.score_label_var.set(f"Score: {self.current_score}")

        if not self.practice_mode_checkbox_var.get():
            self.time_left = self.START_TIME
            self.update_timer()

    def generate_questions(self) -> None:
        """Generate the questions based on the selected question type."""
        try:
            selected_min_value = self.range_min_value.get()
            selected_max_value = self.range_max_value.get()

        except tk.TclError:
            msg = "Invalid number range!"
            raise NumberRangeError(msg) from None

        if selected_min_value < 1:
            msg = "Min range value cannot\nbe below 1!"
            raise NumberRangeError(msg)

        if selected_max_value > self.RANGE_MAX_VALUE:
            msg = "Max range value cannot\nbe above 10 000 !"
            raise NumberRangeError(msg)

        numbers_list = list(
            range(selected_min_value, selected_max_value + 1),
        )

        if len(numbers_list) < 1:
            msg = "Invalid number range!"
            raise NumberRangeError(msg)

        if self.question_type_var.get() == "squares":
            for number in numbers_list:
                question = f"What is {number}^2?"
                answer = number**2
                self.questions.append({"question": question, "answer": str(answer)})

        if self.question_type_var.get() == "roots":
            for number in numbers_list:
                question = f"What is the square root of\n{number**2}?"
                answer = number
                self.questions.append({"question": question, "answer": str(answer)})

        random.shuffle(self.questions)

    def submit_answer(self, _: tk.Event | None = None) -> None:
        """Process the answer to the current question."""
        answer = self.answer_entry.get().strip()
        correct_answer = self.questions[self.current_question_index]["answer"]

        self.answer_entry.delete(0, tk.END)

        if answer == correct_answer:
            self.current_score += 1
            self.score_label_var.set(f"Score: {self.current_score}")
        else:
            self.shake_answer_entry()

        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.question_label_var.set(
                self.questions[self.current_question_index]["question"],
            )
        else:
            self.end_game()

    def end_game(self) -> None:
        """End the game."""
        self.answer_entry.delete(0, tk.END)

        if (
            self.current_score > self.high_score
            and not self.practice_mode_checkbox_var.get()
        ):
            self.update_high_score()
            self.question_label_var.set("Game Over!\nNew High Score!")
        else:
            self.question_label_var.set("Game Over!")

        self.practice_mode_checkbox.config(state=tk.NORMAL)
        self.end_button.config(state=tk.DISABLED)

        self.game_started = False

        if not self.practice_mode_checkbox_var.get():
            self.time_left = 0
            self.timer_label_var.set(f"Time left: {self.time_left}")

        self.current_question_index = 0
        self.questions.clear()

        self.submit_button_text_var.set("Restart")

    def display_error(self, message: str) -> None:
        """Display an error message on the question label."""
        current_text = self.question_label.cget("text")
        self.question_label_var.set(message)
        self.root.after(2000, self.reset_question_label, current_text)

    def reset_question_label(self, text: str) -> None:
        """Reset the question label to the previous text."""
        self.question_label_var.set(text)


class NumberRangeError(Exception):
    """Raised when the number range is invalid."""

    def __init__(self, message: str) -> None:
        """Initialize the exception."""
        super().__init__(message)


if __name__ == "__main__":
    root = tk.Tk()
    with contextlib.suppress(tk.TclError):
        root.iconbitmap("files/root_square.ico")
    SquaresTester(root)
    root.resizable(width=False, height=False)
    root.mainloop()
