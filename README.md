# CS 498 E2E Final Project (sp24) repo for NetID: nzheng6

GitHub username at initialization time: nzheng6

# CO2 Carbon Emission Dashboard

## Purpose
The purpose of this dashboard is to help visualize the amount of carbon dioxide (CO2) emitted by each country from 1960 to 2019. 

## Context
With global warming, the emission of greenhouse gases is growing concern. By visualizing CO2 emissions, we can evaluate the effectiveness of climate policies and better allocate our efforts in reducing carbon emissions. 

This dashboard uses data from the [CO2 Emissions](https://www.kaggle.com/datasets/ulrikthygepedersen/co2-emissions-by-country) Kaggle dataset.

## Setup
1. Clone repository
```bash
$ git clone https://github.com/illinois-cs-coursework/sp24_cs498e2e-final_nzheng6.git
```

2. Install `uv`
```bash
$ python3.11 -m pip install uv
```

3. Create a virtual environment
```bash
$ uv venv
```

4. Install required dependencies
```bash
$ uv pip install -r requirements.txt
```

4. Run app.py using the Shiny VSCode extension or try:
```bash
$ shiny run app.py
```
---
## Usage
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