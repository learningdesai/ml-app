from itertools import combinations

class PreProcessUtils:
    
    @staticmethod
    def opt_switch(opt,col,val,data):        
        cases =  {
            'lt': data[data[col]<val],
            'gt': data[data[col]>val],
            'eq': data[data[col]==val],
            'gteq': data[data[col]>=val],
            'lteq': data[data[col]<=val],
        }
        return cases[opt]
        
    @staticmethod
    def create_combinations(data, col_list):
        print("PreProcessUtils: creating combinations")
        length = len(col_list)
        try:                    
            all_combinations = combinations(col_list, length - 1)            
            for combination in all_combinations:
                col_name = "".join([s[0] for s in combination])            
                data[col_name] = data[combination[0]]
                for i in range(1,len(combination)):
                    data[col_name] *= data[combination[i]]                
            col_name = "".join([s[0] for s in col_list])
            data[col_name] = data[col_list[0]]
            
            for i in range(1, len(col_list)):
                data[col_name] *= data[col_list[i]]
        except:
            pass
        print("PreProcessUtils: done creating combinations")
        return data