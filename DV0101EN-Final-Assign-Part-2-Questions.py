#!/usr/bin/env python
# coding: utf-8


import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px



# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Sales Statistics Dashboard"

# Define the layout
app.layout = html.Div([
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={
            'textAlign': 'center',  # Center align the heading
            'color': '#503D36',     # Set the color
            'fontSize': 24          # Set the font size
        }
    )
])

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    html.H1("Automobile Statistics Dashboard", style={'width': '80%','padding': '3px',
    'fontSize': '20px','text-align':'center','color':'#FFFFFF', 'bold':True}),
    html.Div([
            html.Label("Select Statistics:"),
            dcc.Dropdown(
                id='stat-type',
                options=dropdown_options,
                value='Yearly Statistics',
                placeholder='Yearly Statistics'
        )
    ]),
    html.Div(dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value='2006'
                         )
            ),
    html.Div([html.Div(id='output-container', className='chart-grid', style=
    {'display': 'flex', 'background-color':""})])
])


#Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='stat-type',component_property='value'))

def update_input_container(selected_statistics):
    if selected_statistics =='Yearly Statistics': 
        return False
    else: 
        return True



# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='value'), 
    Input(component_id='stat-type', component_property='value')])

def update_output_container(input_year, stat_type):
    if stat_type == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        

# To Create and display graphs for Recession Report Statistics

#Plot 1 Automobile sales fluctuate over Recession Period (year wise)
       
        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        chart1 = dcc.Graph(
                            figure=px.line(yearly_rec, 
                            x='Year',
                            y='Automobile_Sales',
                            title="Average Automobile Sales fluctuation over Recession Period"))

#Plot 2 Calculate the average number of vehicles sold by vehicle type       

        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].count().reset_index()                           
        chart2  = dcc.Graph(figure=px.bar(average_sales, 
                                                x='Vehicle_Type',
                                                y='Automobile_Sales',
                                                title= 'Average number of Vehicles sold'
                                                ))
                                
        
# Plot 3 Pie chart for total expenditure share by vehicle type during recessions
       
        exp_rec= recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        chart3 =dcc.Graph(figure=px.pie(exp_rec, values='Advertising_Expenditure', names="Vehicle_Type",
                                        title='Total Expenditure by Vehicle Type '))

# Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        df = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].sum().reset_index()
        chart4 = dcc.Graph(figure=px.bar(df,x='unemployment_rate',y="Automobile_Sales", color='Vehicle_Type',
                                        title='Effect of Unemployment Rate on Sales'))

        return [
            html.Div(className='chart-item', children=[html.Div(children=chart1),html.Div(children=chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=chart3),html.Div(children=chart4)])
            ]

 # Yearly Statistic Report Plots                             
    elif (input_year and stat_type=='Yearly Statistics') :
        yearly_data = data[data['Year']== int(input_year)]
                              
                              
#Plot 1 Yearly Automobile sales using line chart for the whole period.
        yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
    
        chart1 = dcc.Graph(figure= px.line(yas, 
                        x='Year',
                        y='Automobile_Sales',
                        title='Automobile Sales for the year'
                        ))
            
# Plot 2 Total Monthly Automobile sales using line chart.
        month = yearly_data.groupby('Month')['Automobile_Sales'].sum()
        new_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        month = month.reindex(new_order,axis=0)
        month = month.reset_index()
        chart2 = dcc.Graph(figure=px.line(month, x='Month', y='Automobile_Sales',
                                         title= f'Monthly sale for the year {input_year}'))
        
            # Plot bar chart for average number of vehicles sold during the given year
        avr_vdata= yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].count().reset_index()
        chart3 =  dcc.Graph(figure=px.bar(avr_vdata,x='Vehicle_Type', y='Automobile_Sales',
                                        title= 'Average Vehicles Sold by Vehicle Type in the year'))
                             
            # Total Advertisement Expenditure for each vehicle using pie chart
        exp_data=yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        chart4 = dcc.Graph(figure=px.pie(exp_data,values='Advertising_Expenditure', names='Vehicle_Type',
                                        title= 'Expenditure on each vehicle'))
                            


        return [
            html.Div(className='chart-item', children=[html.Div(children=chart1),html.Div(children=chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=chart3),html.Div(children=chart4)])
            ]
        
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
