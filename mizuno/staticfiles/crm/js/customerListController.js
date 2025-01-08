document.addEventListener('DOMContentLoaded', function () {
    const customerListTable = document.getElementById('customerList').querySelector('tbody');


    // 獲取顧客數據
    fetch('http://localhost:8000/crm/api/customers/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            // 渲染顧客列表
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
            const errorRow = document.createElement('tr');
            errorRow.innerHTML = `<td colspan="7">無法載入數據，請稍後再試。</td>`;
            customerListTable.appendChild(errorRow);
        });
},


function addCustomer() {
    const customer_ID = document.getElementById('customer_ID').value;
    const name = document.getElementById('name').value;


    if (!customer_ID || !name) {
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
            customer_ID: customer_ID,
            name: name
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
},


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
},


function getCsrfToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfToken ? csrfToken.value : '';
}


);



