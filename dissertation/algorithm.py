from pyBKT.models import Model
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

model = Model(num_fits=1)
count = 0

def runmodel():
    '''
    Initialises the model, global count variable ensures its only ran once on development 
    server 

    :return: A trained model
    '''
    global count
    if count == 0:
        df = pd.read_csv('dataset.csv')
        train, test = train_test_split(df, test_size=0.2)
        model.fit(data=train)
        print('TRAINED PARAMS', model.params())
        pred = model.predict(data=test)
        print('TEST', pred)

        # Evaluation
        training_auc = model.evaluate(data=test, metric='auc')
        training_acurracy = model.evaluate(data=test, metric='accuracy')
        print("Training AUC: %f" % training_auc)
        print("Training Accuracy: %f" % training_acurracy)

        count += 1
    return model


def predictmodel(s_df):
    '''
    Takes a dataframe with the userid, question_type, correct
    Predicts the students cognitive state based on the inputs
    Returns a dataframe with correct_prediction and state_prediction

    :param s_df: dataframe with student information
    :return: dataframe with correct and state_predictions
    '''
    print('PREDICTED PARAMS', model.params())
    df = s_df
    retrain(df)
    preds_df = model.predict(data=s_df)
    return preds_df

def retrain(df):
    '''
    Performs a partial fit on the model, first adds the new data to the dataset
    :param s_df: dataframe with student information
    :return: no return
    '''
    f = open('dataset.csv', 'a')
    df.to_csv(f, header=False)
    f.close()
    df = pd.read_csv('dataset.csv')
    model.partial_fit(data=df)
    print(model.params())

def evaluate():
    '''
    Performs 3 different types of evaluation on the dataset 
    '''
    df = pd.read_csv('dataset.csv')
    training_rmse = model.evaluate(data=df)
    training_auc = model.evaluate(data=df, metric='auc')
    training_acurracy = model.evaluate(data=df, metric='accuracy')
    print("Training RMSE: %f" % training_rmse)
    print("Training AUC: %f" % training_auc)
    print("Training Accuracy: %f" % training_acurracy)
    return training_rmse, training_auc, training_acurracy
