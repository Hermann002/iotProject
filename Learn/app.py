from dash import Dash, html, dcc
import dash

external_stylesheets = ['https://fonts.googleapis.com/css?family=Audiowide', 'https://fonts.googleapis.com/css2?family=Hind+Madurai']

app = Dash(__name__, use_pages = True, external_stylesheets=external_stylesheets)


app.layout = html.Div([
	
    html.Header(
        [
            html.Nav([
		        html.Div(
                    className = "nav-items",
                    children = [
                        dcc.Link(f"{page['name']}", href=page["relative_path"], className='nav-item')]
                )
                    for page in dash.page_registry.values()
		    ],className = "nav-bar"),
        
            html.Span('Dashboard', className='title-header')
        ],className="app-header"),
    
    
	dash.page_container
],className="main")

if __name__ == '__main__':
	app.run_server(debug=True)