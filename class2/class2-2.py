shopping_list = []

while True:
    # --- Display Shopping List ---
    print("Current shopping list:")
    for i in range(len(shopping_list)):
        print(f"{i}: {shopping_list[i]}")
    print()

    # --- Display User Menu ---
    print("User Menu:")
    print("1 - Add item")
    print("2 - Modify item")
    print("3 - Delete item")
    print("4 - Exit")
    print("Type 'done' to finish.")
    choice = input("Please choose an option: ")

    # Simulate clearing the previous menu
    if choice in ["1", "2", "3", "4"]:
        print("\n" * 20)

    # --- Handle User Choice ---
    if choice == "done" or choice == "4":
        break
    elif choice == "1":
        item = input("Enter the item to add: ")
        shopping_list.append(item)
    elif choice == "2":
        if len(shopping_list) == 0:
            print("The list is empty.")
            input("Press Enter to continue...")
            continue
        index = input("Enter the index of the item to modify: ")
        if index.isdigit():
            idx = int(index)
            if 0 <= idx < len(shopping_list):
                new_item = input("Enter the new item: ")
                shopping_list[idx] = new_item
            else:
                print("Invalid index.")
                input("Press Enter to continue...")
        else:
            print("Invalid index.")
            input("Press Enter to continue...")
    elif choice == "3":
        if len(shopping_list) == 0:
            print("The list is empty.")
            input("Press Enter to continue...")
            continue
        print("Delete Menu:")
        print("a - Delete by index")
        print("b - Delete by name")
        delete_choice = input("Choose delete method (a/b): ")
        if delete_choice == "a":
            index = input("Enter the index of the item to delete: ")
            if index.isdigit():
                idx = int(index)
                if 0 <= idx < len(shopping_list):
                    shopping_list.pop(idx)
                    print("Item deleted by index.")
                else:
                    print("Invalid index.")
                    input("Press Enter to continue...")
            else:
                print("Invalid index.")
                input("Press Enter to continue...")
        elif delete_choice == "b":
            item = input("Enter the name of the item to delete: ")
            if item in shopping_list:
                shopping_list.remove(item)
                print(f"Removed '{item}' from the shopping list.")
            else:
                print("Item not found.")
                input("Press Enter to continue...")
        else:
            print("Unknown delete option.")
            input("Press Enter to continue...")
    else:
        print("Unknown option.")
        input("Press Enter to continue...")
