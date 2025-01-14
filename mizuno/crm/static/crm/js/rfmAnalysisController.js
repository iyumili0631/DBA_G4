document.addEventListener('DOMContentLoaded', function () {
    loadRFM();    
});

function loadRFM (){
    const rfmList = document.getElementById('rfmList').querySelector('tbody');

    fetch('/crm/api/rfm_analysis/')
    .then(response => response.json())
    .then(data => {
        rfmList.innerHTML = '';  // 清空表格
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
            rfmList.appendChild(row);
        });
    })
    .catch(error => {
        console.error('Error fetching RFM data:', error);
    });
}

function saveButton(){
    fetch('/crm/trigger_rfm_analysis/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('RFM 分析計算成功！');
            loadRFM();
        } else {
            alert('RFM 分析計算失敗！');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('發生錯誤，請稍後再試。');
    });
}