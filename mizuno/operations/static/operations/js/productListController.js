document.addEventListener('DOMContentLoaded', function () {
    const productList = document.getElementById('productList').querySelector('tbody');
    const materialList = document.getElementById('materialList').querySelector('tbody');
    const productRestockList = document.getElementById('productRestockList').querySelector('tbody');
    const materialRestockList = document.getElementById('materialRestockList').querySelector('tbody');




    //產品清單
    fetch('http://localhost:8000/operations/api/products/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            // 渲染顧客列表
            productList.innerHTML = ''; // 清空表格內容
            data.forEach(product => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${product.product_ID}</td>
                    <td>${product.product_name}</td>
                    <td>${product.product_price}</td>
                    <td>${product.product_inventory}</td>
                    <td>${product.product_safe_inventory}</td>
                    <td>${product.product_inventory_status}</td>
                `;
                productList.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching customer data:', error);
            const errorRow = document.createElement('tr');
            errorRow.innerHTML = `<td colspan="7">無法載入數據，請稍後再試。</td>`;
            productList.appendChild(errorRow);
        });


        //產品補貨機制
        fetch('http://localhost:8000/operations/api/product_restock/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            // 渲染顧客列表
            productRestockList.innerHTML = ''; // 清空表格內容
            data.forEach(productRestock => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${productRestock.product_name}</td>
                    <td>${productRestock.product_prediction}</td>
                    <td>${productRestock.restock_date}</td>
                    <td>${productRestock.restock_quantity}</td>
                `;
                productRestockList.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching customer data:', error);
            const errorRow = document.createElement('tr');
            errorRow.innerHTML = `<td colspan="7">無法載入數據，請稍後再試。</td>`;
            productRestockList.appendChild(errorRow);
        });


        //物料清單
        fetch('http://localhost:8000/operations/api/materials/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            // 渲染顧客列表
            materialList.innerHTML = ''; // 清空表格內容
            data.forEach(material => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${material.material_ID}</td>
                    <td>${material.material_name}</td>
                    <td>${material.material_inventory}</td>
                    <td>${material.material_safe_inventory}</td>
                    <td>${material.material_inventory_status}</td>
                `;
                materialList.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching customer data:', error);
            const errorRow = document.createElement('tr');
            errorRow.innerHTML = `<td colspan="7">無法載入數據，請稍後再試。</td>`;
            materialList.appendChild(errorRow);
        });


        //物料補貨機制
        fetch('http://localhost:8000/operations/api/material_restock/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            // 渲染顧客列表
            materialRestockList.innerHTML = ''; // 清空表格內容
            data.forEach(materialRestock => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${materialRestock.material_name}</td>
                    <td>${materialRestock.material_prediction}</td>
                    <td>${materialRestock.restock_date}</td>
                    <td>${materialRestock.restock_quantity}</td>
                `;
                materialRestockList.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching customer data:', error);
            const errorRow = document.createElement('tr');
            errorRow.innerHTML = `<td colspan="7">無法載入數據，請稍後再試。</td>`;
            materialRestockList.appendChild(errorRow);
        });
});



