document.addEventListener('DOMContentLoaded', function () {
    const saveButton = document.getElementById('saveButton');
    fetch('http://localhost:8000/crm/api/rfm_analysis/')
    .then(response => response.json())
    .then(data => {
        rfmListTable.innerHTML = '';  // 清空表格
        data.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.customer}</td>
                <td>${item.recency}</td>
                <td>${item.frequency}</td>
                <td>${item.monetary}</td>
                <td>${item.rfm_value}</td>
                <td>${item.customer_group}</td>
                <td>${item.most_valuable_customer}</td>
                <td>${item.marketing_strategy_suggestion}</td>
            `;
            rfmListTable.appendChild(row);
        });
    })
    .catch(error => {
        console.error('Error fetching RFM data:', error);
    });
});

    saveButton.addEventListener('click', function () {
        fetch('http://localhost:8000/crm/trigger_rfm_analysis/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('RFM 分析計算成功！');
                // 在這裡更新 RFM 分析列表或重載頁面
            } else {
                alert('RFM 分析計算失敗！');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('發生錯誤，請稍後再試。');
        });
    });

