document.addEventListener('DOMContentLoaded', function () {
    const bomListTable = document.getElementById('bomList').querySelector('tbody');

    // 獲取顧客數據
    fetch('{% url '/operations/api/boms/' %}')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            // 渲染顧客列表
            bomListTable.innerHTML = ''; // 清空表格內容
            const fragment = document.createDocumentFragment(); // 提高性能
            data.forEach(BOM => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${BOM.BOM_ID}</td>
                    <td>${BOM.product_name}</td>
                    <td>${BOM.material_name}</td>
                    <td>${BOM.material_quantity}</td>
                `;
                fragment.appendChild(row);
            });
            bomListTable.appendChild(fragment);// 一次性插入
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

