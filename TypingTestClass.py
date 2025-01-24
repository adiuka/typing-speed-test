import tkinter as tk
import time
import random
import words as w
import json # We will use this to save and show our highscore!
from datetime import datetime
import os # Might use later

scores = "high_scores.json" # We will use this file to add scores

class TypingTest: # Trying to create a class that uses the controller attribute as an argument. The argument here could be a module, in my case Tkinter. Saw this on Stacked and wanted to try.
    def __init__(self, controller):
        self.controller = controller 
        self.background_colour = "#9bdeac" # The class constatnt for a background color
        self.font = "Courier" # The class constant for the font
        controller.title("Typing speed test") 
        controller.config(padx=100, pady=100, bg=self.background_colour)

        self.word_list = w.word_list # Initialise our list
        self.current_word = random.choice(self.word_list) # Set the first random work from our list

        self.timer = None # Need this to be able to switch it to None once I call the reset function
        self.words_typed = 0 # Keeps the typed word count
        
        # Set up our labels
        self.high_scores = self.load_highscores() # The function is called to load the Highscores
        self.high_score_label = tk.Label(controller, text=self.display_high_score(), bg=self.background_colour, font=(self.font, 30, "bold"))
        self.high_score_label.grid(column=1, row=0)

        self.timer_label = tk.Label(controller, text="00:00", bg="white", font=(self.font, 45, "bold"))
        self.timer_label.grid(column=1, row=1, padx=20, pady=20)

        self.word_label = tk.Label(controller, text="Word", bg=self.background_colour, font=(self.font, 30, "bold"))
        self.word_label.grid(column=1, row=2)

        self.word_entry = tk.Entry(controller, width=30)
        self.word_entry.grid(column=0, row=3, columnspan=3)
        self.word_entry.bind("<space>", self.check_word) # Bind the space key as the submit word button, similarly to the website

        self.start_button= tk.Button(controller, text="Start", command=self.start_test)
        self.start_button.grid(column=0, row=4)

        self.reset_button = tk.Button(controller, text="Reset", command=self.reset_test)
        self.reset_button.grid(column=2, row=4)

        self.result_label = tk.Label(controller, text="", bg=self.background_colour, font=(self.font, 20, "bold"))
        self.result_label.grid(column=0, row=5, columnspan=3, pady=20)


    def check_word(self, event):
        """Function to check if entered word is correct, then give a score."""
        user_word = self.word_entry.get().strip() # Gets the current word in the box and strips it of spaces
        if user_word.lower() == self.current_word:
            self.words_typed += 1
            self.word_entry.delete(0, tk.END)
            self.current_word = random.choice(self.word_list)
            self.word_label.config(text=self.current_word, fg='black')
        else:
            self.word_label.config(text=f"Words do not match {self.current_word} : {user_word}", fg='red')

    def start_test(self):
        """The starting Function. Calls the countdown and sets the current word"""
        self.word_label.config(text=f"{self.current_word}")
        self.word_entry.focus_set() # This sets the focus on the entering field
        self.countdown(t=60) # The tests calculates words per minute
        

    def reset_test(self):
        """The reset function, that turns the counter to 0 and resets the whole application"""
        self.controller.after_cancel(self.timer) # Cancels the previous functions timer attribute
        self.timer_label.config(text="00:00") # Sets the label to 00:00 again
        self.words_typed = 0
        self.result_label.config(text="")
        self.word_label.config(text="Word", fg='black')

    def countdown(self, t):
        """The countdown mechanism"""
        if t > 0: # The loop will continue as long as there are seconds
            mins, secs = divmod(t, 60) # Calculates the minutes and seconds using divmod. Returns a tupple of minutes in the division, everything that is left is seconds as the 2nd nr.
            self.timer_label.config(text="{:02d}:{:02d}".format(mins, secs)) # sets the formating and configures the label to the given time from mins secs
            self.timer = self.controller.after(1000, self.countdown, t - 1) # Schedule countdown again after 1000ms (1 second)
            t -= 1 # During this time the inputed seconds will be reduced by one
        else:
            self.timer_label.config(text="00:00")
            self.result_label.config(text=f"Score: {self.words_typed} words per minute.")
            self.update_high_scores(self.words_typed)
            self.words_typed = 0

    def load_highscores(self):
        """Loads highscores from a .json file"""
        try:
            with open(scores, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return [] # Returns an empty list if the file does not exist. Mostly useful for the first time...
        
    def save_high_score(self):
        """Saves high scores to .json file."""
        with open(scores, "w") as f:
            json.dump(self.high_scores, f)

    def update_high_scores(self, wpm):
        """Updates the high score list and saves it to the file."""
        score_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Gets the current date and time and formats it nicely
        self.high_scores.append({"wpm": wpm, "date": score_date})
        self.high_scores.sort(key=lambda x: x["wpm"], reverse=True) # Sorts it in descending order!
        self.save_high_score()
        self.high_score_label.config(text=self.display_high_score())

    def display_high_score(self):
        """Formats the highscore to display with score date"""
        if not self.high_scores:
            return "No High Scores Yet!"
        else:
            top_score = self.high_scores[0] # Gets the very first score from the .json
            return f"High Score: {top_score['wpm']} WPM - {top_score['date']}"
