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

    collision_input = ttk.Label(main_frame, text="What spot do I avoid?")
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

    enter_button = ttk.Button(main_frame, text='Enter')
    enter_button.grid(row=8, column=2)
    # enter_button['command'] = lambda: main_frame.grid_remove()
    enter_button['command'] = lambda: waiting(mqtt_client, int(starting_row_entry.get()),
                                              int(starting_column_entry.get()), int(end_row_entry.get()),
                                              int(end_column_entry.get()), int(collision_row_entry.get()),
                                              int(collision_column_entry.get()))
    print('check')

    root.mainloop()


def waiting(mqtt_client, starting_row, starting_column, goal_row, goal_column, collision_row, collision_column):
    direction = 0
    current_row = starting_row
    current_column = starting_column

    if goal_row > starting_row:
        while direction != 0:
            mqtt_client.send_message('turn_degrees', [95, 500])
            direction = direction - 1
            if direction == -1:
                direction = 3
        while current_row != goal_row:
            if collision_column != current_column:
                mqtt_client.send_message('drive_inches', [12, 500])
                current_row += 1
                mqtt_client.send_message('check_ir', [])
            else:
                if collision_row != current_row + 1:
                    mqtt_client.send_message('drive_inches', [12, 500])
                    current_row += 1
                    mqtt_client.send_message('check_ir', [])
                else:
                    if current_column != 4:
                        mqtt_client.send_message('turn_degrees', [-95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [12, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [24, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [12, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [-95, 500])
                        mqtt_client.send_message('check_ir', [])
                    else:
                        mqtt_client.send_message('turn_degrees', [95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [12, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [-95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [24, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [-95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [12, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [95, 500])
                        mqtt_client.send_message('check_ir', [])
                    current_row += 2

    if goal_row < starting_row:
        while direction != 2:
            mqtt_client.send_message('turn_degrees', [95, 500])
            direction = direction - 1
            if direction == -1:
                direction = 3
        while current_row != goal_row:
            if collision_column != current_column:
                mqtt_client.send_message('drive_inches', [12, 500])
                current_row -= 1
                mqtt_client.send_message('check_ir', [])
            else:
                if collision_row != current_row - 1:
                    mqtt_client.send_message('drive_inches', [12, 500])
                    current_row -= 1
                    mqtt_client.send_message('check_ir', [])
                else:
                    if current_column != 1:
                        mqtt_client.send_message('turn_degrees', [-95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [12, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [24, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [12, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [-95, 500])
                        mqtt_client.send_message('check_ir', [])
                    else:
                        mqtt_client.send_message('turn_degrees', [95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [12, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [-95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [24, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [-95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [12, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [95, 500])
                        mqtt_client.send_message('check_ir', [])
                    current_row -= 2

    if goal_column > starting_column:
        while direction != 1:
            mqtt_client.send_message('turn_degrees', [95, 500])
            direction = direction - 1
            if direction == -1:
                direction = 3
        while current_column != goal_column:
                if collision_column != current_column + 1:
                    mqtt_client.send_message('drive_inches', [12, 500])
                    current_column += 1
                    mqtt_client.send_message('check_ir', [])
                else:
                    if current_row != 1:
                        mqtt_client.send_message('turn_degrees', [-95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [12, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [24, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [12, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [-95, 500])
                        mqtt_client.send_message('check_ir', [])
                    else:
                        mqtt_client.send_message('turn_degrees', [95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [12, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [-95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [24, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [-95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [12, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [95, 500])
                        mqtt_client.send_message('check_ir', [])
                    current_column += 2

    if goal_column < starting_column:
        while direction != 3:
            mqtt_client.send_message('turn_degrees', [95, 500])
            direction = direction - 1
            if direction == -1:
                direction = 3
        while current_column != goal_column:
                if collision_column != current_column - 1:
                    mqtt_client.send_message('drive_inches', [12, 500])
                    current_column -= 1
                    mqtt_client.send_message('check_ir', [])
                else:
                    if current_column != 4:
                        mqtt_client.send_message('turn_degrees', [-95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [12, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [24, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [12, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [-95, 500])
                        mqtt_client.send_message('check_ir', [])
                    else:
                        mqtt_client.send_message('turn_degrees', [95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [12, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [-95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [24, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [-95, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('drive_inches', [12, 500])
                        mqtt_client.send_message('check_ir', [])
                        mqtt_client.send_message('turn_degrees', [95, 500])
                        mqtt_client.send_message('check_ir', [])
                    current_column -= 2


main()
