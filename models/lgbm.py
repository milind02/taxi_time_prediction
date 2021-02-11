from init import *

def lgbm_pred(df_train, df_test, train_cols, cat_features):
    '''Run Light Gradient Boosted Model pipeline. 
    Returns the following: RMSE, Accuracy, Predictions, 
                           True Values, Model, Train Set'''

    X_train = df_train[train_cols]
    y_train = df_train['target']
    X_test = df_test[train_cols]
    y_test = df_test['target']
    
    lgb_train = lgb.Dataset(X_train, y_train)
    lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)

    params = {
        'boosting_type': 'gbdt',
        'objective': 'regression',
        'metric': {'l2', 'l1'}
    }

    gbm = lgb.train(params,
                    lgb_train,
                    num_boost_round=200,
                    valid_sets=lgb_eval,
                    early_stopping_rounds=5,
                    categorical_feature = cat_features)


    y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)
    
    rmse = mean_squared_error(y_test, y_pred) ** 0.5
    acc = pred_accuracy(y_test, y_pred)
    
    return rmse, acc, y_pred, y_test, gbm, X_train