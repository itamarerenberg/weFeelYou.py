import PySimpleGUI as sg

import songs_db_maneger


def add_songs():

    sg.theme('BluePurple')


    layout=[
        [sg.Text('enter the link to the spotify playlist', justification='center'), sg.InputText()],
        [sg.Button('ADD')]
    ]

    # Create the Window
    window = sg.Window('We Feel You', layout, location=(0, 0), resizable=True).finalize()
    window.maximize()

    while True:
        event, values = window.read()
        if event == 'ADD':
            songs_db_maneger.add_songs_to_db(values[0])
            break
        if event==sg.WIN_CLOSED:
            break
    window.close()