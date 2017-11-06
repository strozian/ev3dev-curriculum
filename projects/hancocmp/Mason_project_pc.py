# CSSE 120 Final Project
#
# Mason Hancock

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


def main():
    print('Main')
    root = tkinter.Tk()
    root.title('Final Project')

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    button = ttk.Checkbutton(main_frame, text='button')
    button.grid()
    button['command'] = lambda: run(button)
    root.mainloop()


def run(button):
    state=button.instate(['selected'])
    print(state)



main()
