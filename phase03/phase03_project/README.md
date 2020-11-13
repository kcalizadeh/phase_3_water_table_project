# Pump It Up: Data Mining the Water Table
![title](images/well.jpg)
#### Repo Contents:
- a [folder](https://github.com/kcalizadeh/phase_3_water_table_project/tree/master/phase03/phase03_project/pump_data) containing data used in the project
- a [folder](https://github.com/kcalizadeh/phase_3_water_table_project/tree/master/phase03/phase03_project/images) containing relevant images
- an [EDA notebook](https://github.com/kcalizadeh/phase_3_water_table_project/blob/master/phase03/phase03_project/EDA_notebook.ipynb) containing some visualizations and exploration
- a [model notebook](https://github.com/kcalizadeh/phase_3_water_table_project/blob/master/phase03/phase03_project/model_notebook.ipynb) explaining our model and going over various iterations
- a [functions.py file](https://github.com/kcalizadeh/phase_3_water_table_project/blob/master/phase03/phase03_project/functions.py) containing custom functions and imports used in both notebooks
- a [slide deck presentation](https://github.com/kcalizadeh/phase_3_water_table_project/blob/master/phase03/phase03_project/presentation.pdf) of the findings

This repo contains work for the Pump It Up data science competition. The competition website can be found [here](https://www.drivendata.org/competitions/7/pump-it-up-data-mining-the-water-table/page/23/).

The overall aim of the project is to use ML to predict the operational status of wells in Tanzania. These wells fell into three categories: functional, functional but in need of repair, and non-functional. 

We used an OSEMN approach to handle this task.

### Obtain & Scrub
The data was available for download from the competition website. Looking it over, we discovered several null values, redundant columns, and placeholder values. These we dealt with in ways appropriate for each category. For example. for 0s in the 'construction_year' category, we imputed random years based on the existing spread of years.

### Explore
Here we examined the connection between various features and the functionality of the wells. We built a helper function to visualize the percent of working wells in each category and went through each category looking for those that could help classify the data. Some visualizations and details of this process can be found in the EDA notebook; one example is provided below.

![title](images/well_functionality_by_year.png)

### Model
We built a Random Forest model and used a grid search to tweak hyperparameters. Our final model was reasonably accurate. Results were confirmed with a confusion matrix. Overall, it was the repairable wells that were hardest to classify. This is likely due in part to a class imbalance, but SMOTE was not able to correct the problem and indeed made our model worse. 

Upon submission, this was our highest score:

![](images/submission_result2.png)

### Interpret
The most important features for our model were the geographic features, especially latitude, longitude, and gps_height. Other relevant strong features were waterpoint type and extraction method. 

![](images/confusion_matrix.png)

As this confusion matrix shows, we were better at predicting functional wells than non-functional. This could reflect a slight bias in the data - slightly more wells were functional than non-functional. 

A cost matrix analysis and more interpretation is included in the model notebook.


## Future Work
- try to find features that uniquely identify the wells in need of repair, since those should be our top priorities
- work to chart out the most water-starved regions. Many broken wells exist adjacent to functioning wells; when it comes to actually improving people's lives, fixing those wells is not as important as focusing on areas where there are fewer functioning wells per person.
- deal more thoroughly with data cleaning:
    - impute missing long/lat data by using data from villages, basins, etc.
    - create more macro-categories for funders, schemes, and other features with too many categories
- work on model-stacking to combine several models and hopefully increase accuracy
    - this could be exceptionally useful if we did KNN on the geographic data, for example.