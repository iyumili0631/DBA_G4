document.addEventListener('DOMContentLoaded', function () {
    const productOrderList = document.getElementById('productOrderList').querySelector('tbody');


    // 獲取顧客訂單資料
    fetch('http://localhost:8000/operations/api/production_orders/')
        .then(response => response.json())
        .then(data => {
            productOrderList.innerHTML = '';  // 清空表格內容
            data.forEach(productionOrder => {
                const row = document.createElement('tr');


                // 顯示顧客訂單資料
                row.innerHTML = `
                    <td>${productionOrder.order_ID}</td>
                    <td>${productionOrder.order_date}</td>
                    <td>${productionOrder.product_name}</td>
                    <td>${productionOrder.product_quantity}</td>
                    <td>${productionOrder.material_name}</td>
                    <td>${productionOrder.material_quantity}</td>
                    <td id="orderStatus-${productionOrder.order_ID}">${productionOrder.order_status}</td>
                    <td>
                        <select id="status-select-${productionOrder.order_ID}" onchange="updateStatus(${productionOrder.order_ID})">
                            <option value="處理中" ${productionOrder.order_status === '處理中' ? 'selected' : ''}>處理中</option>
                            <option value="已完成" ${productionOrder.order_status === '已完成' ? 'selected' : ''}>已完成</option>
                            <option value="已取消" ${productionOrder.order_status === '已取消' ? 'selected' : ''}>已取消</option>
                        </select>
                    </td>
                    <td>${productionOrder.order_deadline}</td>


                   
                `;


                // 將訂單行添加到表格中
                productOrderList.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });


    // 更新訂單狀態的函數


    window.updateStatus = function (orderId) {
        const status = document.getElementById(`status-select-${orderId}`).value;
        const orderStatusCell = document.getElementById(`orderStatus-${orderId}`);


        // 顯示正在更新的狀態
        orderStatusCell.textContent = '更新中...';


        // 發送 POST 請求到後端
        fetch(`http://localhost:8000/operations/api/production_orders/${orderId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()  // 確保 CSRF 保護
            },
            body: JSON.stringify({ status: status})
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

