# In-memory storage for expenses
# Format: [id, month, description, amount]
expenses = [
    [1, "05", "Data Subscription", 2500],
    [2, "06", "Lunch", 1200],
    [3, "06", "Transport", 800]
]

def get_next_id():
    """Helper to generate a unique ID based on existing ones"""
    if not expenses:
        return 1
    # Get max id to ensure uniqueness even after deletions
    return max([expense[0] for expense in expenses]) + 1

def add_expense(month, description, amount):
    expense_id = get_next_id()
    expenses.append([expense_id, month, description, amount])
    print(f"Expense added successfully! ID: {expense_id}")

def view_expenses():
    if not expenses:
        print("No expenses found.")
        return
    print(f"{'ID':<5} | {'Month':<6} | {'Description':<20} | {'Amount':<10}")
    print("-" * 50)
    for expense in expenses:
        print(f"{expense[0]:<5} | {expense[1]:<6} | {expense[2]:<20} | ₦{expense[3]:<10.2f}")

def update_expense(expense_id, new_description, new_amount):
    for expense in expenses:
        if expense[0] == expense_id:
            expense[2] = new_description
            expense[3] = new_amount
            print(f"Expense {expense_id} updated successfully.")
            return
    print(f"Expense with ID {expense_id} not found.")

def delete_expense(expense_id):
    for i, expense in enumerate(expenses):
        if expense[0] == expense_id:
            del expenses[i]
            print(f"Expense {expense_id} deleted successfully.")
            return
    print(f"Expense with ID {expense_id} not found.")

def summary_all():
    # Use list comprehension to extract amounts
    amounts = [expense[3] for expense in expenses]
    total = sum(amounts)
    print(f"Total spent across all months: ₦{total:.2f}")

def summary_by_month(month):
    # Use list comprehension to filter by month and extract amounts
    amounts = [expense[3] for expense in expenses if expense[1] == month]
    total = sum(amounts)
    print(f"Total spent in month {month}: ₦{total:.2f}")

def main():
    while True:
        print("\n--- Command Line Expense Tracker ---")
        print("1. Add an expense")
        print("2. View all expenses")
        print("3. Update an expense")
        print("4. Delete an expense")
        print("5. View total summary")
        print("6. View monthly summary")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ")
        
        if choice == '1':
            month = input("Enter month (e.g., 05, 06): ")
            description = input("Enter description: ")
            try:
                amount = float(input("Enter amount: "))
                add_expense(month, description, amount)
            except ValueError:
                print("Invalid amount. Please enter a valid number.")
                
        elif choice == '2':
            print("\n--- All Expenses ---")
            view_expenses()
            
        elif choice == '3':
            try:
                expense_id = int(input("Enter expense ID to update: "))
                new_description = input("Enter new description: ")
                new_amount = float(input("Enter new amount: "))
                update_expense(expense_id, new_description, new_amount)
            except ValueError:
                print("Invalid input. ID and amount must be numbers.")
                
        elif choice == '4':
            try:
                expense_id = int(input("Enter expense ID to delete: "))
                delete_expense(expense_id)
            except ValueError:
                print("Invalid ID. Please enter a valid number.")
                
        elif choice == '5':
            print("\n--- Total Summary ---")
            summary_all()
            
        elif choice == '6':
            month = input("Enter month to summarize (e.g., 05, 06): ")
            print(f"\n--- Summary for Month {month} ---")
            summary_by_month(month)
            
        elif choice == '7':
            print("Exiting Tracker. All data will be lost. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
