document.addEventListener('DOMContentLoaded', function () {
    fetchChart();
});


async function fetchChart(){
    try {
        // 從後端 API 獲取數據
        const response = await fetch('http://localhost:8000/crm/api/marketing_metrics/');
        if (!response.ok) {
            throw new Error(`Failed to fetch data: ${response.statusText}`);
        }

        const data = await response.json();
        console.log('Fetched Data:', data);

        const labels = data.map(MarketingMetrics => `${MarketingMetrics.year} ${MarketingMetrics.quarter}`);
        const values1 = data.map(MarketingMetrics => MarketingMetrics.quarter_sales);
        const values2 = data.map(MarketingMetrics => MarketingMetrics.quarter_growth_rate);

        createBarChart (labels, values1);
        createLineChart (labels, values2);

    }
    catch (error){
        console.error('Error:', error);
    }

};

function createBarChart(labels, values) {
    const ctx = document.getElementById('salesChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar', // 直方圖
        data: {
            labels: labels,
            datasets: [{
                label: '季銷售額',
                data: values,
                borderColor: 'rgb(59, 62, 77)',
                backgroundColor: ' #405580',
                borderWidth: 1,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true
                },
                tooltip: {
                    enabled: true
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Year and Quarter'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Quarter Sales'
                    },
                    beginAtZero: true
                }
            }
        }
    });
}

function createLineChart (labels, values){
    const ctx = document.getElementById('growthRateChart').getContext('2d');
    new Chart(ctx, {
        type: 'line', // 折線圖
        data: {
            labels: labels,
            datasets: [{
                label: '季銷售額成長率',
                data: values,
                borderColor: '#405580',
                backgroundColor: 'rgb(255, 255, 255)',
                borderWidth: 2,
                tension: 0.1 // 平滑曲線
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true
                },
                tooltip: {
                    enabled: true
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Year and Quarter'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Quarter Growth Rate'
                    },
                    beginAtZero: true
                }
            }
        }
    });
}

function saveButton (){

    fetch('http://localhost:8000/crm/api/marketing_metrics/update/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
        },
        
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('重整成功！');
            fetchChart();
        } else {
            alert('重整失敗！');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('發生錯誤，請稍後再試。');
    });
}

function getCsrfToken() {
    const csrfTokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
    if (!csrfTokenInput) {
        console.error('CSRF Token not found!');
        return '';
    }
    return csrfTokenInput.value;
}
