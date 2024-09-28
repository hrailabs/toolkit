import dash_bootstrap_components as dbc
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import yaml

import model
import src.app_layout_functions as alf

with open('config.yaml') as f:
    config = yaml.safe_load(f)

# run model
model = model.Model(config)
df_prep, tbl = model.prep()
df_results = model.analysis(df_prep.copy(), tbl)

# app components
external_stylesheets = [dbc.themes.BOOTSTRAP]
app_layout: dbc.Container = alf.run_layout_build(df_results)

# initialize the app
app = dash.Dash(
    __name__, 
    external_stylesheets=external_stylesheets
)

# layout the app
app.layout = app_layout

"""# Callback to update the graph based on dropdown selection
@app.callback(
    Output('category-graph', 'figure'),
    [Input('category-dropdown', 'value')]
)
def update_graph(
    selected_category
):
    filtered_df = df[df['Category'] == selected_category]
    #fig = px.scatter(filtered_df, x='Value', y='Other Value', title=f"Category {selected_category}")
    return fig
"""
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)