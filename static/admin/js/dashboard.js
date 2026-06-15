const PALETTE = ['#e8452c','#f5a623','#27c06b','#3b82f6','#a855f7','#ec4899','#14b8a6','#f97316'];
const GRID_COLOR  = 'rgba(255,255,255,0.06)';
const TEXT_COLOR  = '#8b93ad';

Chart.defaults.color = TEXT_COLOR;
Chart.defaults.font.family = "'DM Mono', 'Fira Code', monospace";
Chart.defaults.font.size   = 12;

function doughnut(id, labels, data) {
  new Chart(document.getElementById(id), {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{ data, backgroundColor: PALETTE, borderWidth: 0, hoverOffset: 6 }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      cutout: '65%',
      plugins: {
        legend: {
          position: 'right',
          labels: { boxWidth: 10, padding: 12, font: { size: 11 } }
        },
        tooltip: {
          callbacks: {
            label: ctx => ` ${ctx.label}: ${ctx.raw} xe`
          }
        }
      }
    }
  });
}

function barChart(id, labels, data, label) {
  new Chart(document.getElementById(id), {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label,
        data,
        backgroundColor: PALETTE[0],
        borderRadius: 5,
        borderSkipped: false,
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: { legend: { display: false } },
      scales: {
        x: {
          grid: { color: GRID_COLOR },
          ticks: { stepSize: 1 }
        },
        y: { grid: { display: false } }
      }
    }
  });
}

// Fuel — doughnut
doughnut('chartFuel', {{ fuel_chart_labels|safe }}, {{ fuel_chart_data|safe }});

// Body type — horizontal bar
barChart('chartBody', {{ body_chart_labels|safe }}, {{ body_chart_data|safe }}, 'Số biến thể');

// Price bracket — doughnut
doughnut('chartPrice', {{ price_bracket_labels|safe }}, {{ price_bracket_data|safe }});