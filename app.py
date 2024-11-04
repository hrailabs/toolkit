import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import io
import base64
import pandas as pd

import model_app as mod
import src.app_layout_functions as alf

# app components
external_stylesheets = [dbc.themes.BOOTSTRAP]

# Initialize the app
app = dash.Dash(
    __name__, 
    external_stylesheets=external_stylesheets
)

app_layout: dbc.Container = html.Div(
    [
        dcc.Store(id='store-data'),

        # Disclaimer Section
        alf.div_disclaimer(),

        # Main Application Layout (initially hidden)
        dbc.Container(
            id='main_app_layout', 
            children=alf.run_layout_build(pd.DataFrame()),
            style={'display': 'none'}  # Hide the main layout initially
        ),
    ]
)

# Layout the app
app.layout = app_layout

#server = app.server  # Expose the Flask app as `server` for App Engine


# Callbacks
@app.callback(
    Output('continue_button', 'disabled'),
    Input('accept_disclaimer', 'value')
)
def toggle_continue_button(accepted_values):
    return 'accepted' not in accepted_values

@app.callback(
    Output('disclaimer', 'style'),
    Output('main_app_layout', 'style'),
    Input('continue_button', 'n_clicks'),
    prevent_initial_call=True
)
def update_layout(n_clicks):
    # Hide the disclaimer and show the main layout when the continue button is clicked
    return {'display': 'none'}, {'display': 'block'}

@app.callback(
    Output("tooltip", "is_open"),
    [Input("tooltip-icon", "n_clicks")],
    [State("tooltip", "is_open")],
)
def toggle_tooltip(n, is_open):
    if n:
        return not is_open
    return is_open
    
@app.callback(
    Output('data_table', 'columns'),
    Output('data_table', 'data'),
    Output('group_variable', 'options'),
    Output('outcome_variable', 'options'),
    Output('analysis_variable', 'options'),
    Input('upload_file', 'contents')
)
def update_table(contents):
    if contents is None:
        return [], [], [], [], []  # Return empty values for all outputs        
    
    else:
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        
        columns = [{'name': col, 'id': col} for col in df.columns]
        data = df.to_dict('records')
        
        # Set options for the Group Variable dropdown
        group_variable_options = [{'label': col, 'value': col} for col in df.columns]
        outcome_variable_options = [{'label': col, 'value': col} for col in df.columns]
        outcome_analysis_options = [{'label': col, 'value': col} for col in df.columns]
        
        return columns, data, group_variable_options, outcome_variable_options, outcome_analysis_options

@app.callback(
    Output('group_target_value_selector', 'options'),
    Output('group_other_value_selector', 'options'),
    Output('outcome_target_value_selector', 'options'),
    Output('outcome_other_value_selector', 'options'),
    Output('analysis_value_selector', 'options'),
    Input('group_variable', 'value'),
    Input('outcome_variable', 'value'),    
    Input('analysis_variable', 'value'),
    Input('data_table', 'data')
)
def update_group_value_selector(
    selected_group_variable, 
    selected_outcome_variable,
    selected_analysis_variable,
    data
):
    if data is None or not data:
        return [], [], [], [], []  # Return empty options if no data is available

    df = pd.DataFrame(data)

    group_target_val_selector = []
    group_other_val_selector = []
    outcome_target_val_selector = [] 
    outcome_other_val_selector = []
    analysis_val_selector = []

    if selected_group_variable:
        if selected_group_variable in df.columns:
            unique_group_variable_values = df[selected_group_variable].unique()
            group_target_val_selector = [{'label': str(value), 'value': value} for value in unique_group_variable_values]
            group_other_val_selector = [{'label': str(value), 'value': value} for value in unique_group_variable_values]
        
    if selected_outcome_variable:
        if selected_outcome_variable in df.columns:
            unique_outcome_variable_values = df[selected_outcome_variable].unique()
            outcome_target_val_selector = [{'label': str(value), 'value': value} for value in unique_outcome_variable_values]
            outcome_other_val_selector = [{'label': str(value), 'value': value} for value in unique_outcome_variable_values]

    if selected_analysis_variable:
        if selected_analysis_variable in df.columns:
            unique_analysis_variable_values = df[selected_analysis_variable].unique()
            analysis_val_selector = [{'label': str(value), 'value': value} for value in unique_analysis_variable_values]

    return (
        group_target_val_selector, 
        group_other_val_selector, 
        outcome_target_val_selector,
        outcome_other_val_selector,
        analysis_val_selector
    )

@app.callback(
    Output('group_target_val', 'value'),
    Output('group_other_val', 'value'),
    Output('outcome_target_value_selector', 'value'),
    Output('outcome_other_value_selector', 'value'),
    Output('analysis_target_value_selector', 'value'),
    Input('group_value_selector', 'value'),
    Input('outcome_value_selector', 'value'),
    Input('analysis_value_selector', 'value')
)
def map_group_values(selected_group_value, selected_outcome_value, selected_analysis_value):
    # Initialize the mapping results
    target_group_value = ""
    other_group_value = ""
    target_outcome_value = ""
    other_outcome_value = ""
    target_analysis_value = ""
    
    if selected_group_value:
        # Map the selected group value
        target_group_value = selected_group_value  # Set the target value
        other_group_value = selected_group_value  # Customize this logic as needed

    if selected_outcome_value:
        # Map the selected outcome value
        target_outcome_value = selected_outcome_value  # Set the target value
        other_outcome_value = selected_outcome_value  # Customize this logic as needed

    if selected_analysis_value:
        # Map the selected analysis value
        target_analysis_value = selected_analysis_value  # Set the target value

    return target_group_value, other_group_value, target_outcome_value, other_outcome_value, target_analysis_value

# Run model
@app.callback(
    Output("main_app_layout", "children"),  # Update this to point to the app layout
    Output("output", "children"),  # Retain your original output
    Input("harmonize_button", "n_clicks"),
    Input('upload_file', 'contents'),
    State("group_variable", "value"),
    State("group_target_value_selector", "value"),
    State("group_other_value_selector", "value"),
    State("outcome_variable", "value"),
    State("outcome_target_value_selector", "value"),
    State("outcome_other_value_selector", "value"),
    State("analysis_variable", "value"),
    State("analysis_value_selector", "value"),
    prevent_initial_call=True
)
def harmonize_data(
    n_clicks, 
    upload_contents,
    form_group_variable, 
    form_group_target_val, 
    form_group_other_val,
    form_outcome_variable,
    form_outcome_target_val,
    form_outcome_other_val,
    form_analysis_variable,
    form_analysis_value
):
    if upload_contents is None:
        return [], ""     
    
    content_type, content_string = upload_contents.split(",")
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        
    if n_clicks > 0:
        config = {
            "Ingest": {
                "filepath": "app loaded",
                "group_variable": form_group_variable,
                "group_target_val": form_group_target_val,
                "group_other_val": form_group_other_val,
                "outcome_variable": form_outcome_variable,
                "outcome_target_val": form_outcome_target_val,
                "outcome_other_val": form_outcome_other_val,
                "grpers": form_analysis_variable,
                "grpers_val": form_analysis_value
            }
        }
        # Run model
        model = mod.Model(df, config)
        df_prep, tbl = model.prep()
        df_results = model.analysis(df_prep.copy(), tbl)

        # Update the layout with new results
        new_layout = alf.run_layout_build(df_results)

        return new_layout, f"Harmonization completed with parameters: {config}"

    return dash.no_update, "No harmonization completed."

# Run the app
if __name__ == '__main__':
    
    app.run_server(
        debug=False, 
        #host="0.0.0.0", 
        port=8080
    )
