document.addEventListener('DOMContentLoaded', function () {
    loadCustomerList(); // 初始化顧客清單
});




function loadCustomerList() {
    // 手動觸發顧客列表更新
    const customerListTable = document.getElementById('customerList').querySelector('tbody');
    fetch('http://localhost:8000/crm/api/customers/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            customerListTable.innerHTML = ''; // 清空表格內容
            data.forEach(customer => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${customer.customer_ID}</td>
                    <td>${customer.name}</td>
                    <td>${customer.last_purchase_date || 'N/A'}</td>
                    <td>${customer.avg_purchase_interval || 'N/A'}</td>
                    <td>${customer.avg_purchase_value || 'N/A'}</td>
                    <td>${customer.avg_customer_years || 'N/A'}</td>
                    <td>${customer.lifetime_value || 'N/A'}</td>
                `;
                customerListTable.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching customer data:', error);
        });
}


function addCustomer() {
    const customerNum = parseInt(document.getElementById('customerNum').value, 10);
    const customerName = document.getElementById('customerName').value;


    if (!customerNum || !customerName) {
        alert('請填寫所有欄位！');
        return;
    }


    // 發送 POST 請求到後端
    fetch('http://localhost:8000/crm/api/customers/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(), // CSRF 保護
        },
        body: JSON.stringify({
            customer_ID: customerNum,
            name: customerName
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('新增顧客成功！');
                // 更新顧客清單或重新載入頁面
                loadCustomerList();
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
    const csrfTokenMeta = document.querySelector('meta[name="csrf-token"]');
    return csrfTokenMeta ? csrfTokenMeta.getAttribute('content') : '';
}




