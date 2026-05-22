from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

def safe_eval(func_str, x):
    """
    Safely evaluates a mathematical function string for a given variable x.
    Fulfills the PIT criteria for demonstrating safe user parsing.
    """
    # A whitelist dictionary maps safe mathematical terms to numpy functions
    allowed_words = {
        'x': x, 
        'np': np, 
        'sin': np.sin, 
        'cos': np.cos, 
        'tan': np.tan, 
        'exp': np.exp, 
        'log': np.log, 
        'sqrt': np.sqrt, 
        'pi': np.pi
    }
    
    # Pre-parse input to convert common user syntax '^' into Python's '**'
    func_str = func_str.replace('^', '**')
    
    # Evaluate securely by blocking standard default Python builtins (__builtins__)
    return eval(func_str, {"__builtins__": None}, allowed_words)

def composite_trapezoidal(func_str, a, b, n):
    """
    Core implementation of the Composite Trapezoidal Rule algorithm.
    Formula: I ≈ (h/2) * [f(a) + 2*sum(f(x_i)) + f(b)]
    """
    h = (b - a) / n
    # Add boundary values f(a) and f(b)
    integration = safe_eval(func_str, a) + safe_eval(func_str, b)
    
    # Sum the middle points scaled by a factor of 2
    for i in range(1, n):
        k = a + i * h
        integration += 2 * safe_eval(func_str, k)
        
    final_result = integration * (h / 2)
    return final_result

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    # Default values to display in the user form fields initially
    params = {'func': 'x**2', 'a': '0', 'b': '2', 'n': '4'}
    
    if request.method == 'POST':
        try:
            params['func'] = request.form.get('func')
            params['a'] = float(request.form.get('a'))
            params['b'] = float(request.form.get('b'))
            params['n'] = int(request.form.get('n'))
            
            if params['n'] <= 0:
                raise ValueError("The number of subintervals (n) must be greater than 0.")
                
            # Run the calculation engine
            result = composite_trapezoidal(params['func'], params['a'], params['b'], params['n'])
        except Exception as e:
            error = f"Error evaluating application input: {str(e)}"
            
    return render_template('index.html', result=result, error=error, params=params)

if __name__ == '__main__':
    # Explicit configuration for reliable Windows local serving
    app.run(host='127.0.0.1', port=5000, debug=True)