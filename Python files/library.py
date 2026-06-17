# Initial Inventory
# Format: [Item Name, Status]
inventory = [
    ["Arduino Starter Kit", "Available"],
    ["Digital Multimeter", "Borrowed"],
    ["Python Crash Course Book", "Available"],
    ["Raspberry Pi 4", "Available"]
]

def borrow_item(item_name):
    """Marks an item as 'Borrowed' if it is 'Available'."""
    # Using case-insensitive search for better user experience
    for item in inventory:
        if item[0].lower() == item_name.lower():
            if item[1] == "Available":
                item[1] = "Borrowed"
                print(f"Success! You have borrowed the '{item[0]}'.")
                return
            else:
                print(f"Sorry, the '{item[0]}' is currently borrowed. You have to wait.")
                return
    print(f"Item '{item_name}' not found in the inventory.")

def return_item(item_name):
    """Marks an item as 'Available' if it is 'Borrowed'."""
    for item in inventory:
        if item[0].lower() == item_name.lower():
            if item[1] == "Borrowed":
                item[1] = "Available"
                print(f"Success! You have returned the '{item[0]}'.")
                return
            else:
                print(f"The '{item[0]}' is already marked as available. Are you sure you borrowed it?")
                return
    print(f"Item '{item_name}' not found in the inventory.")

def add_new_item(item_name):
    """Adds a new item to the inventory, defaulting to 'Available'."""
    # Check if it already exists
    for item in inventory:
        if item[0].lower() == item_name.lower():
            print(f"Item '{item[0]}' already exists in the inventory.")
            return
    
    inventory.append([item_name, "Available"])
    print(f"Success! Added '{item_name}' to the inventory.")

def get_available_items():
    """Returns a list of all items that are currently 'Available' using list comprehension."""
    return [item for item in inventory if item[1] == "Available"]

def search_items(keyword):
    """Returns a list of items that contain the keyword in their name using list comprehension."""
    return [item for item in inventory if keyword.lower() in item[0].lower()]

def display_items(items):
    """Helper function to beautifully display a list of items."""
    if not items:
        print("No items found.")
        return
    print(f"\n{'-'*45}")
    print(f"{'Item Name':<30} | {'Status':<10}")
    print(f"{'-'*45}")
    for item in items:
        print(f"{item[0]:<30} | {item[1]:<10}")
    print(f"{'-'*45}\n")

def main():
    while True:
        print("\n--- CPE Department Library & Equipment Tracker ---")
        print("1. View all available items")
        print("2. Borrow an item")
        print("3. Return an item")
        print("4. Add a new item")
        print("5. View all inventory items")
        print("6. Search for an item (Keyword)")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ")
        
        if choice == '1':
            available = get_available_items()
            print("\n>> Viewing Available Items:")
            display_items(available)
            
        elif choice == '2':
            item_name = input("Enter the name of the item to borrow: ")
            borrow_item(item_name)
            
        elif choice == '3':
            item_name = input("Enter the name of the item to return: ")
            return_item(item_name)
            
        elif choice == '4':
            item_name = input("Enter the name of the new equipment: ")
            add_new_item(item_name)
            
        elif choice == '5':
            print("\n>> Viewing All Inventory:")
            display_items(inventory)
            
        elif choice == '6':
            keyword = input("Enter keyword to search for (e.g., Arduino): ")
            print(f"\n>> Search Results for '{keyword}':")
            results = search_items(keyword)
            display_items(results)
            
        elif choice == '7':
            print("Exiting Tracker. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
