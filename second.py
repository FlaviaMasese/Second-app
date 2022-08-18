import dash  # version 1.13.1
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
sparklingdf=pd.read_csv(r'C:\Users\flavi\OneDrive\Desktop\Dataset\Sparkling.csv')
#df.rename(columns={'under_trial': 'under trial', 'state_name': 'state'}, inplace=True)
template_theme1 = "sketchy"
template_theme2 = "darkly"
url_theme1 = dbc.themes.SKETCHY
url_theme2 = dbc.themes.DARKLY
theme_switch = ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2])

app = dash.Dash(__name__, external_stylesheets= [dbc.themes.SOLAR])

theme_colors = ["primary","danger","info","light","dark", "link",]
buttons = html.Div(
    [dbc.Button(f"{color}", color=f"{color}", size="sm") for color in theme_colors]
)
colors = html.Div(["Theme Colors:", buttons], className="mt-2")

app.layout = html.Div([
    html.Div(children=[
        html.Button('Add Chart', id='add-chart', n_clicks=0),
    ]),
    html.Div(id='container', children=[]),
    dbc.Container(
    dbc.Row(dbc.Col([ theme_switch, colors,])),
    className="m-4 dbc",
    fluid=True,
)
])


@app.callback(
    Output('container', 'children'),
    [Input('add-chart', 'n_clicks')],
    [State('container', 'children')]
)
def display_graphs(n_clicks, div_children):
    new_child = html.Div(
        style={'width': '45%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10,'color': 'blue',},
        children=[
            dcc.Graph(
                id={
                    'type': 'dynamic-graph',
                    'index': n_clicks
                },
                figure={}
            ),
            dcc.RadioItems(
                id={
                    'type': 'dynamic-choice',
                    'index': n_clicks
                },
                options=[{'label': 'Bar Chart', 'value': 'bar'},
                         {'label': 'Line Chart', 'value': 'line'},
                         {'label': 'Pie Chart', 'value': 'pie'}],
                value='bar',
            ),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-s',
                    'index': n_clicks
                },
                options=[{'label': s, 'value': s} for s in np.sort(sparklingdf['Country'].unique())],
                multi=True,
                value=["Select Country"],
            ),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-ctg',
                    'index': n_clicks
                },
                options=[{'label': c, 'value': c} for c in ['Region', 'Name']],
                value='Name',
                clearable=False
            ),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-num',
                    'index': n_clicks
                },
                options=[{'label': n, 'value': n} for n in ['NumberOfRatings', 'Price', 'Rating']],
                value='Price',
                clearable=False
            )
        ]
    )
    div_children.append(new_child)
    return div_children


@app.callback(
    Output({'type': 'dynamic-graph', 'index': MATCH}, 'figure'),
    [Input(component_id={'type': 'dynamic-dpn-s', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-dpn-ctg', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-dpn-num', 'index': MATCH}, component_property='value'),
     Input({'type': 'dynamic-choice', 'index': MATCH}, 'value'),
     Input(ThemeSwitchAIO.ids.switch("theme"), "value")]
)
def update_graph(s_value, ctg_value, num_value, chart_choice,toggle):
    print(s_value)
    template = template_theme1 if toggle else template_theme2
    dff = sparklingdf[sparklingdf['Country'].isin(s_value)]

    if chart_choice == 'bar':
        dff = dff.groupby([ctg_value], as_index=False)[['NumberOfRatings', 'Price', 'Rating']].sum()
        fig = px.bar(dff, x=ctg_value, y=num_value,template=template)
        return fig
    elif chart_choice == 'line':
        if len(s_value) == 0:
            return {}
        else:
            dff = dff.groupby([ctg_value, 'Year'], as_index=False)[['NumberOfRatings', 'Price', 'Rating']].sum()
            fig = px.line(dff, x='Year', y=num_value, color=ctg_value,template=template)
            return fig
    elif chart_choice == 'pie':
        fig = px.pie(dff, names=ctg_value, values=num_value,template=template)
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)