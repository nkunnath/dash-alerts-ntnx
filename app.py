  
'''
    ##############################################################################
    #   Script Name: Alerts Dashboard for Nutanix
    #   Author: nimal.kunnath@nutanix.com
    ##############################################################################
    
.synopsis
    This app enables you to visualize the alerts stats from your cluster
    
.disclaimer
    This code is intended as a standalone example.  Subject to licensing restrictions defined on nutanix.dev, this can be downloaded, copied and/or modified in any way you see fit.
    Please be aware that all public code samples provided by Nutanix are unofficial in nature, are provided as examples only, are unsupported and will need to be heavily scrutinized and potentially modified before they can be used in a production environment.  All such code samples are provided on an as-is basis, and Nutanix expressly disclaims all warranties, express or implied.
 
    All code samples are © Nutanix, Inc., and are provided as-is under the MIT license. (https://opensource.org/licenses/MIT)
'''


import json
import math
from datetime import datetime
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Initialize the required lists
list_of_months = []
list_of_days = []

# Use the Nutanix v2 alerts API to get all the alerts and generate a response

from request import request_details

ip, auth = request_details()

URL = "https://{}:9440/api/nutanix/v2.0/alerts/".format(ip)
header = {"content-type": "application/json"}
response_list = []
res = requests.get(url=URL, auth=auth, headers=header, params={'count':1}, verify=False)
total_entities = res.json().get('metadata').get('total_entities')
total_pages = math.ceil(total_entities/1000)

for page in range(1, total_pages + 1):
    response = requests.get(url=URL, auth=auth, headers=header, params={'count':1000, 'page':page}, verify=False)
    response_list.append(response)

LINK_TO_CLUSTER = "https://{}:9440/".format(ip)

# Generate a pandas dataframe with all the alerts
df = pd.DataFrame(columns=['Title', 'Severity', 'Created-Time'])

index = 0
for response in range(total_pages):
    for item in response_list[response].json().get('entities'):
        new_list = []
        new_list.append(item.get('alert_title'))
        new_list.append(item.get('severity')[1:])
        new_list.append(item.get('created_time_stamp_in_usecs'))
        df.loc[index] = new_list
        index += 1

# Modify the Alert creation time/date
df['Created-Time'] = pd.to_datetime(df['Created-Time'], unit='us')
df['Created-Time'] = df['Created-Time'].dt.date


# Create a date range of 31 days for each month
placeholder = []
month_start = pd.date_range(start='1/1/2020', periods=12, freq='MS')
for beginning_date in month_start:
    placeholder.append(str(beginning_date).split(' ')[0])
for item, df_mon in zip(placeholder, range(1, 13)):
    df_mon = pd.date_range(start=item, periods=31, freq='D')
    list_of_months.append(df_mon)


# Create a list of all the days in the year 2020
for mon_number in range(len(list_of_months)):
    for month in list_of_months[mon_number]:
        list_of_days.append(str(month).split(' ')[0])

list_of_days.remove('2020-03-01')
list_of_days.remove('2020-03-02')
list_of_days.remove('2020-05-01')
list_of_days.remove('2020-07-01')
list_of_days.remove('2020-10-01')
list_of_days.remove('2020-12-01')


# Create a dataframe with all the days and columns for different alert severity levels
df_entire_year = pd.DataFrame(index=list_of_days, columns=['Title', 'Severity', 'Created-Time'])
df_entire_year['Created-Time'] = df_entire_year.index
df_entire_year['Critical'] = 0
df_entire_year['Warning'] = 0
df_entire_year['Info'] = 0
day = []
for i in df_entire_year['Created-Time']:
    day.append(str(i).split('-')[2])
df_entire_year['Day'] = day


# Populatie the number of alerts for respective severity levels for every day
for i in range(len(df)):
    if str(df.at[i, 'Created-Time']) in df_entire_year['Created-Time']:
        get_index = df_entire_year[df_entire_year['Created-Time'] == str(df.at[i, 'Created-Time'])].index.item()
        if str(df.at[i, 'Severity']) == 'Critical':
            df_entire_year.at[get_index, 'Critical'] += 1
        elif str(df.at[i, 'Severity']) == 'Warning':
            df_entire_year.at[get_index, 'Warning'] += 1
        elif str(df.at[i, 'Severity']) == 'Info':
            df_entire_year.at[get_index, 'Info'] += 1


# Slice out 12 monthly dataframes
df_jan = df_entire_year.iloc[0:31]
df_feb = df_entire_year.iloc[31:60]
df_mar = df_entire_year.iloc[60:91]
df_apr = df_entire_year.iloc[91:121]
df_may = df_entire_year.iloc[121:152]
df_jun = df_entire_year.iloc[152:182]
df_jul = df_entire_year.iloc[182:213]
df_aug = df_entire_year.iloc[213:244]
df_sep = df_entire_year.iloc[244:274]
df_oct = df_entire_year.iloc[274:305]
df_nov = df_entire_year.iloc[305:335]
df_dec = df_entire_year.iloc[335:366]

monthly_combo = [df_jan, df_feb, df_mar, df_apr, df_may, df_jun, df_jul, df_aug, df_sep, df_oct, df_nov, df_dec]

# Find the total alerts generated every day
for month in monthly_combo:
    column_list = list(month)
    column_list.remove('Title')
    column_list.remove('Severity')
    column_list.remove('Created-Time')
    month['Total'] = month[column_list].sum(axis=1)


dict_essential = {i:j for i, j in zip(range(1, 13), [df_jan, df_feb, df_mar, df_apr, df_may, df_jun, df_jul, df_aug, df_sep, df_oct, df_nov, df_dec])}


# Create the final dataframes for Critical, Warning, Info and Total alerts
list_of_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


list_of_sum_critical = [i['Critical'].sum() for i in monthly_combo]
list_of_sum_warnings = [i['Warning'].sum() for i in monthly_combo]
list_of_sum_info = [i['Info'].sum() for i in monthly_combo]
list_of_sum_total = [x+y+z for x, y, z in zip(list_of_sum_critical, list_of_sum_warnings, list_of_sum_info)]

df_monthly_critical = pd.DataFrame({'Month' : list_of_months, 'total-critical' : list_of_sum_critical}) 

df_monthly_warning = pd.DataFrame({'Month' : list_of_months, 'total-warnings' : list_of_sum_warnings}) 

df_monthly_info = pd.DataFrame({'Month' : list_of_months, 'total-info' : list_of_sum_info}) 

df_monthly_total = pd.DataFrame({'Month' : list_of_months, 'total-alerts' : list_of_sum_total})



# Initialize app
app = dash.Dash(__name__, title='Prism Alerts Dashboard')

# Create a 2x2 figure for monthly alerts
fig10 = make_subplots(rows=2, cols=2)

fig10.add_trace(
    go.Bar(x=df_monthly_total['Month'], y=df_monthly_total['total-alerts'], name="Total Alerts", marker_color='rgb(255,0,0)'),
    row=2, col=2)

fig10.add_trace(
    go.Bar(x=df_monthly_warning['Month'], y=df_monthly_warning['total-warnings'], name="Warning Alerts", marker_color='rgb(255,255,102)'),
    row=1, col=2)

fig10.add_trace(
    go.Bar(x=df_monthly_info['Month'], y=df_monthly_info['total-info'], name="Informational Alerts", marker_color='rgb(211,211,211)'),
    row=2, col=1, secondary_y=False)

fig10.add_trace(
    go.Bar(x=df_monthly_critical['Month'], y=df_monthly_critical['total-critical'], name="Critical Alerts", marker_color='rgb(255,0,0)'),
    row=1, col=1, secondary_y=False)

fig10.update_xaxes(showgrid=False)
fig_layout = fig10["layout"]
fig_data = fig10["data"]
fig_data[0]["marker"]["color"] = "#2cfec1"
fig_data[0]["marker"]["opacity"] = 1
fig_data[0]["marker"]["line"]["width"] = 0
fig_layout["paper_bgcolor"] = "#1f2630"
fig_layout["plot_bgcolor"] = "#1f2630"
fig_layout["font"]["color"] = "#2caec1"
fig_layout["title"]["font"]["color"] = "#2cfec1"
fig_layout["title"]["font"]["family"] = "PT Sans Narrow"
fig_layout["title"]["font"]["size"] = 20
fig_layout["xaxis"]["tickfont"]["color"] = "#2cfec1"
fig_layout["yaxis"]["tickfont"]["color"] = "#2cfec1"
fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"
fig_layout["margin"]["t"] = 75
fig_layout["margin"]["r"] = 50
fig_layout["margin"]["b"] = 100
fig_layout["margin"]["l"] = 50


#Create the layout of the app
app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.Img(id="logo", src=app.get_asset_url("nutanix.jpeg")),
                html.H4(children="Alerts Dashboard"),
                html.Div([
                  html.P(
                    id="description",
                    children="Prism Element Alerts by the month for 2020",
                ),
                dcc.Link("Take me to the cluster", id='prismlink', href=LINK_TO_CLUSTER, target="_blank")
                ]),
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="slider-container",
                            children=[
                                html.P(
                                    id="slider-text",
                                    children="Drag the slider to change the month",
                                ),
                                # Div for the slider to change months
                                dcc.Slider(
                                    id="monthly-slider",
                                    min=1,
                                    max=12,
                                    step=1,
                                    value=8,
                                    updatemode="drag",
                                    marks={key:value for key, value in zip(range(1, 13), list_of_months)},
                                ),
                            ],
                        ),
                        # Div for the individual graphs for critical, warning, info alerts
                        html.Div(
                            children=[
                                dcc.Graph(
                                    id='crit-alert-graph',
                                    style={'float': 'right', 'height': 500, 'width': 550},
                                    config={
                                        "scrollZoom": True,
                                    },                               
                                ),
                                dcc.Graph(
                                    id='warn-alert-graph', 
                                    style={'float': 'right', 'height': 500, 'width': 550},
                                    config={
                                        "scrollZoom": True,
                                    },
                                ),
                                dcc.Graph(
                                    id='info-alert-graph',
                                    style={'float': 'right', 'height': 500, 'width': 550},
                                    config={
                                        "scrollZoom": True,
                                    },                                
                                ),
                             ], style={'display': 'flex'}
                        ),
                        html.Div(
                            id="monthly-alert",
                            children=[
                                html.H4(
                                    id="monthly-alert-text",
                                    children="Alerts visualization for Year 2020",
                                ),
                                html.P(
                                    id="monthly-description",
                                    children="Hover over the graphs to see more information",
                                )
                            ]
                        ),
                        # Div for the 2x2 monthly alert graph
                        html.Div(
                           children=[    
                                dcc.Graph(id='monthly-alert-graph', 
                                    style={'float': 'right', 'height': 800, 'width': 1400, 'margin-left': 150},
                                    figure=fig10,
                                    config={
                                        "scrollZoom": True,
                                    },
                                ),
                           ], style={'display': 'flex'}
                        ),
                    ],
                ),
            ],
        ),
    ],
)


def update_fig(fig):
    """
    This function defines the appearance of the graph. The graph template function calls this function.
    """
    fig.update_xaxes(showgrid=False)
    fig.update_traces(mode='lines+markers')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig_layout = fig["layout"]
    fig_data = fig["data"]
    fig_data[0]["marker"]["color"] = "#2cfec1"
    fig_data[0]["marker"]["opacity"] = 1
    fig_data[0]["marker"]["line"]["width"] = 0
    fig_layout["paper_bgcolor"] = "#1f2630"
    fig_layout["plot_bgcolor"] = "#1f2630"
    fig_layout["font"]["color"] = "#2caec1"
    fig_layout["font"]["size"] = 14
    fig_layout["title"]["font"]["color"] = "#2cfec1"
    fig_layout["title"]["font"]["family"] = "PT Sans Narrow"
    fig_layout["xaxis"]["tickfont"]["color"] = "#2cfec1"
    fig_layout["yaxis"]["tickfont"]["color"] = "#2cfec1"
    fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
    fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"
    fig_layout["margin"]["t"] = 75
    fig_layout["margin"]["r"] = 50
    fig_layout["margin"]["b"] = 100
    fig_layout["margin"]["l"] = 50


def graph_template(dff):
    """
    Creates scatter plots and calls update_fig() for styling
    """
    fig1 = px.scatter(dff, x='Day', y='Critical')
    fig2 = px.scatter(dff, x='Day', y='Warning')
    fig3 = px.scatter(dff, x='Day', y='Info')
    fig1.update_yaxes(title='Critical Alerts')
    fig2.update_yaxes(title='Warning Alerts')
    fig3.update_yaxes(title='Informational Alerts')
    for figure in [fig1, fig2, fig3]:
        update_fig(figure)
    return fig1, fig2, fig3


@app.callback(
    [dash.dependencies.Output('crit-alert-graph', 'figure'),
     dash.dependencies.Output('warn-alert-graph', 'figure'),
     dash.dependencies.Output('info-alert-graph', 'figure')],
    [dash.dependencies.Input('monthly-slider', 'value')])
def update_crit_alerts(value):
    if value in dict_essential:
        dff = dict_essential[value]
    return graph_template(dff)


if __name__ == '__main__':
    app.run_server(debug=True)
