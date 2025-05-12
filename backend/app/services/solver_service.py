from sympy import symbols, Function, Eq, dsolve, Derivative, simplify, latex, sympify
import re

def solve_step_by_step(equations, variables, initial_conditions=None):
    steps = []

    # Definir las variables
    x = symbols(variables[0])
    y_func = Function(variables[1])
    y = y_func(x)

    # Diccionario local para evaluar expresiones
    local_dict = {
        variables[0]: x,
        variables[1]: y_func,
        f'{variables[1]}({variables[0]})': y,
    }

    def preprocess_equation(eq):
        # Reemplazar potencias tipo x^2 por x**2
        eq = eq.replace('^', '**')

        # Reemplazar derivadas tipo y'' y y'
        eq = eq.replace('dy/dx', f'Derivative({variables[1]}({variables[0]}), {variables[0]})')
        eq = re.sub(rf"\b{variables[1]}'''", f'Derivative({variables[1]}({variables[0]}), {variables[0]}, 3)', eq)
        eq = re.sub(rf"\b{variables[1]}''", f'Derivative({variables[1]}({variables[0]}), {variables[0]}, 2)', eq)
        eq = re.sub(rf"\b{variables[1]}'", f'Derivative({variables[1]}({variables[0]}), {variables[0]})', eq)

        # Insertar * entre número y letra, como 3y → 3*y, 4x → 4*x
        eq = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', eq)

        # Asegurar que "y" se convierte en "y(x)" si no está ya como y(x)
        eq = re.sub(rf"\b{variables[1]}\b(?!\()", f'{variables[1]}({variables[0]})', eq)

        return eq

    try:
        # Limpiar comillas extra si existen
        raw_eq = equations[0].strip('"').strip("'")
        equation_str = preprocess_equation(raw_eq)

        print(f"[INFO] Ecuación procesada: {equation_str}")

        lhs_str, rhs_str = map(str.strip, equation_str.split('='))
        print(f"[INFO] Lado izquierdo: {lhs_str}, Lado derecho: {rhs_str}")

        lhs = sympify(lhs_str, locals=local_dict)
        rhs = sympify(rhs_str, locals=local_dict)
        eq = Eq(lhs, rhs)

        steps.append({
            "title": "Interpretación de la ecuación",
            "description": f"Se reescribe como: {str(eq)}",
            "latex_description": f"\\text{{Se reescribe como: }} {latex(eq)}"
        })

        # Resolver la ecuación general
        sol = dsolve(eq, y)
        steps.append({
            "title": "Solución general",
            "description": f"y(x) = {str(sol.rhs)}",
            "latex_description": f"y(x) = {latex(sol.rhs)}"
        })

        # Aplicar condiciones iniciales si existen
        if initial_conditions:
            x0 = initial_conditions.get("x0")
            y0 = initial_conditions.get("y0")
            dy0 = initial_conditions.get("dy0")

            ics = {}
            if x0 is not None:
                if y0 is not None:
                    ics[y.subs(x, x0)] = y0
                    steps.append({
                        "title": "Condición inicial aplicada",
                        "description": f"Se usa la condición y({x0}) = {y0}",
                        "latex_description": f"\\text{{Se usa la condición }} y({x0}) = {y0}"
                    })
                if dy0 is not None:
                    ics[Derivative(y, x).subs(x, x0)] = dy0
                    steps.append({
                        "title": "Condición inicial aplicada",
                        "description": f"Se usa la condición y'({x0}) = {dy0}",
                        "latex_description": f"\\text{{Se usa la condición }} y'({x0}) = {dy0}"
                    })

            # Resolver con condiciones iniciales si hay alguna
            if ics:
                particular_solution = dsolve(eq, y, ics=ics)
                simplified = simplify(particular_solution.rhs)

                steps.append({
                    "title": "Solución particular",
                    "description": f"y(x) = {str(simplified)}",
                    "latex_description": f"y(x) = {latex(simplified)}"
                })

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        steps.append({
            "title": "Error",
            "description": f"Ocurrió un error al procesar la ecuación: {str(e)}",
            "latex_description": f"\\text{{Error al procesar la ecuación: }} {str(e)}"
        })

    return steps
