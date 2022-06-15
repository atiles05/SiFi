import dash
from dash import html,dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

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
        ),
        html.Div(
            id = 'devicesContainer',
            children = [
                html.H4(
                    'Devices'
                )
            ]
        ),
        html.Div(
            id = 'reportsContainer',
            children = [
                html.H4(
                    'Reports'
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
def showTopWorstInnerTabContent(currentTab):
    if currentTab == 'Devices':
        return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}
    elif currentTab == 'Reports':
        return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}, {'display': 'none'}
    elif currentTab == 'Tests':
        return {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, {'display': 'none'}
    else:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'block'}

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='5006', dev_tools_silence_routes_logging=False)