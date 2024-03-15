import tkinter as tk
from tkinter import messagebox
import sqlite3

class ExpenseTrackerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Expense Tracker")

        self.db = ExpenseDB("expenses.db")

        self.create_widgets()
        self.load_expenses()

    def create_widgets(self):
        self.expense_listbox = tk.Listbox(self.master, width=50, height=20)
        self.expense_listbox.pack(padx=10, pady=10)

        self.amount_entry = tk.Entry(self.master)
        self.amount_entry.pack(pady=5)
        self.amount_entry.insert(0, "Amount")

        self.description_entry = tk.Entry(self.master)
        self.description_entry.pack(pady=5)
        self.description_entry.insert(0, "Description")

        self.add_button = tk.Button(self.master, text="Add Expense", command=self.add_expense)
        self.add_button.pack(pady=5)

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            description = self.description_entry.get()
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0")
                return
            expense = Expense(amount, description)
            self.db.add_expense(expense)
            self.load_expenses()
            messagebox.showinfo("Success", "Expense added successfully")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")

    def load_expenses(self):
        self.expense_listbox.delete(0, tk.END)
        expenses = self.db.get_all_expenses()
        for expense in expenses:
            self.expense_listbox.insert(tk.END, f"${expense.amount:.2f} - {expense.description}")

class Expense:
    def __init__(self, amount, description):
        self.amount = amount
        self.description = description

class ExpenseDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses
                               (amount REAL, description TEXT)''')
        self.conn.commit()

    def add_expense(self, expense):
        self.cursor.execute('''INSERT INTO expenses VALUES (?, ?)''', (expense.amount, expense.description))
        self.conn.commit()

    def get_all_expenses(self):
        self.cursor.execute('''SELECT * FROM expenses''')
        rows = self.cursor.fetchall()
        expenses = [Expense(row[0], row[1]) for row in rows]
        return expenses

def main():
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
