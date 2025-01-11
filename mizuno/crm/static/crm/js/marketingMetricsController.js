document.addEventListener('DOMContentLoaded', function () {
    fetchChart();
});

function fetchChart(){
    try {
        // 從後端 API 獲取數據
        const response = fetch('http://localhost:8000/crm/api/marketing_metrics/');
        if (!response.ok) {
            throw new Error(`Failed to fetch data: ${response.statusText}`);
        }

        const data = response.json();

        const labels = data.map(MarketingMetrics.year, MarketingMetrics.quarter);
        const values1 = data.map(MarketingMetrics.quarter_sales);
        const values2 = data.map(MarketingMetrics.quarter_growth_rate);

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
                label: 'Marketing Metrics',
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
                        text: 'Quarter Sales'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Year, Quarter'
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
                label: 'Marketing Metrics',
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
                        text: 'Quarter Growth Rate'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Year, Quarter'
                    },
                    beginAtZero: true
                }
            }
        }
    });
}