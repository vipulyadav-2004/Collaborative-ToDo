loadTask();
function addTask(){
  const newTask = document.createElement('li');
  const taskList = document.getElementById('taskList');
  taskList.appendChild(newTask);
  newTask.textContent = document.getElementById('inpu-task').value;
  document.getElementById('inpu-task').value="";
  saveTask()
  deleteTask(newTask);
}
function deleteTask(newTask){
  const deletebtn = document.createElement('button');
  deletebtn.textContent="Delete";
  deletebtn.classList.add("delete-btn");
  newTask.appendChild(deletebtn);
  deletebtn.onclick = function(){
    newTask.remove()
  }
}
function saveTask() {
  const taskList = document.getElementById('taskList');  
  let tasks = [];
  taskList.querySelectorAll('li').forEach(function (item) { 
     let text = item.firstChild.textContent.trim();
    tasks.push(text);
  });
  localStorage.setItem('task', JSON.stringify(tasks));
}
function loadTask(){
  const tasks = JSON.parse(localStorage.getItem('tasks')) || [];
  tasks.forEach(addTask)
}