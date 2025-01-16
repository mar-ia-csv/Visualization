import pandas as pd
import plotly.express as px


file_path = r'AviationData.csv'
aviation_data = pd.read_csv(file_path, encoding='latin1', low_memory=False)


aviation_data['Purpose.of.flight'] = aviation_data['Purpose.of.flight'].str.strip()


def relabel_flight_purpose(purpose):
    if purpose in ['Personal', 'Skydiving', 'Air Race/show', 'Air Race show']:
        return 'Recreational'
    elif purpose in ['Business', 'Executive/corporate', 'Public Aircraft', 
                     'Public Aircraft - Federal', 'Public Aircraft - Local', 'Public Aircraft - State']:
        return 'Commercial'
    elif purpose in ['Ferry', 'Aerial Observation', 'Aerial Application', 'Firefighting', 
                     'Banner Tow', 'External Load']:
        return 'Operational'
    elif purpose in ['Instructional', 'Flight Test']:
        return 'Training/Testing'
    elif purpose in ['Other Work Use', 'Positioning']:
        return 'Other'
    else:
        return 'Exclude'

aviation_data['Flight Purpose Category'] = aviation_data['Purpose.of.flight'].apply(relabel_flight_purpose)


aviation_data_filtered = aviation_data[
    (aviation_data['Flight Purpose Category'] != 'Exclude') & 
    aviation_data['Flight Purpose Category'].notna()
]


purpose_counts = aviation_data_filtered.groupby('Flight Purpose Category').size().reset_index(name='Accident Count')


custom_colors = {
    "Recreational": "#5dade2",   
    "Commercial": "#85c1e9",       
    "Operational": "#ec7063",      
    "Training/Testing": "#f1948a",  
    "Other": "#aed6f1"    
}


text_colors = {
    "Recreational": "darkblue",
    "Commercial": "darkblue",
    "Operational": "darkred",
    "Training/Testing": "darkred",
    "Other": "darkblue"
}


purpose_counts['Text Color'] = purpose_counts['Flight Purpose Category'].map(text_colors)

fig = px.treemap(
    purpose_counts,
    path=['Flight Purpose Category'],
    values='Accident Count',
    title="Distribución de Accidentes Aéreos por Propósito del Vuelo",
    labels={'Flight Purpose Category': 'Propósito del Vuelo'},
    color='Flight Purpose Category',  
    color_discrete_map=custom_colors  
)


fig.update_traces(
    texttemplate="<b>%{label}</b><br>Accidentes: %{value}",
    textfont=dict(size=18),
    insidetextfont=dict(
        color=purpose_counts['Text Color']
    )
)


fig.update_layout(
    title=dict(
        text="Distribución de Accidentes Aéreos según Tipo de Vuelo",
        font=dict(size=24, family="Roboto, sans-serif"),
        x=0.5
    ),
    paper_bgcolor="#f0f0f0",
    margin=dict(t=50, b=20, l=20, r=20)
)

output_path = "html_pages/4_treemap.html"
fig.write_html(output_path, auto_open=True)
