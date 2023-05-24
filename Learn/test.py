app.layout = html.Div([
	html.Div([
       
        html.Div([
                html.Div([
                    dcc.Link(
                        f"{page['name']}", href=page["relative_path"], className="text-decoration-none text-emphasis-secondary text-underline-opacity-100-hover"
                    )
            ],className="d-flex flex-row mb-3")
                for page in dash.page_registry.values()
        ],className="ms-10"),
	
        html.Div([
            html.Div('Multi-page app with Dash Pages', className= "text-success text-center fs-3 px-10")
        ]),

        
    ], className="d-flex justify-content-around mt-10 bg-body-tertiary"),

    dash.page_container
])