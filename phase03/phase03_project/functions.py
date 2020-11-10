import numpy as np
import pandas as pd 

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_selection import SelectKBest
from sklearn.preprocessing import KBinsDiscretizer, OneHotEncoder
from sklearn.metrics import confusion_matrix, plot_confusion_matrix


from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import BernoulliNB, BaseEstimator, BaseNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline

import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly
import plotly.graph_objects as go

class Cleaner(BaseEstimator):
    
    def __init__( self, columns=None):
        self.columns = columns
    
    def fit( self, X, y = None ):
        return self 
    
    def transform( self, X, y = None):
        # to_drop = X.loc[X['amount_tsh'] > 40005].index
        # X = X.drop(to_drop)
        # y = y.drop(to_drop)
        try:
            X['funder'] = X['funder'].fillna(value='unknown', axis=0)
            X['public_meeting'] = X['public_meeting'].fillna(value='unknown', axis=0)
            X['scheme_management'] = X['scheme_management'].fillna(value='unknown', axis=0)
            X['waterpoint_type_group'] = X['waterpoint_type_group'].map(lambda x: lambda x: 'other' if x == 'dam' 
                                                                        else 'other' if x == 'cattle trough' 
                                                                        else 'other' if x == 'improved spring' else x)

        except:
            X = X
        X = pd.get_dummies(X)
        return X


def assess_categorical_correlation_printout(column_name, dataframe):
    working_total = []
    broken_total = []
    fixable_total = []

    for value in dataframe[column_name].unique():
        all_working = len(dataframe.loc[(dataframe[column_name] == value) & (dataframe['status_group'] == 'functional')])
        all_broken = len(dataframe.loc[(dataframe[column_name] == value) & (dataframe['status_group'] == 'non functional')])
        all_fixable = len(dataframe.loc[(dataframe[column_name] == value) & (dataframe['status_group'] == 'functional needs repair')])
        total_val = len(dataframe.loc[dataframe[column_name] == value])

        working_perc = all_working / total_val
        broken_perc = all_broken / total_val
        fixable_perc = all_fixable / total_val

        working_total.append(working_perc)
        broken_total.append(broken_perc)
        fixable_total.append(fixable_perc)

        print(f'percent working for {value} is {all_working / total_val}')
        print(f'percent broken for {value} is {all_broken / total_val}')
        print(f'percent fixable for {value} is {all_fixable / total_val}')
        print('\n')
    
    print(f'working {np.array(working_total).mean()}')
    print(f'broken {np.array(broken_total).mean()}')
    print(f'fixable {np.array(fixable_total).mean()}')

def assess_categorical_correlation_dict(column_name, dataframe):
    working_total = []
    broken_total = []
    fixable_total = []

    cat_dicts = []

    for value in dataframe[column_name].unique():
        all_working = len(dataframe.loc[(dataframe[column_name] == value) & (dataframe['status_group'] == 'functional')])
        all_broken = len(dataframe.loc[(dataframe[column_name] == value) & (dataframe['status_group'] == 'non functional')])
        all_fixable = len(dataframe.loc[(dataframe[column_name] == value) & (dataframe['status_group'] == 'functional needs repair')])
        total_val = len(dataframe.loc[dataframe[column_name] == value])

        working_perc = all_working / total_val
        broken_perc = all_broken / total_val
        fixable_perc = all_fixable / total_val

        working_total.append(working_perc)
        broken_total.append(broken_perc)
        fixable_total.append(fixable_perc)

        single_cat_dict = {}
        single_cat_dict['value'] = value.upper()
        single_cat_dict['Percent Working'] = working_perc
        single_cat_dict['Percent Broken'] = broken_perc
        single_cat_dict['Percent Needing Repair'] = fixable_perc
        cat_dicts.append(single_cat_dict) 
    
    totals_dict = {'value': 'overall', 'Percent Working': np.array(working_total).mean(), 'Percent Broken': np.array(broken_total).mean(),
                                        'Percent Needing Repair': np.array(fixable_total).mean()}
    cat_dicts.append(totals_dict)
    return cat_dicts

def plot_comparison_chart(category, df, overall=True):
    comp_dict_list = assess_categorical_correlation_dict(category, df)
    if not overall:
        comp_dict_list = comp_dict_list[0:-1]
    comp_df = pd.DataFrame(comp_dict_list)
    comp_df = comp_df.set_index('value')
    comp_df = comp_df.sort_values('value')
    ax = comp_df.plot.bar(rot=0, figsize=(20,10))
    plt.show()
