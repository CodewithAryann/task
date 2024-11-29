import random
import tkinter as tk
from tkinter import messagebox


def load_jokes(file_path):
    """
    Loads jokes from a file and returns a list of tuples (setup, punchline).
    Each joke is split by the '?' character into setup and punchline.
    """
    jokes = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if '?' in line:
                    setup, punchline = line.strip().split('?', 1)
                    jokes.append((setup.strip() + "?", punchline.strip()))
    except FileNotFoundError:
        messagebox.showerror("Error", "The jokes file was not found. Please check the file path and try again.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred while loading jokes: {e}")
    return jokes


def tell_joke():
    """
    Selects and displays a random joke.
    """
    if jokes:
        joke = random.choice(jokes)
        setup, punchline = joke
        joke_label.config(text=setup)
        reveal_button.config(state=tk.NORMAL, command=lambda: reveal_punchline(punchline))
        punchline_label.config(text="")  # Clear previous punchline
    else:
        joke_label.config(text="No jokes available. Please load a valid jokes file.")
        reveal_button.config(state=tk.DISABLED)


def reveal_punchline(punchline):
    """
    Reveals the punchline of the current joke.
    """
    punchline_label.config(text=punchline)
    reveal_button.config(state=tk.DISABLED)


# Create the main application window
app = tk.Tk()
app.title("Alexa's Joke Bot")
app.geometry("600x400")
app.resizable(True, True)

# Load jokes from file
jokes = load_jokes("./ex2/randomJokes.txt")  # Update the file path as needed

# GUI Components
title_label = tk.Label(app, text="😂 Alexa's Joke Bot 😂", font=("Comic Sans MS", 20, "bold"), fg="#4444FF", pady=10)
title_label.pack()

frame = tk.Frame(app, padx=20, pady=20)
frame.pack(fill=tk.BOTH, expand=True)

joke_label = tk.Label(
    frame,
    text="Click the button below to hear a joke!",
    font=("Comic Sans MS", 14),
    wraplength=500,
    pady=20,
    justify="center"
)
joke_label.pack()

reveal_button = tk.Button(
    frame,
    text="Reveal Punchline",
    state=tk.DISABLED,
    font=("Comic Sans MS", 12),
    bg="#FFD700",
    activebackground="#FFA500",
    cursor="hand2"
)
reveal_button.pack(pady=10)

punchline_label = tk.Label(
    frame,
    text="",
    font=("Comic Sans MS", 14, "italic"),
    wraplength=500,
    pady=20,
    fg="#555555",
    justify="center"
)
punchline_label.pack()

tell_joke_button = tk.Button(
    app,
    text="Tell Me a Joke",
    font=("Comic Sans MS", 14, "bold"),
    bg="#4CAF50",
    fg="white",
    activebackground="#45A049",
    cursor="hand2",
    command=tell_joke
)
tell_joke_button.pack(pady=20)

# Start the Tkinter event loop
app.mainloop()
