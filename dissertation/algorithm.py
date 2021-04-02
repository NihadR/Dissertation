from pyBKT.models import Model
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

model = Model()
count = 0


def runmodel():
    '''
    Initialises the model, global count variable ensures its only ran once on development 
    server 
    '''
    global count
    if count == 0:
        df = pd.read_csv('dataset.csv')
        train, test = train_test_split(df, test_size=0.2)
        print(len(train))
        print(len(test))
        model.fit(data=train)
        print('TRAINED PARAMS', model.params())
        pred = model.predict(data=test)
        print('TEST', pred)

        # Do accuracy 
        training_rmse = model.evaluate(data=test)
        training_auc = model.evaluate(data=test, metric='auc')
        print("Training RMSE: %f" % training_rmse)
        print("Training AUC: %f" % training_auc)


        count += 1
    return model


def predictmodel(s_df):
    '''
    Takes a dataframe with the userid, question_type, correct
    Predicts the students cognitive state based on the inputs
    Returns a dataframe with correct_prediction and state_prediction
    '''
    print('PREDICTED PARAMS', model.params())
    df = s_df
    retrain(df)
    print('thaisd', df)
    preds_df = model.predict(data=s_df)
    print(preds_df)
    return preds_df

def retrain(df):
    f = open('dataset.csv', 'a')
    df.to_csv(f, header=False)
    f.close()
    print(df)
    df = pd.read_csv('dataset.csv')
    model.partial_fit(data=df)
    print(model.params())
