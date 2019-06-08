import subprocess

import tkinter
from tkinter import ttk

import venvs_handler

class VenvHandler(ttk.Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.master.title("dcc-venv handler")
        self.style = ttk.Style()
        self.style.theme_use("default")

        frame = ttk.Frame(self, relief=tkinter.RAISED, borderwidth=1)
        frame.pack(fill=tkinter.BOTH, expand=True)
        
        configs_label = ttk.Label(frame, text="DCC Configurations")
        configs_label.pack(side=tkinter.TOP, anchor="w", padx=5, pady=5)
        
        # Populate DCC Configs list
        self.check_boxes = {}
        for dcc_name in venvs_handler.get_dcc_configs().keys():
            dcc_check = tkinter.IntVar()
            dcc_check.set(1)
            checkbox = ttk.Checkbutton(frame, variable=dcc_check, text=dcc_name)
            checkbox.pack(side=tkinter.TOP, anchor="w")
            self.check_boxes[checkbox] = dcc_check

        self.pack(fill=tkinter.BOTH, expand=True)
        
        
        self.dev_check = tkinter.IntVar()
        dev_check_box = ttk.Checkbutton(frame, text="Tool Developer", variable=self.dev_check)
        dev_check_box.pack(side=tkinter.BOTTOM, anchor="w", padx=5, pady=5)
        
        install_button = ttk.Button(self, text="Install", command=lambda: self.call_command("install"))
        install_button.pack(side=tkinter.LEFT, padx=5, pady=5)
        
        uninstall_button = ttk.Button(self, text="Uninstall", command=lambda: self.call_command("uninstall"))
        uninstall_button.pack(side=tkinter.LEFT)
        
        upgrade_button = ttk.Button(self, text="Update", command=lambda: self.call_command("update"))
        upgrade_button.pack(side=tkinter.RIGHT, padx=5, pady=5)

    def get_active_dccs(self):
        dccs = []
        for check_box, dcc_check in self.check_boxes.items():
            if dcc_check.get():
                dccs.append(check_box.cget("text"))
        return dccs
    
    def call_command(self, command_type):
        dccs = self.get_active_dccs()
        if not dccs:
            return
        
        is_dev = str(self.dev_check.get() is not 0)
        print(is_dev)
        subprocess.Popen(['python', venvs_handler.__file__, command_type, "-dev", is_dev, "-dccs", *dccs])
    

def main():

    root = tkinter.Tk()
    root.geometry("300x200+300+300")
    app = VenvHandler()
    root.mainloop()


if __name__ == '__main__':
    main()
    


"""

import tkinter

BUTTON_WIDTH = 15

class HandlerUI:

    def __init__(self, window):

        
        tkinter.Label(window, text="dcc venv handler", height=3).grid(row=0, column=1)
        
        self.populate_dcc_list()

        mytext2 = tkinter.Button(window, text="Install", width=BUTTON_WIDTH, height=3)
        mytext2.grid(row=2, column=0, sticky="nsew")

        mytext4 = tkinter.Button(window, text="Upgrade", width=BUTTON_WIDTH, height=3)
        mytext4.grid(row=2, column=1, sticky="nsew")

        mytext3 = tkinter.Button(window, text="Uninstall", width=BUTTON_WIDTH, height=3)
        mytext3.grid(row=2, column=2, sticky="nsew")

        window.columnconfigure(0, weight=1)
        
    def populate_dcc_list(self):
        for dcc_name in venvs_handler.get_dcc_configs().keys():
            self.check_cmd = tkinter.IntVar()
            checkbox = tkinter.Checkbutton(window, variable=self.check_cmd, onvalue=1, offvalue=0, text=dcc_name)
            checkbox.grid(row=1, column=1, sticky="nsew")
    
    def say_hi(self):
        print(self.check_cmd.get())
        # print(checkbox.cget("text"))
        

window = tkinter.Tk()
window.title("dcc-venv handler")
window.geometry("250x250+300+300")

handler_ui = HandlerUI(window)

window.mainloop()
"""