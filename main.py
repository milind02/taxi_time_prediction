# -*- coding: utf-8 -*-
"""main

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BQd4fa7OgfVyNOF5VIrjP0ExoVvkHs1i
"""

# Custom Imports 
from init import *
from custom_metrics import * 
from preprocessing_functions import *
from models import *

# Load and Process Data
print('Processing Train Set...')
df_train = preprocess(geo_path =  'data/geographic_data.csv', 
                      airport_path = 'data/training_set_airport_data.csv', 
                      weather_path = 'data/Weather_data.csv')

print('Processing Test Set...')
df_test = preprocess(geo_path =  'data/geographic_data.csv', 
                     airport_path = 'data/test_set_airport_data.csv', 
                      weather_path = 'data/test_set_weather_data.csv')


# Assign Features
train_cols = ['aircraft_model', 'Stand', 'Runway',
       'temperature', 'apparentTemperature', 'dewPoint', 'humidity',
       'windSpeed', 'windBearing', 'cloudCover', 'uvIndex',
       'visibility', 'precipType', 'precipAccumulation', 'ozone', 'N', 'Q',
       'distance', 'dist_log', 'AOBT_year', 'AOBT_month', 'AOBT_day',
       'AOBT_hour', 'AOBT_min']

cat_features = ['aircraft_model', 'Stand', 'Runway', 'AOBT_year', 'AOBT_month',
              'AOBT_day','AOBT_hour', 'AOBT_min', 'precipType']


# Cross Validation
print('Cross-Validating on 2018 Data...')

df_train_cv = df_train.query('AOBT_year < 2018')
df_val = df_train.query('AOBT_year == 2018')

print('Running Baseline Moving Average...')
ma_rmse_val, ma_acc_val, ma_y_pred_val = moving_average_pred(df_train, 'AOBT_year == 2018')

print('Running Light Gradient Boosted Model...')
lgbm_rmse_val, lgbm_acc_val, lgbm_y_pred_val, lgbm_y_test_val, lgbm_val, lgbm_X_train_val = lgbm_pred(df_train_cv, df_val, train_cols, cat_features)

print('Running XGBoost...')
xgb_rmse_val, xgb_acc_val, xgb_y_pred_val, xgb_y_test_val, xgb_val, xgb_X_train_val = xgb_pred(df_train_cv, df_val, train_cols, cat_features)

print('Running Random Forest...')
rf_rmse_val, rf_acc_val, rf_y_pred_val, rf_y_test_val, rf_val, rf_X_train_val = rf_pred(df_train_cv, df_val, train_cols, cat_features)

print('Cross-Validation Results:')

print('Baseline RMSE / Accuracy: ' + str(ma_rmse_val) + ' / ' + str(ma_acc_val))
print('LGBM RMSE / Accuracy: ' + str(lgbm_rmse_val) + ' / ' + str(lgbm_acc_val))
print('XGB RMSE / Accuracy: ' + str(xgb_rmse_val) + ' / ' + str(xgb_acc_val))
print('RF RMSE / Accuracy: ' + str(rf_rmse_val) + ' / ' + str(rf_acc_val))



# Modeling on Full Data
print('Modeling on Full Dataset...')

print('Running Baseline Moving Average...')
ma_rmse, ma_acc, ma_y_pred = moving_average_pred(pd.concat([df_train, df_test]).reset_index(), 
                                                 'AOBT_year == 2019')

print('Running Light Gradient Boosted Model...')
lgbm_rmse, lgbm_acc, lgbm_y_pred, lgbm_y_test, lgbm, lgbm_X_train = lgbm_pred(df_train, df_test, train_cols, cat_features)

print('Running XGBoost...')
xgb_rmse, xgb_acc, xgb_y_pred, xgb_y_test, xgb, xgb_X_train = xgb_pred(df_train, df_test, train_cols, cat_features)

print('Running Random Forest...')
rf_rmse, rf_acc, rf_y_pred, rf_y_test, lr, rf_X_train = rf_pred(df_train, df_test, train_cols, cat_features)

print('Final Results:')

print('Baseline RMSE / Accuracy: ' + str(ma_rmse) + ' / ' + str(ma_acc))
print('LGBM RMSE / Accuracy: ' + str(lgbm_rmse) + ' / ' + str(lgbm_acc))
print('XGB RMSE / Accuracy: ' + str(xgb_rmse) + ' / ' + str(xgb_acc))
print('RF RMSE / Accuracy: ' + str(rf_rmse) + ' / ' + str(rf_acc))

