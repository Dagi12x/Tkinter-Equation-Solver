import tkinter as tk
from tkinter import messagebox
import re
import math

def extract_variable(equation):
    match = re.search(r'[a-zA-Z]', equation)
    if match:
        return match.group(0)
    return None

def solve_linear_equation(equation, variable):
    parts = equation.split('=')
    left_side = parts[0].strip()
    right_side = parts[1].strip()
    terms = re.findall(rf'[-+]?\s*\d*\s*{variable}|\d+', left_side)
    x_coefficient = 0
    constant = 0

    for term in terms:
        term = term.strip()
        if term.endswith(variable):
            if term == variable:
                x_coefficient += 1
            elif term[:-1] == '' or term[:-1] == '+':
                x_coefficient += 1 if term[0] != '-' else -1
            else:
                x_coefficient += int(term[:-1])
        else:
            constant += int(term)

    try:
        solution = (int(right_side) - constant) / x_coefficient
        return solution
    except ZeroDivisionError:
        return "No solution (division by zero)"

def solve_quadratic_equation(equation, variable):
    parts = equation.split('=')
    left_side = parts[0].strip()
    right_side = parts[1].strip()

    coefficients = re.findall(rf'([-+]?\s*\d*\s*{variable}?\^?\d*)', left_side)[:3]
    coefficients += ['0'] * (3 - len(coefficients))

    a, b, c = [0 if not coeff else coeff.strip() for coeff in coefficients]
    a = a.replace(f'{variable}^2', '').replace(variable, '')
    b = b.replace(variable, '')
    c = c.replace(variable, '')

    a = int(a) if a else 0
    b = int(b) if b else 0
    c = int(c) if c else 0

    discriminant = b**2 - 4*a*c

    if discriminant < 0:
        return None, None

    root1 = (-b + math.sqrt(discriminant)) / (2*a)
    root2 = (-b - math.sqrt(discriminant)) / (2*a)

    return root1, root2

def solve_equation():
    equation_type = equation_type_var.get()
    equation = equation_entry.get()

    variable = extract_variable(equation)
    if not variable:
        messagebox.showerror("Error", "No valid variable found in the equation.")
        return

    if equation_type == 'Linear':
        solution = solve_linear_equation(equation, variable)
        result_label.config(text=f"The solution for {variable} is: {solution}")
    elif equation_type == 'Quadratic':
        root1, root2 = solve_quadratic_equation(equation, variable)
        if root1 is None:
            result_label.config(text="No real roots")
        else:
            result_label.config(text=f"The roots are: {root1} and {root2}")
    else:
        messagebox.showerror("Error", "Invalid equation type")

def append_to_equation(symbol):
    current_text = equation_entry.get()
    equation_entry.delete(0, tk.END)
    equation_entry.insert(0, current_text + symbol)

# Create Tkinter window
root = tk.Tk()
root.title("Equation Solver")

# Set a fixed window size (width x height)
root.geometry("420x350")
root.resizable(False, False)  # Disable window resizing

# Main frame to hold all widgets
main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(expand=True, fill=tk.BOTH)

# Create and place the widgets
equation_label = tk.Label(main_frame, text="Enter Equation:", font=("Arial", 10))
equation_label.grid(row=0, column=0, sticky="w", pady=5)

equation_entry = tk.Entry(main_frame, width=50, font=("Arial", 10))
equation_entry.grid(row=0, column=1, pady=5)

equation_type_label = tk.Label(main_frame, text="Equation Type:", font=("Arial", 10))
equation_type_label.grid(row=1, column=0, sticky="w", pady=5)

equation_type_var = tk.StringVar()
equation_type_var.set("Linear")
equation_type_menu = tk.OptionMenu(main_frame, equation_type_var, "Linear", "Quadratic")
equation_type_menu.config(width=12, font=("Arial", 10))
equation_type_menu.grid(row=1, column=1, pady=5, sticky="w")

solve_button = tk.Button(main_frame, text="Solve", font=("Arial", 11), command=solve_equation)
solve_button.grid(row=2, column=0, columnspan=2, pady=15)

result_label = tk.Label(main_frame, text="", font=("Arial", 12), fg="blue")
result_label.grid(row=3, column=0, columnspan=2, pady=10)

# Run Tkinter event loop
root.mainloop()
