import tkinter as tk
from datetime import datetime

def calculate_age():
    birthdate_str = entry_birthdate.get()
    try:
        birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
        today = datetime.today()
        
        # Calculate age taking leap years into account
        if (today.month, today.day) < (birthdate.month, birthdate.day):
            age = today.year - birthdate.year - 1
        else:
            age = today.year - birthdate.year
        
        label_result.config(text=f"Your age is: {age} years")
    except ValueError:
        label_result.config(text="Invalid date format")

# Create the main application window
app = tk.Tk()
app.title("Age Calculator App")

# Create and pack widgets
label_instruction = tk.Label(app, text="Enter your birthdate (YYYY-MM-DD):")
entry_birthdate = tk.Entry(app)
button_calculate = tk.Button(app, text="Calculate Age", command=calculate_age)
label_result = tk.Label(app, text="")

label_instruction.pack()
entry_birthdate.pack()
button_calculate.pack()
label_result.pack()

# Start the main loop
app.mainloop()
