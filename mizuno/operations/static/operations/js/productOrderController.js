document.addEventListener('DOMContentLoaded', function () {
    loadProductOrder();
});

function loadProductOrder(){
    const productOrderList = document.getElementById('productOrderList').querySelector('tbody');

    fetch('http://localhost:8000/operations/api/production_orders/')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
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
                    <td id="orderStatus-${productionOrder.id}">${productionOrder.order_status}</td>
                    <td>
                        <select id="status-select-${productionOrder.id}" onchange="updateProductOrderStatus(${productionOrder.id})">
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
        })

}

function updateProductOrderStatus(orderId){
    const status = document.getElementById(`status-select-${orderId}`).value;
        const orderStatusCell = document.getElementById(`orderStatus-${orderId}`);


        // 顯示正在更新的狀態
        orderStatusCell.textContent = '更新中...';


        // 發送 PATCH 請求到後端
        fetch(`http://localhost:8000/operations/api/production_orders/${orderId}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()  // 確保 CSRF 保護
            },
            body: JSON.stringify({ order_status: status})
        })
        .then(response => response.json())
        .then(data => {
            // 更新訂單狀態顯示
            orderStatusCell.textContent = data.order_status;
        })
        .catch(error => {
            console.error('Error:', error);
            orderStatusCell.textContent = '更新失敗';
        })
}

function addProductOrder(){
    const orderDate = document.getElementById('orderDate').value;
    const productName = document.getElementById('productName').value;
    const Pquantity = document.getElementById('Pquantity').value;
    const materialName = document.getElementById('materialName').value;
    //const Mquantity = document.getElementById('Mquantity').value;
    const deadline = document.getElementById('deadline').value;


    if (!orderDate || !productName) {
        alert('請填寫所有欄位！');
        return;
    }

    // 發送 POST 請求到後端
    fetch('http://localhost:8000/operation/api/create_production_orders/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(), // CSRF 保護
        },
        body: JSON.stringify({
            order_date: orderDate,
            product_name: productName,
            product_quantity: Pquantity,
            material_name: materialName,
            //material_quantity: Mquantity,
            order_deadline: deadline
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('新增顧客成功！');
                // 更新顧客清單或重新載入頁面
                loadProductOrder();
            } else {
                alert('新增顧客失敗：' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('新增顧客時發生錯誤');
        });
}


// 獲取 CSRF token（如果需要）
function getCsrfToken() {
    const csrfTokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
    if (!csrfTokenInput) {
        console.error('CSRF Token not found!');
        return '';
    }
    return csrfTokenInput.value;
}