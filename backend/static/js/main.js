// ensure DOM is ready before loading tasks
document.addEventListener('DOMContentLoaded', loadTask);

function addTask(taskText) {
  const taskList = document.getElementById('taskList');
  const newTask = document.createElement('li');

  // if called from loadTask, use the passed text; otherwise use the input field
  if (typeof taskText === 'string' && taskText.length) {
    newTask.textContent = taskText;
  } else {
    const input = document.getElementById('inpu-task');
    const value = input.value.trim();
    if (!value) return; // don't add empty tasks
    newTask.textContent = value;
    input.value = '';
  }

  taskList.appendChild(newTask);
  deleteTask(newTask);
  saveTask(); // update storage after adding
}

function deleteTask(newTask) {
  const deletebtn = document.createElement('button');
  deletebtn.textContent = "Delete";
  deletebtn.classList.add("delete-btn");
  newTask.appendChild(deletebtn);

  deletebtn.onclick = function () {
    newTask.remove();
    saveTask(); // update storage after deleting
  }
}

function saveTask() {
  const taskList = document.getElementById('taskList');
  const tasks = [];

  taskList.querySelectorAll('li').forEach(function (item) {
    // read only the text node (not the button)
    const first = item.childNodes[0];
    const text = first && first.textContent ? first.textContent.trim() : '';
    if (text) tasks.push(text);
  });

  localStorage.setItem('tasks', JSON.stringify(tasks)); // use key "tasks"
}

function loadTask() {
  const tasks = JSON.parse(localStorage.getItem('tasks')) || [];
  tasks.forEach(taskText => addTask(taskText));
}
