import tkinter as tk
import random

class SquaresTester:
    def __init__(self, root, max_number: list):
        self.numbers = list(range(11, max_number + 1))
        random.shuffle(self.numbers)
        
        self.questions = []
        self.current_question_index = 0
        self.game_started = False
        
        self.current_score = 0
        self.current_score_label = tk.StringVar(value=f'Score: {self.current_score}')
        
        self.time_left = 31
        self.timer_label = tk.StringVar(value='')

        self.root = root
        self.root.title("Squares Practice")
        self.center_window(430, 200)

        self.high_score_label = tk.Label(root, text=f'Best: {self.read_high_score()}')
        self.high_score_label.grid(row=0, column=0, padx=(10, 30), pady=10, sticky="nw")
        
        self.score_label = tk.Label(root, text=self.current_score_label, textvariable=self.current_score_label)
        self.score_label.grid(row=0, column=1, padx=(10, 10), pady=10, sticky="ew")
        self.score_label.grid_remove()
        
        self.timer_display = tk.Label(root, textvariable=self.timer_label, width=10)
        self.timer_display.grid(row=0, column=2, padx=(10, 10), pady=10, sticky="ne")

        self.question_label = tk.Label(root, text='Press the button to start!', height=2, width=20, anchor="w")
        self.question_label.grid(row=1, column=1, columnspan=2, padx=0, pady=10, sticky="w")

        self.answer_entry = tk.Entry(root, width=20)
        self.answer_entry.grid(row=2, column=1, padx=0, pady=(2, 0))
        self.answer_entry.bind("<Return>", self.button_pressed)
        self.answer_entry.bind("<space>", self.button_pressed)
        self.answer_entry.focus_set()

        self.submit_button = tk.Button(root, text="Start", command=self.button_pressed)
        self.submit_button.grid(row=2, column=2, padx=(5, 0), pady=10)

        self.question_type_var = tk.StringVar(value="squares")
        self.squares_radio = tk.Radiobutton(root, text="Squares", variable=self.question_type_var, value="squares")
        self.squares_radio.grid(row=0, column=3, padx=(25, 10), pady=(15, 0), sticky="nw")

        self.roots_radio = tk.Radiobutton(root, text="Roots", variable=self.question_type_var, value="roots")
        self.roots_radio.grid(row=1, column=3, padx=(25, 10), pady=(5, 5), sticky="nw")

    
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    
    def read_high_score(self):
        with open('high_score.txt', 'r') as f:
            high_score = f.read()
        return high_score
    
    
    def update_high_score(self):
        with open('high_score.txt', 'w') as f:
            f.write(str(self.current_score))
        self.high_score_label.config(text=f'Best: {self.read_high_score()}')
            
    
    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.set(f'Time left: {self.time_left}')
            self.root.after(1000, self.update_timer)
        else:
            self.end_game()
    

    def generate_questions(self):
        if self.question_type_var.get() == "squares":
            for number in self.numbers:
                question = f'What is {number}^2?'
                answer = number ** 2
                self.questions.append({'question': question, 'answer': answer})

        if self.question_type_var.get() == "roots":
            for number in self.numbers:
                question = f'What is square root of {number ** 2}?' 
                answer = number
                self.questions.append({'question': question, 'answer': answer})
                
        random.shuffle(self.questions)

    
    def button_pressed(self, _ = None):
        if self.game_started:
            self.submit_answer()
        else:
            self.start_game()
    

    def start_game(self, _ = None):
        self.time_left = 31
        self.timer_label.set(f'Time left: {self.time_left}')
        
        self.generate_questions()
        self.game_started = True
        self.submit_button.config(text="Submit")
        self.question_label.config(text=self.questions[self.current_question_index]['question'])
        self.score_label.grid()
        self.timer_display.grid()
        
        self.update_timer()
                    
    
    def submit_answer(self, _ = None):
        try:
            answer = int(self.answer_entry.get().strip())
        except ValueError:
            answer = None
            
        correct_answer = self.questions[self.current_question_index]['answer']
        if answer == correct_answer:
            self.current_score += 1
        self.current_score_label.set(f'Score: {self.current_score}')
            
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.question_label.config(text=self.questions[self.current_question_index]['question'])
        else:
            self.end_game()
            
        self.answer_entry.delete(0, tk.END)
    
    
    def end_game(self):
        if self.current_score > int(self.read_high_score()):
            self.update_high_score()
            self.question_label.config(text="Game Over!\nNew High Score!")
        else:
            self.question_label.config(text="Game Over!")
        
        self.game_started = False
        
        self.current_score = 0
        self.current_score_label.set(f'Score: {self.current_score}')
        self.current_question_index = 0
        self.questions.clear()
        
        self.submit_button.config(text="Restart")


if __name__ == "__main__":
    root = tk.Tk()
    app = SquaresTester(root, 75)
    root.mainloop()