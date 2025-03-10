from flask import Flask, render_template, request, jsonify
from calculator import Calculator

app = Flask(__name__)
calculator = Calculator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        expression = data.get('expression', '')
        scientific_mode = data.get('scientific_mode', False)
        
        calculator.is_scientific_mode = scientific_mode
        result = calculator.evaluate(expression)
        
        calculator.add_to_history(expression, result)
        
        return jsonify({
            'status': 'success',
            'result': result
        })
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/toggle_angle_unit', methods=['POST'])
def toggle_angle_unit():
    unit = calculator.toggle_angle_unit()
    return jsonify({'unit': unit})

@app.route('/memory_store', methods=['POST'])
def memory_store():
    data = request.get_json()
    value = data.get('value')
    message = calculator.store_memory(float(value))
    return jsonify({'message': message})

@app.route('/memory_recall', methods=['GET'])
def memory_recall():
    value = calculator.recall_memory()
    return jsonify({'value': str(value)})

@app.route('/memory_clear', methods=['POST'])
def memory_clear():
    message = calculator.clear_memory()
    return jsonify({'message': message})

@app.route('/get_history', methods=['GET'])
def get_history():
    history = calculator.get_history()
    return jsonify({'history': history})

if __name__ == '__main__':
    app.run(debug=True)