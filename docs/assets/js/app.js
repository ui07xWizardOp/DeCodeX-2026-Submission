/**
 * VoltRide Dashboard Core Logic
 * Version: 2.0 (Granular Data)
 */

// Configuration
const CONFIG = {
    dataUrl: './assets/data/metrics.json',
    chartsUrl: './assets/data/charts.json',
    tableUrl: './assets/data/table_data.json',
    colors: {
        killZone: '#ef4444',
        goldilocks: '#10b981',
        warning: '#f59e0b',
        primary: '#3b82f6',
        text: '#f8fafc',
        grid: '#334155'
    },
    itemsPerPage: 10
};

let rawTableData = [];
let currentPage = 1;

// Initialization
document.addEventListener('DOMContentLoaded', async () => {
    console.log('⚡ VoltRide Dashboard Initializing...');

    try {
        const [metrics, charts, tableData] = await Promise.all([
            fetch(CONFIG.dataUrl).then(r => r.json()),
            fetch(CONFIG.chartsUrl).then(r => r.json()),
            fetch(CONFIG.tableUrl).then(r => r.json())
        ]);

        rawTableData = tableData;

        renderKPIs(metrics.kpis);
        renderCharts(charts);
        renderTable(1);
        setupPagination();

        console.log('Dashboard Loaded Successfully');
    } catch (error) {
        console.error('Initialization failed:', error);
    }
});

function renderKPIs(kpis) {
    animateValue("kpi-kill-zone", 0, kpis.kill_zone_rate, 2000, "%");
    animateValue("kpi-goldilocks", 0, kpis.goldilocks_rate, 2000, "%");
    animateValue("kpi-revenue", 0, kpis.revenue_loss / 1000, 2000, "K", "$");
    // Update Total Demand if element exists, or just log
}

function renderCharts(data) {
    renderBatteryCliff(data.battery_cliff);
    renderHeapmap(data.heatmap);
    renderInfraParadox(data.infra_paradox);
    renderHourlyTrend(data.hourly_trend);
    renderRevenueTrend(data.revenue_trend);
}

function renderHourlyTrend(data) {
    const ctx = document.getElementById('chart-hourly-trend');
    if (!ctx || !data) return;

    const trace1 = {
        x: data.hours,
        y: data.demand,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Total Demand',
        line: { color: CONFIG.colors.primary, width: 3 }
    };

    const trace2 = {
        x: data.hours,
        y: data.cancellations,
        type: 'bar',
        name: 'Cancellations',
        marker: { color: CONFIG.colors.killZone, opacity: 0.6 }
    };

    const layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: CONFIG.colors.text, family: 'Inter' },
        margin: { t: 10, b: 40, l: 40, r: 10 },
        legend: { x: 0, y: 1.1, orientation: 'h' },
        xaxis: { title: 'Hour of Day', gridcolor: CONFIG.colors.grid },
        yaxis: { gridcolor: CONFIG.colors.grid }
    };

    Plotly.newPlot(ctx, [trace1, trace2], layout, { responsive: true, displayModeBar: false });
}

function renderRevenueTrend(data) {
    const ctx = document.getElementById('chart-revenue-trend');
    if (!ctx || !data) return;

    const trace = {
        x: data.hours,
        y: data.lost_revenue,
        type: 'bar',
        marker: { color: CONFIG.colors.warning }
    };

    const layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: CONFIG.colors.text, family: 'Inter' },
        margin: { t: 10, b: 40, l: 50, r: 10 },
        xaxis: { title: 'Hour of Day', gridcolor: CONFIG.colors.grid },
        yaxis: { title: 'Lost Revenue ($)', gridcolor: CONFIG.colors.grid }
    };

    Plotly.newPlot(ctx, [trace], layout, { responsive: true, displayModeBar: false });
}

function renderBatteryCliff(data) {
    const ctx = document.getElementById('chart-battery-cliff');
    const colors = data.labels.map(label => {
        if (label.includes("0-20")) return CONFIG.colors.killZone;
        if (label.includes("30-40") || label.includes("40-50") || label.includes("50-60")) return CONFIG.colors.goldilocks;
        if (label.includes("80-100")) return CONFIG.colors.warning;
        return CONFIG.colors.primary;
    });

    const trace = {
        x: data.labels,
        y: data.values,
        type: 'bar',
        marker: { color: colors },
        text: data.values.map(v => `${v}%`),
        textposition: 'auto',
        hovertemplate: '<b>%{x}</b><br>Canc Rate: %%{y}%<extra></extra>'
    };

    const layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: CONFIG.colors.text, family: 'Inter' },
        margin: { t: 20, b: 40, l: 40, r: 20 },
        xaxis: { gridcolor: CONFIG.colors.grid },
        yaxis: { gridcolor: CONFIG.colors.grid, title: 'Cancellation Rate (%)' },
        shapes: [{
            type: 'line', x0: -0.5, x1: 6.5, y0: 29.6, y1: 29.6,
            line: { color: 'gray', width: 2, dash: 'dot' }
        }]
    };

    Plotly.newPlot(ctx, [trace], layout, { responsive: true, displayModeBar: false });
}

function renderHeapmap(data) {
    if (!data) return;
    const ctx = document.getElementById('chart-heatmap');

    // Sort logic to make sure Zone 1 is at top or bottom? Plotly heatmap default is bottom-up.
    // Let's keep data order.

    const trace = {
        z: data.z,
        x: data.x,
        y: data.y,
        type: 'heatmap',
        colorscale: [
            [0, '#10b981'], [0.3, '#3b82f6'], [0.5, '#f59e0b'], [1, '#ef4444']
        ],
        hovertemplate: '<b>%{y}</b><br>Hour: %{x}:00<br>Canc: %{z:.1f}%<extra></extra>'
    };

    const layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: CONFIG.colors.text, family: 'Inter' },
        margin: { t: 20, b: 50, l: 100, r: 20 },
        xaxis: { title: 'Hour of Day (0-23)' }
    };

    Plotly.newPlot(ctx, [trace], layout, { responsive: true, displayModeBar: false });
}

function renderInfraParadox(data) {
    if (!data) return;
    const ctx = document.getElementById('chart-infra-paradox');
    const trace = {
        x: data.labels,
        y: data.values,
        type: 'bar',
        marker: { color: [CONFIG.colors.primary, CONFIG.colors.warning] },
        text: data.values.map(v => `${v}%`),
        textposition: 'auto'
    };
    const layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: CONFIG.colors.text, family: 'Inter' },
        margin: { t: 20, b: 30, l: 30, r: 10 },
        yaxis: { range: [0, 40], gridcolor: CONFIG.colors.grid }
    };
    Plotly.newPlot(ctx, [trace], layout, { responsive: true, displayModeBar: false });
}

// Table Logic
function renderTable(page) {
    const tbody = document.getElementById('data-table-body');
    const start = (page - 1) * CONFIG.itemsPerPage;
    const end = start + CONFIG.itemsPerPage;
    const items = rawTableData.slice(start, end);

    tbody.innerHTML = items.map(row => `
        <tr class="hover:bg-gray-800 transition">
            <td class="p-3 font-mono text-xs">${String(row.id).substring(0, 8)}...</td>
            <td class="p-3">${row.city}</td>
            <td class="p-3">${row.hour}:00</td>
            <td class="p-3">Zone ${row.zone}</td>
            <td class="p-3">
                <span class="${row.battery < 20 ? 'text-red-400 font-bold' : 'text-green-400'}">
                    ${row.battery}%
                </span>
            </td>
            <td class="p-3">
                <span class="px-2 py-1 rounded text-xs ${row.status === 'Cancelled' ? 'bg-red-900 text-red-200' : 'bg-green-900 text-green-200'}">
                    ${row.status}
                </span>
            </td>
        </tr>
    `).join('');

    document.getElementById('page-indicator').innerText = `Page ${page}`;
    document.getElementById('btn-prev').disabled = page === 1;
    document.getElementById('btn-next').disabled = end >= rawTableData.length;
}

function setupPagination() {
    document.getElementById('btn-prev').addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            renderTable(currentPage);
        }
    });

    document.getElementById('btn-next').addEventListener('click', () => {
        if (currentPage * CONFIG.itemsPerPage < rawTableData.length) {
            currentPage++;
            renderTable(currentPage);
        }
    });
}

// Utility
function animateValue(id, start, end, duration, suffix = "", prefix = "") {
    const obj = document.getElementById(id);
    if (!obj) return;
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const value = progress * (end - start) + start;
        const displayValue = Number.isInteger(end) ? Math.floor(value) : value.toFixed(1);
        obj.innerHTML = prefix + displayValue + suffix;
        if (progress < 1) window.requestAnimationFrame(step);
    };
    window.requestAnimationFrame(step);
}

function downloadReport() {
    alert("Downloading report...");
}
