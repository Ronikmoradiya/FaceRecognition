'''import webapp2


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/plain"
        self.response.write("Congratulations, it's a web app!")

routes = [('/', MainPage)]

my_app = webapp2.WSGIApplication(routes, debug=True)
'''

'''
print ("Content-Type: text/plain")

print ("Congratulations, it's a web app!")

import dash
import dash_core_components as dcc
import dash_html_components as html
app = dash.Dash()
colors = { 'background': '#87D653', 'text': '#ff0033'}
app.layout = html.Div(style={'backgroundColor': colors['background']},
children=[
 html.H1(
 children='Hello Dash',
 style={ 'textAlign': 'center', 'color': colors['text'] }
 ),
 html.Div(children='Dash: A web application framework for Python.', style={
 'textAlign': 'center',
 'color': colors['text']
 }),
 dcc.Graph(
 id='example-graph-2',
#Python Web Development Libraries52
 figure={
 'data': [
 {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name':
'Delhi'},
 {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name':
u'Mumbai'},
 ],
 'layout': {
 'plot_bgcolor': colors['background'],
 'paper_bgcolor': colors['background'],
 'font': {
 'color': colors['text']
 }
 }
 }
 )
])
if __name__ == '__main__':
 app.run_server(debug=True)

 '''

from django.shortcuts import render_to_response
from django.template import RequestContext


def index(request):
    return render_to_response('test.php')
