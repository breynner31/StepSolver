from sympy import symbols, Function, Eq, dsolve, Derivative, simplify, latex, sympify
import re

def solve_step_by_step(equations, variables, initial_conditions=None):
    steps = []

    # Definir las variables
    x = symbols(variables[0])
    y_func = Function(variables[1])
    y = y_func(x)

    # Diccionario local para mapear las variables
    local_dict = {
        variables[0]: x,
        variables[1]: y_func,
        f'{variables[1]}({variables[0]}': y,
    }

    def preprocess_equation(eq):
        # Reemplaza diff por Derivative, para hacerlo compatible con sympy
        eq = eq.replace('dy/dx', 'Derivative(y(x), x)')
        eq = re.sub(rf"\b{variables[1]}''", f'Derivative({variables[1]}({variables[0]}), {variables[0]}, 2)', eq)
        eq = re.sub(rf"\b{variables[1]}'", f'Derivative({variables[1]}({variables[0]}), {variables[0]})', eq)

        # Reemplaza y por y(x), excepto si ya está en forma de función como y(x)
        eq = re.sub(rf"\b{variables[1]}\b(?!\s*\()", f'{variables[1]}({variables[0]})', eq)

        return eq

    try:
        # Preprocesamiento de la ecuación
        equation_str = preprocess_equation(equations[0])
        lhs_str, rhs_str = map(str.strip, equation_str.split('='))

        print(f"Ecuación procesada: {equation_str}")
        print(f"Lado izquierdo: {lhs_str}, Lado derecho: {rhs_str}")

        # Usar sympify para convertir la ecuación a un objeto sympy
        lhs = sympify(lhs_str)
        rhs = sympify(rhs_str)
        eq = Eq(lhs, rhs)

        steps.append({
            "title": "Interpretación de la ecuación",
            "description": f"Se reescribe como: {str(eq)}",
            "latex_description": f"\\text{{Se reescribe como: }} {latex(eq)}"
        })

        # Resolver la ecuación
        sol = dsolve(eq, y)
        steps.append({
            "title": "Solución general",
            "description": f"y(x) = {str(sol.rhs)}",
            "latex_description": f"y(x) = {latex(sol.rhs)}"
        })

        # Si hay condiciones iniciales
        if initial_conditions:
            x0 = initial_conditions.get("x0")
            y0 = initial_conditions.get("y0")
            if x0 is not None and y0 is not None:
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
            else:
                raise ValueError("Se requieren condiciones iniciales válidas.")

    except Exception as e:
        steps.append({
            "title": "Error",
            "description": f"Ocurrió un error al procesar la ecuación: {str(e)}",
            "latex_description": f"\\text{{Error al procesar la ecuación: }} {str(e)}"
        })

    return steps
