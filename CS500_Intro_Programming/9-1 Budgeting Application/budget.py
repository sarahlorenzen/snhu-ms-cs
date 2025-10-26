import json
import matplotlib.pyplot as plt
from datetime import datetime
import os
from typing import Dict, List, Optional, Any

# Expense Class
class Expense:
    """Represents a single expense entry."""
    
    def __init__(self, amount: float, description: str, date: str):
        """
        Initialize an expense.
        
        Args:
            amount: The expense amount (must be positive)
            description: Brief description of the expense
            date: Date in YYYY-MM-DD format
            
        Raises:
            ValueError: If amount is negative or zero
        """
        if amount <= 0:
            raise ValueError("Expense amount must be positive")
        
        self.amount = amount
        self.description = description
        self.date = date
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert expense to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of the expense
        """
        return {
            'amount': self.amount,
            'description': self.description,
            'date': self.date
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Expense':
        """
        Create an Expense from dictionary data.
        
        Args:
            data: Dictionary containing expense data
            
        Returns:
            Expense object
        """
        return cls(
            amount=data['amount'],
            description=data['description'],
            date=data['date']
        )
    
    def __repr__(self) -> str:
        """String representation of expense."""
        return f"Expense(${self.amount:.2f}, '{self.description}', {self.date})"

# Budget Category Class
class BudgetCategory:

    def __init__(self, name: str):
        """
        Initialize a budget category.
        
        Args:
            name: The name of the category (e.g., 'rent', 'groceries')
        """
        self.name = name
        self.expenses: List[Expense] = []

    # TO DO: Define function add_expense()

    def add_expense(self, amount: float, description: str, date: str) -> None:
        """
        Add an expense to this category.
        
        Args:
            amount: The expense amount (must be positive)
            description: Brief description of the expense
            date: Date in YYYY-MM-DD format
            
        Raises:
            ValueError: If amount is negative or zero
        """
        expense = Expense(amount, description, date)
        self.expenses.append(expense)
        
    # TO DO: Define function total_expenses()
    
    def total_expenses(self) -> float:
        """
        Calculate the total expenses for this category.
        
        Returns:
            Sum of all expenses in this category
        """
        return sum(expense.amount for expense in self.expenses)
    
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert category to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of the category
        """
        return {
            'name': self.name,
            'expenses': [expense.to_dict() for expense in self.expenses]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BudgetCategory':
        """
        Create a BudgetCategory from dictionary data.
        
        Args:
            data: Dictionary containing category data
            
        Returns:
            BudgetCategory object
        """
        category = cls(data['name'])
        category.expenses = [
            Expense.from_dict(exp_data) 
            for exp_data in data.get('expenses', [])
        ]
        return category


# Budget Manager Class
class BudgetManager:
    
    """Main class for managing budget, income, expenses, and savings goals."""
    
    DATA_FILE = 'budget_data.json'

    def __init__(self):
        """Initialize the budget manager."""
        self.income: float = 0.0
        self.savings_goal: float = 0.0
        self.categories: Dict[str, BudgetCategory] = {}
        self.load_data()


    # TO DO: Define function: set_income()

    def set_income(self, amount: float) -> None:
        """
        Set the user's income.
        
        Args:
            amount: Income amount (must be non-negative)
            
        Raises:
            ValueError: If amount is negative
        """
        if amount < 0:
            raise ValueError("Income cannot be negative")
        self.income = amount
        
    # TO DO: Define function: set_savings_goal()

    def set_savings_goal(self, amount: float) -> None:
        """
        Set the savings goal.
        
        Args:
            amount: Savings goal amount (must be non-negative)
            
        Raises:
            ValueError: If amount is negative
        """
        if amount < 0:
            raise ValueError("Savings goal cannot be negative")
        self.savings_goal = amount
        
    # TO DO: Define function: add_expense()

    def add_expense(self, category_name: str, amount: float, 
                   description: str, date: str) -> None:
        """
        Add an expense to a category.
        
        Args:
            category_name: Name of the expense category
            amount: Expense amount
            description: Brief description
            date: Date in YYYY-MM-DD format
        """
        # Sanitize category name
        category_name = category_name.strip().lower()
        
        if category_name not in self.categories:
            self.categories[category_name] = BudgetCategory(category_name)
        
        self.categories[category_name].add_expense(amount, description, date)
        
    # TO DO: Define function: total_expenses()

    def total_expenses(self) -> float:
        """
        Calculate total expenses across all categories.
        
        Returns:
            Sum of all expenses
        """
        return sum(category.total_expenses() 
                  for category in self.categories.values())
        
    # TO DO: Define function: progress_toward_goal()

    def progress_toward_goal(self) -> Dict[str, Any]:
        """
        Calculate progress toward savings goal.
        
        Returns:
            Dictionary with 'on_track' (bool), 'current_savings' (float),
            and 'needed' (float) keys
        """
        total_exp = self.total_expenses()
        current_savings = self.income - total_exp
        needed = self.savings_goal - current_savings
        
        return {
            'on_track': current_savings >= self.savings_goal,
            'current_savings': current_savings,
            'needed': needed if needed > 0 else 0
        }
        
    # TO DO: Define function: save_data()

    def save_data(self) -> None:
        """Save budget data to JSON file."""
        try:
            data = {
                'income': self.income,
                'savings_goal': self.savings_goal,
                'categories': {
                    name: category.to_dict() 
                    for name, category in self.categories.items()
                }
            }
            
            with open(self.DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error saving data: {e}")
            raise
        
    # TO DO: Define function: load_data()

    def load_data(self) -> None:
        """Load budget data from JSON file."""
        if not os.path.exists(self.DATA_FILE):
            return
        
        try:
            with open(self.DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.income = data.get('income', 0.0)
            self.savings_goal = data.get('savings_goal', 0.0)
            
            categories_data = data.get('categories', {})
            self.categories = {
                name: BudgetCategory.from_dict(cat_data)
                for name, cat_data in categories_data.items()
            }
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading data: {e}. Starting with fresh data.")
        
    # TO DO: Define function: visualize_expenses()

    def visualize_expenses(self) -> None:
        """Generate and display expense visualization."""
        if not self.categories:
            print("No expenses to visualize.")
            return
        
        # Prepare data
        category_names: List[str] = []
        category_totals: List[float] = []
        
        for name, category in self.categories.items():
            total = category.total_expenses()
            if total > 0:  # Only include categories with expenses
                category_names.append(name.capitalize())
                category_totals.append(total)
        
        if not category_totals:
            print("No expenses to visualize.")
            return
        
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Pie chart
        colors = plt.cm.Set3.colors
        ax1.pie(category_totals, labels=category_names, autopct='%1.1f%%',
                startangle=90, colors=colors)
        ax1.set_title('Expense Distribution by Category')
        
        # Bar chart
        ax2.bar(category_names, category_totals, color=colors[:len(category_names)])
        ax2.set_xlabel('Category')
        ax2.set_ylabel('Amount ($)')
        ax2.set_title('Total Expenses by Category')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()


# Input Validation Functions

# TO DO: Define function: get_valid_float()

def get_valid_float(prompt: str, allow_zero: bool = False) -> float:
    """
    Get a valid float input from user.
    
    Args:
        prompt: The prompt to display to the user
        allow_zero: Whether to allow zero as a valid input
        
    Returns:
        Valid float value
    """
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Error: Value cannot be negative. Please try again.")
            elif not allow_zero and value == 0:
                print("Error: Value must be greater than zero. Please try again.")
            else:
                return value
        except ValueError:
            print("Error: Please enter a valid number.")

# TO DO: Define function: get_valid_date()

def get_valid_date(prompt: str) -> str:
    """
    Get a valid date input from user in YYYY-MM-DD format.
    
    Args:
        prompt: The prompt to display to the user
        
    Returns:
        Valid date string in YYYY-MM-DD format
    """
    while True:
        date_str = input(prompt)
        try:
            # Validate date format and that it's a real date
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            print("Error: Please enter date in YYYY-MM-DD format (e.g., 2025-10-25).")

# TO DO: Define function: get_non_empty_string()

def get_non_empty_string(prompt: str) -> str:
    """
    Get a non-empty string from user.
    
    Args:
        prompt: The prompt to display
        
    Returns:
        Non-empty string
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Error: Input cannot be empty. Please try again.")

# Main Program
def main():
    """Main program loop."""
    manager: BudgetManager = BudgetManager()
    
    print("=" * 50)
    print("Welcome to the Personal Budgeting Application!")
    print("=" * 50)
    
    while True:
        print("\n" + "=" * 50)
        print("\nMenu:")
        print("=" * 50)
        print("1. Set Income")
        print("2. Set Savings Goal")
        print("3. Add Expense")
        print("4. View Total Expenses")
        print("5. View Savings Progress")
        print("6. Visualize Expenses")
        print("7. Save & Exit")
        print("=" * 50)
        
        choice: str = input("Choose an option (1-7): ").strip()

        if choice == '1':
        	# TO DO: Prompt for monthly income as input. Set income and display what income is set to.
            
            try:
                income: float = get_valid_float("Enter your monthly income: $", allow_zero=True)
                manager.set_income(income)
                print(f"Income set to: ${income:.2f}")
            except Exception as e:
                print(f"Error setting income: {e}")
        
        elif choice == '2':
        	# TO DO: Prompt for savings goal as input. Set savings goal and display savings goal is set to.
            
            try:
                goal: float = get_valid_float("Enter your savings goal: $", allow_zero=True)
                manager.set_savings_goal(goal)
                print(f"Savings goal set to: ${goal:.2f}")
            except Exception as e:
                print(f"Error setting savings goal: {e}")
        
        elif choice == '3':
        	# TO DO: 
            #      Prompt for expense category as input. 
            #      Prompt for expense amount as input. 
            #      Prompt for a brief description of the expense. 
            #      Prompt for expense date in the format of (YYYY-MM-DD)
            #      Add expense.
            #      Display added expense.
            
            try:
                category: str = get_non_empty_string("Enter expense category (e.g., rent, groceries): ")
                amount: float = get_valid_float("Enter expense amount: $")
                description: str = get_non_empty_string("Enter a brief description: ")
                date: str = get_valid_date("Enter expense date (YYYY-MM-DD): ")
                
                manager.add_expense(category, amount, description, date)
                print(f"Added expense: ${amount:.2f} for {category} on {date}")
            except ValueError as e:
                print(f"Error adding expense: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
        
        elif choice == '4':
	        # TO DO: Get total expenses. Display total expenses.
            
            total: float = manager.total_expenses()
            print(f"\n{'='*50}")
            print(f"Total Expenses: ${total:.2f}")
            print(f"{'='*50}")
            
            # Show breakdown by category
            if manager.categories:
                print("\nBreakdown by category:")
                for name, category in sorted(manager.categories.items()):
                    cat_total: float = category.total_expenses()
                    if cat_total > 0:
                        print(f"  {name.capitalize()}: ${cat_total:.2f}")
        
        elif choice == '5':
            # TO DO: Get progress towards goal. If on track, display: You are on track!, and also display the 
            #        current savings amount. If not on track, display: Current savings $xxx. You need $xxx to 
            #        reach your goal.
            
            progress: Dict[str, Any] = manager.progress_toward_goal()
            print(f"\n{'='*50}")
            print("Savings Progress")
            print(f"{'='*50}")
            print(f"Income: ${manager.income:.2f}")
            print(f"Total Expenses: ${manager.total_expenses():.2f}")
            print(f"Current Savings: ${progress['current_savings']:.2f}")
            print(f"Savings Goal: ${manager.savings_goal:.2f}")
            print(f"{'='*50}")
            
            if progress['on_track']:
                print("You are on track!")
            else:
                print(f"You need ${progress['needed']:.2f} more to reach your goal.")

        elif choice == '6':
	        # TO DO: call visualize_expenses() to show expense graph or pie chart
            
            try:
                manager.visualize_expenses()
            except Exception as e:
                print(f"Error creating visualization: {e}")

        elif choice == '7':
	        # TO DO: Save data and exit program. Display a message to indicate that data has been saved 
            #        successfully and exiting the program.
            
            try:
                manager.save_data()
                print("\nData saved successfully!")
                print("Thank you for using The Personal Budgeting Application!")
                print("Goodbye!")
                break
            except Exception as e:
                print(f"Error saving data: {e}")
                retry: str = input("Do you still want to exit? (yes/no): ").lower()
                if retry == 'yes':
                    break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

