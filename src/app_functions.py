from pandas import DataFrame
import plotly.graph_objects as go

def gen_card_1_results(
    df_results: DataFrame
) -> str:
    
    four_fifths_test = df_results['four_fifths_test'].values[0]
    
    test_result = df_results['test_result'].values[0]
    pval = round(df_results['pvalue'].values[0],2)
    dof = round(df_results['dof'].values[0],2)
    statistic = round(df_results['statistic'].values[0],2)
    alpha = round(df_results['alpha'].values[0],2)
    display = f"""{four_fifths_test}
    
{test_result}: 
pvalue: {pval}
degrees of freedom: {dof}
alpha: {alpha}
statistic: {statistic}"""
    
    return display
    
def gen_card_2_results(
    df_results: DataFrame
) -> str:
    
    display = df_results['result_desc'].values[0]
        
    return display
    
def gen_card_3_results(
    df_results: DataFrame
) -> go.Figure:

    # Extracting the data
    tbl = df_results['tbl'].values[0]
    tbl_rows = df_results['tbl_rows'].values[0]
    tbl_cols = df_results['tbl_cols'].values[0]
    tbl_cols = [col.title().replace('_', ' ') for col in tbl_cols]  # Capitalize and format column names

    # Heatmap for the contingency table
    fig = go.Figure(
        data=go.Heatmap(
            z=tbl,  # The 2x2 data
            y=tbl_rows,  # The row labels
            x=tbl_cols,  # The column labels
            colorscale='Blues',  # Choose a color scale
            text=[[f"{val}" for val in row] for row in tbl],  # Add text for the cell counts
            hoverinfo='text'
        )
    )

    # Update the layout
    fig.update_layout(
        yaxis_title='Groups',
        annotations=[
            dict(
                x=0.5,
                y=1.1,
                xref='paper',
                yref='paper',
                text='Outcomes',
                showarrow=False,
                font=dict(size=14)
            )
        ],
        autosize=False,
        width=500,
        height=400
    )

    # Adding values to the heatmap cells
    fig.data[0].texttemplate = '%{text}'  # Show the actual values in cells
    fig.data[0].textfont = dict(size=14)  # Font size for the text in cells


    return fig

def gen_card_4_results(
    df_results: DataFrame
) -> go.Figure:

    # Extracting the data
    tbl = df_results['expected_freq'].values[0]
    tbl_rows = df_results['tbl_rows'].values[0]
    tbl_cols = df_results['tbl_cols'].values[0]
    tbl_cols = [col.title().replace('_', ' ') for col in tbl_cols]  # Capitalize and format column names

    # Heatmap for the contingency table
    fig = go.Figure(
        data=go.Heatmap(
            z=tbl,  # The 2x2 data
            y=tbl_rows,  # The row labels
            x=tbl_cols,  # The column labels
            colorscale='Blues',  # Choose a color scale
            text=[[f"{val}" for val in row] for row in tbl],  # Add text for the cell counts
            hoverinfo='text'
        )
    )

    # Update the layout
    fig.update_layout(
        yaxis_title='Groups',
        annotations=[
            dict(
                x=0.5,
                y=1.1,
                xref='paper',
                yref='paper',
                text='Expected Outcomes',
                showarrow=False,
                font=dict(size=14)
            )
        ],
        autosize=False,
        width=500,
        height=400
    )

    # Adding values to the heatmap cells
    fig.data[0].texttemplate = '%{text}'  # Show the actual values in cells
    fig.data[0].textfont = dict(size=14)  # Font size for the text in cells


    return fig