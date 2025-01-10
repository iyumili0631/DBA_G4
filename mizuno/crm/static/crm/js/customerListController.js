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
    const formData = {
        name: document.getElementById('name').value,
    }

    axios.post('https://localhost:8000/crm/api/customers_create/', formData)
        .then(response => {
            console.log('新增成功:', response.data);
            alert('訂單新增成功！');
            // 在這裡更新前端的訂單列表
            updateCustomerList(response.data);
        })
        .catch(error => {
            console.error('新增失敗:', error.response.data);
            alert('訂單新增失敗，請檢查輸入數據！');
        });
}

function updateCustomerList(customer) {
    const tableBody = document.querySelector('#customerList tbody');
    const newRow = `
        <tr>
            <td>${customer.id}</td>
            <td>${customer.name}</td>
            <td>${customer.last_purchase_date || 'N/A'}</td>
            <td>${customer.avg_purchase_interval || 'N/A'}</td>
            <td>${customer.avg_purchase_value || 'N/A'}</td>
            <td>${customer.avg_customer_years || 'N/A'}</td>
            <td>${customer.lifetime_value || 'N/A'}</td>
        </tr>
    `;
    tableBody.insertAdjacentHTML('beforeend', newRow);
} 


function getCsrfToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfToken ? csrfToken.value : '';
}



