"""
Simple Calculator Program for CS 500
Performs basic arithmetic operations: addition, subtraction, multiplication, and division.
"""

def display_menu():
    """Display the calculator menu of available operations."""
    print("\n" + "="*40)
    print("        SIMPLE CALCULATOR")
    print("="*40)
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (×)")
    print("4. Division (÷)")
    print("5. Exit")
    print("="*40)


def get_operation_choice():
    """
    Get and validate the user's operation choice.
    
    Returns:
        int: Valid operation choice (1-5)
    """
    while True:
        try:
            choice = int(input("\nEnter your choice (1-5): "))
            if 1 <= choice <= 5:
                return choice
            else:
                print("Error: Please enter a number between 1 and 5.")
        except ValueError:
            print("Error: Invalid input. Please enter a number.")


def get_number(prompt):
    """
    Get and validate a numeric input from the user.
    
    Args:
        prompt (str): The prompt message to display
        
    Returns:
        float: Valid numeric input
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Error: Invalid input. Please enter a valid number.")


def add(num1, num2):
    """Return the sum of two numbers."""
    return num1 + num2


def subtract(num1, num2):
    """Return the difference of two numbers."""
    return num1 - num2


def multiply(num1, num2):
    """Return the product of two numbers."""
    return num1 * num2


def divide(num1, num2):
    """
    Return the quotient of two numbers.
    
    Args:
        num1 (float): Dividend
        num2 (float): Divisor
        
    Returns:
        float: Quotient, or None if division by zero
    """
    if num2 == 0:
        return None
    return num1 / num2


def perform_calculation(operation, num1, num2):
    """
    Perform the selected arithmetic operation.
    
    Args:
        operation (int): Operation choice (1-4)
        num1 (float): First number
        num2 (float): Second number
        
    Returns:
        tuple: (result, operation_symbol) or (None, symbol) if error
    """
    if operation == 1:
        return add(num1, num2), "+"
    elif operation == 2:
        return subtract(num1, num2), "-"
    elif operation == 3:
        return multiply(num1, num2), "×"
    elif operation == 4:
        result = divide(num1, num2)
        return result, "÷"


def main():
    """Main program loop."""
    print("Welcome to the CS500 Python Simple Calculator!")
    
    while True:
        # Step 1: Display menu
        display_menu()
        
        # Step 2: Get operation choice
        operation = get_operation_choice()
        
        # Check if user wants to exit
        if operation == 5:
            print("\nThank you for using the calculator. Goodbye!")
            break
        
        # Step 2: Get numbers from user
        print("\nEnter your numbers:")
        num1 = get_number("First number: ")
        num2 = get_number("Second number: ")
        
        # Step 3: Perform calculation
        result, symbol = perform_calculation(operation, num1, num2)
        
        # Step 4: Display result with error handling for division by zero
        if result is None:
            print(f"Error: YOU Cannot divide by zero!")
        else:
            print(f"\n✓ Result: {num1} {symbol} {num2} = {result}")
        
        # Step 5: Ask if user wants to continue
        print("\n" + "-"*40)
        continue_choice = input("Do you want to perform another calculation? (yes/no): ").lower() # change to lowercase to account for CAPS or Camel Case
        
        if continue_choice not in ['yes', 'y']:
            print("\nThank you for using the calculator. Goodbye!")
            break


if __name__ == "__main__":
    main()
