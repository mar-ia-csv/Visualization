import pandas as pd
import plotly.express as px


file_path = r'..\Aviation_datasets\AviationData.csv'
aviation_data = pd.read_csv(file_path, encoding='latin1', low_memory=False)


aviation_data = aviation_data.dropna(subset=['Broad.phase.of.flight', 'Weather.Condition', 'Investigation.Type'])
aviation_data = aviation_data[
    (aviation_data['Broad.phase.of.flight'] != 'Unknown') &
    (aviation_data['Weather.Condition'] != 'Unknown') &
    (aviation_data['Investigation.Type'] == 'Accident') 
]


aviation_data['Broad.phase.of.flight'] = aviation_data['Broad.phase.of.flight'].replace({
    'Taxi': 'Rodaje',
    'Takeoff': 'Despegue',
    'Climb': 'Ascenso',
    'Cruise': 'Crucero',
    'Descent': 'Descenso',
    'Approach': 'Aproximación',
    'Landing': 'Aterrizaje',
    'Standing': 'En tierra'
})

aviation_data['Weather.Condition'] = aviation_data['Weather.Condition'].replace({
    'VMC': 'VMC',
    'IMC': 'IMC'
})


sunburst_data = aviation_data.groupby(['Broad.phase.of.flight', 'Weather.Condition']).size().reset_index(name='Count')


fig = px.sunburst(
    sunburst_data,
    path=['Broad.phase.of.flight', 'Weather.Condition'],
    values='Count',
    title="Accidentes por Fase de Vuelo y Condiciones Meteorológicas",
    color='Count',
    color_continuous_scale='Blues',
    labels={
        'Broad.phase.of.flight': 'Fase de Vuelo',
        'Weather.Condition': 'Condiciones Meteorológicas'
    }
)


fig.add_annotation(
    text="<b>VMC</b>: Condiciones Meteorológicas Visuales<br><b>IMC</b>: Condiciones Meteorológicas Instrumentales",
    x=0.9,  
    y=0.95,  
    showarrow=False,
    font=dict(size=12, family="Roboto, sans-serif", color="black"),
    align="center",
    xref="paper",
    yref="paper",
    bgcolor="rgba(255, 255, 255, 0.8)",
    bordercolor="black",
    borderwidth=1
)


fig.update_layout(
    title=dict(
        text="Fases de Vuelo y Detalles de Accidentes según Condiciones Meteorológicas",
        font=dict(size=24, family="Roboto, sans-serif"),
        x=0.5
    ),
    paper_bgcolor="#f9f9f9",
    plot_bgcolor="#f9f9f9",
    margin=dict(t=100, b=40) 
)


output_path = "html_pages/3_sunburst.html"
fig.write_html(output_path, auto_open=True)
