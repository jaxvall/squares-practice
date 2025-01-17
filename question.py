import random

class Questions:
    def __init__(self, number_range: list, modes=['squares']):
        self.numbers = random.shuffle(range(1, number_range + 1))
        self.modes = modes
        
        self.questions = []
        if 'squares' in self.modes:
            for number in self.numbers:
                question = f'What is {number}^\u00b2?'
                answer = number ** 2
                self.questions.append({'question': question, 'answer': answer})

        if 'roots' in self.modes:
            for number in self.numbers:
                question = f'What is root {number}?' 
                answer = number
                self.questions.append({'question': question, 'answer': answer})