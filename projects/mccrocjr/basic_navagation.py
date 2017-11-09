import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title('Navagation Control')

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    starting_input = ttk.Label(main_frame, text="Where am I at right now?")
    starting_input.grid(row=0, column=2)

    starting_row = ttk.Label(main_frame, text="Row")
    starting_row.grid(row=1, column=0)

    starting_row_entry = ttk.Entry(main_frame, width=4)
    starting_row_entry.insert(0, "0")
    starting_row_entry.grid(row=1, column=1)

    starting_column = ttk.Label(main_frame, text="Column")
    starting_column.grid(row=1, column=3)

    starting_column_entry = ttk.Entry(main_frame, width=4)
    starting_column_entry.insert(0, "0")
    starting_column_entry.grid(row=1, column=4)

    end_input = ttk.Label(main_frame, text="Where do I need to go?")
    end_input.grid(row=2, column=2)

    end_row = ttk.Label(main_frame, text="Row")
    end_row.grid(row=3, column=0)

    end_row_entry = ttk.Entry(main_frame, width=4)
    end_row_entry.insert(0, "0")
    end_row_entry.grid(row=3, column=1)

    end_column = ttk.Label(main_frame, text="Column")
    end_column.grid(row=3, column=3)

    end_column_entry = ttk.Entry(main_frame, width=4)
    end_column_entry.insert(0, "0")
    end_column_entry.grid(row=3, column=4)

    collision_input = ttk.Label(main_frame, text="Are there any collision?")
    collision_input.grid(row=4, column=2)

    collision_row = ttk.Label(main_frame, text="Row")
    collision_row.grid(row=5, column=0)

    collision_row_entry = ttk.Entry(main_frame, width=4)
    collision_row_entry.insert(0, "0")
    collision_row_entry.grid(row=5, column=1)

    collision_column = ttk.Label(main_frame, text="Column")
    collision_column.grid(row=5, column=3)

    collision_column_entry = ttk.Entry(main_frame, width=4)
    collision_column_entry.insert(0, "0")
    collision_column_entry.grid(row=5, column=4)

    collision2_row = ttk.Label(main_frame, text="Row")
    collision2_row.grid(row=6, column=0)

    collision2_row_entry = ttk.Entry(main_frame, width=4)
    collision2_row_entry.insert(0, "0")
    collision2_row_entry.grid(row=6, column=1)

    collision2_column = ttk.Label(main_frame, text="Column")
    collision2_column.grid(row=6, column=3)

    collision2_column_entry = ttk.Entry(main_frame, width=4)
    collision2_column_entry.insert(0, "0")
    collision2_column_entry.grid(row=6, column=4)

    collision3_row = ttk.Label(main_frame, text="Row")
    collision3_row.grid(row=7, column=0)

    collision3_row_entry = ttk.Entry(main_frame, width=4)
    collision3_row_entry.insert(0, "0")
    collision3_row_entry.grid(row=7, column=1)

    collision3_column = ttk.Label(main_frame, text="Column")
    collision3_column.grid(row=7, column=3)

    collision3_column_entry = ttk.Entry(main_frame, width=4)
    collision3_column_entry.insert(0, "0")
    collision3_column_entry.grid(row=7, column=4)

    root.mainloop()

main()
