import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import plotly.graph_objs as go

import plotly.io as pio
pio.templates.default = "plotly_dark"

file_path = 'kc_house_data.csv'
data = pd.read_csv(file_path)
data['date'] = pd.to_datetime(data['date'])
data['year'] = pd.to_datetime(data['date'], unit='s').dt.year
data['month'] = pd.to_datetime(data['date'], unit='s').dt.month

train_data = data.copy()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# navbar dashboard
app.layout = html.Div(
    style={'backgroundColor': '#1d253a', 'padding': '18px', 'padding-left': '24px','padding-right': '24px'},
    children=[
        html.Div([
            html.H1("Dashboard Real Estate", style={'color': 'white', 'font-weight': 'bold'}),
            html.Link(href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css", rel="stylesheet"),

            html.Div([
                dbc.Button("All", id='btn-all', n_clicks=0, color="primary", className="mr-1", style={'margin-right': '10px','width': '100px'}),
                dbc.Button("2014", id='btn-2014', n_clicks=0, color="primary", className="mr-1", style={'margin-right': '10px','width': '100px'}),
                dbc.Button("2015", id='btn-2015', n_clicks=0, color="primary", className="mr-1", style={'margin-right': '10px','width': '100px'})
            ], style={'text-align': 'left'}),
        ], style={'display': 'flex', 'justify-content': 'space-between', 'padding': '18px'}),

#Garis dashboard
         html.Hr(style={'border-top': '3px solid white'}),

# isi dashboard
        dbc.Row([
            # total rumah
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.Div([
                            html.Div([
                                html.H4("Total Rumah", className="card-title", style={'color': 'white', 'text-align': 'center', 'margin-bottom': '5px'}),
                                html.I(className="fas fa-home fa-3x", style={'color': 'white', 'margin-top': '5px'}),
                            ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'justifyContent': 'center'}),
                            html.Div([
                                html.P(id='total-houses', className="card-text", style={'color': 'white', 'text-align': 'center'}),
                            ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                        ], style={'display': 'flex', 'flexDirection': 'column'}),
                    ]),
                    color="#252C40",
                    inverse=True,
                    style={'backgroundColor': '#252C40'}
                ),
                width=3
            ),
            
            #luas basement
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.Div([
                            html.Div([
                                html.H4("Max Luas Basement", className="card-title", style={'color': 'white', 'text-align': 'center', 'margin-bottom': '5px'}),
                                html.I(className="fas fa-chart-bar fa-3x", style={'color': 'white', 'margin-top': '5px'}),
                            ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'justifyContent': 'center'}),
                            html.Div([
                                html.P(id='total-max-basement', className="card-text", style={'color': 'white', 'text-align': 'center'}),
                            ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                        ], style={'display': 'flex', 'flexDirection': 'column'}),
                    ]),
                    color="#252C40",
                    inverse=True,
                    style={'backgroundColor': '#252C40'}
                ),
                width=3
            ),
        ], style={'margin-top': '20px'}),

        dbc.Row([
            dbc.Col(
                dcc.Graph(id='donut-chart'),
                width=6,
                style={'backgroundColor': '#252C40'}
                ),
            dbc.Col(
                dcc.Graph(id='clustered-bar-chart'),
                width=6,
                style={'backgroundColor': '#252C40'}
                ),
            
        ], style={'margin-top': '20px'}),

        dbc.Row([
            dbc.Col(
                dcc.Graph(id='price-chart'),
                width=6,
                style={'backgroundColor': '#252C40'}
                ),
            dbc.Col(
                dcc.Graph(id='area-chart'),
                width=6,
                style={'backgroundColor': '#252C40'}
                ),
            
        ], style={'margin-top': '20px'}),

        dbc.Row([
            html.H2("Forecasting", style={'color': 'white', 'font-weight': 'bold'}),
            html.Hr(style={'border-top': '1px solid white'}),
            dbc.Col(
                dcc.Graph(id='forecasting-chart'),
                style={'backgroundColor': '#252C40'}
            ),
        ],  style={'margin-top': '20px'}),
        html.Div(id='output-data'),

    ]
)


#Callback

@app.callback(
    Output('clustered-bar-chart', 'figure'),
    [Input('btn-all', 'n_clicks'),
     Input('btn-2014', 'n_clicks'),
     Input('btn-2015', 'n_clicks')]
)

def update_clustered_bar_chart(btn_all, btn_2014, btn_2015):
    ctx = dash.callback_context
    if not ctx.triggered:
        df = data
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'btn-all':
            df = data
        elif button_id == 'btn-2014':
            df = data[data['date'].dt.year == 2014]
        else:
            df = data[data['date'].dt.year == 2015]

    fig = px.bar(df, x='grade', y='price', title='Harga Rumah berdasarkan Grade', barmode='group')
    fig.update_layout(
        xaxis_title='Grade',
        yaxis_title='Harga Rumah',
        plot_bgcolor='#252C40',
        paper_bgcolor='#252C40',
        font=dict(color='white')
    )
    return fig
@app.callback(
    Output('area-chart', 'figure'),
    [Input('btn-all', 'n_clicks'),
     Input('btn-2014', 'n_clicks'),
     Input('btn-2015', 'n_clicks')]
)

def update_area_chart(btn_all, btn_2014, btn_2015):
    ctx = dash.callback_context
    if not ctx.triggered:
        df = data
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'btn-all':
            df = data
        elif button_id == 'btn-2014':
            df = data[data['date'].dt.year == 2014]
        else:
            df = data[data['date'].dt.year == 2015]
    
    zipcode_count = df.groupby('zipcode')['id'].count().reset_index()
    fig = px.bar(zipcode_count, x='zipcode', y='id', title='Jumlah ID berdasarkan ZIP code')
    fig.update_xaxes(title='ZIP code')
    fig.update_yaxes(title='Jumlah ID')
    fig.update_traces(marker=dict(color='rgb(158, 218, 229)'))
    fig.update_layout(
        plot_bgcolor='#252C40',
        paper_bgcolor='#252C40',
        font=dict(color='white')
    )

    return fig
    
@app.callback(
    Output('forecasting-chart', 'figure'),
      [Input('btn-all', 'n_clicks'),
     Input('btn-2014', 'n_clicks'),
     Input('btn-2015', 'n_clicks')]
)

def update_forecasting_chart(btn_all, btn_2014, btn_2015):

    data_2015 = data[data['date'].dt.year == 2015]

    avg_prices_2015 = data_2015.groupby('month')['price'].mean().reset_index()

    train_X = avg_prices_2015[['month']]
    train_y = avg_prices_2015['price']

    model = LinearRegression()
    model.fit(train_X, train_y)

    future_month = 12
    prediction = model.predict([[future_month]])

    fig = px.line(avg_prices_2015, x='month', y='price', title='Prediksi Rata-rata Harga Rumah Tahun Depan')
    fig.add_trace(go.Scatter(x=[future_month], y=[prediction[0]], mode='lines+markers', 
                             marker=dict(color='red', size=10), name='Prediksi Rata-rata Harga Rumah di Tahun Depan'))
    fig.update_layout(  plot_bgcolor='#252C40',
                        paper_bgcolor='#252C40',
                        font=dict(color='white')
                      )
    return fig
        

@app.callback(
    Output('donut-chart', 'figure'),
    [Input('btn-all', 'n_clicks'),
     Input('btn-2014', 'n_clicks'),
     Input('btn-2015', 'n_clicks')]
)

def update_donut_chart(btn_all, btn_2014, btn_2015):
    ctx = dash.callback_context
    if not ctx.triggered:
        df = data
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'btn-all':
            df = data
        elif button_id == 'btn-2014':
            df = data[data['date'].dt.year == 2014]
        else:
            df = data[data['date'].dt.year == 2015]

    avg_sqft_basement = df.groupby('view')['sqft_basement'].mean().reset_index()
    fig = px.pie(avg_sqft_basement, values='sqft_basement', names='view', title='Rata-rata Luas Basement per View')
    fig.update_traces(textinfo='percent+label', hole=0.4)
    fig.update_layout(
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        plot_bgcolor='#252C40',
        paper_bgcolor='#252C40',
        font=dict(color='white')
    )
    return fig

@app.callback(
    Output('price-chart', 'figure'),
    [Input('btn-all', 'n_clicks'),
     Input('btn-2014', 'n_clicks'),
     Input('btn-2015', 'n_clicks')]
)

def update_price_chart(btn_all, btn_2014, btn_2015):
    ctx = dash.callback_context
    if not ctx.triggered:
        df = data
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'btn-all':
            df = data
        elif button_id == 'btn-2014':
            df = data[data['date'].dt.year == 2014]
        else:
            df = data[data['date'].dt.year == 2015]

    avg_prices = df.groupby('month')['price'].mean().reset_index()
    fig = px.line(avg_prices, x='month', y='price', title='Rata-rata Harga Rumah per Bulan')
    fig.update_traces(mode='markers+lines')
    fig.update_layout(
        plot_bgcolor='#252C40',
        paper_bgcolor='#252C40',
        font=dict(color='white')
    )
    fig.update_layout(  xaxis_title='Bulan', 
                        yaxis_title='Rata-rata Harga',
                        plot_bgcolor='#252C40',
                        paper_bgcolor='#252C40',
                        font=dict(color='white')
                      )
    return fig

@app.callback(
    Output('total-max-basement', 'children'),
    [Input('btn-all', 'n_clicks'),
     Input('btn-2014', 'n_clicks'),
     Input('btn-2015', 'n_clicks')]
)
def update_total_max_basement(btn_all, btn_2014, btn_2015):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'btn-all':
        max_basement = data['sqft_basement'].max()
        return f"{max_basement} sqft"
    elif button_id == 'btn-2014':
        data_2014 = data[data['date'].dt.year == 2014]
        max_basement_2014 = data_2014['sqft_basement'].max()
        return f"{max_basement_2014} sqft"
    elif button_id == 'btn-2015':
        data_2015 = data[data['date'].dt.year == 2015]
        max_basement_2015 = data_2015['sqft_basement'].max()
        return f"{max_basement_2015} sqft"

    return f"{data['sqft_basement'].max()} sqft"

@app.callback(
    Output('total-houses', 'children'),
    [Input('btn-all', 'n_clicks'),
     Input('btn-2014', 'n_clicks'),
     Input('btn-2015', 'n_clicks')]
)

def update_total_houses(btn_all, btn_2014, btn_2015):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
    if button_id == 'btn-all':
        return f"{len(data)}"
    elif button_id == 'btn-2014':
        data_2014 = data[data['date'].dt.year == 2014]
        return f"{len(data_2014)}"
    elif button_id == 'btn-2015':
        data_2015 = data[data['date'].dt.year == 2015]
        return f"{len(data_2015)}"
    else:
        return f"{len(data)}"
    
@app.callback(
    Output('output-data', 'children'),
    [Input('btn-all', 'n_clicks'),
     Input('btn-2014', 'n_clicks'),
     Input('btn-2015', 'n_clicks')]
)
def update_options(btn_all, btn_2014, btn_2015):
    pass

if __name__ == '__main__':
    app.run_server(debug=True)
