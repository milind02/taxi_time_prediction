from init import *
from custom_metrics import *

def xgb_pred(df_train, df_test, train_cols, cat_features):
    '''Run XGBoost Model pipeline. 
    Returns the following: RMSE, Accuracy, Predictions, 
                           True Values, Model, Train Set'''
    
    X_train = df_train[train_cols]
    y_train = df_train['target']
    X_test = df_test[train_cols]
    y_test = df_test['target']
    
    X_train_cat = pd.get_dummies(X_train, columns = cat_features)
    X_test_cat = pd.get_dummies(X_test, columns = cat_features)

    # Make sure Test set has the same columns
    excess_cols_in_train = list(set(X_train_cat.columns) - set(X_test_cat.columns))

    X_test_cat = X_test_cat\
                        .assign(**dict(zip(excess_cols_in_train, [0]*len(excess_cols_in_train))))\
                        [X_train_cat.columns]

    xgb = XGBRegressor()

    xgb.fit(X_train_cat, y_train)

    y_pred = xgb.predict(X_test_cat)
    
    rmse = mean_squared_error(y_test, y_pred) ** 0.5
    acc = pred_accuracy(y_test, y_pred)
    
    return rmse, acc, y_pred, y_test, xgb, X_train