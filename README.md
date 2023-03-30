# Utilities through Climate
*A project to search for any interesting patterns between boston's climate and Olin's electricity consumption.*

# Purpose

This repo is meant to:

- tidy and wrangle Olin's utility data from an excel sheet
- save and process different types of Boston's climate data
- visualize relationships between variables
- perform ANOVA F-test between total monthly electricity consumption and the regressors
- deliver an analysis and remarks on any interesting patterns

# Getting Started

First download all required python packages using `pip install -r requirements.txt`
Running the jupyter notebook file for the computational essay will require the utility data that is not public on the repository. 
*Contact either Ellen Sun (esun@olin.edu) or Daeyoung Kim (dkim2@olin.edu) for a csv file containing the utility data.*


# Unit Testing

All the unit tests are available in `tests/`. To run unit tests:  
```
pytest tests/
```