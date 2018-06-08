try:    
    from PreProcessStrategy import PreProcessStrategy    
except:    
    from app.core.PreProcessStrategy import PreProcessStrategy
from sklearn.preprocessing import StandardScaler

import pandas as pd
import numpy as np


class ModelPreProcess(PreProcessStrategy):
       
    def load_csv(self, filename):
        """ read a csv file and return pandas dataframe object """
        data = pd.read_csv(filename)        
        return data
    
    def shuffle_dataframe(self, df):
        """ returns the randomly shuffled pandas dataframe 'df' """
        return df.sample(frac=1)
    
    def dataframe_to_csv(self, df, filename, headers):
        """ saves given dataframe as csv file """
        try:
            df.to_csv(filename, index=False, columns = headers)
        except Exception as e:
            print(str(e))      
    
    def split_dataframe(self, df, rowLimit):
        """ returns splitted dataframe """
        df_new1, df_new2 = df.iloc[:rowLimit, :], df.iloc[rowLimit:, :]
        return df_new1, df_new2
    
    def json_to_dataframe(self, json_data):
        """ returns pandas dataframe from the given json_data """
        #df = pd.DataFrame.from_dict(json_data, orient='index')
        #df.reset_index(level=0, inplace=True)
        ##df = pd.read_json(json_data)
        columns = list(json_data.keys())
        values = list(json_data.values())
        arr_len = len(values)
        df = pd.DataFrame(np.array(values, dtype=object).reshape(1, arr_len), columns=columns)
        return df
    
    def concat(self, train, test):
        """ returns dataframe after concatenating train and test """
        data = pd.concat(objs=[train, test], axis=0)
        data = data.reset_index(drop=True)
        return data
    
    def feature_scale_fit(self, data):
        scaler = StandardScaler().fit(data)
        return scaler
    
    def feature_scale_transform(self, scaler, data):        
        return scaler.transform(data)   

    def feature_scale_inverse_transform(self, scaler, data):
        return scaler.inverse_transform(data)
        
        
    
    def getXandY(self, data, cols, encoder_data):
        """ does the data processing tasks such as
        limiting, encoding etc.. """
        
        print(len(data))
        # take only the below columns data
        data = self.filter_data(data, cols['f_cols'])
        
        # take care of any missing values in the data
        data = self.fix_missing_data(data)
        
        # Remove skewing and outliers         
        
        try:
            print("removng outliers")
            data = self.remove_outliers(data, cols['conditions'])
            print("done removing outliers")
        except:
            pass
        
        # label Encode categorical column(s)
        try:        
            data = self.label_encoder(data, encoder_data['label_enc_col'])
        except:
            pass
                
        
        # create aggregation data    
        try:            
            data = self.aggregation_transformation(data, cols['agg_cols'])
        except:
            pass
        
        
        # Excluding 'Dependent Variable' everything is taken
        X = data.iloc[:, 1:].values
        # Only take 'Dependent Variable'
        y = data.iloc[:, :1].values
        
        # one-hot-encode the categorical column
        try:
            if encoder_data["one_hot"]:
                X = self.one_hot_encoder(X, encoder_data["one_hot"])
        except:
            pass
        print("ModelPreProcess: ", X.shape, y.shape)
        
        """
        #try:            
        scaler = self.feature_scale_fit(X)
        X = self.feature_scale_transform(scaler, X)
        
        print("scaling..")
        #except:
        #print("scaling not done..")
        print("X: ", X[:5])
        print("y: ", y[:5])
        """
        return X, y
    
   