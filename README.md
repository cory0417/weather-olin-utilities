# Utilities through Climate
*A project to search for any interesting patterns between Boston's climate and Olin's electricity consumption.*

As students at Olin, we wanted to investigate further into the effects of local climate on Olin community's utility consumption, specifically, the electricity consumption. One of the possible pattern we brainstormed was that electricity usage is proportional to the temperature since the cooling in the central plant uses electricity. However, we had no quantitative evidence to support our hunch. Similarly, we wanted to visualize and quantitatively analyze any additional pattern in the datasets. 


# Purpose

This repo is meant to:

- Tidy and wrangle Olin's utility data from an excel sheet
- Save and process different types of Boston's climate data
- Visualize relationships between variables
- Perform ANOVA F-test between total monthly electricity consumption and the regressors
- Deliver an analysis and remarks on any interesting patterns

# Structure

In the root directory are the folders `data/` and `tests/`, which contain all necessary dataset to run the jupyter notebook `computational_essay.ipynb`, and the unit tests, respectively. There's also an `images/` folder to store images used in the jupyter notebook. Finally, there a `functions/` folder, which contains all the python functions used for the project.  

# Getting Started

To run the jupyter notebook, first download all required python packages using `pip install -r requirements.txt`.

The jupyter notebook will also require the utility data (`data/electricity_FY13_23_jittered.csv`). To avoid publicly releasing the utility data of Olin College, we've written a script (`jitter_data.py`) to add some randomness to the original data while keeping the general trend alive. If you would like to add your own data, make sure that your data is contained in a csv file with the top row as "start_read_date,end_read_date,total_consumption,time_of_peak_demand,total_cost", marking the column names. You could modify the functions that are used for plotting and statistics to add more columns of data.

To use a different set of climate data from [National Centers for Environmental Information's Climate Data Online (CDO) API](https://www.ncdc.noaa.gov/cdo-web/webservices/v2), make sure to store your API key to a file named `API_KEY.txt` in the root directory of the repo. You can modify the queries by changing the values of `STATION_ID`, `DATASET_ID`, `START_DATE`, `END_DATE`, and `LIMIT` in `functions_manage_data.py`. 

# Unit Testing

All the unit tests are available in `tests/`. To run unit tests:  
```
python -m pytest
```