import abc
import pandas as pd

from sklearn.preprocessing import OneHotEncoder,LabelEncoder
try:
    from PreProcessUtils import PreProcessUtils
except:
    from app.core.PreProcessUtils import PreProcessUtils

class PreProcessStrategy(object):
    __metaclass__ = abc.ABCMeta       
          
                  
    @abc.abstractmethod
    def load_csv(self, filename):
        """Required Method"""
    
    @abc.abstractmethod
    def concatTest(self, train, test):
        """Required Method"""

    def filter_data(self, data, f_cols):
        """ f_cols is list of column names to be
        returned in 'data' dataframe """
        return data[f_cols]
    
    def fix_missing_data(self, data, mean=False):
        """ handles any NaN values in the dataframe """
        if mean:
            data.fillna(data.mean())
        else:
            data = data[pd.notnull(data)]
        return data
    
    def remove_outliers(self,data, conditions):        
        """
        args:
            conditions: {"column_name": ("lt", limit_number), ...}
        """        
        for col in conditions:
            
            opt = conditions[col][0]
            
            val = conditions[col][1]
            
            data = PreProcessUtils.opt_switch(opt, col, val, data)
                        
        return data
        
    def aggregation_transformation(self, data, col_list):
        if not col_list:
            return data          
        return PreProcessUtils.create_combinations(data, col_list)
    
    def label_encoder(self, data, col):
        """label Encode categorical column(s)"""
        data[[col]] = data[[col]].apply(LabelEncoder().fit_transform)
        return data
    
    def one_hot_encoder(self, X, colNum):
        """ one hot encode seperately the given column """
        oneHotEnc = OneHotEncoder(categorical_features=[colNum])
        X = oneHotEnc.fit_transform(X).toarray()   
        # avoiding the dummy variable trap... remove the first column
        X = X[:, 1:]
        return X
    
    