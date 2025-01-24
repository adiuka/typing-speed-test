# Typing speed test in Tkinter

Hello and welcome to the typing speed test. It is quite a simple application, that when started will give you 60 seconds to type in the words you see.

Use spacebar to submit the word. If incorrect the text will turn red and you need to fix it and press space again. Once 60 seconds are up, you will get a score. It will be added to a .json with a date, and the highest score from there will be displayed everytime you start the app.

Room for improvement:
1. Honestly I think the .json saving method is not the best, I would prefer a CSV or a database that is hardcoded into the directory. Could implement that
2. I think I can also add a keystrokes per minute calculation there, that can capture how many button presses were made. Could be fun!
3. Once again the UI is not the best, would like to place it somewhere other than Tkinter, or use a Tkinter template.
4. I am sure I can simplify the code, as it ended up being more complicated than I though. Working with timers is complex in my oppinion so would love to come back here and make it more simple.

Otherwise, happy typing!
