import math
import cmath
from enum import Enum

class AngleUnit(Enum):
    DEGREES = 'degrees'
    RADIANS = 'radians'

class Calculator:
    def __init__(self):
        self.memory = 0
        self.history = []
        self.decimal_places = 2
        self.angle_unit = AngleUnit.DEGREES
        self.is_scientific_mode = False

    # Basic Operations
    def add(self, x, y):
        return complex(x) + complex(y)
    
    def subtract(self, x, y):
        return complex(x) - complex(y)
    
    def multiply(self, x, y):
        return complex(x) * complex(y)
    
    def divide(self, x, y):
        if y == 0:
            raise ValueError("Cannot divide by zero!")
        return complex(x) / complex(y)

    # Scientific Operations
    def sin(self, x):
        if self.angle_unit == AngleUnit.DEGREES:
            x = math.radians(x)
        return cmath.sin(complex(x))

    def cos(self, x):
        if self.angle_unit == AngleUnit.DEGREES:
            x = math.radians(x)
        return cmath.cos(complex(x))

    def tan(self, x):
        if self.angle_unit == AngleUnit.DEGREES:
            x = math.radians(x)
        return cmath.tan(complex(x))

    def log10(self, x):
        return cmath.log10(complex(x))

    def ln(self, x):
        return cmath.log(complex(x))

    def power(self, x, y):
        return pow(complex(x), complex(y))

    def square_root(self, x):
        return cmath.sqrt(complex(x))

    def factorial(self, n):
        if not float(n).is_integer() or float(n) < 0:
            raise ValueError("Factorial is only defined for non-negative integers")
        return math.factorial(int(n))

    def exp(self, x):
        return cmath.exp(complex(x))

    # Utility Functions
    def toggle_angle_unit(self):
        if self.angle_unit == AngleUnit.DEGREES:
            self.angle_unit = AngleUnit.RADIANS
        else:
            self.angle_unit = AngleUnit.DEGREES
        return self.angle_unit.value

    def toggle_scientific_mode(self):
        self.is_scientific_mode = not self.is_scientific_mode
        return self.is_scientific_mode

    def format_complex(self, num):
        if isinstance(num, (int, float)):
            return self.format_result(num)
        
        real = self.format_result(num.real)
        imag = self.format_result(num.imag)
        
        if num.imag == 0:
            return real
        elif num.real == 0:
            return f"{imag}i"
        else:
            sign = '+' if num.imag >= 0 else ''
            return f"{real}{sign}{imag}i"

    def format_result(self, result):
        return f"{result:.{self.decimal_places}f}"

    def add_to_history(self, expression, result):
        self.history.append(f"{expression} = {result}")
        if len(self.history) > 100:
            self.history.pop(0)

    def get_history(self, limit=10):
        return self.history[-limit:]

    def evaluate(self, expression):
        try:
            allowed_chars = set("0123456789+-*/(). sincotalgqrexp!")
            if not all(c in allowed_chars for c in expression.lower()):
                raise ValueError("Invalid characters in expression")
            
            expression = expression.lower()
            if 'sin(' in expression:
                result = self.sin(float(expression[4:-1]))
            elif 'cos(' in expression:
                result = self.cos(float(expression[4:-1]))
            elif 'tan(' in expression:
                result = self.tan(float(expression[4:-1]))
            elif 'log10(' in expression:
                result = self.log10(float(expression[6:-1]))
            elif 'ln(' in expression:
                result = self.ln(float(expression[3:-1]))
            elif 'sqrt(' in expression:
                result = self.square_root(float(expression[5:-1]))
            elif 'factorial(' in expression:
                result = self.factorial(float(expression[10:-1]))
            else:
                expression = expression.replace('i', 'j')
                result = eval(expression)

            if isinstance(result, (complex, int, float)):
                return self.format_complex(result)
            return str(result)
            
        except ZeroDivisionError:
            raise ValueError("Division by zero!")
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")

    def clear_memory(self):
        self.memory = 0
        return "Memory cleared"

    def store_memory(self, value):
        self.memory = value
        return f"Stored in memory: {self.format_complex(value)}"

    def recall_memory(self):
        return self.memory
    def clear_history(self):
        self.history = []
        return "History cleared"