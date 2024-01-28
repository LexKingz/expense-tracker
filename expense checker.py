import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# Connect to SQLite database
conn = sqlite3.connect('expense_tracker.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        amount REAL,
        date TEXT
    )
''')
conn.commit()


# Tkinter GUI
class ExpenseTrackerApp:
    def __init__(self, master):
        self.master = master
        master.title("Expense Tracker")

        # Entry widgets
        self.description_entry = tk.Entry(master, width=30)
        self.description_entry.grid(row=0, column=1, padx=10, pady=10)
        self.amount_entry = tk.Entry(master, width=30)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)

        # Label widgets
        self.description_label = tk.Label(master, text="Description:")
        self.description_label.grid(row=0, column=0, padx=10, pady=10)
        self.amount_label = tk.Label(master, text="Amount:")
        self.amount_label.grid(row=1, column=0, padx=10, pady=10)

        # Button widgets
        self.add_button = tk.Button(master, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.view_button = tk.Button(master, text="View Expenses", command=self.view_expenses)
        self.view_button.grid(row=3, column=0, columnspan=2, pady=10)

    def add_expense(self):
        description = self.description_entry.get()
        amount = float(self.amount_entry.get()) if self.amount_entry.get() else 0.0

        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)', (description, amount, date))
        conn.commit()
        messagebox.showinfo("Expense Added", "Expense added successfully!")

    def view_expenses(self):
        cursor.execute('SELECT * FROM expenses')
        expenses = cursor.fetchall()

        if not expenses:
            messagebox.showinfo("No Expenses", "No expenses found.")
        else:
            expense_list = "\n".join([f"ID: {expense[0]}, Description: {expense[1]}, Amount: ${expense[2]:.2f}, Date: {expense[3]}" for expense in expenses])
            messagebox.showinfo("Expenses", expense_list)


# Create Tkinter window
root = tk.Tk()
app = ExpenseTrackerApp(root)
root.mainloop()

# Close the database connection
conn.close()
