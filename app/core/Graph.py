import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

    
class Graph:
    def __init__(self, hasActual=True):        
        self.hasActual = hasActual                
        self.plot_save_path = "app/core/results/"
        
    def plot(self, column_names, values, x_axis_label, y_axis_label_list, graph_file_name=""):
            
        df = pd.DataFrame(np.array(values, dtype=object), columns=column_names)
        
        ax = df.plot(x=x_axis_label, y=y_axis_label_list, kind="bar", figsize=(20,10))
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
        
        file_name = self.plot_save_path + graph_file_name
        
        fig = ax.get_figure()
        fig.savefig(file_name)
        plt.close(fig)
        
        ax = df.plot(x=x_axis_label, y=y_axis_label_list, kind="kde")
        fig = ax.get_figure()
        fig.savefig(file_name + "_kde.png")
        plt.close(fig)
        
        return file_name + '.png'
     
    def pair_plot(self, df):
        sns.set(style="ticks", color_codes=True)
        g = sns.pairplot(df)
        print("done pair plot")
        

"""sns.set(style="ticks", color_codes=True)
df = pd.read_csv('datasets/Dimen3k.csv')
df = df[["ShipmentCount", "CustomStdWidth", "CustomStdHeight", "CustomStdLength"]]
sns.pairplot(df)"""

    
