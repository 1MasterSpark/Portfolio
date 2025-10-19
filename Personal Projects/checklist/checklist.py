import tkinter as tk

window = tk.Tk()

window.title("Daily Checklist App")

label = tk.Label(window, text="Today's Tasks:")
label.pack()

task1 = tk.Checkbutton(window, text="Pray")
task1.pack()

task2 = tk.Checkbutton(window, text="Exercise")
task2.pack()

task3 = tk.Checkbutton(window, text="Water plants")
task3.pack()

window.mainloop()