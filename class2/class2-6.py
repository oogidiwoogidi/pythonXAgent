import os

fruit_store = {"apple": 25, "banana": 20, "orange": 30}


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_menu():
    print("\nFruit Store Menu:")
    print("1. Add fruit price")
    print("2. Modify fruit price")
    print("3. Delete fruit")
    print("4. Show all fruits")
    print("5. Exit")


while True:
    clear_screen()
    print_menu()
    choice = input("Enter your choice (1-5): ")
    if choice == "1":
        fruit = input("Enter fruit name to add: ").strip().lower()
        if fruit in fruit_store:
            print(f"{fruit} already exists.")
        else:
            try:
                price = int(input(f"Enter price for {fruit}: "))
                fruit_store[fruit] = price
                print(f"{fruit} added with price {price}.")
            except ValueError:
                print("Invalid price.")
    elif choice == "2":
        fruit = input("Enter fruit name to modify: ").strip().lower()
        if fruit in fruit_store:
            try:
                price = int(input(f"Enter new price for {fruit}: "))
                fruit_store[fruit] = price
                print(f"{fruit} price updated to {price}.")
            except ValueError:
                print("Invalid price.")
        else:
            print(f"{fruit} not found.")
    elif choice == "3":
        fruit = input("Enter fruit name to delete: ").strip().lower()
        if fruit in fruit_store:
            del fruit_store[fruit]
            print(f"{fruit} deleted.")
        else:
            print(f"{fruit} not found.")
    elif choice == "4":
        if fruit_store:
            for fruit, price in fruit_store.items():
                print(f"{fruit}: {price}")
        else:
            print("No fruits in store.")
    elif choice == "5":
        print("Exiting system.")
        break
    else:
        print("Invalid choice. Please enter a number from 1 to 5.")
