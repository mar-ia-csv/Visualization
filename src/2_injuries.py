import pandas as pd
import plotly.express as px

file_path = r'AviationData.csv'
aviation_data = pd.read_csv(file_path, encoding='latin1', low_memory=False)


aviation_data['Event.Date'] = pd.to_datetime(aviation_data['Event.Date'], errors='coerce')


aviation_data['Year'] = aviation_data['Event.Date'].dt.year


aviation_data_filtered = aviation_data[aviation_data['Year'] >= 1982]


aviation_data['Total.Fatal.Injuries'] = pd.to_numeric(aviation_data['Total.Fatal.Injuries'], errors='coerce').fillna(0)
aviation_data['Total.Serious.Injuries'] = pd.to_numeric(aviation_data['Total.Serious.Injuries'], errors='coerce').fillna(0)
aviation_data['Total.Minor.Injuries'] = pd.to_numeric(aviation_data['Total.Minor.Injuries'], errors='coerce').fillna(0)


injury_severity = aviation_data_filtered.groupby('Year').agg({
    'Total.Fatal.Injuries': 'sum',
    'Total.Serious.Injuries': 'sum',
    'Total.Minor.Injuries': 'sum'
}).reset_index()


injury_severity_melted = injury_severity.melt(
    id_vars='Year',
    value_vars=['Total.Fatal.Injuries', 'Total.Serious.Injuries', 'Total.Minor.Injuries'],
    var_name='Injury Severity',
    value_name='Count'
)


injury_severity_melted['Injury Severity'] = injury_severity_melted['Injury Severity'].replace({
    'Total.Fatal.Injuries': 'Lesiones mortales',
    'Total.Serious.Injuries': 'Lesiones graves',
    'Total.Minor.Injuries': 'Lesiones menores'
})


fig = px.area(
    injury_severity_melted,
    x='Year',
    y='Count',
    color='Injury Severity',
    title="Severidad de lesiones en accidentes aeronáuticos",
    labels={'Count': 'Número de lesiones', 'Year': 'Año'},
    color_discrete_sequence=[
        '#000080',  
        '#2171B5',  
        '#6BAED6'   
    ]
)


fig.update_traces(
    line=dict(width=0.5)  
)

fig.update_traces(opacity=1)


fig.update_layout(
    title=dict(
        text="Severidad de lesiones en accidentes aeronáuticos",
        font=dict(size=24, family="Roboto, sans-serif"),
        x=0.5
    ),
    xaxis=dict(
        title="Año",
        tickmode="linear",
        dtick=5,
    ),
    yaxis=dict(
        title="Número de lesiones",
    ),
    legend=dict(
        title="Severidad de lesiones",
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    paper_bgcolor="#f9f9f9",
    plot_bgcolor="#f9f9f9",
)

output_path = "html_pages/2_injuries.html"
fig.write_html(output_path, auto_open=True)
