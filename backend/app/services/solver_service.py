from sympy import symbols, Function, Eq, dsolve, Derivative, simplify, latex, sympify
import re
import threading
import time

def timeout_wrapper(func, timeout_seconds):
    """Wrapper simple para timeout que funciona en Windows"""
    result = [None]
    exception = [None]
    
    def target():
        try:
            result[0] = func()
        except Exception as e:
            exception[0] = e
    
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()
    thread.join(timeout=timeout_seconds)
    
    if thread.is_alive():
        raise TimeoutError("La operación tardó demasiado tiempo")
    
    if exception[0]:
        raise exception[0]
    
    return result[0]

def solve_step_by_step(equations, variables, initial_conditions=None, socketio=None):
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
        eq = eq.replace('^', '**')

        for order in range(10, 0, -1):
            apostrophes = "'" * order
            pattern = rf"\b{variables[1]}{re.escape(apostrophes)}\b"
            replacement = f"Derivative({variables[1]}({variables[0]}), {variables[0]}, {order})"
            eq = re.sub(pattern, replacement, eq)

        eq = re.sub(rf"\b{variables[1]}'\b", f'Derivative({variables[1]}({variables[0]}), {variables[0]})', eq)

        eq = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', eq)

        eq = re.sub(rf"\b{variables[1]}\b(?!\()", f'{variables[1]}({variables[0]})', eq)

        return eq

    try:
        # Progreso: Procesando ecuación
        if socketio:
            socketio.emit('progress', {
                'step': 1,
                'total': 4,
                'message': 'Procesando y validando la ecuación...',
                'percentage': 30
            })

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

        # Detectar el orden de la ecuación
        max_order = 0
        for term in eq.lhs.args:
            if isinstance(term, Derivative):
                max_order = max(max_order, term.args[2] if len(term.args) > 2 else 1)
        
        steps.append({
            "title": "Análisis de la ecuación",
            "description": f"Ecuación diferencial de orden {max_order}",
            "latex_description": f"\\text{{Ecuación diferencial de orden }} {max_order}"
        })

        # Progreso: Iniciando resolución
        if socketio:
            socketio.emit('progress', {
                'step': 2,
                'total': 4,
                'message': f'Resolviendo ecuación diferencial de orden {max_order}...',
                'percentage': 50
            })

        # Intentar resolver con timeout
        try:
            def solve_equation():
                print(f"[INFO] Intentando resolver ecuación de orden {max_order}...")
                return dsolve(eq, y)
            
            sol = timeout_wrapper(solve_equation, 30)  # 30 segundos de timeout
            print(f"[INFO] Ecuación resuelta exitosamente")
            
            steps.append({
                "title": "Solución general",
                "description": f"y(x) = {str(sol.rhs)}",
                "latex_description": f"y(x) = {latex(sol.rhs)}"
            })

            # Progreso: Ecuación resuelta
            if socketio:
                socketio.emit('progress', {
                    'step': 2,
                    'total': 4,
                    'message': 'Ecuación resuelta exitosamente',
                    'percentage': 60
                })
        except TimeoutError:
            print(f"[WARNING] Timeout al resolver ecuación de orden {max_order}")
            steps.append({
                "title": "Solución general",
                "description": f"La ecuación de orden {max_order} es demasiado compleja para resolver analíticamente en tiempo razonable. Se recomienda usar métodos numéricos.",
                "latex_description": f"\\text{{La ecuación de orden }} {max_order} \\text{{ es demasiado compleja para resolver analíticamente}}"
            })
            return steps  # Retornar sin intentar condiciones iniciales
        except Exception as e:
            print(f"[ERROR] Error al resolver: {str(e)}")
            steps.append({
                "title": "Error en resolución",
                "description": f"No se pudo resolver la ecuación: {str(e)}",
                "latex_description": f"\\text{{No se pudo resolver la ecuación: }} {str(e)}"
            })
            return steps

        if initial_conditions:
            x0 = initial_conditions.get("x0")
            y0 = initial_conditions.get("y0")
            dy0 = initial_conditions.get("dy0")
            d2y0 = initial_conditions.get("d2y0")
            d3y0 = initial_conditions.get("d3y0")
            d4y0 = initial_conditions.get("d4y0")
            d5y0 = initial_conditions.get("d5y0")
            d6y0 = initial_conditions.get("d6y0")
            d7y0 = initial_conditions.get("d7y0")
            d8y0 = initial_conditions.get("d8y0")
            d9y0 = initial_conditions.get("d9y0")
            d10y0 = initial_conditions.get("d10y0")

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
                if d2y0 is not None:
                    ics[Derivative(y, x, 2).subs(x, x0)] = d2y0
                    steps.append({
                        "title": "Condición inicial aplicada",
                        "description": f"Se usa la condición y''({x0}) = {d2y0}",
                        "latex_description": f"\\text{{Se usa la condición }} y''({x0}) = {d2y0}"
                    })
                if d3y0 is not None:
                    ics[Derivative(y, x, 3).subs(x, x0)] = d3y0
                    steps.append({
                        "title": "Condición inicial aplicada",
                        "description": f"Se usa la condición y^{{(3)}}({x0}) = {d3y0}",
                        "latex_description": f"\\text{{Se usa la condición }} y^{{(3)}}({x0}) = {d3y0}"
                    })
                if d4y0 is not None:
                    ics[Derivative(y, x, 4).subs(x, x0)] = d4y0
                    steps.append({
                        "title": "Condición inicial aplicada",
                        "description": f"Se usa la condición y^{{(4)}}({x0}) = {d4y0}",
                        "latex_description": f"\\text{{Se usa la condición }} y^{{(4)}}({x0}) = {d4y0}"
                    })
                if d5y0 is not None:
                    ics[Derivative(y, x, 5).subs(x, x0)] = d5y0
                    steps.append({
                        "title": "Condición inicial aplicada",
                        "description": f"Se usa la condición y^{{(5)}}({x0}) = {d5y0}",
                        "latex_description": f"\\text{{Se usa la condición }} y^{{(5)}}({x0}) = {d5y0}"
                    })
                if d6y0 is not None:
                    ics[Derivative(y, x, 6).subs(x, x0)] = d6y0
                    steps.append({
                        "title": "Condición inicial aplicada",
                        "description": f"Se usa la condición y^{{(6)}}({x0}) = {d6y0}",
                        "latex_description": f"\\text{{Se usa la condición }} y^{{(6)}}({x0}) = {d6y0}"
                    })
                if d7y0 is not None:
                    ics[Derivative(y, x, 7).subs(x, x0)] = d7y0
                    steps.append({
                        "title": "Condición inicial aplicada",
                        "description": f"Se usa la condición y^{{(7)}}({x0}) = {d7y0}",
                        "latex_description": f"\\text{{Se usa la condición }} y^{{(7)}}({x0}) = {d7y0}"
                    })
                if d8y0 is not None:
                    ics[Derivative(y, x, 8).subs(x, x0)] = d8y0
                    steps.append({
                        "title": "Condición inicial aplicada",
                        "description": f"Se usa la condición y^{{(8)}}({x0}) = {d8y0}",
                        "latex_description": f"\\text{{Se usa la condición }} y^{{(8)}}({x0}) = {d8y0}"
                    })
                if d9y0 is not None:
                    ics[Derivative(y, x, 9).subs(x, x0)] = d9y0
                    steps.append({
                        "title": "Condición inicial aplicada",
                        "description": f"Se usa la condición y^{{(9)}}({x0}) = {d9y0}",
                        "latex_description": f"\\text{{Se usa la condición }} y^{{(9)}}({x0}) = {d9y0}"
                    })
                if d10y0 is not None:
                    ics[Derivative(y, x, 10).subs(x, x0)] = d10y0
                    steps.append({
                        "title": "Condición inicial aplicada",
                        "description": f"Se usa la condición y^{{(10)}}({x0}) = {d10y0}",
                        "latex_description": f"\\text{{Se usa la condición }} y^{{(10)}}({x0}) = {d10y0}"
                    })

            if ics:
                # Progreso: Aplicando condiciones iniciales
                if socketio:
                    socketio.emit('progress', {
                        'step': 2,
                        'total': 4,
                        'message': 'Aplicando condiciones iniciales...',
                        'percentage': 70
                    })

                try:
                    def apply_conditions():
                        print(f"[INFO] Aplicando condiciones iniciales...")
                        particular_solution = dsolve(eq, y, ics=ics)
                        return simplify(particular_solution.rhs)
                    
                    simplified = timeout_wrapper(apply_conditions, 20)  # 20 segundos adicionales
                    
                    # Verificar si la solución es demasiado compleja
                    if len(str(simplified)) > 200:  # Ajusta este número según necesites
                        steps.append({
                            "title": "Solución particular",
                            "description": "La solución particular es demasiado compleja para mostrarse",
                            "latex_description": "\\text{La solución particular es demasiado compleja para mostrarse}"
                        })
                    else:
                        steps.append({
                            "title": "Solución particular",
                            "description": f"y(x) = {str(simplified)}",
                            "latex_description": f"y(x) = {latex(simplified)}"
                        })
                    print(f"[INFO] Condiciones iniciales aplicadas exitosamente")
                except TimeoutError:
                    print(f"[WARNING] Timeout al aplicar condiciones iniciales")
                    steps.append({
                        "title": "Solución particular",
                        "description": "Las condiciones iniciales son demasiado complejas para resolver en tiempo razonable",
                        "latex_description": "\\text{Las condiciones iniciales son demasiado complejas para resolver en tiempo razonable}"
                    })
                except Exception as e:
                    print(f"[ERROR] Error al aplicar condiciones iniciales: {str(e)}")
                    steps.append({
                        "title": "Solución particular",
                        "description": f"No se pudo encontrar una solución particular: {str(e)}",
                        "latex_description": f"\\text{{No se pudo encontrar una solución particular: }} {str(e)}"
                    })

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        steps.append({
            "title": "Error",
            "description": f"Ocurrió un error al procesar la ecuación: {str(e)}",
            "latex_description": f"\\text{{Error al procesar la ecuación: }} {str(e)}"
        })

    return steps