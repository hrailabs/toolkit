from pandas import DataFrame
from typing import Tuple

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dash_table import DataTable

import src.app_functions as af 

def div_disclaimer():
    return html.Div(
        id='disclaimer', 
        children=[
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H1("Equity Toolkit", className="card-title"),
                        html.H5("Disparate Impact Testing", className="card-title"),
                        html.Br(),
                        html.H3("Usage Terms and Conditions", className="card-title"),
                        html.Br(),
                        html.Ul([
                            html.Li("Disclaimer: Please do not include sensitive and personally identifiable information in your upload."),
                            html.Li("Consult with experts to determine the appropriate analysis techniques that vary by federal, state, and local regulations."),
                            html.Li("By using this application, you consent to the collection, processing, and storage of your data."),
                            html.Li("This application is intended for use by individuals aged 18 years and older."),
                            html.Li("The developers of this application shall not be liable for any damages arising from the use or inability to use this application."),
                            html.Li("The analysis and results provided by this application are for informational purposes only and do not guarantee specific outcomes."),
                            html.Li("Users are responsible for ensuring compliance with all applicable laws and regulations."),
                            html.Li("While we strive to protect your data, we cannot guarantee the absolute security of your information."),
                            html.Li("We reserve the right to modify these terms and conditions at any time without prior notice."),
                            html.Li("This application is provided 'as is' without any warranties of any kind, either express or implied."),
                            html.Li("In no event shall the developers be liable for any indirect, incidental, or consequential damages arising from the use of this application to the maximum extent permitted by law."),
                            html.Li("Users are solely responsible for their actions based on the output of this application and should seek professional advice as needed."),
                            html.Li("The developers do not endorse or take responsibility for any external links or content that may be referenced within the application."),
                        ]),
                        html.Br(),
                        html.H3("Check 'Accept' to Continue", className="card-title"),
                        dcc.Checklist(
                            id='accept_disclaimer',
                            options=[{'label': ' I accept the terms and conditions', 'value': 'accepted'}],
                            value=[],
                            inline=True
                        ),
                        dbc.Button("Continue", id='continue_button', n_clicks=0, color="primary", disabled=True)
                    ]
                ),
            ),
            ]
        )

def run_layout_build(df_results: DataFrame) -> dbc.Container:
    
    """
    Builds the layout of the app by generating a 
    container with 2x2 grid of cards.

    :param df_results:
        DataFrame
    """
    
    (
        card_header,
        card_1, 
        card_2, 
        card_3, 
        card_4 
    ) = gen_cards(df_results)
    
    app_layout = gen_layout_container(
        card_header,
        card_1, 
        card_2, 
        card_3, 
        card_4 
    )
    
    return app_layout

def gen_layout_container(
    card_header: dbc.Card,
    card_1: dbc.Card,
    card_2: dbc.Card,
    card_3: dbc.Card,
    card_4: dbc.Card
) -> dbc.Container:
    
    """
    Generates a layout container with 2x2 grid of cards.
    """
    
    return dbc.Container(
        [
            html.Br(),
            
            dbc.Row(
                [
                    dbc.Col(card_header),
                ]
            ),
            
            html.Br(),
            
            dbc.Row(
                [
                    dbc.Col(card_1, width=6),
                    dbc.Col(card_2, width=6),
                ]
            ),

            dbc.Row(
                [
                    dbc.Col(card_3, width=6),
                    dbc.Col(card_4, width=6),
                ]
            )
        ], 

        fluid=True
    )
    
def gen_cards(
    df_results: DataFrame
) -> Tuple[dbc.Card, dbc.Card, dbc.Card, dbc.Card, dbc.Card]:
    
    """
    Generates four cards with content.
    """
    
    card_header = dbc.Card(
        dbc.CardBody([
            html.H3("Equity Toolkit", className="card-title"),
            html.H4("Disparate Impact Testing", className="card-title"),
            html.Br(),
            html.A("Inquires: HRai Labs", href='https://hrailabs.com', target="_blank", className="card-title"),
            html.Br(),
            html.A("GitHub Open Source Code", href='https://github.com/hrailabs/toolkit', target="_blank", className="card-title")
        ]),
        className="mb-4",
        style={'backgroundColor': '#318ce7', 'color': 'white'}  # Setting background color and text color

    )
    
    card_1 = dbc.Card(
        dbc.CardBody(
            [
                # File Upload Section
                dbc.Row(
                    dbc.Col(
                        [
                            html.H5("CSV File Upload", className="card-title"),
                            
                            dbc.Button(
                                "ℹ️",  # Info icon
                                id="tooltip-icon",
                                color="link",
                                style={'marginLeft': '5px'}  # Space between title and icon
                            ),
                            dbc.Tooltip(
                                html.Div(
                                    [
                                        html.A(
                                            "Download sample CSV",
                                            href='sample_input.csv',
                                            download='sample_input.csv',
                                            style={
                                                'color': 'white', 
                                                'textDecoration': 'underline'
                                            }
                                        )
                                    ],
                                    style={
                                        'whiteSpace': 'nowrap',
                                    }  
                                ),
                                id="tooltip",  # Add an id to the tooltip
                                is_open=False,
                                trigger=None,
                                target="tooltip-icon",  # Target the icon for the tooltip
                                placement="right"  # You can choose 'left', 'right', 'top', or 'bottom'
                            ),
                            
                            dcc.Upload(
                                id='upload_file',
                                children=html.Div(["Drag and Drop or ", html.A("Select File")]),
                                style={'width': '100%', 'height': '60px', 'lineHeight': '60px', 
                                       'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px', 
                                       'textAlign': 'center', 'margin': '10px'},
                                multiple=False,
                            ),
                            
                            DataTable(
                                id='data_table',
                                columns=[],
                                data=[],
                                style_table={'overflowX': 'auto'},
                                page_size=10,
                                style_cell={'textAlign': 'left'},
                            ),
                            html.Div(id='div_upload_preview', className="mt-3")
                        ], 
                        
                    
                    ),

                ),
                

                # Harmonization Form
                dbc.Row(
                    [
                        dbc.Col(html.H5("File Harmonization Parameters", className="card-title"), width=12),
                        
                        dbc.Col(
                            html.Label(html.Strong("Group Variable:")),
                            width=4
                        ),
                        dbc.Col(
                            dcc.Dropdown(id="group_variable", options=[], placeholder="e.g. Gender"),
                            width=8
                        ),
                        dbc.Col(
                            html.Label(html.Strong("Group Target Value:")),
                            width=4
                        ),
                        dbc.Col(
                            dcc.Dropdown(id="group_target_value_selector", placeholder="e.g. Female"),
                            width=8
                        ),
                        dbc.Col(
                            html.Label(html.Strong("Group Other Value:")),
                            width=4
                        ),
                        dbc.Col(
                            dcc.Dropdown(id="group_other_value_selector", placeholder="e.g. Male"),
                            width=8
                        ),
                        
                        dbc.Col(
                            html.Label(html.Strong("Outcome Variable:")),
                            width=4
                        ),
                        dbc.Col(
                            dcc.Dropdown(id="outcome_variable", placeholder="e.g. Hiring"),
                            width=8
                        ),
                        dbc.Col(
                            html.Label(html.Strong("Outcome Target Value:")),
                            width=4
                        ),
                        dbc.Col(
                            dcc.Dropdown (id="outcome_target_value_selector", placeholder="e.g. Hired"),
                            width=8
                        ),
                        dbc.Col(
                            html.Label(html.Strong("Outcome Other Value:")),
                            width=4
                        ),
                        dbc.Col(
                            dcc.Dropdown(id="outcome_other_value_selector", placeholder="e.g. Not Hired"),
                            width=8
                        ),
                        
                        dbc.Col(
                            html.Label(html.Strong("Analysis Variable:")),
                            width=4
                        ),
                        dbc.Col(
                            dcc.Dropdown(id="analysis_variable", placeholder="e.g., job_title"),
                            width=8
                        ),
                        dbc.Col(
                            html.Label(html.Strong("Analysis Target Value:")),
                            width=4
                        ),
                        dbc.Col(
                            dcc.Dropdown (id="analysis_value_selector", placeholder="e.g. Analyst"),
                            width=8
                        ),
                        
                        html.Br(),
                        html.Br(),
                        dbc.Col(
                            dbc.Button(
                                "Submit Harmonize", 
                                id="harmonize_button", 
                                n_clicks=0, 
                                color="primary",
                                style={"width": "100%"}  # Optionally set width to 100%
                            ),
                            width=4  # Full width for the button                            
                        ),

                    ],
                    className="mt-3"
                ),

                
                # Output result after harmonization
                dbc.Row(
                    dbc.Col(html.Div(id="output"), className="mt-3")
                )
            ],
        )
    )
    
    if len(df_results) >0:
    
        text_c2a, text_c2b = af.gen_card_2_results(df_results.copy())
        text_c2a = f"{text_c2a}."
        text_c2b = f"{text_c2b}."

        fig_c3 = af.gen_card_3_results(df_results.copy())
        fig_c4 = af.gen_card_4_results(df_results.copy())

        card_2 = dbc.Card(
            dbc.CardBody([

                html.H5("Testing Results", className="card-title"),
                html.P("4/5ths Test and Chi2 Test of Independence.", className="card-text"),
                html.Pre(text_c2a, style={"whiteSpace": "pre-wrap", "border": "1px solid #ccc", "padding": "10px", "background-color": "#f8f9fa"}),

                html.Br(),
                html.Br(),

                html.H5("Interpretation of Testing Results", className="card-title"),
                #html.P("This is the content of card 2.", className="card-text"),
                html.Pre(text_c2b, style={"whiteSpace": "pre-wrap", "border": "1px solid #ccc", "padding": "10px", "background-color": "#f8f9fa"})

            ]),
            className="mb-4"
        )

        card_3 = dbc.Card(
            dbc.CardBody([
                html.H5("2x2 Contingency Table", className="card-title"),
                html.P("Used to compute Chi2 Test of Independence.", className="card-text"),
                dcc.Graph(
                    id='heatmap-graph_c3',
                    figure=fig_c3
                )        
            ]),
            className="mb-4"
        )

        card_4 = dbc.Card(
            dbc.CardBody([
                html.H5("Statistically Expected Outcomes", className="card-title"),
                html.P("Expected non-descrimination results.", className="card-text"),
                dcc.Graph(
                    id='heatmap-graph_c4',
                    figure=fig_c4
                )        
            ]),
            className="mb-4"
        )
        
    else:
        card_2 = []
        card_3 = []
        card_4 = []

    return card_header, card_1, card_2, card_3, card_4
