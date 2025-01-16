import pandas as pd
import plotly.express as px

"""
Este programa de Python mostrará un dot density map que representa accidentes e incidentes aéreos a nivel global.
"""

file_path = r'..\\Aviation_datasets\\AviationData.csv'
aviation_data = pd.read_csv(file_path, encoding='latin1', low_memory=False)
#print(aviation_data.columns)

aviation_data['Latitude'] = pd.to_numeric(aviation_data['Latitude'], errors='coerce')
aviation_data['Longitude'] = pd.to_numeric(aviation_data['Longitude'], errors='coerce')
aviation_data_geo = aviation_data.dropna(subset=['Latitude', 'Longitude'])

aviation_data_geo['Total.Fatal.Injuries'] = aviation_data_geo['Total.Fatal.Injuries'].fillna(0)
aviation_data_geo['Total.Serious.Injuries'] = aviation_data_geo['Total.Serious.Injuries'].fillna(0)
aviation_data_geo['Total.Minor.Injuries'] = aviation_data_geo['Total.Minor.Injuries'].fillna(0)

aviation_data_geo['Total_Injuries'] = (
    aviation_data_geo['Total.Fatal.Injuries'] +
    aviation_data_geo['Total.Serious.Injuries'] +
    aviation_data_geo['Total.Minor.Injuries']
)

aviation_data_geo['Total_Injuries'] = aviation_data_geo['Total_Injuries'].apply(lambda x: max(x, 1))

aviation_data_geo['Type'] = aviation_data_geo['Investigation.Type']

fig = px.scatter_geo(
    aviation_data_geo,
    lat='Latitude',
    lon='Longitude',
    title="Accidentes e incidentes aéreos a nivel global (desde 1962)",
    projection="orthographic",
    opacity=0.8,
    color='Type',  
    size='Total_Injuries', 
    size_max=20,  
    color_discrete_map={
        'Accident': '#FF6F61',  
        'Incident': '#3498DB'  
    },
    hover_data={
        'Event.Date': True,  
        'Make': True,        
        'Model': True,       
        'Total.Fatal.Injuries': True,  
        'Total.Serious.Injuries': True,  
        'Total.Minor.Injuries': True, 
        'Type': True,        
        'Latitude': False,   
        'Longitude': False,   
        'Total_Injuries': False
    }
)

fig.update_traces(marker=dict(opacity=0.9, sizemin=3)) 
fig.update_layout(
    title=dict(
        text="Accidentes e incidentes aéreos a nivel global (desde 1962)",
        x=0.5, 
        font=dict(
            family="Roboto, sans-serif",
            size=26,
            color="#2c3e50"  
        )
    ),
    annotations=[
        dict(
            text="Fuente: Aviation Accident Database & Synopses (NSTB)",  
            x=0.5,  
            y=1.02,  
            showarrow=False,
            font=dict(
                family="Roboto, sans-serif",
                size=16,
                color="#2c3e50"
            ),
            xref="paper",  
            yref="paper"  
        )
    ],

    geo=dict(
        showland=True,
        landcolor="#d3d3d3",  
        oceancolor="#eaf6f8",  
        showocean=True,
        coastlinecolor="#34495e",  
        coastlinewidth=0.7, 
        projection_scale=0.95,  
    ),
    margin=dict(l=40, r=40, t=60, b=40),  
    paper_bgcolor="#fefefe",  
    plot_bgcolor="#fefefe",
)

output_path = "html_pages/1_map.html"
fig.write_html(output_path, auto_open=True)
