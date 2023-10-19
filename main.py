import tkinter as tk
from tkinter import filedialog
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
matplotlib.use('TkAgg')


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SPE Reader")
        self.geometry("800x600")

        roi_start = 10
        roi_end = 500

        figure = Figure(figsize=(6, 4), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, self)
        NavigationToolbar2Tk(figure_canvas, self)
        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        def open_file():

            filepath = filedialog.askopenfilename(filetypes=[('SPE files', '*.spe')])
            if filepath != "":
                figure.clear()
                data = []
                channels = []
                start_data_index = -1
                info_count_index = -1
                channel_start = 0
                channel_end = 0

                with open(filepath, "r", encoding='unicode_escape') as f:
                    i = 0
                    for line in f:
                        if line == '$DATA:\n':
                            info_count_index = i + 1
                            start_data_index = i + 2

                        if i == info_count_index:
                            info_count = line[:-1].split(' ')
                            channel_start = int(info_count[0])
                            channel_end = int(info_count[1])

                        if i == start_data_index:
                            if channel_start <= channel_end:
                                data.append(int(line[:-1].replace(' ', '')))
                                channels.append(channel_start)
                                start_data_index = start_data_index + 1
                                channel_start = channel_start + 1

                        i = i + 1
                        
                axes = figure.add_subplot()
                axes.plot(channels[roi_start:roi_end], data[roi_start:roi_end])
                axes.fill_between(channels[roi_start:roi_end], data[roi_start:roi_end], alpha=0.5)
                axes.set_title(filepath)
                axes.set_ylabel('Count')
                axes.set_xlabel('Channel')

                figure_canvas.draw()

        open_button = tk.Button(text="Open file \".spe\"...", command=open_file)
        open_button.pack()


if __name__ == '__main__':
    app = App()
    app.mainloop()
