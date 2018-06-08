try:
    from app.core.ModelPreProcess import ModelPreProcess
    from app.core.OLSRegressor import OLSRegressor  
except: # to avoid exception when runing localy and service
    from ModelPreProcess import ModelPreProcess
    from OLSRegressor import OLSRegressor   
  
import json

class Train:
    
    def __init__(self, mode="", TRAIN_FILE=""):
        self.mode = mode
        self.shp = ModelPreProcess()
        self.ols = OLSRegressor()
        
        self.TRAIN_FILE = TRAIN_FILE

    def train(self):            
        
        temp_mode = self.mode
        if temp_mode == "":
            temp_mode = "complete"
            
        APP_PATH = "app/core/" 
        
        train_df = self.shp.load_csv(self.TRAIN_FILE)
        
        # Shuffle and Split the train_df
        train_df = self.shp.shuffle_dataframe(train_df)        
        train_df, test_df = self.shp.split_dataframe( train_df, (len(train_df.index)*80)//100 )
        self.shp.dataframe_to_csv(train_df, self.TRAIN_FILE[:-4] + "_Train.csv", train_df.columns)
        self.shp.dataframe_to_csv(test_df, self.TRAIN_FILE[:-4] + "_Test.csv", train_df.columns)
        
        try:
            with open('config/'+temp_mode+'.json') as f:
                data = json.load(f)
        except:
            with open('app/core/config/'+temp_mode+'.json') as f:
                data = json.load(f)
        
        cols, encoder_data  = data['cols'], data['encoder_data']
        
        X, y = self.shp.getXandY(train_df, cols, encoder_data)
        
        model = self.ols.fit(X, y)                                
        
        # if TRAIN_FILE name contains 'app/core/' in the
        # beginning (because of service call) then remove it before saving
        if self.TRAIN_FILE.startswith(APP_PATH):
            self.TRAIN_FILE = self.TRAIN_FILE[len(APP_PATH):]
        
        try:
            self.ols.save_data(model, APP_PATH + 'models/' + self.mode +'/pickledModel.pkl')        
            self.ols.save_data(len(X), APP_PATH + 'models/' + self.mode +'/pickledTrainingLength.pkl')                
            self.ols.save_data(self.TRAIN_FILE[:-4] + "_Train.csv", APP_PATH + 'models/' + self.mode +'/pickledTrainFileName.pkl')
        except: # to avoid exception when runing localy and service
            self.ols.save_data(model, 'models/'+self.mode + '/pickledModel.pkl')        
            self.ols.save_data(len(X), 'models/'+self.mode +'/pickledTrainingLength.pkl')        
            self.ols.save_data(self.TRAIN_FILE[:-4] + "_Train.csv", 'models/'+self.mode + '/pickledTrainFileName.pkl')
        
        return self.ols.getRsquared(model)
        
"""
    if needs to be trained locally from this file only, uncomment the following lines:
    
# For Month
t = Train(mode="month", TRAIN_FILE="datasets/Data11k_m.csv")
t.train()
            
# For weight
t = Train(mode="weight", TRAIN_FILE="datasets/Data11k_w.csv")
t.train()
            
# For complete
t = Train(mode="", TRAIN_FILE="datasets/Data11k.csv")
t.train()

# For delwin
t = Train(mode="delwin", TRAIN_FILE="datasets/delwin_6k.csv")
t.train()

"""