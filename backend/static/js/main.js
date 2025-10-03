function addTask(){
  const newTask = document.createElement('li');
  const taskList = document.getElementById('taskList');
  taskList.appendChild(newTask);
  newTask.textContent = document.getElementById('inpu-task').value;
  document.getElementById('inpu-task').value="";
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