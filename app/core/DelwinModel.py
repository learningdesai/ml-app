import numpy as np

try:
    from app.core.ResultModel import ResultModel
except:
    from ResultModel import ResultModel



class DelwinModel(ResultModel):
    
    def get_json_result(self, data, y_pred, y_test, hasActual=True, mode=None):
        
        """ make a dictionary with the test results
        for the complete dataset """        
        
        if not hasActual:             
            # create a dummy shipmentCount column
            data['Diff_Time'] = -1
                            
        
        results = []
        
        length = len(y_pred) 
        
        for i in range(length):          
            
            stop_actual = np.asscalar(np.int64(data.iloc[i]['Stop_Actual_Sequence_Num']))
            postal_code = np.asscalar(np.int64(data.iloc[i]['Postal_Code']))
            district_num = np.asscalar(np.int64(data.iloc[i]['District_Num']))
            street_num = np.asscalar(np.int64(data.iloc[i]['Street_Num']))
            results.append({
                "stop_actual_seq": stop_actual,                        
                "postal_code": postal_code, 
                "district_num": district_num, 
                "street_num": street_num, 
                "actual_diff_time": np.asscalar(np.int64(y_test[i][0])),
                "predicted_diff_time": np.asscalar(np.int64(int(round(y_pred[i])))),
                "diff": np.asscalar(np.int16(int(round(abs(y_pred[i] - y_test[i])[0])) )) if hasActual else -1
            }) 
        
        return results 
    
  