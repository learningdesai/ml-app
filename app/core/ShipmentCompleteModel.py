import numpy as np

try:
    from app.core.ResultModel import ResultModel
except:
    from ResultModel import ResultModel



class ShipmentCompleteModel(ResultModel):
    
    def get_json_result(self, data, y_pred, y_test, hasActual=True, mode=None):
        
        """ make a dictionary with the test results
        for the complete dataset """        
        
        if not hasActual:             
            # create a dummy shipmentCount column
            data['ShipmentCount'] = -1
                            
        
        results = []
        
        length = len(y_pred) 
        
        for i in range(length):          
            location = data.iloc[i]['DestLocCode']
            month = np.asscalar(np.int64(data.iloc[i]['MonthNumber']))
            weight = np.asscalar(np.int64(data.iloc[i]['StandardWeightInKG']))
            results.append({
                "location": location,                        
                "month": month, 
                "weight": weight,                         
                "actual_count": np.asscalar(np.int64(y_test[i][0])),
                "predicted_count": np.asscalar(np.int64(int(round(y_pred[i])))),
                "diff": np.asscalar(np.int16(int(round(abs(y_pred[i] - y_test[i])[0])) )) if hasActual else -1
            }) 
        
        return results 
    
  
   