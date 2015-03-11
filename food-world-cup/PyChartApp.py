from matplotlib import pyplot as plt
from matplotlib.widgets import Button
import seaborn as sns
import time
from ProcessManager import ProcessManager

__author__ = 'davidabrahams & tomheale'


class PyChartApp:
    def __init__(self):
        """
        Get process data, create figure, and set runtime parameters
        """
        self.proc_manager = ProcessManager()
        self.fig = plt.figure('Active Process RAM Usage')
        self.ax = self.fig.add_subplot(111)
        self.selected_pid = None
        self.viewing_ram = True
        self.running = True
        self.sleep_time = 0.5

    def shorten_names(self, names):
        """
        Cuts string short at first space
        Used later to remove excess data from labels
        """
        new_names = []
        for name in names:
            if ' ' in name:
                new_names.append(name[0:name.index(' ')])
            else:
                new_names.append(name)
        return new_names


    def update(self):
        """
        Updates process data and displays the app
        """
        tic = time.clock()

        self.proc_manager.update()
        data = self.proc_manager.data
        keys = data.keys()

        # Only display processes with more than 20Mb RAM or 2% CPU usage
        indices_to_remove = []
        vals = []
        for i, k in enumerate(keys):
            pid, cpu, ram = data[k]
            if (self.viewing_ram and ram < 20.0) or (not self.viewing_ram and cpu < 2.0):
                indices_to_remove.append(i)
            else:
                # Set the pie chart values according to which option is selectied
                if self.viewing_ram:
                    vals.append(ram)
                else:
                    vals.append(cpu)
        # Iterate backward in order to remove correct indices.
        for i in reversed(indices_to_remove):
            keys.pop(i)

        # get the process names and put them in a list
        names = self.shorten_names([data[k][0] for k in keys])

        # explode the selected process
        explode_list = [0] * len(keys)
        if self.selected_pid in keys:
            explode_list[keys.index(self.selected_pid)] = 0.2

        # Make a pie graph w/buttons
        plt.clf()  # If we don't clear the figure, the labels overlap
        self.plot_pie(vals, names, explode_list, keys)
        self.make_buttons()

        # Maintains update rate and redraws pie plot
        toc = time.clock()
        plt.pause(max([self.sleep_time - (toc - tic), 0.0001]))


    def plot_pie(self, vals, names, explode_list, keys):
        """
        Generates new pie chart drawing and sets picker
        """
        plt.axis('equal')
        wedges, pie_labels = plt.pie(vals, labels=names, explode=explode_list)
        self.wedge_dict = dict(zip(wedges, keys))
        self.make_picker(self.fig, wedges)

    def make_buttons(self):
        """
        Creates switch and terminate buttons and sets click function
        """
        # Make Terminate button
        term_button_ax = plt.axes([0.52, 0.01, 0.2, 0.07])
        button_term = Button(term_button_ax, 'Terminate')
        button_term.on_clicked(self.terminate)
        term_button_ax._button = button_term

        # Make Switch button
        switch_button_ax = plt.axes([0.28, 0.01, 0.2, 0.07])
        if not self.viewing_ram:
            button_switch = Button(switch_button_ax, 'Switch to RAM')
        else:
            button_switch = Button(switch_button_ax, 'Switch to CPU')
        button_switch.on_clicked(self.switch)
        switch_button_ax._button = button_switch

    def run(self):
        """
        Runs app until self.running is set to False
        """
        while self.running:
            self.update()

    def make_picker(self, fig, wedges):
        """
        Event manager for wedge selection
        """

        def onclick(event):
            wedge = event.artist
            pid = self.wedge_dict[wedge]
            self.selected_pid = pid

        # stop running the loop when the user closes the window
        def handle_close(event):
            self.running = False

        # Make wedges selectable
        for wedge in wedges:
            wedge.set_picker(True)

        # add click and close events
        fig.canvas.mpl_connect('pick_event', onclick)
        fig.canvas.mpl_connect('close_event', handle_close)


    def terminate(self, event):
        """
        Murders the chosen process using its process ID
        """
        self.proc_manager.terminate_process(self.selected_pid)

    def switch(self, event):
        """
        Swaps from viewing RAM to viewing CPU
        """
        self.viewing_ram = not self.viewing_ram


if __name__ == '__main__':
    p = PyChartApp()
    p.run()