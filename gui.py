import customtkinter as ctk
from canvas import Canvas
from main import run_experiment
import time


class App(ctk.CTk):

    WIDTH = 660
    HEIGHT = 540

    def __init__(self):
        super().__init__()

        self.title('Circles Problem App')
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol('WM_DELETE_WINDOW', self.on_closing) # call on_closing() when app gets closed

        # Default parameters
        self.params = {
            'CANVAS_WIDTH': 500,
            'CANVAS_HEIGHT': 500,
            'MAIN_RADIUS': 200,
            'INNER_CIRCLES': 5,
            'INNER_RADIUSES': 40,
            'INNER_ID': 2,
        }

        # Color schema for figures and collisions
        self.color_map = {
            '0': 'blue',  # Main circle
            '1': 'green',  # Road
            '2': 'red',  # Inner circles
            '*': 'black',  # Collisions
        }

        # app canvas
        self.canvas = Canvas(self.params['CANVAS_WIDTH'], self.params['CANVAS_HEIGHT'])

        self.grid_rowconfigure((0, 3), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        # gui display 
        self.display = ctk.CTkCanvas(
            master=self,
            width=self.params['CANVAS_WIDTH'],
            height=self.params['CANVAS_HEIGHT'],
        )
        self.display.grid(row=0, column=0, rowspan=2, padx=20, pady=(0, 0))

        self.progress_bar = ctk.CTkProgressBar(master=self, width=400, mode='determinate')
        self.progress_bar.set(1)
        self.progress_bar.grid(row=2, column=0)

        self.button = ctk.CTkButton(self, command=self.generate_results, text='Run experiment')
        self.button.grid(row=3, column=0, padx=20, pady=20)

        self.stats_label = ctk.CTkLabel(self, text='Run the experiment to see stats', width=200)
        self.stats_label.grid(row=0, column=1, padx=20, pady=20)

        # Panel for parameters configuration
        self.parameter_panel = ctk.CTkFrame(self)
        self.parameter_panel.grid(row=1, column=1, padx=20, pady=20)

        self.inner_num_input = ctk.CTkEntry(self.parameter_panel, placeholder_text='Inner circles number')
        self.inner_num_input.grid(row=0, column=0, padx=10, pady=10)

        self.inner_radius_input = ctk.CTkEntry(self.parameter_panel, placeholder_text='Inner circles radiuses')
        self.inner_radius_input.grid(row=1, column=0, padx=10, pady=10)

        self.params_button = ctk.CTkButton(self.parameter_panel, command=self.set_params, text='Set parameters')
        self.params_button.grid(row=2, column=0, padx=10, pady=10)
    
    # Try to set parameters if there are some and it is valid
    def set_params(self):
        try:
            inner_circles = int(self.inner_num_input.get())
            self.params['INNER_CIRCLES'] = inner_circles
        except ValueError:
            print('Circles number not set')
        try:
            inner_radiuses = int(self.inner_radius_input.get())
            self.params['INNER_RADIUSES'] = inner_radiuses
        except ValueError:
            print('Inner radiuses not set')
    
    # Run experiment and show the results
    def generate_results(self):
        self.display.delete('all')
        self.canvas.erase()

        start_time = time.perf_counter()
        run_experiment(self.canvas, **self.params)

        height = self.params['CANVAS_HEIGHT']
        width = self.params['CANVAS_WIDTH']

        self.progress_bar.set(0)
        delta = int(height/100)
        progress_value = delta

        # Draw result of the experiment on canvas and update progress bar
        canvas_array = self.canvas.get_pixel_array()
        for y in range(height): 
            for x in range(width):
                if canvas_array[y][x] == '.':
                    continue
                self.display.create_rectangle(x, y, x, y, outline=self.color_map[canvas_array[y][x]])
            
            if y == progress_value:
                progress_value += delta
                self.progress_bar.set(y/height)
                self.update_idletasks()
        self.progress_bar.set(1)

        experiment_time = time.perf_counter() - start_time

        self.stats_label.configure(
            text=f'Road hits = {self.canvas.line_overlaps}\n'
            + f'Total shots = {self.params["INNER_CIRCLES"]}\n'
            + f'Hit chance = {self.canvas.line_overlaps/self.params["INNER_CIRCLES"]:.2%}\n'
            + f'Exec time = {experiment_time:.2f}sec\n'
        )
    
    # Destroy self and all child widgets 
    def on_closing(self, event=0):
        self.destroy()


if __name__ == '__main__':
    app = App()
    app.mainloop()