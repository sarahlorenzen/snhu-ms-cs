"""
Unit tests for calculator.py
Tests all arithmetic operations including edge cases.
"""

import unittest
from calculator import add, subtract, multiply, divide, perform_calculation


class TestAddition(unittest.TestCase):
    """Test cases for addition operation."""
    
    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        self.assertEqual(add(5, 3), 8)
        self.assertEqual(add(100, 50), 150)
    
    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        self.assertEqual(add(-5, -3), -8)
        self.assertEqual(add(-10, -20), -30)
    
    def test_add_mixed_signs(self):
        """Test adding positive and negative numbers."""
        self.assertEqual(add(10, -5), 5)
        self.assertEqual(add(-10, 5), -5)
    
    def test_add_with_zero(self):
        """Test adding zero (identity element)."""
        self.assertEqual(add(0, 5), 5)
        self.assertEqual(add(5, 0), 5)
        self.assertEqual(add(0, 0), 0)
    
    def test_add_decimals(self):
        """Test adding decimal numbers."""
        self.assertAlmostEqual(add(3.5, 2.7), 6.2, places=1)
        self.assertAlmostEqual(add(0.1, 0.2), 0.3, places=1)


class TestSubtraction(unittest.TestCase):
    """Test cases for subtraction operation."""
    
    def test_subtract_positive_numbers(self):
        """Test subtracting positive numbers."""
        self.assertEqual(subtract(10, 5), 5)
        self.assertEqual(subtract(100, 30), 70)
    
    def test_subtract_negative_numbers(self):
        """Test subtracting negative numbers."""
        self.assertEqual(subtract(-5, -3), -2)
        self.assertEqual(subtract(-10, -20), 10)
    
    def test_subtract_mixed_signs(self):
        """Test subtracting with mixed signs."""
        self.assertEqual(subtract(10, -5), 15)
        self.assertEqual(subtract(-10, 5), -15)
    
    def test_subtract_with_zero(self):
        """Test subtracting zero."""
        self.assertEqual(subtract(5, 0), 5)
        self.assertEqual(subtract(0, 5), -5)
        self.assertEqual(subtract(0, 0), 0)
    
    def test_subtract_decimals(self):
        """Test subtracting decimal numbers."""
        self.assertAlmostEqual(subtract(5.5, 2.3), 3.2, places=1)
        self.assertAlmostEqual(subtract(10.0, 3.7), 6.3, places=1)


class TestMultiplication(unittest.TestCase):
    """Test cases for multiplication operation."""
    
    def test_multiply_positive_numbers(self):
        """Test multiplying positive numbers."""
        self.assertEqual(multiply(5, 3), 15)
        self.assertEqual(multiply(10, 10), 100)
    
    def test_multiply_negative_numbers(self):
        """Test multiplying negative numbers."""
        self.assertEqual(multiply(-5, -3), 15)
        self.assertEqual(multiply(-10, -2), 20)
    
    def test_multiply_mixed_signs(self):
        """Test multiplying with mixed signs."""
        self.assertEqual(multiply(5, -3), -15)
        self.assertEqual(multiply(-5, 3), -15)
    
    def test_multiply_with_zero(self):
        """Test multiplying by zero (zero property)."""
        self.assertEqual(multiply(0, 5), 0)
        self.assertEqual(multiply(5, 0), 0)
        self.assertEqual(multiply(0, 0), 0)
    
    def test_multiply_with_one(self):
        """Test multiplying by one (identity element)."""
        self.assertEqual(multiply(1, 5), 5)
        self.assertEqual(multiply(5, 1), 5)
    
    def test_multiply_decimals(self):
        """Test multiplying decimal numbers."""
        self.assertAlmostEqual(multiply(2.5, 4), 10.0, places=1)
        self.assertAlmostEqual(multiply(3.3, 3), 9.9, places=1)


class TestDivision(unittest.TestCase):
    """Test cases for division operation."""
    
    def test_divide_positive_numbers(self):
        """Test dividing positive numbers."""
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(100, 4), 25)
    
    def test_divide_negative_numbers(self):
        """Test dividing negative numbers."""
        self.assertEqual(divide(-10, -2), 5)
        self.assertEqual(divide(-20, -4), 5)
    
    def test_divide_mixed_signs(self):
        """Test dividing with mixed signs."""
        self.assertEqual(divide(10, -2), -5)
        self.assertEqual(divide(-10, 2), -5)
    
    def test_divide_by_one(self):
        """Test dividing by one (identity)."""
        self.assertEqual(divide(5, 1), 5)
        self.assertEqual(divide(100, 1), 100)
    
    def test_divide_zero_by_number(self):
        """Test dividing zero by a number."""
        self.assertEqual(divide(0, 5), 0)
        self.assertEqual(divide(0, 100), 0)
    
    def test_divide_decimals(self):
        """Test dividing decimal numbers."""
        self.assertAlmostEqual(divide(7.5, 2.5), 3.0, places=1)
        self.assertAlmostEqual(divide(10.0, 4.0), 2.5, places=1)
    
    # EDGE CASE: Division by zero
    def test_divide_by_zero(self):
        """Test dividing by zero returns None (edge case)."""
        self.assertIsNone(divide(10, 0))
        self.assertIsNone(divide(100, 0))
        self.assertIsNone(divide(-5, 0))
        self.assertIsNone(divide(0, 0))


class TestPerformCalculation(unittest.TestCase):
    """Test cases for the perform_calculation function."""
    
    def test_perform_addition(self):
        """Test perform_calculation with addition."""
        result, symbol = perform_calculation(1, 5, 3)
        self.assertEqual(result, 8)
        self.assertEqual(symbol, "+")
    
    def test_perform_subtraction(self):
        """Test perform_calculation with subtraction."""
        result, symbol = perform_calculation(2, 10, 4)
        self.assertEqual(result, 6)
        self.assertEqual(symbol, "-")
    
    def test_perform_multiplication(self):
        """Test perform_calculation with multiplication."""
        result, symbol = perform_calculation(3, 6, 7)
        self.assertEqual(result, 42)
        self.assertEqual(symbol, "×")
    
    def test_perform_division(self):
        """Test perform_calculation with division."""
        result, symbol = perform_calculation(4, 20, 4)
        self.assertEqual(result, 5)
        self.assertEqual(symbol, "÷")
    
    def test_perform_division_by_zero(self):
        """Test perform_calculation handles division by zero."""
        result, symbol = perform_calculation(4, 10, 0)
        self.assertIsNone(result)
        self.assertEqual(symbol, "÷")


class TestEdgeCases(unittest.TestCase):
    """Additional edge case tests."""
    
    def test_very_large_numbers(self):
        """Test operations with very large numbers."""
        self.assertEqual(add(1e10, 1e10), 2e10)
        self.assertEqual(multiply(1e6, 1e6), 1e12)
    
    def test_very_small_numbers(self):
        """Test operations with very small numbers."""
        self.assertAlmostEqual(add(0.0001, 0.0002), 0.0003, places=4)
        self.assertAlmostEqual(multiply(0.1, 0.1), 0.01, places=2)
    
    def test_negative_zero(self):
        """Test operations with negative zero."""
        self.assertEqual(add(0, -0), 0)
        self.assertEqual(subtract(0, -0), 0)


def run_tests_with_verbose_output():
    """Run tests with detailed output."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAddition))
    suite.addTests(loader.loadTestsFromTestCase(TestSubtraction))
    suite.addTests(loader.loadTestsFromTestCase(TestMultiplication))
    suite.addTests(loader.loadTestsFromTestCase(TestDivision))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformCalculation))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Run with verbose output
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
    # Run tests with verbose output
    run_tests_with_verbose_output()
