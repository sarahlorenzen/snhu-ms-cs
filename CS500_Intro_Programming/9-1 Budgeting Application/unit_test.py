import unittest
import json
import os
from datetime import datetime
from unittest.mock import patch, mock_open
from typing import Any
import sys

# Import the classes from the main application
# Adjust the import to match your filename
# If your file is named 'budget.py', change to: from budget import ...
from budget import Expense, BudgetCategory, BudgetManager, get_valid_float, get_valid_date


class TestExpense(unittest.TestCase):
    """Test cases for Expense class."""
    
    def test_init_valid(self) -> None:
        """Test expense initialization with valid data."""
        expense = Expense(50.00, "Weekly shopping", "2025-10-20")
        self.assertEqual(expense.amount, 50.00)
        self.assertEqual(expense.description, "Weekly shopping")
        self.assertEqual(expense.date, "2025-10-20")
    
    def test_init_negative_amount(self) -> None:
        """Test that negative amount raises ValueError."""
        with self.assertRaises(ValueError):
            Expense(-10.00, "Invalid", "2025-10-20")
    
    def test_init_zero_amount(self) -> None:
        """Test that zero amount raises ValueError."""
        with self.assertRaises(ValueError):
            Expense(0, "Invalid", "2025-10-20")
    
    def test_to_dict(self) -> None:
        """Test conversion to dictionary."""
        expense = Expense(50.00, "Test", "2025-10-20")
        data = expense.to_dict()
        self.assertEqual(data['amount'], 50.00)
        self.assertEqual(data['description'], "Test")
        self.assertEqual(data['date'], "2025-10-20")
    
    def test_from_dict(self) -> None:
        """Test creation from dictionary."""
        data = {'amount': 100.00, 'description': 'Monthly rent', 'date': '2025-10-01'}
        expense = Expense.from_dict(data)
        self.assertEqual(expense.amount, 100.00)
        self.assertEqual(expense.description, 'Monthly rent')
        self.assertEqual(expense.date, '2025-10-01')
    
    def test_repr(self) -> None:
        """Test string representation."""
        expense = Expense(50.00, "Test", "2025-10-20")
        repr_str = repr(expense)
        self.assertIn("50.00", repr_str)
        self.assertIn("Test", repr_str)


class TestBudgetCategory(unittest.TestCase):
    """Test cases for BudgetCategory class."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        self.category = BudgetCategory("groceries")
    
    def test_init(self) -> None:
        """Test category initialization."""
        self.assertEqual(self.category.name, "groceries")
        self.assertEqual(self.category.expenses, [])
        self.assertIsInstance(self.category.expenses, list)
    
    def test_add_expense_valid(self) -> None:
        """Test adding a valid expense."""
        self.category.add_expense(50.00, "Weekly shopping", "2025-10-20")
        self.assertEqual(len(self.category.expenses), 1)
        self.assertIsInstance(self.category.expenses[0], Expense)
        self.assertEqual(self.category.expenses[0].amount, 50.00)
        self.assertEqual(self.category.expenses[0].description, "Weekly shopping")
    
    def test_add_expense_negative(self) -> None:
        """Test that negative expenses raise ValueError."""
        with self.assertRaises(ValueError):
            self.category.add_expense(-10.00, "Invalid", "2025-10-20")
    
    def test_add_expense_zero(self) -> None:
        """Test that zero expenses raise ValueError."""
        with self.assertRaises(ValueError):
            self.category.add_expense(0, "Invalid", "2025-10-20")
    
    def test_total_expenses_empty(self) -> None:
        """Test total expenses with no expenses."""
        self.assertEqual(self.category.total_expenses(), 0.0)
    
    def test_total_expenses_single(self) -> None:
        """Test total expenses with single expense."""
        self.category.add_expense(100.00, "Test", "2025-10-20")
        self.assertEqual(self.category.total_expenses(), 100.00)
    
    def test_total_expenses_multiple(self) -> None:
        """Test total expenses with multiple expenses."""
        self.category.add_expense(50.00, "Expense 1", "2025-10-20")
        self.category.add_expense(75.50, "Expense 2", "2025-10-21")
        self.category.add_expense(24.50, "Expense 3", "2025-10-22")
        self.assertEqual(self.category.total_expenses(), 150.00)
    
    def test_to_dict(self) -> None:
        """Test conversion to dictionary."""
        self.category.add_expense(50.00, "Test", "2025-10-20")
        data = self.category.to_dict()
        self.assertEqual(data['name'], "groceries")
        self.assertEqual(len(data['expenses']), 1)
        self.assertIsInstance(data['expenses'][0], dict)
    
    def test_from_dict(self) -> None:
        """Test creation from dictionary."""
        data = {
            'name': 'rent',
            'expenses': [
                {'amount': 1200.00, 'description': 'Monthly rent', 'date': '2025-10-01'}
            ]
        }
        category = BudgetCategory.from_dict(data)
        self.assertEqual(category.name, 'rent')
        self.assertEqual(len(category.expenses), 1)
        self.assertIsInstance(category.expenses[0], Expense)
        self.assertEqual(category.total_expenses(), 1200.00)


class TestBudgetManager(unittest.TestCase):
    """Test cases for BudgetManager class."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        # Use a test-specific data file
        BudgetManager.DATA_FILE = 'test_budget_data.json'
        self.manager = BudgetManager()
        # Clear any existing test data
        self.manager.income = 0.0
        self.manager.savings_goal = 0.0
        self.manager.categories = {}
    
    def tearDown(self) -> None:
        """Clean up after tests."""
        if os.path.exists('test_budget_data.json'):
            os.remove('test_budget_data.json')
    
    def test_init(self) -> None:
        """Test manager initialization."""
        self.assertEqual(self.manager.income, 0.0)
        self.assertEqual(self.manager.savings_goal, 0.0)
        self.assertEqual(self.manager.categories, {})
    
    def test_set_income_valid(self) -> None:
        """Test setting valid income."""
        self.manager.set_income(5000.00)
        self.assertEqual(self.manager.income, 5000.00)
    
    def test_set_income_zero(self) -> None:
        """Test setting income to zero."""
        self.manager.set_income(0)
        self.assertEqual(self.manager.income, 0)
    
    def test_set_income_negative(self) -> None:
        """Test that negative income raises ValueError."""
        with self.assertRaises(ValueError):
            self.manager.set_income(-1000.00)
    
    def test_set_savings_goal_valid(self) -> None:
        """Test setting valid savings goal."""
        self.manager.set_savings_goal(1000.00)
        self.assertEqual(self.manager.savings_goal, 1000.00)
    
    def test_set_savings_goal_negative(self) -> None:
        """Test that negative savings goal raises ValueError."""
        with self.assertRaises(ValueError):
            self.manager.set_savings_goal(-500.00)
    
    def test_add_expense_new_category(self) -> None:
        """Test adding expense to new category."""
        self.manager.add_expense("groceries", 50.00, "Weekly shopping", "2025-10-20")
        self.assertIn("groceries", self.manager.categories)
        self.assertEqual(self.manager.categories["groceries"].total_expenses(), 50.00)
        self.assertIsInstance(self.manager.categories["groceries"].expenses[0], Expense)
    
    def test_add_expense_existing_category(self) -> None:
        """Test adding expense to existing category."""
        self.manager.add_expense("groceries", 50.00, "Shopping 1", "2025-10-20")
        self.manager.add_expense("groceries", 30.00, "Shopping 2", "2025-10-21")
        self.assertEqual(self.manager.categories["groceries"].total_expenses(), 80.00)
        self.assertEqual(len(self.manager.categories["groceries"].expenses), 2)
    
    def test_add_expense_case_insensitive(self) -> None:
        """Test that category names are case-insensitive."""
        self.manager.add_expense("Groceries", 50.00, "Test 1", "2025-10-20")
        self.manager.add_expense("GROCERIES", 30.00, "Test 2", "2025-10-21")
        self.assertIn("groceries", self.manager.categories)
        self.assertEqual(self.manager.categories["groceries"].total_expenses(), 80.00)
    
    def test_total_expenses_empty(self) -> None:
        """Test total expenses with no expenses."""
        self.assertEqual(self.manager.total_expenses(), 0.0)
    
    def test_total_expenses_single_category(self) -> None:
        """Test total expenses with single category."""
        self.manager.add_expense("rent", 1200.00, "Monthly rent", "2025-10-01")
        self.assertEqual(self.manager.total_expenses(), 1200.00)
    
    def test_total_expenses_multiple_categories(self) -> None:
        """Test total expenses across multiple categories."""
        self.manager.add_expense("rent", 1200.00, "Rent", "2025-10-01")
        self.manager.add_expense("groceries", 300.00, "Food", "2025-10-15")
        self.manager.add_expense("utilities", 150.00, "Electric", "2025-10-10")
        self.assertEqual(self.manager.total_expenses(), 1650.00)
    
    def test_progress_toward_goal_on_track(self) -> None:
        """Test progress calculation when on track."""
        self.manager.set_income(5000.00)
        self.manager.set_savings_goal(1000.00)
        self.manager.add_expense("rent", 1200.00, "Rent", "2025-10-01")
        self.manager.add_expense("groceries", 300.00, "Food", "2025-10-15")
        
        progress = self.manager.progress_toward_goal()
        self.assertTrue(progress['on_track'])
        self.assertEqual(progress['current_savings'], 3500.00)
        self.assertEqual(progress['needed'], 0)
    
    def test_progress_toward_goal_not_on_track(self) -> None:
        """Test progress calculation when not on track."""
        self.manager.set_income(3000.00)
        self.manager.set_savings_goal(1000.00)
        self.manager.add_expense("rent", 1200.00, "Rent", "2025-10-01")
        self.manager.add_expense("groceries", 1000.00, "Food", "2025-10-15")
        
        progress = self.manager.progress_toward_goal()
        self.assertFalse(progress['on_track'])
        self.assertEqual(progress['current_savings'], 800.00)
        self.assertEqual(progress['needed'], 200.00)
    
    def test_save_and_load_data(self) -> None:
        """Test saving and loading data."""
        # Set up data
        self.manager.set_income(5000.00)
        self.manager.set_savings_goal(1000.00)
        self.manager.add_expense("rent", 1200.00, "Monthly rent", "2025-10-01")
        self.manager.add_expense("groceries", 300.00, "Food", "2025-10-15")
        
        # Save data
        self.manager.save_data()
        
        # Create new manager and load data
        new_manager = BudgetManager()
        self.assertEqual(new_manager.income, 5000.00)
        self.assertEqual(new_manager.savings_goal, 1000.00)
        self.assertEqual(new_manager.total_expenses(), 1500.00)
        
        # Verify expenses are Expense objects
        for category in new_manager.categories.values():
            for expense in category.expenses:
                self.assertIsInstance(expense, Expense)


class TestInputValidation(unittest.TestCase):
    """Test cases for input validation functions."""
    
    @patch('builtins.input', side_effect=['50.00'])
    def test_get_valid_float_valid(self, mock_input: Any) -> None:
        """Test getting valid float input."""
        result = get_valid_float("Enter amount: ")
        self.assertEqual(result, 50.00)
    
    @patch('builtins.input', side_effect=['abc', '-10', '0', '50.00'])
    def test_get_valid_float_with_retries(self, mock_input: Any) -> None:
        """Test getting valid float with invalid inputs first."""
        result = get_valid_float("Enter amount: ")
        self.assertEqual(result, 50.00)
        self.assertEqual(mock_input.call_count, 4)
    
    @patch('builtins.input', side_effect=['0'])
    def test_get_valid_float_allow_zero(self, mock_input: Any) -> None:
        """Test getting valid float allowing zero."""
        result = get_valid_float("Enter amount: ", allow_zero=True)
        self.assertEqual(result, 0.0)
    
    @patch('builtins.input', side_effect=['2025-10-25'])
    def test_get_valid_date_valid(self, mock_input: Any) -> None:
        """Test getting valid date input."""
        result = get_valid_date("Enter date: ")
        self.assertEqual(result, '2025-10-25')
    
    @patch('builtins.input', side_effect=['10/25/2025', '2025-13-01', '2025-02-30', '2025-10-25'])
    def test_get_valid_date_with_retries(self, mock_input: Any) -> None:
        """Test getting valid date with invalid inputs first."""
        result = get_valid_date("Enter date: ")
        self.assertEqual(result, '2025-10-25')
        self.assertEqual(mock_input.call_count, 4)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        BudgetManager.DATA_FILE = 'test_budget_integration.json'
        self.manager = BudgetManager()
        self.manager.income = 0.0
        self.manager.savings_goal = 0.0
        self.manager.categories = {}
    
    def tearDown(self) -> None:
        """Clean up after tests."""
        if os.path.exists('test_budget_integration.json'):
            os.remove('test_budget_integration.json')
    
    def test_complete_budget_workflow(self) -> None:
        """Test a complete budget workflow."""
        # Set income
        self.manager.set_income(5000.00)
        
        # Set savings goal
        self.manager.set_savings_goal(1000.00)
        
        # Add various expenses
        self.manager.add_expense("rent", 1200.00, "Monthly rent", "2025-10-01")
        self.manager.add_expense("groceries", 300.00, "Weekly shopping", "2025-10-15")
        self.manager.add_expense("utilities", 150.00, "Electric bill", "2025-10-10")
        self.manager.add_expense("entertainment", 100.00, "Movies", "2025-10-20")
        
        # Check total expenses
        self.assertEqual(self.manager.total_expenses(), 1750.00)
        
        # Check savings progress
        progress = self.manager.progress_toward_goal()
        self.assertTrue(progress['on_track'])
        self.assertEqual(progress['current_savings'], 3250.00)
        
        # Save and reload
        self.manager.save_data()
        new_manager = BudgetManager()
        
        # Verify data persisted
        self.assertEqual(new_manager.income, 5000.00)
        self.assertEqual(new_manager.savings_goal, 1000.00)
        self.assertEqual(new_manager.total_expenses(), 1750.00)


def run_tests() -> unittest.TestResult:
    """
    Run all tests with detailed output.
    
    Returns:
        Test result object
    """
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestExpense))
    suite.addTests(loader.loadTestsFromTestCase(TestBudgetCategory))
    suite.addTests(loader.loadTestsFromTestCase(TestBudgetManager))
    suite.addTests(loader.loadTestsFromTestCase(TestInputValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result


if __name__ == "__main__":
    # Run the tests
    result = run_tests()
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)