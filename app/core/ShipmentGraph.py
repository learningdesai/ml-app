try:    
    from ShipmentCompleteModel import ShipmentCompleteModel
    from Graph import Graph
except:    
    from app.core.ShipmentMonthModel import ShipmentMonthModel
    from app.core.Graph import Graph

from datetime import datetime

class ShipmentGraph:

    def start(self, results):
    
        smm = ShipmentMonthModel()
        g = Graph()
        
        # only plotting month results right now
        
        month_result = smm.get_month_results(results)
        try:
            currentDT = (str(datetime.now()).split('.'))[0] # 2018-03-01 17:03:46.759624
            currentDT = currentDT.replace(':','-')
            graph_file_name = "Month-" + currentDT
            
            print("this is file: ", graph_file_name)
            file_path = g.plot(month_result[0], month_result[1], month_result[2], month_result[3], graph_file_name)
            print("done.. ploting...")
            result = { "status": "success", "file_path":  file_path}
        except Exception as e:
            print(str(e))
            print("error during plotting...")
            result = { "status": "failure", "error": "check log data" }
        return result