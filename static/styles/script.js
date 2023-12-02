let taskInput = document.getElementById("new-task");
let addButton = document.getElementById("addButton");
let incompleteTasks = document.getElementById("incomplete-tasks");
let completedTasks = document.getElementById("completed-tasks");
let clearButton = document.getElementById("clear");

let createNewTask = function(taskName) {
    // create List Item
    let listItem = document.createElement("li");
    // input checkbox
    let checkBox = document.createElement("input");
    // label
    let label = document.createElement("label");
    // input (text)
    let editInput = document.createElement("input");
    // button.edit
    let editButton = document.createElement("button");
    // button.delete
    let deleteButton = document.createElement("button");

    //Each element needs modified 
    checkBox.type = "checkBox";
    editInput.type = "text";
    editButton.innerText = "Edit";
    editButton.className = "edit";
    deleteButton.innerText = "Delete";
    deleteButton.className = "delete";
    label.innerText = taskName;
    listItem.appendChild(checkBox);
    listItem.appendChild(label);
    listItem.appendChild(editInput);
    listItem.appendChild(editButton);
    listItem.appendChild(deleteButton);

    return listItem;
}

let addTask = function() {
    if (taskInput.value == "") {
        alert("Task to be added should not be empty!");
        return;
    }
    let listItem = createNewTask(taskInput.value);

    fetch('/api/log_task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ task: taskInput.value, type: 'incomplete' })
    })
    .then(response => response.json())
    .then(data => console.log('Result:', data.result));

    incompleteTasks.append(listItem);
    bindTaskEvents(listItem, taskCompleted);
    taskInput.value = "";
}
addButton.addEventListener("click", addTask);

let bindTaskEvents = function(taskListItem, checkBoxEventHandler) {
    // select listitems children
    let checkBox = taskListItem.querySelector('input[type="checkbox"]');
    let editButton = taskListItem.querySelector("button.edit");
    let deleteButton = taskListItem.querySelector("button.delete");
    //bind editTask to edit button
    editButton.onclick = editTask;
    //bind deleteTask to delete button
    deleteButton.onclick = deleteTask;
    //bind checkBoxEventHandler to checkbox
    checkBox.onchange = checkBoxEventHandler;
}

let editTask = function() {
    let listItem = this.parentNode;
    let editInput = listItem.querySelector("input[type=text]");
    let label = listItem.querySelector("label");
    let containsClass = listItem.classList.contains("editMode");

    // if the listItem element contains the editMode class
    if (containsClass) {
        // log
        fetch('/api/log_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ task: listItem.getElementsByTagName('label')[0].textContent + " -> " + editInput.value, type: 'edit' })
        })
        .then(response => response.json())
        .then(data => console.log('Result:', data.result));

        //Switch from .editMode
        //label text become the input's value
        label.innerText = editInput.value;
        
    } else {
        //Switch to .editMode
        //input value becomes the labels text
        editInput.value = label.innerText;
    }
    //Toggle .editMode class on and off
    listItem.classList.toggle("editMode");
}

let deleteTask = function() {
    let listItem = this.parentNode;
    let ul = listItem.parentNode;

    fetch('/api/log_task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ task: listItem.getElementsByTagName('label')[0].textContent, type: 'delete' })
    })
    .then(response => response.json())
    .then(data => console.log('Result:', data.result));

    ul.removeChild(listItem);
}

let taskCompleted = function() {
    let listItem = this.parentNode;

    fetch('/api/log_task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ task: listItem.getElementsByTagName('label')[0].textContent, type: 'complete' })
    })
    .then(response => response.json())
    .then(data => console.log('Result:', data.result));

    completedTasks.appendChild(listItem);
    bindTaskEvents(listItem, taskIncomplete);
}

let taskIncomplete = function() {
    let listItem = this.parentNode;

    fetch('/api/log_task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ task: listItem.getElementsByTagName('label')[0].textContent, type: 'incomplete' })
    })
    .then(response => response.json())
    .then(data => console.log('Result:', data.result));

    incompleteTasks.appendChild(listItem);
    bindTaskEvents(listItem, taskCompleted);
}

let clear = function() {
    fetch('/api/log_task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ task: 'ALL', type: 'clear' })
    })
    .then(response => response.json())
    .then(data => console.log('Result:', data.result));

    incompleteTasks.innerHTML = "";
    completedTasks.innerHTML = "";
}
clearButton.addEventListener('click', clear);