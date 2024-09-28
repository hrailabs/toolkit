from pandas import DataFrame
from typing import Tuple

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

import src.app_functions as af 

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
    text_c1 = af.gen_card_1_results(df_results.copy())
    text_c1 = f"{text_c1}."
    
    text_c2 = af.gen_card_2_results(df_results.copy())
    text_c2 = f"{text_c2}."
    
    fig_c3 = af.gen_card_3_results(df_results.copy())
    fig_c4 = af.gen_card_4_results(df_results.copy())
    
    card_header = dbc.Card(
        dbc.CardBody([
            html.H3("Equity Toolkit", className="card-title"),
            html.H5("Disparate Impact Testing", className="card-title"),
        ]),
        className="mb-4",
        style={'backgroundColor': '#318ce7', 'color': 'white'}  # Setting background color and text color

    )
    
    card_1 = dbc.Card(
        dbc.CardBody([
            html.H5("Testing Results", className="card-title"),
            html.P("4/5ths Test and Chi2 Test of Independence.", className="card-text"),
            html.Pre(text_c1, style={"whiteSpace": "pre-wrap", "border": "1px solid #ccc", "padding": "10px", "background-color": "#f8f9fa"})

        ]),
        className="mb-4"
    )

    card_2 = dbc.Card(
        dbc.CardBody([
            html.H5("interpretation of Testing Results", className="card-title"),
            html.P("This is the content of card 2.", className="card-text"),
            html.Pre(text_c2, style={"whiteSpace": "pre-wrap", "border": "1px solid #ccc", "padding": "10px", "background-color": "#f8f9fa"})

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
    
    return card_header, card_1, card_2, card_3, card_4
