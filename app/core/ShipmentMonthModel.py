import numpy as np
import calendar
from collections import OrderedDict

try:
    from app.core.ResultModel import ResultModel
except:
    from ResultModel import ResultModel



class ShipmentMonthModel(ResultModel):
    
    def get_json_result(self, data, y_pred, y_test, hasActual=True, mode=None):
        
        """ make a dictionary with the test results
        for the complete dataset """        
        
        if not hasActual:             
            # create a dummy shipmentCount column
            data['ShipmentCount'] = -1
                            
        
        results = []
        
        length = len(y_pred) 
      
        
        
        for i in range(length):
            month = np.asscalar(np.int64(data.iloc[i]['MonthNumber']))
            results.append({                
                "month": month,                     
                "actual_count": np.asscalar(np.int64(y_test[i][0])),
                "predicted_count": np.asscalar(np.int64(int(round(y_pred[i])))),
                "diff": np.asscalar(np.int16(int(round(abs(y_pred[i] - y_test[i])[0])) )) if hasActual else -1
            }) 
        
        
        return results 
    
    def get_month_results(self, results, hasActual=True):
     
        # [ [12, 8934, 9837], [05, 1923, 1239], ...]
        output = [ [ i["month"], i["actual_count"], i["predicted_count"] ] for i in results]
        dic = {}
        month = {
            1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
        }
        for i in output:
            if month[i[0]] not in dic:
                dic[ month[i[0]] ] = [month[i[0]], i[1], i[2]]
            else:
                dic[ month[i[0]] ] = [ month[i[0]], dic[ month[i[0]] ][1] + i[1],  dic[ month[i[0]] ][2] + i[2] ]
        
        month_numeric_mapping = {abb: index for abb in dic for index, long in enumerate(calendar.month_name[1:]) if str.lower(abb) in str.lower(long)}
        a = OrderedDict(sorted(dic.items(), key=lambda x: month_numeric_mapping[x[0]] ))
        
        column_names = ["Month", "Actual", "Predicted"]
        values = list(a.values())
        
        x_axis_label = "Month"
        y_axis_label_list = ["Actual", "Predicted"]
        
        return column_names, values, x_axis_label, y_axis_label_list
    

    