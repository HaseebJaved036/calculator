let expression = document.getElementById('expression');
let result = document.getElementById('result');
let isScientificMode = false;
let isRadianMode = false;

function toggleMode() {
    isScientificMode = !isScientificMode;
    document.querySelector('.calculator').classList.toggle('scientific-mode');
    document.querySelector('.scientific').classList.toggle('visible');
    document.getElementById('modeToggle').textContent = 
        isScientificMode ? 'Basic Mode' : 'Scientific Mode';
}

function toggleAngleUnit() {
    isRadianMode = !isRadianMode;
    document.getElementById('angleUnitToggle').textContent = 
        isRadianMode ? 'RAD' : 'DEG';
    fetch('/toggle_angle_unit', { method: 'POST' });
}

function appendFunction(func) {
    expression.value += func;
}

function memoryStore() {
    const result = document.getElementById('result').textContent;
    fetch('/memory_store', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ value: result })
    });
}

function memoryRecall() {
    fetch('/memory_recall')
        .then(response => response.json())
        .then(data => {
            expression.value += data.value;
        });
}

function memoryClear() {
    fetch('/memory_clear', { method: 'POST' });
}

function updateHistory() {
    fetch('/get_history')
        .then(response => response.json())
        .then(data => {
            const historyList = document.getElementById('history-list');
            historyList.innerHTML = data.history.map(item => 
                `<div>${item}</div>`
            ).join('');
        });
}

function appendToDisplay(value) {
    expression.value += value;
}

function clearDisplay() {
    expression.value = '';
    result.textContent = '';
}

function calculate() {
    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            expression: expression.value,
            scientific_mode: isScientificMode
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            document.getElementById('result').textContent = data.result;
            updateHistory();
        } else {
            document.getElementById('result').textContent = data.message;
        }
    })
    .catch(error => {
        document.getElementById('result').textContent = 'Error occurred';
        console.error('Error:', error);
    });
}

// Add keyboard support
document.addEventListener('keydown', (event) => {
    const key = event.key;
    
    if (key >= '0' && key <= '9' || '+-*/.()'.includes(key)) {
        appendToDisplay(key);
    } else if (key === 'Enter') {
        calculate();
    } else if (key === 'Escape') {
        clearDisplay();
    } else if (key === 'Backspace') {
        expression.value = expression.value.slice(0, -1);
    }
});
function backspace() {
    expression.value = expression.value.slice(0, -1);
}

function clearHistory() {
    fetch('/clear_history', { method: 'POST' })
        .then(() => {
            document.getElementById('history-list').innerHTML = '';
        });
}