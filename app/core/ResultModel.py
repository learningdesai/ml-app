import abc


class ResultModel(object):    
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod    
    def get_json_result(self, data, y_pred, y_test, hasActual=True, mode=None):
        """Required Method"""
         
    
    def calculate_metrics(self, predictions, actual, limit=10, ):
        """ returns various metrics related to the data """
        
        length = len(predictions) 
        
        count, zero = 0, 0
        sum_of_diff, sq_diff = 0, 0
        
        # Mean absolute percentage error
        per_err = 0
        # Symmetric mean absolute percentage error
        smape = 0
        
        for i in range(length):
            diff = abs(predictions[i] - actual[i])
            if actual[i] != 0:
                per_err += abs(diff/actual[i])
            smape += (diff/ ((abs(actual[i]) + abs(predictions[i]))/2) )
            sum_of_diff += diff
            sq_diff += (diff ** 2)
            if diff >= limit:
                count += 1
            elif diff < 1 and diff > -1:
                zero += 1
                
        if length == 0:
            return
        
        per_err = round(((per_err/length)*100)[0], 2)
        smape = round(((smape/length)*100)[0], 2)
        mea = round((sum_of_diff/length)[0], 2)
        mse = round((sq_diff/length)[0], 2) 
        rmse = round(pow(mse, 0.5), 2)
        
        return {
                "Length_Of_test_set": str(length),
                "Rows_With_Zero_error": str(zero), 
                "cross_the_limit_count": str(count), 
                "Percent_Error": str(per_err), 
                "Mean_Absolute_Error": str(mea), 
                "Semetric_Mean_Absolute_Percentage_Error": str(smape), 
                "Mean_Squared_Error": str(mse), 
                "Root_Mean_squared_error": str(rmse)
               }
      
    def get_metrics_statements(self, metrics):
        """ returns a list of strings used for 
        displaying metrics data """
        
        metricsStatements = [
                "Rows with zero difference: "+ metrics['Rows_With_Zero_error']+ " out of "+ metrics['Length_Of_test_set'],
                "Mean absolute percentage error"+ metrics['Percent_Error'],
                "Mean Absolute Error : ", metrics['Mean_Absolute_Error'],
                "Mean Squared Error: ", metrics['Mean_Squared_Error'],
                "Root Mean Squared Error: ", metrics['Root_Mean_squared_error']
        ]
        return metricsStatements
        
    
    
    def print_metrics(self, metrics):
        """ metrics is a dict object. Print the results
        in the console """
        
        metricsStatements = self.get_metrics_statements(metrics)
        
        print("Comparing Predicted and Actual Values: ") 
        for statement in metricsStatements:
            print(statement)
       

    def createMetricsFile(self, fileName, metrics):
        """ create a txt file with metrics details """
        
        metricsStatements = self.get_metrics_statements(metrics)
        
        with open(fileName, 'w') as out:
            for statement in metricsStatements:
                out.write(statement + '\n')         

    
    def get_metrics(self, predictions, actual, limit=10, fileName=False, hasActual=True):
        """ prints and returns or creates file
        containing the various metrics info """
        
        length = len(predictions) 
               
        if not hasActual:
            # there is nothing to compare with. So just,
            return {"length_of_test_data": length}
            
        metrics = self.calculate_metrics(predictions, actual, limit)
        
        self.print_metrics(metrics)
        
        if fileName:
            self.createMetricsFile(fileName)
       
        else:
            # no need to create metrics file, so just
            """
            return {                    
                    "length_of_test_data": metrics['length'],
                    "mean_absolute_error": metrics['mea'],
                    "mean_absolute_per_error": metrics['per_err'],
                    "symmetric_mean_abs_per_error": metrics['smape'],
                    "mean_squared_error": metrics['mse'],
                    "root_mean_squared_error": metrics['rmse']
                }
            """
            return metrics