from sympy import symbols, Function, Eq, dsolve, Derivative, simplify, latex
from sympy.parsing.sympy_parser import parse_expr
import re

def solve_step_by_step(equations, variables, initial_conditions=None):
    steps = []

    x = symbols(variables[0])
    y_func = Function(variables[1])
    y = y_func(x)

    local_dict = {
        variables[0]: x,
        variables[1]: y_func,
        f'{variables[1]}({variables[0]})': y,
    }

    def preprocess_equation(eq):
        eq = re.sub(rf'd{variables[1]}/d{variables[0]}', f'Derivative({variables[1]}({variables[0]}), {variables[0]})', eq)
        eq = re.sub(rf'\b{variables[1]}\b(?!\()', f'{variables[1]}({variables[0]})', eq)
        return eq

    equation_str = preprocess_equation(equations[0])
    lhs_str, rhs_str = map(str.strip, equation_str.split('='))
    lhs = parse_expr(lhs_str, local_dict=local_dict)
    rhs = parse_expr(rhs_str, local_dict=local_dict)
    eq = Eq(lhs, rhs)

    steps.append({
        "title": "Interpretación de la ecuación",
        "description": f"Se reescribe como: {str(eq)}",
        "latex_description": f"\\text{{Se reescribe como: }} {latex(eq)}"
    })

    sol = dsolve(eq, y)
    steps.append({
        "title": "Solución general",
        "description": f"y(x) = {str(sol.rhs)}",
        "latex_description": f"y(x) = {latex(sol.rhs)}"
    })

    if initial_conditions:
        x0 = initial_conditions.get("x0")
        y0 = initial_conditions.get("y0")
        ics = {y.subs(x, x0): y0}
        particular_solution = dsolve(eq, y, ics=ics)
        simplified = simplify(particular_solution.rhs)

        steps.append({
            "title": "Aplicando condiciones iniciales",
            "description": f"Se usa la condición y({x0}) = {y0} para encontrar C1",
            "latex_description": f"\\text{{Se usa la condición }} y({x0}) = {y0} \\text{{ para encontrar }} C_1"
        })

        steps.append({
            "title": "Solución particular",
            "description": f"y(x) = {str(simplified)}",
            "latex_description": f"y(x) = {latex(simplified)}"
        })

    return steps
