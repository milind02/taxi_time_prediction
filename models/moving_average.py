from init import *
from custom_metrics import *

def moving_average_pred(df, test_threshold):
    '''Compute RMSE and accuracy of baseline moving average predictions'''

    y_pred = df.sort_values('AOBT')\
               .assign(moving_average = df.target.expanding().mean().shift(1))\
               .query(test_threshold)['moving_average']
    
    y_test = df.sort_values('AOBT')\
               .query(test_threshold)['target']
    
    rmse = mean_squared_error(y_test, y_pred) ** 0.5
    acc = pred_accuracy(y_test, y_pred)
    
    return rmse, acc, y_pred