import threading

import PySimpleGUI as sg
from data_base import songs_db_maneger as sDB
from gui import ui_capture_picture
from main import *
import webbrowser


def sign_in():
    sg.theme('BluePurple')
    layout = [
        [sg.Text('sign in', justification='center')],
        [sg.Text('user name'), sg.InputText(key='userName')],
        [sg.Button('sign in'), sg.Button('new user?')],
    ]
    # Create the Window
    window = sg.Window('We Feel You', layout, location=(0, 0), resizable=True).finalize()
    window.maximize()

    while True:
        event, values = window.read()
        if event=='sign in':
            main(values['userName'])
            break
        if event=='new user?':
            new_user(values['userName'])
            main(values['userName'])
            break
        if event==sg.WIN_CLOSED:
            break
    window.close()


def add_songs(userName):

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
            adder = threading.Thread(target=sDB.add_songs_to_db, args=(values[0], userName))
            adder.start()
            break
        if event==sg.WIN_CLOSED:
            break
    window.close()


def main(userName):
    sg.theme('BluePurple')

    layout = [
        [sg.Text('We Feel You', justification='center')],
        [sg.Button('Generate Playlist To Your Mood'), sg.Button('Add Playlist To DataBase')]
    ]
    # Create the Window
    window = sg.Window('We Feel You', layout, location=(0, 0), resizable=True).finalize()
    window.maximize()

    while True:
        event, values = window.read()
        if event=='Generate Playlist To Your Mood':
            face_pic = ui_capture_picture.take_picture()
            pl = fit_playlist(face_pic, userName=userName)
            webbrowser.open(pl)
            break
        if event=='Add Playlist To DataBase':
            add_songs(userName)
            break
        if event==sg.WIN_CLOSED:
            break
    window.close()


if __name__ == '__main__':
    sign_in()