# -*- coding: utf-8 -*-
from ctypes import alignment
from multiprocessing import Value
from re import X
import time as datetime 
from datetime import date
import os
from tkinter import CENTER
from click import command
from dash import Dash, Input, Output, callback, dash_table
from dash import Dash, dcc, html, callback_context, State
from dash.dependencies import Input, Output
import classes
import mysql.connector
from dash import Dash, dash_table
import pandas as pd
import numpy as np
from collections import OrderedDict
from pythonping import ping
import paramiko
import dash_daq as daq
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go



# DB Connection Parameters
dbPara = classes.dbCredentials()

def read_csv_sftp(hostname: str, username: str, remotepath: str, password: str, *args, **kwargs) -> pd.DataFrame:
    """
    Read a file from a remote host using SFTP over SSH.
    Args:
        hostname: the remote host to read the file from
        username: the username to login to the remote host with
        remotepath: the path of the remote file to read
        *args: positional arguments to pass to pd.read_csv
        **kwargs: keyword arguments to pass to pd.read_csv
    Returns:
        a pandas DataFrame with data loaded from the remote host
    """
    # open an SSH connection
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)
    #command = "sudo timeout 10s wash -i wlan0mon -s -u -2 -5 -a -p > /home/kali/Reports/wifi_networks/basic.wifi.csv && cat /home/kali/Reports/wifi_networks/basic.wifi.csv"
    #client.exec_command(command)
    # read the file using SFTP
    sftp = client.open_sftp()
    remote_file = sftp.open(remotepath)
    dataframe = pd.read_csv(remote_file, *args, **kwargs)
    remote_file.close()
    # close the connections
    sftp.close()
    client.close()
    return dataframe




def toSSH(host: str, password: str, interfaceValue: str):
    host = host
    port = 22
    username = "kali"
    password = password
    DATE = date.today().strftime('%Y-%m-%d-%H_%M')
    data_wifi_csv = "wifi_net" + DATE
    #command = "sudo timeout 20s airodump-ng wlan1mon -w /home/kali/Reports/wifi_networks/"+data_wifi_csv+" --wps --output-format csv --write-interval 5 > /home/kali/Reports/wifi_networks/wifi_last.csv"
    #command = "ls"

    interfaceValue = interfaceValue
    command = "sudo timeout 10s wash -i " + interfaceValue + " -s -u -2 -5 -a -p > /home/kali/Reports/wifi_networks/basic.wifi.csv && cat /home/kali/Reports/wifi_networks/basic.wifi.csv"
    #command = "sudo iwlist wlan0 scan | grep ESSID"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    #ssh.exec_command(command)
    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    #lines = ""
    return 
    
def toSSH2(host, interfaceValue):
    host = host
    port = 22
    username = "kali"
    password = "kali"
    DATE = date.today().strftime('%Y-%m-%d-%H_%M')
    data_wifi_csv = "wifi_net" + DATE
    #command = "sudo timeout 10s airodump-ng wlan0mon -w /home/kali/Reports/wifi_networks/wifi_last --wps --output-format csv | sudo python /home/kali/Reports/wifi_networks/pyexcel.py | cat /home/kali/Reports/wifi_networks/wifi_last-01.csv"
    command = "sudo rm -rf /home/kali/Reports/wifi_networks/wifi_last-01.csv && sudo timeout 10s airodump-ng wlan1mon -w /home/kali/Reports/wifi_networks/wifi_last --wps --output-format csv && sudo python /home/kali/Reports/wifi_networks/pyexcel.py"
    #command = "ls"
    #command = "sudo timeout 10s wash -i wlan2mon -s -u -2 -5 -a -p > /home/kali/Reports/wifi_networks/basic.wifi.csv && cat /home/kali/Reports/wifi_networks/basic.wifi.csv"
    #command = "sudo iwlist wlan0 scan | grep ESSID"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    #ssh.exec_command(command)
    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    #lines = ""
    return 

#def UpdateSSIDTable():
            
          #  dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

                        #columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in  read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
           #         data = read_csv_sftp("100.64.0.77", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").to_dict('records'), style_cell={'textAlign': 'left'},
            #            style_header={
             #               'backgroundColor': 'rgb(30, 30, 30)',
              #              'color': 'white'
               #         },
                #        style_data={
                 #           'backgroundColor': 'rgb(50, 50, 50)',
                  #          'color': 'white'
                 #       },            
            #)


def check_ping(ip):
    response = os.system("ping -n 1 " + ip)
    # and then check the response...
    if response == 0:
        pingstatus = True
    else:
        pingstatus = False
    
    return pingstatus


def pingdef(ip):
    response_list = ping(ip,count=10)

    return response_list.rtt_avg_ms
    # Connect to DB
connectr = mysql.connector.connect(user = dbPara.dbUsername, password = dbPara.dbPassword, host = dbPara.dbServerIp , database = dbPara.dataTable)
    # Connection must be buffered when executing multiple querys on DB before closing connection.
pointer = connectr.cursor(buffered=True)
pointer.execute('SELECT * FROM agents;')
queryRaw = pointer.fetchall()
    # Transform the query payload into a dataframe
queryPayload = np.array(queryRaw)
df = pd.DataFrame(queryPayload, columns=['idagents', 'ubicacion', 'ip', 'weburl', 'sshurl', 'agentname','connection'])
#Define Up or DOW in DataTaFrame
def LatencyRating():
    df['connection'] = df['ip'].apply(lambda x:
        'DOWN' if check_ping(x) == False else( 'UP' 
        
                            ))
    
    #Add Latency Column to DataFrame
    df['Latency(ms)'] = df['ip'].apply(lambda x:pingdef(x)
        if check_ping(x) == True else ('0'))
    

    #Rating de la conexions de los Sifi AGENTS desde el server.
    if check_ping("100.64.0.2") == True and check_ping("100.64.0.4") and check_ping("100.64.0.77")  == True: 
        df['Rating'] = df['ip'].apply ( lambda x:
            '⭐⭐⭐' if pingdef(x) < 15 else (
            '⭐⭐' if pingdef(x) < 30 else (
            '⭐' if  pingdef(x) < 60  else '🔥not reliable'
              )))

def SSIDDataTable():
    return html.Div([ html.H3('Sifi Agent 64.2: SSID list'),
            html.H4(        
                dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

                        #columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in  read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
                    data = read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").to_dict('records'), style_cell={'textAlign': 'left'},           
                            )            
                ), html.H3('Sifi Agent 64.4: SSID list'),
            html.H4(   
                    dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

                        #columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in  read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
                    data = read_csv_sftp("100.64.0.4", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "sifi2224").to_dict('records'), style_cell={'textAlign': 'left'},     
                        )
                        
)
        ])

    


app = Dash(__name__, title='SIFI Control Panel')

theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}


tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '5px solid #d6d6d6',
    'padding': '10px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#28BB45',
    'color': 'green',
    'padding': '8px'
}

app.layout = html.Div([ 
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', className='dark-theme-control', children=[
        dcc.Tab(label='Sifi Agents', value='tab-2', style=tab_style, selected_style=tab_selected_style, className='dark-theme-control'),
        dcc.Tab(label='Pre-Run', value='tab-3', style=tab_style, selected_style=tab_selected_style, className='dark-theme-control'),
        dcc.Tab(label='Wireless Assessment', value='tab-4', style=tab_style, selected_style=tab_selected_style, className='dark-theme-control'),
        dcc.Tab(label='Wifi Dashboard', value='tab-5', style=tab_style, selected_style=tab_selected_style, className='dark-theme-control'),
    ], style=tabs_styles),
    html.Div(id='tabs-content-inline', className='dark-theme-control'),  html.Div(id='container-button-timestamp', className='dark-theme-control'),
    html.Button('RefreshData', id = 'submitButton', n_clicks = 0, className='dark-theme-control'),
    dcc.Dropdown(df.ip.unique(), id='pandas-dropdown-1', placeholder="Select SifiAgent"),
    dcc.Dropdown(
    ['WPA/WPA2 Basic Crack', 'WPA/WPA2 Advanced', '4-full-way-Handshake'],
    placeholder="Select Actions To RUN",
    multi=True
    ),
    html.Div(id='pandas-output-container-1', className='dark-theme-control'),
    dcc.Interval(
        id='dataUpateInterval', 
        interval=5*1000, 
        n_intervals=0
    ), dbc.Alert(id='tbl_out', className='dark-theme-control'),
   html.Div([ html.Img(src=app.get_asset_url('sifi.png')), html.H3("A cup of Sifi running like a coffee!") ])
 
    


])
  





@app.callback(
    Output('pandas-output-container-1', 'children'),
    Input('pandas-dropdown-1', 'value')
)
def update_output( value):
    return f'You have selected {value}'
    
@app.callback( 
    Output('tabs-content-inline', 'children'), 
    [
        Input('tabs-styled-with-inline', 'value'), 
        Input('submitButton', 'n_clicks'),
         Input('pandas-dropdown-1', 'value') ]
)
def render_content(tab, callbackContext,DropDownDevvalue):
    # Instantiate the callback context, to find the button ID that triggered the callback
    callbackContext = callback_context
    # Get button ID
    button_id = callbackContext.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'submitButton'and tab == 'tab-3':
        #if check_ping("100.64.0.2") == True:
            toSSH("100.64.0.2", "kali", "wlan1mon")
          
        #if check_ping("100.64.0.4") == True:
            toSSH("100.64.0.4", "sifi2224", "wlan0mon")
            
        #if check_ping("100.64.0.77") == True:
           # toSSH("100.64.0.77", "kali", "wlan1mon")
           
       # SSIDDataTable()
            return html.Div([ html.H3('Sifi Agent 64.2: SSID list'),
                html.H4(        
                dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

                        #columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in  read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
                    data = read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").to_dict('records'), style_cell={'textAlign': 'left'},           
                            )            
                ), html.H3('Sifi Agent 64.4: SSID list'),
                html.H4(   
                    dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

                        #columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in  read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
                    data = read_csv_sftp("100.64.0.4", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "sifi2224").to_dict('records'), style_cell={'textAlign': 'left'},     
                        ), 
                ),

                        html.H3('Sifi Agent 64.77: SSID list') ])
           # html.H4(   
             
             #       dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

                        #columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in  read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
              #      data = read_csv_sftp("100.64.0.77", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").to_dict('records'), style_cell={'textAlign': 'left'},     
                       

                        
    if button_id == 'submitButton' and tab == 'tab-2':
        LatencyRating()
    if button_id == 'submitButton' and tab == 'tab-5':
        if DropDownDevvalue == "10.64.0.4":
            toSSH2("100.64.0.4", "wlan0mon")
            return html.Div([
          # html.H3(toSSH2)
            html.H4(        
                dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

                        #columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in  read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
                            
                                data = read_csv_sftp("100.64.0.4", "kali", "/home/kali/Reports/wifi_networks/wifi_last-01.csv", "sifi2224").to_dict('records'), style_cell={'textAlign': 'left'},
                        style_header={
                          'backgroundColor': 'rgb(30, 30, 30)',
                            'color': 'green'
                        },
                        style_data={
                            'backgroundColor': 'rgb(50, 50, 50)',
                            'color': 'green'
                        }          
                            )
                )

                    ])
        elif DropDownDevvalue =="100.64.0.2":
            toSSH2("100.64.0.2", "wlan1mon")
            return html.Div([
          # html.H3(toSSH2)
            html.H4(        
                dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

                        #columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in  read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
                            
                                data = read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/wifi_last-01.csv", "kali").to_dict('records'), style_cell={'textAlign': 'left'},
                        style_header={
                          'backgroundColor': 'rgb(30, 30, 30)',
                            'color': 'green'
                        },
                        style_data={
                            'backgroundColor': 'rgb(50, 50, 50)',
                            'color': 'green'
                        }          
                            )
                )

                    ])
        
        
       
       

   

    if tab == 'tab-1':
        return html.Div([
            html.H3('Welcome to Sifi WSS')
        ])
    elif tab == 'tab-2':
        return html.Div([
            

                      dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

                        columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in df.columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
                        data = df.to_dict('records'),
                        
                        
                      style_header={
                          'backgroundColor': 'rgb(30, 30, 30)',
                            'color': 'white'
                        },
                        style_data={
                            'backgroundColor': 'rgb(50, 50, 50)',
                            'color': 'green'
                        }         ) 
                         
        ])
    elif tab == 'tab-3':
        return html.Div([ 
            html.H4( "Here you can Discover SSID's with your SifiAgents"),
              html.H4(        
                dash_table.DataTable( 
                        #columns = [{'name': i, 'id': i} ],

                        #columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in  read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
                    data = read_csv_sftp("100.64.0.1", "ittadmin", "/home/ittadmin/Reports/basic.wifi.csv", "L1br0Sh@rkR1ng").to_dict('records'), style_cell={'textAlign': 'left'},
                        style_header={
                          'backgroundColor': 'rgb(30, 30, 30)',
                            'color': 'white'
                        },
                        style_data={
                            'backgroundColor': 'rgb(50, 50, 50)',
                            'color': 'white'
                        },            
                            )
                )    
        ])
    elif tab == 'tab-4':
        if DropDownDevvalue == "100.64.0.4":
            passwordDev = "sifi2224"
            
        else:
            passwordDev = "kali"
        dfra = read_csv_sftp(DropDownDevvalue, "kali", "/home/kali/Reports/wifi_networks/wifi_last-01.csv", passwordDev)
        #dfra=[{"name": "BSSID", "id": i, } for i in dfra.columns ],
        dfra2 = dfra.iloc[:, 0]
        dfra3 = dfra.iloc[:, 13]
        return html.Div([
            html.H3('Select Your Target ESSID and BSSID'),
            dcc.Dropdown(dfra2),
            dcc.Dropdown(dfra3),
           # dcc.Dropdown(read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/wifi_last-01.csv", "kali").BSSID.unique())
        ])
    elif tab == 'tab-5':
       if DropDownDevvalue == "100.64.0.4":
            passwordDev = "sifi2224"
            
       else:
            passwordDev = "kali"
       return html.Div([
          # html.H3(toSSH2)
            html.H4(        
                dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

                        #columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in  read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
                    data = read_csv_sftp( DropDownDevvalue, "kali", "/home/kali/Reports/wifi_networks/wifi_last-01.csv", passwordDev).to_dict('records'), style_cell={'textAlign': 'left'},
                        style_header={
                          'backgroundColor': 'rgb(30, 30, 30)',
                            'color': 'green'
                        },
                        style_data={
                            'backgroundColor': 'rgb(50, 50, 50)',
                            'color': 'green'
                        }          
                            )
                )

        ])


if __name__ == '__main__':
    
    app.run_server(debug=True, host='0.0.0.0', port='5007', dev_tools_silence_routes_logging=False)