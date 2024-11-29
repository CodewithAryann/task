import random
import time
from tkinter import Tk, Label, Button, Entry, StringVar, messagebox

class MathQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz")
        self.root.geometry("400x300")
        
        self.score = 0
        self.question_num = 0
        self.total_questions = 10
        self.num1 = 0
        self.num2 = 0
        self.operation = ""
        self.correct_answer = 0
        self.start_time = time.time()
        
        # Difficulty variable
        self.difficulty = StringVar(value="1")
        
        # Widgets
        Label(root, text="Math Quiz", font=("Arial", 20)).pack(pady=10)
        Label(root, text="Select Difficulty Level:", font=("Arial", 12)).pack()
        
        Button(root, text="Easy (1-digit)", command=lambda: self.start_quiz(1)).pack(pady=5)
        Button(root, text="Moderate (2-digit)", command=lambda: self.start_quiz(2)).pack(pady=5)
        Button(root, text="Advanced (4-digit)", command=lambda: self.start_quiz(3)).pack(pady=5)
        
        self.question_label = Label(root, text="", font=("Arial", 14))
        self.question_label.pack(pady=10)
        
        self.answer_var = StringVar()
        self.answer_entry = Entry(root, textvariable=self.answer_var, font=("Arial", 12))
        self.answer_entry.pack()
        
        self.submit_button = Button(root, text="Submit Answer", command=self.check_answer, state="disabled")
        self.submit_button.pack(pady=10)
        
        self.feedback_label = Label(root, text="", font=("Arial", 12))
        self.feedback_label.pack(pady=5)
        
        self.progress_label = Label(root, text="", font=("Arial", 10))
        self.progress_label.pack(pady=5)
    
    def random_int(self, difficulty):
        if difficulty == 1:  # Easy
            return random.randint(1, 9)
        elif difficulty == 2:  # Moderate
            return random.randint(10, 99)
        elif difficulty == 3:  # Advanced
            return random.randint(1000, 9999)
    
    def decide_operation(self):
        return random.choice(['+', '-'])
    
    def start_quiz(self, difficulty):
        self.difficulty = difficulty
        self.score = 0
        self.question_num = 0
        self.start_time = time.time()
        self.next_question()
        self.submit_button["state"] = "normal"
    
    def next_question(self):
        if self.question_num < self.total_questions:
            self.num1 = self.random_int(self.difficulty)
            self.num2 = self.random_int(self.difficulty)
            self.operation = self.decide_operation()
            
            # Adjust for subtraction to avoid negatives
            if self.operation == '-' and self.num1 < self.num2:
                self.num1, self.num2 = self.num2, self.num1
            
            self.correct_answer = self.num1 + self.num2 if self.operation == '+' else self.num1 - self.num2
            self.question_label.config(text=f"What is {self.num1} {self.operation} {self.num2}?")
            self.answer_var.set("")
            self.feedback_label.config(text="")
            self.progress_label.config(text=f"Question {self.question_num + 1}/{self.total_questions}")
        else:
            self.end_quiz()
    
    def check_answer(self):
        try:
            user_answer = int(self.answer_var.get())
        except ValueError:
            self.feedback_label.config(text="Please enter a valid number.", fg="red")
            return
        
        if user_answer == self.correct_answer:
            self.score += 10
            self.feedback_label.config(text="Correct!", fg="green")
        else:
            self.feedback_label.config(text=f"Wrong! Correct answer: {self.correct_answer}", fg="red")
        
        self.question_num += 1
        self.root.after(1000, self.next_question)  # Wait 1 second before showing the next question
    
    def end_quiz(self):
        elapsed_time = time.time() - self.start_time
        self.question_label.config(text="")
        self.answer_entry.pack_forget()
        self.submit_button.pack_forget()
        self.feedback_label.config(text="")
        
        messagebox.showinfo("Quiz Completed", f"Your final score: {self.score}/100\nTime taken: {elapsed_time:.2f} seconds")
        self.display_results()
    
    def display_results(self):
        grade = ""
        message = ""
        if self.score >= 90:
            grade = "A+"
            message = "Excellent! You are a Math master!"
        elif self.score >= 80:
            grade = "A"
            message = "Great job! You're really good at this!"
        elif self.score >= 70:
            grade = "B"
            message = "Nice work! Keep practicing!"
        elif self.score >= 60:
            grade = "C"
            message = "Good effort, but there's room for improvement."
        else:
            grade = "D"
            message = "Don't worry, practice makes perfect!"
        
        self.feedback_label.config(text=f"Grade: {grade}\n{message}")
        self.progress_label.config(text="Would you like to play again?")
        Button(self.root, text="Play Again", command=self.reset_quiz).pack(pady=10)
    
    def reset_quiz(self):
        self.root.destroy()
        main()  # Restart the app

def main():
    root = Tk()
    app = MathQuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
