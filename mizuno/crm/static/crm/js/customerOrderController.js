document.addEventListener('DOMContentLoaded', function () {
    loadCustomerOrderList();    
});


function loadCustomerOrderList(){
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
                    <td>${customerOrder.required_delivery_date}</td>
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
}


function updateOrderStatus (orderId){
    const status = document.getElementById(`status-select-${orderId}`).value;
    const orderStatusCell = document.getElementById(`customer_order_detail-${orderId}`);


    // 顯示正在更新的狀態
    orderStatusCell.textContent = '更新中...';


    // 發送 POST 請求到後端
    fetch(`http://localhost:8000/crm/api/customer_orders/${orderId}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()  // 確保 CSRF 保護
        },
        body: JSON.stringify({ status })  // 傳遞新的訂單狀態
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
}


function addCustomerOrder(){
    const customerName = document.getElementById('customerName').value;
    const orderNum = document.getElementById('orderNum').value;
    const orderDate = document.getElementById('orderDate').value;
    const orderContent = document.getElementById('orderContent').value;
    const quantity = document.getElementById('quantity').value;

    if (!orderNum || !customerName) {
        alert('請填寫所有欄位！');
        return;
    }


    // 發送 POST 請求到後端
    fetch('http://localhost:8000/crm/api/create_customer_orders/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(), // CSRF 保護
        },
        body: JSON.stringify({
            customer: customerName,
            order_ID: orderNum,
            order_date: orderDate,
            order_product: orderContent,
            order_quantity: quantity
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('新增顧客成功！');
                // 更新顧客清單或重新載入頁面
                loadCustomerOrderList();
            } else {
                alert('新增顧客失敗：' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('新增顧客時發生錯誤');
        });
}

fetch ()


function getCsrfToken() {
    const csrfTokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
    if (!csrfTokenInput) {
        console.error('CSRF Token not found!');
        return '';
    }
    return csrfTokenInput.value;
}



