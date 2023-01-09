// API とのやり取りに使う1つのタスクを示す型
interface Task {
    id?: number
    content: string
    completed: boolean
}

/**
 * 画面起動時、各ボタン押した後に画面にタスク一覧を表示する
 */
async function fetchTasks() {
    // Web API 呼び出し
    const res = await fetch("/api/tasks");

    // API からの応答をパースする
    // Task 型の配列になっている
    const tasks = await res.json() as Task[];


    // Task 型の配列を HTML に展開する
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

/**
 * タスク追加ボタンを押した時
 */
async function createTask() {
    // 画面の入力をタスク型に収める
    const input = document.getElementById("newTaskContent") as HTMLInputElement;
    const task = {
        content: input.value,
        completed: false,
    } as Task;

    // Web API 呼び出し
    const res = await fetch("/api/tasks", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(task),
    })

    // ステータスコード 200 なら成功とする
    if (res.status != 200) {
        alert("fail to create new task");
        return;
    }

    // すでにある入力をクリアする
    input.value = "";

    // 画面の一覧のリロード
    await fetchTasks();
}

/**
 * 各タスクの完了ボタンを押した時
 */
async function completeTask(id: number) {
    // Web API 呼び出し
    const res = await fetch(`/api/tasks/${id}/done`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
    })

    // ステータスコード 200 なら成功とする
    if (res.status != 200) {
        alert("fail to make task completed");

        return;
    }

    // 画面の一覧のリロード
    await fetchTasks();
}

// 最初に読み出す
fetchTasks();
