import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from shiny import App, Inputs, Outputs, Session, reactive, render, req, ui
from shinywidgets import output_widget, render_widget

emission_df = pd.read_csv("data/co2_emissions_kt_by_country.csv")

app_ui = ui.page_fillable(
    ui.page_navbar(title="Carbon Dioxide Emission by Country"),
    ui.page_sidebar(
        ui.sidebar(
            ui.input_select("graph", "Graph", selected="Line", multiple=False, choices=("Line", "Bar", "Map")),
            ui.panel_conditional(
                "input.graph == 'Line' || input.graph == 'Bar'",
                ui.input_selectize("country_name", "Country / Region", selected="Aruba", multiple=True, choices=list(emission_df.country_name.unique())),
            ),
            ui.panel_conditional(
                "input.graph == 'Line'",
                ui.input_selectize("start_year", "Start Year", selected=1960, multiple=False, choices=list(range(1960, 2020))),
                ui.input_selectize("end_year", "End Year", selected=2019, multiple=False, choices=list(range(1960, 2020))),
            ),
            ui.panel_conditional(
                "input.graph == 'Bar' || input.graph == 'Map'",
                ui.input_selectize("year", "Year", selected=1960, multiple=False, choices=list(range(1960, 2020))),
            ),
            width = 350,
        ),
        ui.navset_tab(
            ui.nav_panel(
                "Historical",
                ui.panel_conditional(
                    "input.graph == 'Line' || input.graph == 'Bar'",
                    ui.output_plot("plot"), 
                ),
                ui.panel_conditional(
                    "input.graph == 'Map'",
                    output_widget("map"), 
                ),
            ),
            ui.nav_panel("About",
                ui.markdown(
                    """
                    ---
                    # Citation & Acknowledgement
                    ---

                    ### Data
                    Data was obtained from the [CO2 Emissions](https://www.kaggle.com/datasets/ulrikthygepedersen/co2-emissions-by-country) Kaggle dataset.

                    ***License***  
                    [Attribution 4.0 International (CC BY 4.0 DEED)](https://creativecommons.org/licenses/by/4.0/)

                    ---
                    # Context
                    ---
                    With global warming, the emission of greenhouse gases is growing concern. By visualizing CO2 emissions, we can evaluate the effectiveness of climate policies and better allocate our efforts in reducing carbon emissions.  

                    ---
                    # Instructions
                    ---
                    On the left sidebar, select your desired graph under the "Graph" section. You may select from the following choices:  
                    - Line
                    - Bar
                    - Map

                    ### Line Graph
                    When you select "Line" under "Graph", you will see three inputs below:
                    - Country / Region
                    - Start Year
                    - End Year

                    These inputs will modify the line graph according to your preferences.

                    1. Type or select your desired country or region in the "Country / Region" input. You may select multiple countries / regions. 
                    2. Type or select the year that you want to start viewing data from in the "Start Year" input.
                    3. Type or select the year that you want to view the data up to in the "End Year" input.

                    ***Example Usage***
                    1. Type "Belgium" and "Denmark" in the "Country / Region" input. 
                    2. Type "1997" in the "Start Year" input.
                    3. Type "2010" in the "End Year" input. 
                    4. The final line graph shows the CO2 carbon emission in kilotons (kt) for Belgium and Denmark from 1997 to 2010. 

                    ### Bar Graph
                    When you select "Bar" under "Graph", you will see two inputs below:
                    - Country / Region 
                    - Year

                    These inputs will modify the bar graph according to your preferences. 

                    1. Type or select your desired country or region in the "Country / Region" input. You may select multiple countries / regions. 
                    2. Type or select the year that you want to view data from in the "Year" input.

                    ***Example Usage***
                    1. Type "Belgium" and "Denmark" in the "Country / Region" input. 
                    2. Type "2010" in the "Year" input. 
                    3. The final bar graph shows the CO2 carbon emission in kilotons (kt) for Belgium and Denmark in 2010. 

                    ### Map
                    When you select "Line" under "Graph", you will see one input below:
                    - Year

                    This input will determine what year the map is based on.

                    1. Type or select the year that you want to view data from in the "End Year" input.

                    ***Example Usage***
                    1. Type "2010" in the "End Year" input. 
                    2. The final map shows the CO2 carbon emission in kilotons (kt) around the world in 2010. The intensity of the color is based on the carbon emission of the country / region. You may hover over the map to see details. 
                    """
                ) 
            ),
        ),
    )
)

def server(input: Inputs, output: Outputs, session: Session):
    @reactive.Calc
    def filtered_df() -> pd.DataFrame:
        df = emission_df
        if input.graph() == 'Line' or input.graph() == 'Bar':
            df = df[df['country_name'].isin(input.country_name())]
        if input.graph() == 'Line':
            start_year = int(input.start_year())
            end_year = int(input.end_year())
            df = df[(df['year'] >= start_year) & (df['year'] <= end_year)]
        if input.graph() == 'Bar' or input.graph() == 'Map':
            year = int(input.year())
            df = df[df['year'] == year]
        return df

    @render.plot
    def plot():
        df = filtered_df()
        fig, ax = plt.subplots()
        if input.graph() == 'Line':
            sns.lineplot(x='year', y='value', hue='country_name', data=df)
            plt.legend(title='Country / Region')
            ax.set_xlabel('Year')
            ax.set_ylabel('CO2 Emissions in Kiloton (kt)')
            ax.grid()
        elif input.graph() == 'Bar':
            sns.barplot(x='value', y='country_name', hue='country_name', orient='h', errorbar=None, data=df)
            ax.set_xlabel('CO2 Emissions in Kiloton (kt)')
            ax.set_ylabel('Country / Region')
        return fig
    
    @render_widget  
    def map():  
        df = filtered_df()
        fig = px.choropleth(
            df, 
            locations='country_code', 
            hover_name='country_name',
            hover_data=['value'],
            color='value',
            color_continuous_scale='Reds',
        )
        fig.layout.coloraxis.colorbar.title = 'CO2 Emissions in Kiloton (kt)'
        return fig  

app = App(app_ui, server)