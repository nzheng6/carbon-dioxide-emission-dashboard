import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from shiny import App, Inputs, Outputs, Session, reactive, render, req, ui
from shinywidgets import output_widget, render_widget

emission_df = pd.read_csv("data/co2_emissions_kt_by_country.csv")

app_ui = ui.page_fillable(
    ui.page_navbar(title="CO2 Emission by Country"),
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
                    Data was obtained from the Kaggle dataset [CO2 Emissions](https://www.kaggle.com/datasets/ulrikthygepedersen/co2-emissions-by-country).

                    ***License***  
                    [Attribution 4.0 International (CC BY 4.0 DEED)](https://creativecommons.org/licenses/by/4.0/)

                    ---
                    # Context
                    ---

                    ---
                    # Instructions
                    ---
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
            sns.barplot(x='value', y='country_name', hue='country_name', orient='h', ci=None, data=df)
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