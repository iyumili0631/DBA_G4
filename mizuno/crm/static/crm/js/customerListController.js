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
    // 獲取顧客姓名
    const name = document.getElementById('customerName').value;
    
    // 檢查顧客姓名是否輸入
    if (!name) {
        alert("顧客姓名為必填欄位！");
        return;  // 如果沒有輸入顧客姓名，阻止表單提交
    }

    // 準備表單資料，其他欄位使用預設值
    const formData = {
        name: name,  // 顧客姓名
        last_purchase_date: 'N/A',  // 預設值
        avg_purchase_interval: 'N/A',  // 預設值
        avg_purchase_value: 'N/A',  // 預設值
        avg_customer_years: 3.0,  // 預設值
        lifetime_value: 'N/A'  // 預設值
    };

    // 使用 axios 提交資料
    axios.post('http://localhost:8000/crm/api/customers_create/', formData)
        .then(response => {
            console.log('新增成功:', response.data);
            alert('顧客新增成功！');
            // 可以更新顧客列表或者清空表單等
            updateCustomerList(response.data);
        })
        .catch(error => {
            console.error('新增失敗:', error);
            alert('新增失敗，請檢查資料！');
        });
}


function updateCustomerList(customer) {
    const tableBody = document.querySelector('#customerList tbody');
    const newRow = `
        <tr>
            <td>${customer.id || 'N/A'}</td>
            <td>${customer.name || 'N/A'}</td>
            <td>${customer.last_purchase_date || 'N/A'}</td>
            <td>${customer.avg_purchase_interval || 'N/A'}</td>
            <td>${customer.avg_purchase_value || 'N/A'}</td>
            <td>${customer.avg_customer_year || 'N/A'}</td>
            <td>${customer.lifetime_value || 'N/A'}</td>
        </tr>
    `;
    tableBody.insertAdjacentHTML('beforeend', newRow);
} 


function getCsrfToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfToken ? csrfToken.value : '';
}

document.addEventListener('DOMContentLoaded', function () {
    // 在此處調用初始化函數
    loadCustomerList();
});



