import numpy as np
import pandas as pd 
import pickle

from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_selection import SelectKBest
from sklearn.preprocessing import KBinsDiscretizer, OneHotEncoder, StandardScaler
from sklearn.metrics import confusion_matrix, plot_confusion_matrix
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier

from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import BernoulliNB, BaseEstimator, BaseNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier

import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly
import plotly.graph_objects as go

class Cleaner(BaseEstimator):
    
    def __init__( self, columns=None, cat_features=None):
        self.columns = columns
        self.cat_features = cat_features
    
    def fit( self, X, y = None ):
        return self 
    
    def transform( self, X, y = None):
        # fill blanks
        try:
            X['public_meeting'] = X['public_meeting'].fillna(value='unknown', axis=0)
        except:
            X=X

        # consolidate rare groups into bigger groups
        try:
            X['waterpoint_type_group'] = X['waterpoint_type_group'].map(lambda x: 'dam, trough, or spring' if x.lower() == 'dam' 
                                                                                else 'dam, trough, or spring' if x.lower() == 'cattle trough' 
                                                                                else 'dam, trough, or spring' if x.lower() == 'improved spring'
                                                                                else x.lower())
        except:
            X=X
        try:
            X['extraction_type_class'] = X['extraction_type_class'].map(lambda x: 'other' if x.lower() == 'wind-powered' 
                                                                                else 'other' if x.lower() == 'rope pump' 
                                                                                else x)
        except:
            X=X

        try:                                                                                
        # take the top members of a category and group the rest together                                                            
            X['management'] = X['management'].map(lambda x: x if x.lower() == 'vwc' 
                                                            else x if x.lower() == 'wug' 
                                                            else x if x.lower() == 'water board' 
                                                            else x if x.lower() == 'wua' 
                                                            else x if x.lower() == 'private operator' 
                                                            else x if x.lower() == 'parastatal' 
                                                            else 'misc.')
        except:
            X=X
        try:
            X['funder'] = X['funder'].map(lambda x: x if x == 'Government Of Tanzania' 
                                                        else x if x == 'Danida' 
                                                        else x if x == 'Hesawa' 
                                                        else x if x == 'Rwssp' 
                                                        else x if x== 'World Bank' 
                                                        else x if x == 'World Vision' 
                                                    else 'misc.')
        except:
            X=X
        try:                                                    
            X['installer'] = X['installer'].map(lambda x: x if x == 'DWE' 
                                                        else x if x == 'Government' 
                                                        else x if x == 'RWE' 
                                                        else 'misc.')
        except:
            X=X            

        try:
            X['district_code'] = X['district_code'].map(lambda x: str(x) if 0 < x < 6 else 'other')
        except:
            X=X
        
        # dummify categorical columns
        X = pd.get_dummies(X, columns=self.cat_features)
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
        single_cat_dict['value'] = value.title()
        single_cat_dict['Percent Working'] = working_perc
        single_cat_dict['Percent Non Functional'] = broken_perc
        single_cat_dict['Percent Needing Repair'] = fixable_perc
        cat_dicts.append(single_cat_dict) 
    
    totals_dict = {'value': 'overall', 'Percent Working': np.array(working_total).mean(), 'Percent Non Functional': np.array(broken_total).mean(),
                                        'Percent Needing Repair': np.array(fixable_total).mean()}
    cat_dicts.append(totals_dict)
    return cat_dicts

def plot_comparison_chart(category, df, overall=False, norm_line=False, cmap='Pastel1'):
    comp_dict_list = assess_categorical_correlation_dict(category, df)
    if not overall:
        comp_dict_list = comp_dict_list[0:-1]
    comp_df = pd.DataFrame(comp_dict_list)
    comp_df = comp_df.set_index('value')
    comp_df = comp_df.sort_values('value')
    ax = comp_df.plot.bar(rot=0, figsize=(20,10), cmap=cmap)
    if norm_line:
        plt.axhline(label='Overall Well Functionality Rate', y=.5466, dash_joinstyle='miter', color='gray', ls='--')
    plt.legend()
    plt.ylabel('Percent', size='x-large')
    ax.tick_params(axis='x', labelsize=12)
    vals = ax.get_yticks()
    ax.set_yticklabels(['{:.0%}'.format(x) for x in vals], fontsize='large')
    return ax

def plot_pretty_cf(predictor, xtest, ytest, cmap='Blues', normalize='true', title=None):
    fig, ax = plt.subplots(figsize=(8, 8))
    plot_confusion_matrix(predictor, xtest, ytest, cmap=cmap, normalize=normalize, ax=ax)
    ax.set_title(title, size='x-large')
    ax.set_yticklabels(['Functional', 'Functional \nNeeds Repair', 'Non-Functional'])
    ax.set_xticklabels(['Functional', 'Functional \nNeeds Repair', 'Non-Functional'])
    ax.set_xlabel('Predicted Label', size='large')
    ax.set_ylabel('True Label', size='large')
    plt.show()