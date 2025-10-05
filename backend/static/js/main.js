document.addEventListener('DOMContentLoaded', loadTasksFromServer);

// Get the CSRF token from the meta tag
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

async function addTask() {
    const input = document.getElementById('inpu-task');
    const taskContent = input.value.trim();
    if (!taskContent) return;

    const response = await fetch('/add_task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken // <-- Add this header
        },
        body: JSON.stringify({ content: taskContent }),
    });

    if (response.ok) {
        const newTask = await response.json();
        createTaskElement(newTask.content, newTask.id);
        input.value = '';
    } else {
        alert('Failed to add task. You may need to log in again.');
    }
}

async function deleteTask(taskId, taskElement) {
    const response = await fetch(`/delete_task/${taskId}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken // <-- Add this header
        }
    });

    if (response.ok) {
        taskElement.remove();
    } else {
        alert('Failed to delete task. You may need to log in again.');
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
    newTask.dataset.id = id;

    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = "Delete";
    deleteBtn.classList.add("delete-btn");
    deleteBtn.onclick = function () {
        deleteTask(id, newTask);
    };

    newTask.appendChild(deleteBtn);
    taskList.appendChild(newTask);
}