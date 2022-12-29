interface Task {
    id?: number,
    content: string,
    completed: boolean,
}

async function fetchTasks() {
    const res = await fetch("/api/tasks");
    const tasks = await res.json() as Task[];
    const div = document.getElementById("tasksDiv") as HTMLDivElement;
    let html = "";
    tasks.forEach((task) => {
        html += `
          <div class="card m-2" style="width: 28rem">
            <div class="card-body">
              <h5 class="card-title">${task.id}</h5>
              <p class="card-text">${task.content}</p>
              <button class="btn btn-primary" onClick="completeTask(${task.id});">done</button>
            </div>
          </div>
        `
    })
    div.innerHTML = html;
}

async function createTask() {
    const input = document.getElementById("newTaskContent") as HTMLInputElement;
    const task = {
        content: input.value,
        completed: false,
    } as Task;
    const res = await fetch("/api/tasks", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(task),
    })
    if (res.status != 200) {
        alert("fail to create new task");
        return;
    }

    input.value = "";
    await fetchTasks();
}

async function completeTask(id: number) {
    const res = await fetch(`/api/tasks/${id}/done`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
    })
    if (res.status != 200) {
        alert("fail to make task completed");

        return;
    }

    await fetchTasks();
}

fetchTasks();
