
def check(choice_list): #for checking if input is valid
    while True:
        try:
            a = int(input("Enter Choice: "))
            while a not in choice_list:
                print(f"ERROR | {a} is invalid. Try again!") 
                a = int(input("Enter Choice: "))
        except ValueError:
            print("ERROR | Please enter a number.")
            continue
        return a