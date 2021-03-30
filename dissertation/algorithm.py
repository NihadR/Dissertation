from pyBKT.models import Model
import pandas as pd

model = Model()
count = 0


def runmodel():
    '''
    Initialises the model, global count variable ensures its only ran once on development 
    server 
    '''
    global count
    if count == 0:
        # model = Model()
        df = pd.read_csv('dataset.csv')

        model.fit(data=df)

        # print(model.evaluate(data=df))
        print('TRAINED PARAMS', model.params())

        # training_rmse = model.evaluate(data=df)
        # training_auc = model.evaluate(data=df, metric='auc')
        # print("Training RMSE: %f" % training_rmse)
        # print("Training AUC: %f" % training_auc)
        count += 1
    return model


def predictmodel(s_df):
    '''
    Takes a dataframe with the userid, question_type, correct
    Predicts the students cognitive state based on the inputs
    Returns a dataframe with correct_prediction and state_prediction
    '''
    print('PREDICTED PARAMS', model.params())

    preds_df = model.predict(data=s_df)
    print(preds_df)
    return preds_df
