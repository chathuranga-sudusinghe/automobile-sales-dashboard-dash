#!/usr/bin/env python
# coding: utf-8

import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# -----------------------------
# Load the data
# -----------------------------
data = pd.read_csv('automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Automobile Statistics Dashboard"

# -----------------------------
# Dropdown options
# -----------------------------
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

year_list = [i for i in range(1980, 2024)]

# -----------------------------
# App Layout
# -----------------------------
app.layout = html.Div([

    # Title
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={'textAlign': 'center', 'color': '#503D36'}
    ),

    # Statistics Dropdown
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='statistics-dropdown',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select a Report Type'
        )
    ]),

    # Year Dropdown
    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=2020
        )
    ]),

    # Output container
    html.Div([
        html.Div(
            id='output-container',
            className='chart-container',
            style={'marginTop': '30px'}
        )
    ])
])

# ------------------------------------------------
# Disable year dropdown during recession statistics
# ------------------------------------------------
@app.callback(
    Output('select-year', 'disabled'),
    Input('statistics-dropdown', 'value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        return True
    else:
        return False

# ------------------------------------------------
# Callback for Graphs
# ------------------------------------------------
@app.callback(
    Output('output-container', 'children'),
    [
        Input('statistics-dropdown', 'value'),
        Input('select-year', 'value')
    ]
)
def update_output_container(selected_statistics, input_year):

    # ---------------- RECESSION REPORT ----------------
    if selected_statistics == 'Recession Period Statistics':

        recession_data = data[data['Recession'] == 1]

        # Chart 1: Average Automobile Sales (Year-wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title='Average Automobile Sales during Recession Period'
            )
        )

        # Chart 2: Average Sales by Vehicle Type
        avg_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(
                avg_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Sales by Vehicle Type during Recession'
            )
        )

        # Chart 3: Advertisement Expenditure Share
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                names='Vehicle_Type',
                values='Advertising_Expenditure',
                title='Advertisement Expenditure Share during Recession'
            )
        )

        # Chart 4: Unemployment Rate vs Sales
        unemp_data = recession_data.groupby(
            ['unemployment_rate', 'Vehicle_Type']
        )['Automobile_Sales'].mean().reset_index()

        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='unemployment_rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                labels={
                    'unemployment_rate': 'Unemployment Rate',
                    'Automobile_Sales': 'Average Automobile Sales'
                },
                title='Effect of Unemployment Rate on Vehicle Type and Sales'
            )
        )

        return [
            html.Div([
                html.Div(R_chart1, style={'width': '50%'}),
                html.Div(R_chart2, style={'width': '50%'})
            ], style={'display': 'flex'}),

            html.Div([
                html.Div(R_chart3, style={'width': '50%'}),
                html.Div(R_chart4, style={'width': '50%'})
            ], style={'display': 'flex'})
        ]

    # ---------------- YEARLY REPORT ----------------
    elif input_year and selected_statistics == 'Yearly Statistics':

        yearly_data = data[data['Year'] == input_year]

        # Chart 1: Yearly Sales Trend
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title='Average Automobile Sales by Year'
            )
        )

        # Chart 2: Monthly Sales
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x='Month',
                y='Automobile_Sales',
                title='Total Monthly Automobile Sales'
            )
        )

        # Chart 3: Vehicle Type Sales
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title=f'Average Vehicle Sales by Type in {input_year}'
            )
        )

        # Chart 4: Advertisement Expenditure
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                names='Vehicle_Type',
                values='Advertising_Expenditure',
                title='Total Advertisement Expenditure by Vehicle Type'
            )
        )

        return [
            html.Div([
                html.Div(Y_chart1, style={'width': '50%'}),
                html.Div(Y_chart2, style={'width': '50%'})
            ], style={'display': 'flex'}),

            html.Div([
                html.Div(Y_chart3, style={'width': '50%'}),
                html.Div(Y_chart4, style={'width': '50%'})
            ], style={'display': 'flex'})
        ]

    else:
        return None

# -----------------------------
# Run the app
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
