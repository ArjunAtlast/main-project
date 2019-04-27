import tkinter as tk
import tkinter.ttk as ttk
from threading import Thread
from time import sleep

from helpers import feature_list, beautify_text, map_to_value

class GUI:

    predicting = False
    updating = False

    def __init__(self, predictFn, updateFn, features, width=400):
        
        self.predictFn = predictFn

        self.updateFn = updateFn

        self.width = width

        self.features = features

        self.top = tk.Tk()

        self.top.title('Spec Calculator')

    
    def predict(self):

        if not self.predicting:

            # set predicting on
            self.predicting = True

            data = self.predictFn(self.targetMenu.get())

            # set label fields
            self.set_values(data)


            self.predicting = False
    
    def update(self):

        if not self.updating:

            # set predicting on
            self.updating = True

            # show progress
            self.progressBar.start()

            self.updateFn()

            # stop progress
            self.progressBar.stop()

            self.updating = False
    
    def run_update(self):

        Thread(target=self.update).start()
    
    def run_predict(self):

        Thread(target=self.predict).start()
    
    def set_values(self, data:dict):

        for feature, val in data.items():

            self.prediction_labels[feature].configure(text=map_to_value(feature, val))
    
    def load(self):
        """
        Load GUI
        """

        # header
        self.setup_header()

        # body
        self.setup_main()

        # footer
        self.setup_footer()

        # start window
        self.top.mainloop()

    def setup_header(self):

        self.header = tk.Frame(self.top, width=self.width)
        self.header.pack(side = tk.TOP, fill=tk.X)
        self.header.columnconfigure(0, weight=2)
        self.header.columnconfigure(1, weight=1)

        # add progress
        self.progressBar = ttk.Progressbar(self.header, orient=tk.HORIZONTAL, mode="indeterminate")
        self.progressBar.grid(row=0, column=0, sticky=tk.W+tk.E, padx=10, pady=10)

        # add the update button
        self.updateBtn = ttk.Button(self.header, text = 'Update', command=self.run_update)
        self.updateBtn.grid(row=0, column=1, sticky=tk.W+tk.E, padx=10, pady=10)

        # Insert a divider
        sep = ttk.Separator(self.header, orient=tk.HORIZONTAL)
        sep.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E)
    
    def setup_main(self):

        self.main = tk.Frame(self.top, width=self.width)
        self.main.pack(fill=tk.X)
        self.main.columnconfigure(0, weight=1)
        self.main.columnconfigure(1, weight=1)

        # add a label
        label = tk.Label(self.main, text="Base Feature:")
        label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

        # add the option menu
        self.targetMenu = ttk.Combobox(self.main, values=self.features, state="readonly")
        # self.targetMenu = ttk.OptionMenu(self.main, self.target, None, *self.features)
        self.targetMenu.current(1)
        self.targetMenu.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)

        # add a seperator
        sep = ttk.Separator(self.header, orient=tk.HORIZONTAL)
        sep.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E)

        # setup prediction labels
        self.setup_prediction_labels()

    def setup_prediction_labels(self):

        self.prediction_labels = {}

        for index, feature in enumerate(self.features):

            # title label
            tLabel = tk.Label(self.main, text=beautify_text(feature)+':')
            tLabel.grid(row=index+2, column=0, sticky=tk.W, padx=10, pady=5)

            # value label
            vLabel = tk.Label(self.main, text='-')
            vLabel.grid(row=index+2, column=1, sticky=tk.E, padx=10, pady=5)

            self.prediction_labels[feature] = vLabel
            
    def setup_footer(self):

        self.footer = tk.Frame(self.top, width=self.width)
        self.footer.pack(side = tk.BOTTOM, fill=tk.X)
        self.footer.columnconfigure(0, weight=1)

        # add a seperator
        sep = ttk.Separator(self.footer, orient=tk.HORIZONTAL)
        sep.grid(row=0, column=0, sticky=tk.W+tk.E)
        
        self.predictBtn = ttk.Button(self.footer, text="Calculate", command=self.run_predict)
        self.predictBtn.grid(row=1, column=0, sticky=tk.W+tk.E, padx=100, pady=10)

def pred():
    print('predicting...')

    sleep(3)

    return {
        'abs': 1, 
        'compression_ratio': 3, 
        'coupe_type': 4,
        'cylinder_bore': 5, 
        'doors': 4, 
        'fuel_tank_volume':2, 
        'fuel_type':1,
        'kerb_weight':1, 
        'number_of_cylinders':6,
        'number_of_gears':6,
        'number_of_valves_per_cylinder':4, 
        'piston_stroke':4,
        'position_of_cylinders':2, 
        'power':1, 
        'seats':5, 
        'torque':1, 
        'wheelbase':3
    }