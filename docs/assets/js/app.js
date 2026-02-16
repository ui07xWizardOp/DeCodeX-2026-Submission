/**
 * VoltRide Dashboard Core Logic
 * Version: 1.0
 */

// Configuration
const CONFIG = {
    dataUrl: './assets/data/metrics.json',
    chartsUrl: './assets/data/charts.json',
    colors: {
        killZone: '#ef4444',
        goldilocks: '#10b981',
        warning: '#f59e0b',
        primary: '#3b82f6',
        text: '#f8fafc',
        grid: '#334155'
    }
};

// Initialization
document.addEventListener('DOMContentLoaded', async () => {
    console.log('⚡ VoltRide Dashboard Initializing...');

    try {
        const [metrics, charts] = await Promise.all([
            fetch(CONFIG.dataUrl).then(r => r.json()),
            fetch(CONFIG.chartsUrl).then(r => r.json())
        ]);

        renderKPIs(metrics.kpis);
        renderCharts(charts);
        console.log('Dashboard Loaded Successfully');
    } catch (error) {
        console.error('Initialization failed:', error);
        // Fallback for demo purposes if fetch fails locally without server
        // document.body.innerHTML += `<div style="position:fixed;bottom:0;background:red;color:white;padding:10px">Error loading data: ${error.message}. Is a local server running?</div>`;
    }
});

function renderKPIs(kpis) {
    // Animate Numbers
    animateValue("kpi-kill-zone", 0, kpis.kill_zone_rate, 2000, "%");
    animateValue("kpi-goldilocks", 0, kpis.goldilocks_rate, 2000, "%");
    animateValue("kpi-revenue", 0, kpis.revenue_loss / 1000, 2000, "K", "$");
}

function renderCharts(data) {
    renderBatteryCliff(data.battery_cliff);
    renderHeapmap(data.heatmap);
    renderInfraParadox(data.infra_paradox);
}

function renderBatteryCliff(data) {
    const ctx = document.getElementById('chart-battery-cliff');

    // Color logic: Red for <20%, Green for 30-60%, Yellow for >80%
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
        hoverinfo: 'x+y+text',
        hovertemplate: '<b>%{x}</b><br>Cancellation: %{y}%<extra></extra>'
    };

    const layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: CONFIG.colors.text, family: 'Inter' },
        margin: { t: 20, b: 40, l: 40, r: 20 },
        xaxis: {
            gridcolor: CONFIG.colors.grid,
            zeroline: false
        },
        yaxis: {
            gridcolor: CONFIG.colors.grid,
            zeroline: false,
            title: 'Cancellation Rate (%)'
        },
        shapes: [{
            type: 'line',
            x0: -0.5, x1: 6.5,
            y0: 29.6, y1: 29.6,
            line: { color: 'gray', width: 2, dash: 'dot' }
        }],
        annotations: [{
            x: 0, y: 80,
            xref: 'x', yref: 'y',
            text: 'KILL ZONE',
            showarrow: true,
            arrowhead: 2,
            ax: 0, ay: -40,
            font: { color: CONFIG.colors.killZone, size: 12, weight: 'bold' }
        }]
    };

    Plotly.newPlot(ctx, [trace], layout, { responsive: true, displayModeBar: false });
}

function renderHeapmap(data) {
    if (!data) return; // Handle missing heatmap data gracefully

    const ctx = document.getElementById('chart-heatmap');

    const trace = {
        z: data.z,
        x: data.x,
        y: data.y,
        type: 'heatmap',
        colorscale: [
            [0, '#10b981'],   // Green (Low Risk)
            [0.3, '#3b82f6'], // Blue
            [0.5, '#f59e0b'], // Yellow
            [1, '#ef4444']    // Red (High Risk)
        ],
        hoverongaps: false,
        hovertemplate: '<b>%{y}</b><br>Hour: %{x}:00<br>Canc: %{z:.1f}%<extra></extra>'
    };

    const layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: CONFIG.colors.text, family: 'Inter' },
        margin: { t: 20, b: 50, l: 80, r: 20 }, // More left margin for Zone names
        xaxis: { title: 'Hour of Day (0-23)' },
        yaxis: { tickmode: 'linear' }
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
        width: 0.5,
        marker: { color: [CONFIG.colors.primary, CONFIG.colors.warning] },
        text: data.values.map(v => `${v}%`),
        textposition: 'auto',
    };

    const layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: CONFIG.colors.text, family: 'Inter' },
        margin: { t: 20, b: 30, l: 30, r: 10 },
        yaxis: { range: [0, 40] } // Fix range to show slight difference clearly? Or maybe auto.
    };

    Plotly.newPlot(ctx, [trace], layout, { responsive: true, displayModeBar: false });
}

// Utility: Number Animation
function animateValue(id, start, end, duration, suffix = "", prefix = "") {
    const obj = document.getElementById(id);
    if (!obj) return;

    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const value = Math.floor(progress * (end - start) + start);
        // Use toFixed(1) for percentages if needed, currently Math.floor
        const displayValue = Number.isInteger(end) ? value : (progress * (end - start) + start).toFixed(1);
        obj.innerHTML = prefix + displayValue + suffix;
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Utility: Download Report
function downloadReport() {
    alert("This would trigger a PDF download. In submission, checks 'submission_package/'.");
}
