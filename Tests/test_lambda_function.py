import unittest
from unittest.mock import MagicMock
from ExtractText.Models import block
from ExtractText.Services import AWSTextractService, DBServices, EmailNotificationService, S3Services


class TestFunction(unittest.TestCase):
    def test_to_upper_function(self):
        # Arrange
        function = Function()
        context = MagicMock()
        input_string = "hello world"
        
        # Act
        result = function.function_handler(input_string, context)
        
        # Assert
        self.assertEqual(result, "HELLO WORLD")

if __name__ == '__main__':
    unittest.main()

