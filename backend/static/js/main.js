// backend/static/js/main.js

document.addEventListener('DOMContentLoaded', loadTasksFromServer);

async function addTask() {
    const input = document.getElementById('inpu-task');
    const taskContent = input.value.trim();
    if (!taskContent) return;

    // --- Send the new task to the server ---
    const response = await fetch('/add_task', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: taskContent }),
    });

    if (response.ok) {
        const newTask = await response.json(); // Get new task details from server
        createTaskElement(newTask.content, newTask.id); // Create the UI element
        input.value = '';
    } else {
        alert('Failed to add task.');
    }
}

async function deleteTask(taskId, taskElement) {
    // --- Tell the server to delete the task ---
    const response = await fetch(`/delete_task/${taskId}`, { method: 'POST' });

    if (response.ok) {
        taskElement.remove(); // Remove from UI if server confirms
    } else {
        alert('Failed to delete task.');
    }
}

async function loadTasksFromServer() {
    const response = await fetch('/get_tasks');
    if (response.ok) {
        const tasks = await response.json();
        tasks.forEach(task => createTaskElement(task.content, task.id));
    }
}

function createTaskElement(content, id) {
    const taskList = document.getElementById('taskList');
    const newTask = document.createElement('li');
    newTask.textContent = content;
    newTask.dataset.id = id; // Store the task ID on the element

    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = "Delete";
    deleteBtn.classList.add("delete-btn");
    deleteBtn.onclick = function () {
        deleteTask(id, newTask);
    };

    newTask.appendChild(deleteBtn);
    taskList.appendChild(newTask);
}