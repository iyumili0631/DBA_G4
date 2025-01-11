document.addEventListener('DOMContentLoaded', function () {
    loadProductTask();    
});

function loadProductTask (){
    const productTaskList = document.getElementById('productTaskList').querySelector('tbody');

    // 獲取待辦事項資料
    fetch('http://localhost:8000/operations/api/production_tasks/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            // 清空表格內容
            productTaskList.innerHTML = '';
            const fragment = document.createDocumentFragment(); // 提高性能
            data.forEach(task => {
                const row = document.createElement('tr');

                // 顯示資料
                row.innerHTML = `
                    <td>${task.order_ID}</td>
                    <td>${task.task_date}</td>
                    <td id="taskAction-${task.id}">${task.task_action}</td>
                    <td>
                        <select id="action-select-${task.id}" onchange="updateTask(${task.id})">
                            <option value="生產" ${task.task_action === '生產' ? 'selected' : ''}>生產</option>
                            <option value="發貨" ${task.task_action === '發貨' ? 'selected' : ''}>發貨</option>
                            <option value="訂購" ${task.task_action === '訂購' ? 'selected' : ''}>訂購</option>
                        </select>
                    </td>
                    <td>${task.task_content}</td>
                    <td id="taskStatus-${task.id}">${task.task_status}</td>
                    <td>
                        <select id="status-select-${task.id}" onchange="updateTask(${task.id})">
                            <option value="未完成" ${task.task_status === '未完成' ? 'selected' : ''}>未完成</option>
                            <option value="完成" ${task.task_status === '完成' ? 'selected' : ''}>完成</option>
                        </select>
                    </td>
                `;

                fragment.appendChild(row);
            });
            productTaskList.appendChild(fragment); 
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function updateTask (orderId){
    const task_action = document.getElementById(`action-select-${orderId}`).value;
    const task_status = document.getElementById(`status-select-${orderId}`).value;
    const taskActionCell = document.getElementById(`taskAction-${orderId}`);
    const taskStatusCell = document.getElementById(`taskStatus-${orderId}`);

    // 顯示正在更新的狀態
    taskActionCell.textContent = '更新中...';
    taskStatusCell.textContent = '更新中...';

    // 發送 PATCH 請求到後端
    fetch(`http://localhost:8000/operations/api/production_tasks/${orderId}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken() // 確保 CSRF 保護
        },
        body: JSON.stringify({ task_action, task_status })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update task');
            }
            return response.json();
        })
        .then(data => {
            // 更新訂單狀態顯示
            taskActionCell.textContent = data.task_action;
            taskStatusCell.textContent = data.task_status;
        })
        .catch(error => {
            console.error('Error:', error);
            taskActionCell.textContent = '更新失敗';
            taskStatusCell.textContent = '更新失敗';
        });
}

fetch ('http://localhost:8000/operations/api/production_order_IDs/')
    .then(response => {
        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }
        return response.json();
    })
    
    .then(data => {
        const dropdown = document.getElementById('orderNum');

        dropdown.innerHTML = '<option value="">請選擇訂單編號</option>';

        data.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option;
            optionElement.textContent = option;
            dropdown.appendChild(optionElement);
        });
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        alert('無法加載訂單資料，請稍後再試！');
    });


function addAction (){
    const orderNum = document.getElementById('orderNum').value;
    const actionDate = document.getElementById('actionDate').value;
    const action = document.getElementById('action').value;
    const actionContent = document.getElementById('actionContent').value;

    if (!actionDate || !action) {
        alert('請填寫所有欄位！');
        return;
    }

    // 發送 POST 請求到後端
    fetch('http://localhost:8000/operation/api/create_production_tasks/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(), // CSRF 保護
        },
        body: JSON.stringify({
            order_ID: orderNum,
            task_date: actionDate,
            task_action: action,
            task_content: actionContent,
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('新增顧客成功！');
                // 更新顧客清單或重新載入頁面
                loadProductTask();
            } else {
                alert('新增顧客失敗：' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('新增顧客時發生錯誤');
        });
}

function getCsrfToken() {
    const csrfTokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
    if (!csrfTokenInput) {
        console.error('CSRF Token not found!');
        return '';
    }
    return csrfTokenInput.value;
}