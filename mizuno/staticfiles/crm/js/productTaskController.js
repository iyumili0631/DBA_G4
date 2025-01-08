document.addEventListener('DOMContentLoaded', function () {
    const productTaskList = document.getElementById('productTaskList').querySelector('tbody');


    // 獲取顧客訂單資料
    fetch('http://localhost:8000/operations/api/production_tasks/')
        .then(response => response.json())
        .then(data => {
            productTaskList.innerHTML = '';  // 清空表格內容
            data.forEach(task => {
                const row = document.createElement('tr');


                // 顯示顧客訂單資料
                row.innerHTML = `
                    <td>${task.order_ID}</td>
                    <td>${task.task_date}</td>
                    <td id="taskAction-${task.order_ID}">${task.task_action}</td>
                    <td>
                        <select id="action-select-${task.order_ID}" onchange="updateTask(${task.order_ID})">
                            <option value="生產" ${task.task_action === '生產' ? 'selected' : ''}>生產</option>
                            <option value="發貨" ${task.task_action === '發貨' ? 'selected' : ''}>發貨</option>
                            <option value="訂購" ${task.task_action === '訂購' ? 'selected' : ''}>訂購</option>
                        </select>
                    </td>
                    <td>${task.task_content}</td>
                    <td id="taskStatus-${task.order_ID}">${task.task_status}</td>
                    <td>
                        <select id="status-select-${task.order_ID}" onchange="updateTask(${task.order_ID})">
                            <option value="未完成" ${task.task_status === '未完成' ? 'selected' : ''}>未完成</option>
                            <option value="完成" ${task.task_status === '完成' ? 'selected' : ''}>完成</option>
                        </select>
                    </td>
                   
                `;


                // 將訂單行添加到表格中
                customerList.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });


    // 更新訂單狀態的函數


    window.updateTask = function (orderId) {
        const action = document.getElementById(`action-select-${orderId}`).value;
        const status = document.getElementById(`status-select-${orderId}`).value;
        const taskActionCell = document.getElementById(`taskAction-${orderId}`);
        const taskStatusCell = document.getElementById(`taskStatus-${orderId}`);


        // 顯示正在更新的狀態
        taskActionCell.textContent = '更新中...';
        taskStatusCell.textContent = '更新中...';


        // 發送 POST 請求到後端
        fetch(`http://localhost:8000/operations/api/production_tasks/${orderId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()  // 確保 CSRF 保護
            },
            body: JSON.stringify({ action: action, status: status})
        })
        .then(response => response.json())
        .then(data => {
            // 更新訂單狀態顯示
            taskActionCell.textContent = data.action;
            taskStatusCell.textContent = data.status;
        })
        .catch(error => {
            console.error('Error:', error);
            taskStatusCell.textContent = '更新失敗';
            taskActionCell.textContent = '更新失敗';
        });
    };


    // 獲取 CSRF token（如果需要）
    function getCsrfToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        return csrfToken;
    }
});

