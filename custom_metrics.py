from init import *

def pred_accuracy(y_test, y_pred):
    '''Compute accuracy based on whether or not actual value falls between 
    predicted value +/- 2 minutes'''

    bools = ((y_test >= y_pred - 120) & (y_test <= y_pred + 120))*1
    return sum(bools)/len(bools)