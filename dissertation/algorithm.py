from pyBKT.models import Model
import pandas as pd

model = Model()

count = 0


def runmodel():
    global count
    if count == 0:
        df = pd.read_csv('dataset.csv')

        model.fit(data=df)

        # print(model.evaluate(data=df))
        print(model.params())

        # training_rmse = model.evaluate(data=df)
        # training_auc = model.evaluate(data=df, metric='auc')
        # print("Training RMSE: %f" % training_rmse)
        # print("Training AUC: %f" % training_auc)
        count += 1


def predictmodel(s_df):

    preds_df = model.predict(data=s_df)
    print(preds_df)
    return preds_df
