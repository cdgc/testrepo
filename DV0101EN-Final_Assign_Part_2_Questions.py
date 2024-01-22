import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import datetime as dt
# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')
# Create the Dash app
app = dash.Dash(__name__)

# List of years
year_list = [i for i in range(1980, 2024, 1)]
# Define the layout of the app
app.layout = html.Div(
    [
        html.H1('Automobile Sales Statistics Dashboard',
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 24}),
        html.Div([#TASK 2.2: Add two dropdown menus
        html.Label("Select Statistics:", style={'margin-right': '2em'}),
        dcc.Dropdown(id='dropdown-statistics',
                   options=[
                           {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                           {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                           ],
                  placeholder='Select a report type',
                  style={'width': '80%',  # adjust width as needed
                'color': 'blue',  # text color
                'font-size': '20px',  # font size
                'margin-bottom': '20px',  # bottom margin
                 'margin-top': '20px',
                 'padding': '3px'
             })
    ]),
    html.Div(
      dcc.Dropdown(id='select-year',
                   options=[{'label': i, 'value': i} for i in year_list],
                  placeholder='select-year',
                  style={'width': '80%',  # adjust width as needed
                'color': 'blue',  # text color
                'font-size': '20px',  # font size
                'margin-bottom': '20px',  # bottom margin
                 'padding': '3px'
         })),
        html.Div([#TASK 2.3: Add a division for output display
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),
])
    ]
)
#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    Input(component_id='dropdown-statistics',component_property='value'))

def update_input_container(dropdownstatistics):
    if dropdownstatistics =='Yearly Statistics':
        return False
    else:
        return True

#Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')])


def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

#TASK 2.5: Create and display graphs for Recession Report Statistics
#Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        # use groupby to create relevant data for plotting
        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        # Plotting the line graph
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales fluctuation over Recession Period"))
#Plot 2 Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
        # use groupby to create relevant data for plotting
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2  = dcc.Graph(
            figure=px.bar(average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average number of vehicles sold by vehicle type"))
# Plot 3 : Pie chart for total expenditure share by vehicle type during recessions
        # grouping data for plotting
        exp_rec= recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
                figure=px.pie(exp_rec,
                values='Advertising_Expenditure',
                 names='Vehicle_Type',
                 title="Share of Each Vehicle Type in Total Sales during Recessions"))
# Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart4  = dcc.Graph(
            figure=px.bar(average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="effect of unemployment rate on vehicle type and sales"))

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1),html.Div(children='')],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart2),html.Div(children='')],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3),html.Div(children='')],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart4),html.Div(children='')],style={'display': 'flex'})]

# Yearly Statistic Report Plots
    elif (input_year and selected_statistics=='Yearly Statistics') :
        yearly_data = data[data['Year'] == input_year]

# Plot 1 :Yearly Automobile sales using line chart for the whole period.

        yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
                            figure=px.line(yas,
                            x='Year',
                            y='Automobile_Sales',
                            title="Average Automobile Sales fluctuation over Recession Period"))

# Plot 2 :Total Monthly Automobile sales using line chart.
        average_sales = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart2  = dcc.Graph(
            figure=px.bar(average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average number of vehicles sold by vehicle type"))

# Plot bar chart for average number of vehicles sold during the given year
        avr_vdata=yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart3 = dcc.Graph(
                figure=px.pie(avr_vdata,
                values='Advertising_Expenditure',
                 names='Vehicle_Type',
                 title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)))

# Plot 4 Total Advertisement Expenditure for each vehicle using pie chart
        average_sales = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart4  = dcc.Graph(
            figure=px.bar(average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="effect of unemployment rate on vehicle type and sales"))

        return [
         html.Div(className='chart-item', children=[html.Div(children=Y_chart1),html.Div(children='')],style={'display': 'flex'}),
         html.Div(className='chart-item', children=[html.Div(children=Y_chart2),html.Div(children='')],style={'display': 'flex'}),
         html.Div(className='chart-item', children=[html.Div(children=Y_chart3),html.Div(children='')],style={'display': 'flex'}),
         html.Div(className='chart-item', children=[html.Div(children=Y_chart4),html.Div(children='')],style={'display': 'flex'})]

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
