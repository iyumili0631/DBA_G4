document.addEventListener('DOMContentLoaded', function () {
    const rfmListTable = document.getElementById('rfmList').querySelector('tbody');


    // 獲取顧客數據
    fetch('http://localhost:8000/crm/api/rfm_analysis/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            // 渲染顧客列表
            rfmListTable.innerHTML = ''; // 清空表格內容
            data.forEach(RFMAnalysis => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${RFMAnalysis.customer}</td>
                    <td>${RFMAnalysis.recency}</td>
                    <td>${RFMAnalysis.frequency}</td>
                    <td>${RFMAnalysis.monetary}</td>
                    <td>${RFMAnalysis.rfm_value}</td>
                    <td>${RFMAnalysis.customer_group}</td>
                    <td>${RFMAnalysis.most_valuable_customer}</td>
                    <td>${RFMAnalysis.marketing_strategy_suggestion}</td>


                `;
                rfmListTable.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching customer data:', error);
            const errorRow = document.createElement('tr');
            errorRow.innerHTML = `<td colspan="7">無法載入數據，請稍後再試。</td>`;
            rfmListTable.appendChild(errorRow);
        });
});

