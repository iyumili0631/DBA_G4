document.addEventListener('DOMContentLoaded', function () {
    // 獲取數據
    fetch('http://localhost:8000/crm/api/marketing_metrics/')
        .then(response => response.json())
        .then(data => {
            const marketingMetrics = document.getElementById('orderBody');
            marketingMetrics.innerHTML = '';  // 清空表格內容
            let salesData = {}; // 用於存儲每年銷售數據
            let growthRateData = {}; // 用於存儲成長率數據

            // 組織資料並填充表格
            data.forEach(metrics => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${metrics.year}</td>
                    <td>${metrics.quarter}</td>
                    <td>${metrics.quarter_sales}</td>
                    <td>${metrics.quarter_growth_rate}</td>
                `;
                marketingMetrics.appendChild(row);

                // 整理每年銷售額
                if (!salesData[metrics.year]) {
                    salesData[metrics.year] = { Q1: 0, Q2: 0, Q3: 0, Q4: 0 };
                }
                salesData[metrics.year][metrics.quarter] = metrics.quarter_sales;

                // 整理成長率數據
                if (!growthRateData[metrics.year]) {
                    growthRateData[metrics.year] = { Q1: 0, Q2: 0, Q3: 0, Q4: 0 };
                }
                growthRateData[metrics.year][metrics.quarter] = metrics.quarter_growth_rate;
            });

            // 整理趨勢圖數據
            const years = Object.keys(salesData);
            const salesTrends = years.map(year => {
                return [salesData[year]['Q1'], salesData[year]['Q2'], salesData[year]['Q3'], salesData[year]['Q4']];
            });

            const growthRateTrends = years.map(year => {
                return [growthRateData[year]['Q1'], growthRateData[year]['Q2'], growthRateData[year]['Q3'], growthRateData[year]['Q4']];
            });

            // 顯示銷售額趨勢圖
            const salesChart = new Chart(document.getElementById('salesChart'), {
                type: 'line',
                data: {
                    labels: ['Q1', 'Q2', 'Q3', 'Q4'],
                    datasets: years.map((year, index) => ({
                        label: `Year ${year}`,
                        data: salesTrends[index],
                        fill: false,
                        borderColor: `rgb(${index * 50}, ${255 - index * 50}, 100)`,
                        tension: 0.1
                    }))
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return `${value} NTD`;
                                }
                            }
                        }
                    }
                }
            });

            // 顯示銷售額成長率趨勢圖
            const growthRateChart = new Chart(document.getElementById('growthRateChart'), {
                type: 'line',
                data: {
                    labels: ['Q1', 'Q2', 'Q3', 'Q4'],
                    datasets: years.map((year, index) => ({
                        label: `Year ${year}`,
                        data: growthRateTrends[index],
                        fill: false,
                        borderColor: `rgb(${index * 50}, 100, 255)`,
                        tension: 0.1
                    }))
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return `${value.toFixed(2)} %`;
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
