import PySimpleGUI as sg

import ui_add_songs
import ui_capture_picture
from main import fit_playlist


def main():
    sg.theme('BluePurple')

    layout = [
        [sg.Text('We Feel You',justification='center')],
        [sg.Button('Generate Playlist To Your Mood'),sg.Button('Add Playlist To DataBase')]
    ]
    # Create the Window
    window = sg.Window('We Feel You', layout, location=(0, 0), resizable=True).finalize()
    window.maximize()

    while True:
        event, values = window.read()
        if event=='Generate Playlist To Your Mood':
            face_pic = ui_capture_picture.take_picture()
            fit_playlist(face_pic)
            break
        if event=='Add Playlist To DataBase':
            ui_add_songs.add_songs()
            break
        if event==sg.WIN_CLOSED:
            break
    window.close()

main()