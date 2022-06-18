from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import classes
from dash import Dash, dash_table
import pandas as pd
from collections import OrderedDict

# DB Connection Parameters
dbPara = classes.dbCredentials()

app = Dash(__name__, title='SIFI Control Panel')

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

app.layout = html.Div([
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
        dcc.Tab(label='Sifi Agents', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Pre-Run', value='tab-3', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Wireless Assessment', value='tab-4', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Wifi Dashboard', value='tab-5', style=tab_style, selected_style=tab_selected_style)
    ], style=tabs_styles),
    html.Div(id='tabs-content-inline')
])

@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Welcome to Sifi WSS')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3(  datatableDEV()        )
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Tab content 3')
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Tab content 4')
        ])
    elif tab == 'tab-5':
        return html.Div([
            html.H3('Tab content 5')
        ])

def datatableDEV():
 # Connect to DB
    connectr = mysql.connector.connect(user = dbPara.dbUsername, password = dbPara.dbPassword, host = dbPara.dbServerIp , database = dbPara.dataTable)
    # Connection must be buffered when executing multiple querys on DB before closing connection.
    pointer = connectr.cursor(buffered=True)
    pointer.execute('SELECT * FROM agents;')
    queryRaw = pointer.fetchall()
    # Transform the query payload into a dataframe
    df = pd.DataFrame(queryRaw)

    dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[
        {"ubicacion": i, "ip": i} for i in df.columns
    ],
    )






    queryRaw.clear()
    # Set Graph background colores & title font size



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='5007', dev_tools_silence_routes_logging=False)