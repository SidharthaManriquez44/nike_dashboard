from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State

# ----------------------
# Simulate sample data
# ----------------------

def load_data(start_date=None, end_date=None):
    """Generate dummy data for the dashboard. Replace with your actual source."""
    rng = pd.date_range(end=datetime.today(), periods=180, freq='D')
    df = pd.DataFrame({'date': rng})

    np.random.seed(42)
    # Revenue trend
    base_revenue = 6_000_000
    seasonality = 1 + 0.15 * np.sin(np.linspace(0, 6.28 * 3, len(rng)))
    noise = np.random.normal(0, 0.04, len(rng))
    df['revenue'] = (base_revenue * seasonality * (1 + noise)).round(0)

    # Traffic & conversion
    df['sessions'] = (200_000 * (1 + 0.6 * np.sin(np.linspace(0, 3.14, len(rng)))) + np.random.randint(-15000, 15000, len(rng))).astype(int)
    df['conversion_rate'] = (0.015 + 0.005 * np.cos(np.linspace(0, 6.28, len(rng)))) + np.random.normal(0, 0.0015, len(rng))
    df['orders'] = (df['sessions'] * df['conversion_rate']).round().astype(int)
    df['aov'] = (90 + 20 * np.cos(np.linspace(0, 3.14, len(rng))) + np.random.normal(0, 3, len(rng))).round(2)

    # Regions
    regions = ['Americas', 'EMEA', 'APAC']
    region_share = np.array([[0.55, 0.30, 0.15]])
    df_regions = []
    for r in regions:
        share = region_share[0][regions.index(r)]
        df_regions.append(pd.DataFrame({'date': rng, 'region': r, 'revenue': (df['revenue'] * share * (1 + np.random.normal(0, 0.05, len(rng))))}))
    df_regions = pd.concat(df_regions, ignore_index=True)

    # Inventory
    df['inventory_turnover'] = (6 + 1.0 * np.sin(np.linspace(0, 6.28, len(rng)))) + np.random.normal(0, 0.2, len(rng))
    df['stockout_rate'] = (0.02 + 0.01 * np.cos(np.linspace(0, 6.28, len(rng)))) + np.random.normal(0, 0.002, len(rng))

    # NPS simulation
    df['nps'] = (45 + 10 * np.sin(np.linspace(0, 3.14, len(rng)))) + np.random.normal(0, 3, len(rng))

    # Model forecast example (MAPE)
    df['forecast'] = df['revenue'].shift(7).fillna(method='bfill') * (1 + np.random.normal(0, 0.03, len(rng)))
    df['mape'] = ( (df['revenue'] - df['forecast']).abs() / df['revenue'] ).rolling(14).mean().fillna(0)

    # Combine into a single object
    data = {'daily': df, 'regions': df_regions}

    # Filter by dates if provided
    if start_date is not None:
        for k in data:
            data[k] = data[k][data[k]['date'] >= pd.to_datetime(start_date)].copy()
    if end_date is not None:
        for k in data:
            data[k] = data[k][data[k]['date'] <= pd.to_datetime(end_date)].copy()

    return data

# ----------------------
# Auxiliary functions
# ----------------------

def compute_overview_metrics(df):
    revenue = float(df['revenue'].sum())
    yoy_growth = ((df['revenue'].iloc[-1] - df['revenue'].iloc[0]) / max(df['revenue'].iloc[0], 1)) * 100
    digital_share = 0.62  # placeholder
    clv = 180.0  # placeholder
    nps = float(df['nps'].iloc[-1])
    inventory_turn = float(df['inventory_turnover'].mean())
    return {
        'revenue': revenue,
        'yoy_growth': round(yoy_growth, 2),
        'digital_share': round(digital_share * 100, 2),
        'clv': round(clv, 2),
        'nps': round(nps, 1),
        'inventory_turn': round(inventory_turn, 2)
    }

# ----------------------
# App
# ----------------------

app = Dash(__name__, title='Nike KPI Dashboard - Demo')
server = app.server

# Default data range
default_start = (datetime.today() - timedelta(days=90)).strftime('%Y-%m-%d')
default_end = datetime.today().strftime('%Y-%m-%d')

# Layout
app.layout = html.Div(style={'font-family': 'Arial, sans-serif', 'margin': '12px'}, children=[
    html.H1('Nike KPI Dashboard', style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            html.Label('Rango de fechas:'),
            dcc.DatePickerRange(
                id='date-range',
                start_date=default_start,
                end_date=default_end,
                display_format='YYYY-MM-DD'
            )
        ], style={'display': 'inline-block', 'margin-right': '30px'}),
        html.Div([
            html.Label('Canal:'),
            dcc.Dropdown(id='channel-select', options=[
                {'label': 'Todos', 'value': 'all'},
                {'label': 'Direct', 'value': 'direct'},
                {'label': 'Paid', 'value': 'paid'},
                {'label': 'Organic', 'value': 'organic'},
            ], value='all', clearable=False, style={'width': '200px'})
        ], style={'display': 'inline-block'})
    ], style={'margin-bottom': '18px'}),

    # KPI cards
    html.Div(id='kpi-cards', style={'display': 'grid', 'gridTemplateColumns': 'repeat(6, 1fr)', 'gap': '10px'}),

    # Charts grid
    html.Div(style={'display': 'grid', 'gridTemplateColumns': 'repeat(2, 1fr)', 'gap': '18px', 'margin-top': '18px'}, children=[
        html.Div(children=[
            dcc.Graph(id='revenue-timeseries')
        ], style={'background': '#ffffff', 'padding': '12px', 'borderRadius': '8px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.12)'}),

        html.Div(children=[
            dcc.Graph(id='conversion-funnel')
        ], style={'background': '#ffffff', 'padding': '12px', 'borderRadius': '8px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.12)'}),

        html.Div(children=[
            dcc.Graph(id='region-revenue-map')
        ], style={'background': '#ffffff', 'padding': '12px', 'borderRadius': '8px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.12)'}),

        html.Div(children=[
            dcc.Graph(id='inventory-metrics')
        ], style={'background': '#ffffff', 'padding': '12px', 'borderRadius': '8px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.12)'}),
    ]),

    # Lower row: model performance + tables
    html.Div(style={'display': 'grid', 'gridTemplateColumns': 'repeat(2, 1fr)', 'gap': '18px', 'margin-top': '18px'}, children=[
        html.Div(children=[
            dcc.Graph(id='forecast-error')
        ], style={'background': '#ffffff', 'padding': '12px', 'borderRadius': '8px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.12)'}),

        html.Div(children=[
            dcc.Graph(id='nps-trend')
        ], style={'background': '#ffffff', 'padding': '12px', 'borderRadius': '8px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.12)'}),
    ]),

    html.Div(style={'height': '30px'})
])

# ----------------------
# Callbacks
# ----------------------

@app.callback(
    Output('kpi-cards', 'children'),
    Output('revenue-timeseries', 'figure'),
    Output('conversion-funnel', 'figure'),
    Output('region-revenue-map', 'figure'),
    Output('inventory-metrics', 'figure'),
    Output('forecast-error', 'figure'),
    Output('nps-trend', 'figure'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
    Input('channel-select', 'value')
)
def update_dashboard(start_date, end_date, channel):
    data = load_data(start_date=start_date, end_date=end_date)
    df = data['daily']
    df_regions = data['regions']

    # Overview metrics
    overview = compute_overview_metrics(df)

    # KPI cards (6 cards)
    card_style = {
        'background': '#0f172a', 'color': 'white', 'padding': '12px', 'borderRadius': '8px',
        'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center', 'alignItems': 'flex-start'
    }
    cards = []
    cards.append(html.Div([html.Div('Revenue (period)', style={'fontSize': '12px', 'opacity': 0.8}), html.Div(f"${overview['revenue']:,.0f}", style={'fontSize': '20px', 'fontWeight': '700'})], style=card_style))
    cards.append(html.Div([html.Div('YoY growth', style={'fontSize': '12px', 'opacity': 0.8}), html.Div(f"{overview['yoy_growth']}%", style={'fontSize': '20px', 'fontWeight': '700'})], style=card_style))
    cards.append(html.Div([html.Div('Digital revenue share', style={'fontSize': '12px', 'opacity': 0.8}), html.Div(f"{overview['digital_share']}%", style={'fontSize': '20px', 'fontWeight': '700'})], style=card_style))
    cards.append(html.Div([html.Div('CLV', style={'fontSize': '12px', 'opacity': 0.8}), html.Div(f"${overview['clv']}", style={'fontSize': '20px', 'fontWeight': '700'})], style=card_style))
    cards.append(html.Div([html.Div('NPS', style={'fontSize': '12px', 'opacity': 0.8}), html.Div(f"{overview['nps']}", style={'fontSize': '20px', 'fontWeight': '700'})], style=card_style))
    cards.append(html.Div([html.Div('Inventory turnover', style={'fontSize': '12px', 'opacity': 0.8}), html.Div(f"{overview['inventory_turn']}", style={'fontSize': '20px', 'fontWeight': '700'})], style=card_style))

    # Revenue timeseries
    fig_rev = px.line(df, x='date', y='revenue', title='Revenue (Period)', labels={'revenue': 'Revenue', 'date': 'Date'})
    fig_rev.update_traces(mode='lines+markers')

    # Conversion funnel (Sessions -> Orders -> Completed orders)
    latest = df.iloc[-1]
    funnel_values = [int(latest['sessions']), int(latest['orders']), int(latest['orders'] * 0.95)]
    funnel_labels = ['Sessions', 'Orders', 'Completed Orders']
    fig_funnel = go.Figure(go.Funnel(y=funnel_labels, x=funnel_values, textinfo='value+percent initial'))
    fig_funnel.update_layout(title='Funnel de conversión (último día)')

    # Region revenue bar (simple substitute for map)
    region_sum = df_regions.groupby('region')['revenue'].sum().reset_index()
    fig_region = px.pie(region_sum, values='revenue', names='region', title='Distribución de revenue por región')

    # Inventory metrics
    fig_inv = go.Figure()
    fig_inv.add_trace(go.Scatter(x=df['date'], y=df['inventory_turnover'], mode='lines+markers', name='Inventory Turnover'))
    fig_inv.add_trace(go.Scatter(x=df['date'], y=df['stockout_rate'], mode='lines', name='Stockout Rate', yaxis='y2'))
    fig_inv.update_layout(title='Inventario: Turnover y Stockout rate', yaxis=dict(title='Turnover'), yaxis2=dict(title='Stockout rate', overlaying='y', side='right'))

    # Forecast error (MAPE)
    fig_mape = px.line(df, x='date', y='mape', title='MAPE (rolling 14d)')

    # NPS trend
    fig_nps = px.line(df, x='date', y='nps', title='NPS (Trend)')

    return cards, fig_rev, fig_funnel, fig_region, fig_inv, fig_mape, fig_nps

# ----------------------
# Run
# ----------------------
if __name__ == '__main__':
    app.run(debug=True)
