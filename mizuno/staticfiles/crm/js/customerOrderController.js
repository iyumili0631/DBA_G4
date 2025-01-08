document.addEventListener('DOMContentLoaded', function () {
    const customerList = document.getElementById('customerOrder').querySelector('tbody');


    // 獲取顧客訂單資料
    fetch('http://localhost:8000/crm/api/customer_orders/')
        .then(response => response.json())
        .then(data => {
            customerList.innerHTML = '';  // 清空表格內容
            data.forEach(customerOrder => {
                const row = document.createElement('tr');


                // 顯示顧客訂單資料
                row.innerHTML = `
                    <td>${customerOrder.customer}</td>
                    <td>${customerOrder.order_ID}</td>
                    <td>${customerOrder.order_date}</td>
                    <td>${customerOrder.order_product}</td>
                    <td>${customerOrder.order_quantity}</td>
                    <td>${customerOrder.requered_delivery_date}</td>
                    <td id="customer_order_detail-${customerOrder.order_ID}">${customerOrder.status}</td>
                    <td>
                        <select id="status-select-${customerOrder.order_ID}" onchange="updateOrderStatus(${customerOrder.order_ID})">
                            <option value="已完成" ${customerOrder.status === '已完成' ? 'selected' : ''}>已完成</option>
                            <option value="處理中" ${customerOrder.status === '處理中' ? 'selected' : ''}>處理中</option>
                            <option value="已取消" ${customerOrder.status === '已取消' ? 'selected' : ''}>已取消</option>
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
    window.updateOrderStatus = function (orderId) {
        const status = document.getElementById(`status-select-${orderId}`).value;
        const orderStatusCell = document.getElementById(`customer_order_detail-${orderId}`);


        // 顯示正在更新的狀態
        orderStatusCell.textContent = '更新中...';


        // 發送 POST 請求到後端
        fetch(`http://localhost:8000/crm/api/customer_orders/${orderId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()  // 確保 CSRF 保護
            },
            body: JSON.stringify({ status: status })  // 傳遞新的訂單狀態
        })
        .then(response => response.json())
        .then(data => {
            // 更新訂單狀態顯示
            orderStatusCell.textContent = data.status;
        })
        .catch(error => {
            console.error('Error:', error);
            orderStatusCell.textContent = '更新失敗';
        });
    };


    // 獲取 CSRF token（如果需要）
    function getCsrfToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        return csrfToken;
    }
});



