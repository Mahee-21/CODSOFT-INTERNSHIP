function appendToDisplay(value) {
  const display = document.getElementById("display");
  display.value += value;
}

function clearDisplay() {
  document.getElementById("display").value = '';
}

function deleteLast() {
  const display = document.getElementById("display");
  display.value = display.value.slice(0, -1);
}

function calculate() {
  const display = document.getElementById("display");
  try {
    const expression = display.value.replace('%', '/100');
    const result = eval(expression);
    addToHistory(display.value, result);
    display.value = result;
  } catch (e) {
    display.value = 'Error';
  }
}

function addToHistory(expression, result) {
  const historyList = document.getElementById("historyList");
  const listItem = document.createElement("li");
  listItem.textContent = `${expression} = ${result}`;
  historyList.prepend(listItem); // adds newest on top
}
function clearHistory() {
  const historyList = document.getElementById("historyList");
  historyList.innerHTML = ''; // Clear all history items
}
