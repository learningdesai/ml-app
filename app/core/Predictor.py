from app.core.ModelPreProcess import ModelPreProcess
from app.core.OLSRegressor import OLSRegressor
from app.core.ResultModel import ResultModel
from app.core.ShipmentCompleteModel import ShipmentCompleteModel
from app.core.ShipmentMonthModel import ShipmentMonthModel
from app.core.ShipmentWeightModel import ShipmentWeightModel
from app.core.ShipmentDimenModel import ShipmentDimenModel
from app.core.ShipmentPredDimenModel import ShipmentPredDimenModel
from app.core.DelwinModel import DelwinModel

import json

shp = ModelPreProcess()
ols = OLSRegressor()
rm = ResultModel()

models = {
  "complete": ShipmentCompleteModel(),
  "month": ShipmentMonthModel(),
  "weight": ShipmentWeightModel(),
  "delwin": DelwinModel(),
  "dimen": ShipmentDimenModel(),
  "pred_dimen": ShipmentPredDimenModel()
}


class Predictor:
    
    def __init__(self, test_file_name, env="app", mode=None):
        self.TEST_FILE = test_file_name
        APP_PATH = "app/core/"
        if env != "app":
            APP_PATH = ""
        if not mode:
            mode = ""
        else:
            mode += "/"
        
        self.TRAIN_FILE = APP_PATH + ols.get_saved_data(APP_PATH + 'models/'+mode+'pickledTrainFileName.pkl')
        self.TRAIN_LENGTH = ols.get_saved_data(APP_PATH + 'models/'+mode+'pickledTrainingLength.pkl')
        self.MODEL = ols.get_saved_data(APP_PATH + 'models/'+mode+'pickledModel.pkl')        
        
    def start(self,  metrics=False, mode=None):
        
        if not mode:
            mode = "complete"
        
        test_df = shp.load_csv(self.TEST_FILE)        
        
        train_df = shp.load_csv(self.TRAIN_FILE)        
        
        #combined is needed when we are using oneHot encoder
        combined = shp.concat(train_df, test_df)
                
        with open('app/core/config/'+mode+'.json') as f:
            data = json.load(f)
        
        cols, encoder_data = data['cols'], data['encoder_data']
        
        X, y = shp.getXandY(combined, cols, encoder_data)
        
        X, y = X[self.TRAIN_LENGTH:], y[self.TRAIN_LENGTH:]
        print("here x shape: ", X.shape)        
        print("here y shape: ", y.shape)        
        y_pred = ols.getPredictions(self.MODEL, X)

        print("got pred")        
        json_result = models[mode].get_json_result(test_df, y_pred, y)
        print("got results")
        if metrics:
            metrics = rm.get_metrics(y_pred, y)
        else:
            metrics = ""
    
        return {
                "test_file_name": self.TEST_FILE,
                "X": X,
                "y": y,
                "json_result": json_result,
                "metrics": metrics
        }

