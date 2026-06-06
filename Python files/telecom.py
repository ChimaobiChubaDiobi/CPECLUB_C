

def start():
    print("Welcome to the Telecom Dashboard!")
    name = str(input("Enter your name: "))
    while True:
        try:
            phone = int(input("Enter your phone number: "))
            break
        except ValueError:
            print("Please enter a valid phone number")

    bill_amount = 0

    while True:
        print(f"Welcome, {name}!\n --MAIN MENU--\n 1. Make a Call \n 2. Send an SMS \n 3. View Current Bill \n 4. Pay Bill \n 5. Exit")
        while True:
            try:
                choice = int(input("Select an option"))
                break
            except ValueError:
                print("Please enter a valid option")
        if choice == 1:
            while True:
                try:
                    duration = int(input("How many minutes was the call?"))
                    break
                except ValueError:
                    print("Please enter a valid number")
            cost = duration*10
            bill_amount += cost
            print(f"Call completed. #{cost} has been added to your bill.")
        elif choice == 2:
            while True:
                try:
                    message = int(input("How many messages would you like to send?"))
                    break
                except ValueError:
                    print("Please enter a valid number")
            cost = message*4
            bill_amount += cost
            print(f"Message sent! #{cost} has been added to your bill.")
        elif choice == 3:
            print(f"--YOUR PROFILE-- \nName: {name}\nPhone Number: {phone}\nBill Amount: #{bill_amount} ")
        elif choice == 4:
            payment = int(input("How much do you want to pay ?"))
            bill_amount -= payment
            print(f"Payment successful. Your current bill is #{bill_amount}")
        elif choice == 5:
            print("Goodbye from Telecom!")
            break
        else:
            print("Invalid Choice!")



start()