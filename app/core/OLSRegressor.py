import statsmodels.formula.api as sm
import pickle

try:
    from app.core.RegressorStrategy import RegressorStrategy
except:
    from RegressorStrategy import RegressorStrategy

class OLSRegressor(RegressorStrategy):
    
    def fit(self, X_train, y_train):        
        """ returns the OLS Regressor fitted model """
        model = sm.OLS(endog=y_train, exog=X_train).fit() 
        return model
    
    def getSummary(self, model):
        """ returns the OLS Regression summary"""
        return model.summary()
    
    def getRsquared(self, model):        
        """ returns the R squared value of the regression """
        return round(model.rsquared, 2)
    
    def getPredictions(self, model, X):
        """ returns the predictions for 'X' """  
        try:
            y_pred = model.predict(X)
            return y_pred
        except Exception as e:
            print(str(e))
            return None
    
    def save_data(self, data, filename):        
        with open(filename, 'wb') as f:            
            pickle.dump(data, f)
        
    def get_saved_data(self, filename):
        try:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
            return data    
        except Exception as e:
            print(e)
            print("Error during unpickling")
    
