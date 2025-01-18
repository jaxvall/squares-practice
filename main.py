"""A simple application to practice squares and square roots using a Tkinter GUI."""

from __future__ import annotations

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

        self.current_score = 0
        self.current_score_label = tk.StringVar(value=f"Score: {self.current_score}")

        self.time_left = 31
        self.timer_label = tk.StringVar(value="")

        self.high_score = self.read_high_score()

        self.root = root
        self.root.title("Squares Practice")

        self.initialize_widgets()
        self.center_window()

    def initialize_widgets(self) -> None:
        """Initialize the widgets for the application."""
        self.high_score_label = tk.Label(
            root,
            text=f"Best: {self.high_score}",
            width=6,
        )
        self.high_score_label.grid(row=0, column=0, padx=(10, 30), pady=10, sticky="nw")

        self.score_label = tk.Label(
            root,
            text=self.current_score_label,
            textvariable=self.current_score_label,
        )
        self.score_label.grid(row=0, column=1, padx=(10, 10), pady=10, sticky="ew")
        self.score_label.grid_remove()

        self.timer_display = tk.Label(root, textvariable=self.timer_label, width=10)
        self.timer_display.grid(row=0, column=2, padx=(0, 0), pady=10, sticky="ne")

        self.question_label = tk.Label(
            root,
            text="Press the button to start!",
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
        self.answer_entry.bind("<Return>", self.button_pressed)
        self.answer_entry.bind("<space>", self.button_pressed)
        self.answer_entry.focus_set()

        self.submit_button = tk.Button(root, text="Start", command=self.button_pressed)
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
            pady=(15, 0),
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
            command=self.update_high_score_visibility,
        )
        self.practice_mode_checkbox.grid(
            row=2,
            column=3,
            padx=(10, 10),
            pady=(0, 5),
            sticky="nw",
        )

        self.range_label = tk.Label(root, text="Number Range:")
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

        self.range_max_value = tk.IntVar(value=75)
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
        with Path.open("high_score.txt") as f:
            return f.read()

    def update_high_score(self) -> None:
        """Update the high score label and in the file."""
        with Path.open("high_score.txt", "w") as f:
            f.write(str(self.current_score))

        self.high_score = self.current_score
        self.high_score_label.config(text=f"Best: {self.high_score}")

    def update_high_score_visibility(self) -> None:
        """Update visibility of high score label depending on which mode is selected."""
        if self.practice_mode_checkbox_var.get():
            self.high_score_label.config(text="")
        else:
            self.high_score_label.config(text=f"Best: {self.high_score}")

    def update_timer(self) -> None:
        """Update the timer label every second."""
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.set(f"Time left: {self.time_left}")
            self.root.after(1000, self.update_timer)

        elif self.game_started:
            self.end_game()

    def button_pressed(self, _: tk.Event | None = None) -> None:
        """Handle the button press event."""
        if self.game_started:
            self.submit_answer()
        else:
            self.start_game()

    def start_game(self, _: tk.Event | None = None) -> None:
        """Start the game."""
        try:
            self.generate_questions()
        except (tk.TclError, IndexError):
            self.display_error("Invalid number range!")
            return

        self.practice_mode_checkbox.config(state=tk.DISABLED)

        self.answer_entry.focus_set()

        self.game_started = True
        self.submit_button.config(text="Submit")
        self.question_label.config(
            text=self.questions[self.current_question_index]["question"],
        )

        self.current_score = 0
        self.current_score_label.set(f"Score: {self.current_score}")
        self.score_label.grid()

        if not self.practice_mode_checkbox_var.get():
            self.time_left = 31
            self.timer_label.set(f"Time left: {self.time_left}")
            self.update_timer()

    def generate_questions(self) -> None:
        """Generate the questions based on the selected question type."""
        numbers_list = list(
            range(self.range_min_value.get(), self.range_max_value.get() + 1),
        )
        numbers_list[1]

        random.shuffle(numbers_list)

        if self.question_type_var.get() == "squares":
            for number in numbers_list:
                question = f"What is {number}^2?"
                answer = number**2
                self.questions.append({"question": question, "answer": answer})

        if self.question_type_var.get() == "roots":
            for number in numbers_list:
                question = f"What is square root of {number**2}?"
                answer = number
                self.questions.append({"question": question, "answer": answer})

        random.shuffle(self.questions)

    def submit_answer(self, _: tk.Event | None = None) -> None:
        """Process the answer to the current question."""
        try:
            answer = int(self.answer_entry.get().strip())
        except ValueError:
            answer = None

        correct_answer = self.questions[self.current_question_index]["answer"]
        if answer == correct_answer:
            self.current_score += 1
        self.current_score_label.set(f"Score: {self.current_score}")

        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.question_label.config(
                text=self.questions[self.current_question_index]["question"],
            )
        else:
            self.end_game()

        self.answer_entry.delete(0, tk.END)

    def end_game(self) -> None:
        """End the game."""
        if (
            self.current_score > int(self.read_high_score())
            and not self.practice_mode_checkbox_var.get()
        ):
            self.update_high_score()
            self.question_label.config(text="Game Over!\nNew High Score!")
        else:
            self.question_label.config(text="Game Over!")

        self.practice_mode_checkbox.config(state=tk.NORMAL)

        self.game_started = False

        self.time_left = 0
        self.timer_label.set("")
        self.current_question_index = 0
        self.questions.clear()

        self.submit_button.config(text="Restart")

    def display_error(self, message: str) -> None:
        """Display an error message on the question label."""
        current_text = self.question_label.cget("text")
        self.question_label.config(text=message)
        self.root.after(2000, self.reset_question_label, current_text)

    def reset_question_label(self, text: str) -> None:
        """Reset the question label to the previous text."""
        self.question_label.config(text=text)


if __name__ == "__main__":
    root = tk.Tk()
    app = SquaresTester(root)
    root.mainloop()
