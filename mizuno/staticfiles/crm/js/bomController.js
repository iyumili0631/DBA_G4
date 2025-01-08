document.addEventListener('DOMContentLoaded', function () {
    const bomListTable = document.getElementById('bomList').querySelector('tbody');


    // 獲取顧客數據
    fetch('http://localhost:8000/operations/api/boms/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            // 渲染顧客列表
            bomListTable.innerHTML = ''; // 清空表格內容
            data.forEach(BOM => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${BOM.BOM_ID}</td>
                    <td>${BOM.product_name}</td>
                    <td>${BOM.material_name}</td>
                    <td>${BOM.material_quantity}</td>
                `;
                bomListTable.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching customer data:', error);
            const errorRow = document.createElement('tr');
            errorRow.innerHTML = `<td colspan="7">無法載入數據，請稍後再試。</td>`;
            bomListTable.appendChild(errorRow);
        });
});

