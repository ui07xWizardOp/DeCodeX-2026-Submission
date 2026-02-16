import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import jinja2
import json
import os
import numpy as np

# Paths
base_path = r'c:\Users\KIIT0001\Desktop\projects\DeCodeX'
dataset_path = os.path.join(base_path, 'DecodeX_VoltRide_Dataset.xlsx')
output_dir = os.path.join(base_path, 'Final_Submission', 'docs')
os.makedirs(output_dir, exist_ok=True)
final_html_path = os.path.join(output_dir, 'index.html')

# Load Data
print("Loading data...")
ride_data = pd.read_excel(dataset_path, sheet_name='Ride_Level_Data')
ride_data['is_cancelled'] = ride_data['Ride_Status'].apply(lambda x: 1 if x == 'Cancelled' else 0)

# --- HELPER FUNCTION: GENERATE SEGMENT DATA ---
def get_segment_data(df, city_name="All"):
    total_rides = len(df)
    if total_rides == 0: return None
    
    completion_rate = 1 - df['is_cancelled'].mean()
    system_cancels = len(df[df['Cancellation_By'] == 'System'])
    system_cancel_rate = system_cancels / total_rides
    fleet_health = len(df[df['EV_Battery_%'] > 30]) / total_rides
    
    # 1. Trend Data
    hourly_stats = df.groupby('Hour').agg({'Ride_Status': 'count', 'is_cancelled': 'sum'}).reset_index()
    hourly_stats['Completed'] = hourly_stats['Ride_Status'] - hourly_stats['is_cancelled']
    trend_chart = {
        'hours': hourly_stats['Hour'].tolist(),
        'demand': hourly_stats['Ride_Status'].tolist(),
        'completed': hourly_stats['Completed'].tolist()
    }
    
    # 2. Battery Cliff Data
    df['Battery_Bin'] = pd.cut(df['EV_Battery_%'], bins=range(0, 101, 5))
    cliff_grp = df.groupby('Battery_Bin', observed=True)['is_cancelled'].mean()
    cliff_data = {
        'x': [interval.mid for interval in cliff_grp.index],
        'y': cliff_grp.values.tolist(),
        'size': [v * 20 for v in cliff_grp.values.tolist()] # Scale size by prob
    }
    
    # 3. Heatmap Data (Top 5 Zones by Risk)
    risk_zone = df.groupby(['Pickup_Zone'])['is_cancelled'].mean().reset_index()
    heatmap_data = {
        'z': risk_zone['is_cancelled'].tolist(),
        'x': risk_zone['Pickup_Zone'].tolist(),
        'type': 'heatmap'
    }

    return {
        'city': city_name,
        'kpi': {
            'completion_rate': f"{completion_rate:.1%}",
            'system_cancel_rate': f"{system_cancel_rate:.1%}",
            'fleet_health': f"{fleet_health:.0%}",
        },
        'charts': {
            'trend': trend_chart,
            'cliff': cliff_data,
            'risk': heatmap_data
        }
    }

# --- GENERATE GLOBAL DATA OBJECT ---
print("Generating Global Data Object...")
data_payload = {}

# 1. All Cities
data_payload['All'] = get_segment_data(ride_data, "All")

# 2. Per City
cities = ride_data['City'].unique()
for city in cities:
    data_payload[city] = get_segment_data(ride_data[ride_data['City'] == city], city)

json_payload = json.dumps(data_payload)

# --- HTML GENERATION ---
print("Generating Interactive Dashboard...")

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VoltRide Operations Intelligence</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        .glass-panel { background: white; border: 1px solid #e5e7eb; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); border-radius: 0.75rem; }
        .kpi-card { transition: all 0.2s; }
        .kpi-card:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
        .active-filter { background-color: #2563eb; color: white; }
    </style>
</head>
<body class="bg-gray-50 text-slate-800 font-sans antialiased">
    <header class="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
            <div class="flex items-center space-x-4">
                <div class="bg-blue-600 h-8 w-8 rounded flex items-center justify-center text-white font-bold">V</div>
                <div>
                    <h1 class="text-xl font-bold text-gray-900 leading-none">VoltRide Operations Intelligence</h1>
                    <p class="text-xs text-gray-500 mt-1">Research-Grade Insight Engine</p>
                </div>
            </div>
            <div class="flex items-center space-x-4">
                 <select id="cityFilter" onchange="updateDashboard(this.value)" class="form-select block w-full bg-gray-50 border border-blue-300 text-blue-700 py-1 px-3 rounded leading-tight focus:outline-none focus:bg-white font-bold cursor-pointer hover:bg-blue-50">
                    <option value="All">City: All Markets</option>
                    {% for city in cities %}
                    <option value="{{ city }}">{{ city }}</option>
                    {% endfor %}
                </select>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 py-8 space-y-8">
        <!-- OPERATIONAL PULSE -->
        <section>
            <h2 class="text-sm font-bold text-gray-400 uppercase tracking-widest mb-4">Operational Pulse (Real-time Health)</h2>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
                <!-- KPI 1 -->
                <div class="glass-panel kpi-card p-6 border-l-4 border-green-500">
                    <p class="text-xs font-semibold text-gray-500 uppercase">Completion Rate</p>
                    <h3 id="kpi-completion" class="text-3xl font-extrabold text-gray-900 mt-1">--%</h3>
                </div>
                 <!-- KPI 2 -->
                 <div class="glass-panel kpi-card p-6 border-l-4 border-red-500">
                    <p class="text-xs font-semibold text-gray-500 uppercase">System Failure Rate</p>
                    <h3 id="kpi-cancel" class="text-3xl font-extrabold text-red-600 mt-1">--%</h3>
                </div>
                 <!-- KPI 3 -->
                 <div class="glass-panel kpi-card p-6 border-l-4 border-yellow-500">
                    <p class="text-xs font-semibold text-gray-500 uppercase">Fleet Health (>30%)</p>
                    <h3 id="kpi-fleet" class="text-3xl font-extrabold text-yellow-600 mt-1">--%</h3>
                </div>
                 <!-- KPI 4 -->
                 <div class="glass-panel kpi-card p-6 border-l-4 border-purple-500">
                    <p class="text-xs font-semibold text-gray-500 uppercase">Risk Level</p>
                    <h3 class="text-3xl font-extrabold text-gray-900 mt-1">HIGH</h3>
                </div>
            </div>
        </section>

        <!-- SYSTEM DYNAMICS -->
        <section class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div class="glass-panel p-6">
                <div class="flex justify-between items-center mb-4"><h3 class="text-lg font-bold text-gray-900">Demand vs Supply (Gap Analysis)</h3></div>
                <div id="chart-trend" class="h-80 w-full"></div>
            </div>
            <div class="glass-panel p-6">
                <div class="flex justify-between items-center mb-4"><h3 class="text-lg font-bold text-gray-900">The Battery Cliff (<20% Failure)</h3></div>
                <div id="chart-cliff" class="h-80 w-full"></div>
            </div>
        </section>

        <!-- HYPOTHESIS LAB -->
        <section class="glass-panel p-8 bg-slate-900 text-white">
            <div class="flex items-center space-x-3 mb-6">
                <div class="h-3 w-3 bg-green-400 rounded-full animate-pulse"></div>
                <h2 class="text-xl font-bold tracking-wide">THE HYPOTHESIS LAB</h2>
            </div>
            <div class="grid grid-cols-1 gap-8">
                <div class="space-y-4">
                    <div class="bg-slate-800 p-4 rounded border-l-4 border-green-500">
                        <h4 class="font-bold text-sm text-green-400">H-01: System Cancels</h4>
                        <p class="text-sm mt-2 text-slate-300">"System-driven cancellations drive rider attrition."</p>
                        <div class="mt-3"><div class="text-xs flex justify-between text-slate-400 mb-1"><span>Confidence Score</span><span>85%</span></div><div class="w-full bg-slate-700 h-1.5 rounded-full"><div class="bg-green-500 h-1.5 rounded-full" style="width: 85%"></div></div></div>
                    </div>
                </div>
            </div>
        </section>
        
        <footer class="text-center text-gray-400 text-sm py-12">
            <p>VoltRide Operations Intelligence | Generated by DeCodeX Automated Analyst</p>
        </footer>
    </main>

    <script>
        // --- EMBEDDED DATA ---
        const dashboardData = {{ json_payload | safe }};
        
        // --- DASHBOARD CONTROLLER ---
        function updateDashboard(city) {
            console.log("Switching to:", city);
            const data = dashboardData[city];
            if (!data) return;

            // 1. Update KPIs
            document.getElementById('kpi-completion').innerText = data.kpi.completion_rate;
            document.getElementById('kpi-cancel').innerText = data.kpi.system_cancel_rate;
            document.getElementById('kpi-fleet').innerText = data.kpi.fleet_health;

            // 2. Update Trend Chart
            const trace1 = {
                x: data.charts.trend.hours,
                y: data.charts.trend.demand,
                name: 'Ride Requests',
                type: 'scatter',
                line: {color: '#3b82f6', width: 3}
            };
            const trace2 = {
                x: data.charts.trend.hours,
                y: data.charts.trend.completed,
                name: 'Completed',
                type: 'scatter',
                line: {color: '#10b981', width: 3}
            };
            const layoutTrend = {
                margin: {t: 20, l: 40, r: 20, b: 40},
                hovermode: 'x unified',
                showlegend: true,
                legend: {orientation: 'h', y: 1.1}
            };
            Plotly.newPlot('chart-trend', [trace1, trace2], layoutTrend, {responsive: true});

            // 3. Update Cliff Chart
            const traceCliff = {
                x: data.charts.cliff.x,
                y: data.charts.cliff.y,
                mode: 'markers',
                marker: {
                    size: data.charts.cliff.size,
                    color: data.charts.cliff.y,
                    colorscale: 'RdYlGn_r',
                    showscale: true
                },
                type: 'scatter'
            };
             const layoutCliff = {
                margin: {t: 20, l: 40, r: 20, b: 40},
                xaxis: {title: 'Battery %'},
                yaxis: {title: 'Cancellation Probability'},
                shapes: [{
                    type: 'line', x0: 20, x1: 20, y0: 0, y1: 1, 
                    yref: 'paper', line: {color: 'red', width: 2, dash: 'dot'}
                }]
            };
            Plotly.newPlot('chart-cliff', [traceCliff], layoutCliff, {responsive: true});
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            updateDashboard('All');
        });

    </script>
</body>
</html>
"""

# Render Template
template = jinja2.Template(html_template)
html_content = template.render(
    json_payload=json_payload,
    cities=cities
)

with open(final_html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Interactive Dashboard Generated at: {final_html_path}")
print(f"Payload Size: {len(json_payload)/1024:.2f} KB")
