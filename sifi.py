import dash
from dash import html,dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from re import X
import time as datetime 
from datetime import date
import os
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




def toSSH(host: str, password: str):
    host = host
    port = 22
    username = "kali"
    password = password
    DATE = date.today().strftime('%Y-%m-%d-%H_%M')
    data_wifi_csv = "wifi_net" + DATE
    #command = "sudo timeout 20s airodump-ng wlan1mon -w /home/kali/Reports/wifi_networks/"+data_wifi_csv+" --wps --output-format csv --write-interval 5 > /home/kali/Reports/wifi_networks/wifi_last.csv"
    #command = "ls"

    interfaceValue = 'wlan0mon'
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
    
def toSSH2(host):
    host = host
    port = 22
    username = "kali"
    password = "kali"
    DATE = date.today().strftime('%Y-%m-%d-%H_%M')
    data_wifi_csv = "wifi_net" + DATE
    command = "sudo rm -rf /home/kali/Reports/wifi_networks/wifi_last-01.csv | sudo timeout 10s airodump-ng wlan1mon -w /home/kali/Reports/wifi_networks/wifi_last --wps --output-format csv && cat /home/kali/Reports/wifi_networks/wifi_last-01.csv"
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
    return lines

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
    df['Latency'] = df['ip'].apply(lambda x:pingdef(x)
        if check_ping(x) == True else ('0'))
    

    #Rating de la conexions de los Sifi AGENTS desde el server.
    if check_ping("100.64.0.2") == True and check_ping("100.64.0.4") and check_ping("100.64.0.77")  == True: 
        df['Rating'] = df['ip'].apply ( lambda x:
            '⭐⭐⭐' if pingdef(x) < 15 else (
            '⭐⭐' if pingdef(x) < 30 else (
            '⭐' if  pingdef(x) < 60  else '🔥not reliable'
              )))
   # html.Div([  dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

    #                    columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in df.columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
      #                  data = df.to_dict('records'),
     #                   
                        
       #                 style_data_conditional=[
        #                     {
         #                       'if': {'filter_query': '{Connection} == UP',
          #                           'column_id': 'Connection'
           #                              },
            #                        'color': 'tomato',
             #                           'fontWeight': 'bold'
              #                  },
               #         ]
                #        )
                 #    ])

def SSIDDataTable():
    html.Div([ html.H3('Sifi Agent 64.2: SSID list'),
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

























app = dash.Dash(__name__, title='SIFI Main Page')
#server = app.server

app.layout = html.Div(
    children=[
        dcc.Tabs(
            id = 'tabsContainer',
            value = 'Devices',
            children = [
                dcc.Tab(
                    label = 'Devices', 
                    value = 'Devices'
                ),
                dcc.Tab(
                    label = 'Reports', 
                    value = 'Reports'
                ),
                dcc.Tab(
                    label = 'Tests', 
                    value = 'Tests'
                ),
                dcc.Tab(
                    label = 'Dash', 
                    value = 'Dash'
                )
            ]
        ), html.Button('RefreshData', id = 'submitButton', n_clicks = 0), dcc.Interval(
        id='dataUpateInterval', 
        interval=5*1000, 
        n_intervals=0
    ),
        html.Div(
            id = 'devicesContainer',
            children = [
                
                    
                            dash_table.DataTable(id='datatableDEV',
                        #columns = [{'name': i, 'id': i} ],

                        columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in df.columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
                        data = df.to_dict('records'),
                        
                        
                        style_data_conditional=[
                             {
                                'if': {'filter_query': '{Connection} == UP',
                                     'column_id': 'Connection'
                                         },
                                    'color': 'tomato',
                                        'fontWeight': 'bold'
                                },
                           ] )

                
            ]
        ),
        html.Div(
            id = 'reportsContainer',
            children = [
                   
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




                
            ]
        ),
        html.Div(
            id = 'testsContainer',
            children = [
                html.H4(
                    'Tests'
                )
            ]
        ), 
        html.Div(
            id = 'DashContainer',
            children = [
                html.H4(
                    'Dash'
                )
            ]
        )
    ]
)

# Callback to hide/display content
@app.callback(
    [
        Output('devicesContainer', 'style'),
        Output('reportsContainer', 'style'),
        Output('testsContainer', 'style'),
        Output('DashContainer', 'style')
    ], 
    Input('tabsContainer', 'value')
)
def showTopWorstInnerTabContent(currentTab, callbackContext):
    if currentTab == 'Devices':
        return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

    elif currentTab == 'Reports':
        return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}, {'display': 'none'}
    elif currentTab == 'Tests':
        return {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, {'display': 'none'}
    else:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'block'}
@app.callback(
    [
        Output('datatableDEV', 'data')
    ], 
    [
       Input('submitButton', 'n_clicks'),
       Input('tabsContainer', 'value')
    ],
)
def update_data(callbackContext, currentTab):
     # Instantiate the callback context, to find the button ID that triggered the callback
    callbackContext = callback_context
    currentTab = currentTab
    # Get button ID
    button_id = callbackContext.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'submitButton':
        if check_ping("100.64.0.2") == True:
            toSSH("100.64.0.2", "kali")
          
        if check_ping("100.64.0.4") == True:
            toSSH("100.64.0.4", "sifi2224")
            
        if check_ping("100.64.0.77") == True:
            toSSH("100.64.0.77", "kali")
    LatencyRating()
    df.append=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in df.columns ]

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='5006', dev_tools_silence_routes_logging=False)