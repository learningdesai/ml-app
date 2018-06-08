from app.core.ModelPreProcess import ModelPreProcess
from app.core.OLSRegressor import OLSRegressor
from app.core.ResultModel import ResultModel
from app.core.ShipmentCompleteModel import ShipmentCompleteModel
from app.core.ShipmentMonthModel import ShipmentMonthModel
from app.core.ShipmentWeightModel import ShipmentWeightModel
from app.core.ShipmentDimenModel import ShipmentDimenModel
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
  "dimen": ShipmentDimenModel()
}


class PredictorSingle:
    
    def __init__(self, json_data):
        
        self.json_data = json_data
        
        APP_PATH = "app/core/"                        
        
        mode = self.json_data["mode"]
        
        if not mode:
            mode = ""
        else:
            mode += "/"
        print("here ", mode)
        self.TRAIN_FILE = APP_PATH + ols.get_saved_data(APP_PATH + 'models/'+mode+'pickledTrainFileName.pkl')
        self.TRAIN_LENGTH = ols.get_saved_data(APP_PATH + 'models/'+mode+'pickledTrainingLength.pkl')
        self.MODEL = ols.get_saved_data(APP_PATH + 'models/'+mode+'pickledModel.pkl')        
        
    def start(self):
        
        mode = self.json_data["mode"]
        
        if not mode:
            mode = "complete"
        
        #test_df = shp.load_csv(self.TEST_FILE)        
        # convert json_data columns and values to dataframe
        test_df = shp.json_to_dataframe(self.json_data["data"])
        print(test_df)
        train_df = shp.load_csv(self.TRAIN_FILE) 
                        
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
        print("X: ",X)
        print("y: ", y)
        print("y_pred: ", y_pred)
        json_result = models[mode].get_json_result(test_df, y_pred, y)
        print("got results")        
        print(X, y, y_pred, json_result)
        return {                
                "X": X,
                "y": y,
                "json_result": json_result,               
        }

"""
Example POST Data
{
	"mode": "dimen",
    "data": {
        "ShipmentCount": 15,
        "DestLocCode": "CKG",
        "MonthNumber": 9,
        "StandardWeightInKG": 7,
        "CustomStdWidth": 15,
        "CustomStdHeight": 33,
        "CustomStdLength": 51
    }
}
    
    OR

{
	"mode": "",
    "data": {
        "ShipmentCount": 9,
        "DestLocCode": "ONT",
        "MonthNumber": 8,
        "StandardWeightInKG": 11
    }
}
    
"""