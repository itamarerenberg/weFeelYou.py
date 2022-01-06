import threading
import time

import PySimpleGUI as sg

import fitToUser
from data_base import songs_db_maneger as sDB
from main import *
import webbrowser
import cv2


THEME ='darkPurple2'

QA = 'what would you like to listen when you are '
RESULT_PIC=[(1, 0, 0, 0, 0, 0, 0), (0, 0, 1, 0, 0, 0, 0), (0, 0, 0, 1, 0, 0, 0), (0, 0, 0, 0, 1, 0, 0), (0, 0, 0, 0, 0, 1, 0), (0, 0, 0, 0, 0, 0, 1)]
K=2


def ui_first_time(user_name):
    '''
    window of quiz for user
    :param user_name:
    :return: list of pictures result vectors, list of user's choices song
    '''
    songs={}
    def func(rows):
        for row in rows:
            songs[row['name']+row['artists']]=[row['calm'],row['energetic'],row['happy'],row['sad']]
    calm_songs=songs_db_maneger.get_k_most(K,'calm',user_name)
    energetic_songs=songs_db_maneger.get_k_most(K,'energetic',user_name)
    happy_songs=songs_db_maneger.get_k_most(K,'happy',user_name)
    sad_songs=songs_db_maneger.get_k_most(K,'sad',user_name)
    func(calm_songs)
    func(energetic_songs)
    func(happy_songs)
    func(sad_songs)

    songs_vec=list(songs.values())
    songs_name= list(zip(range(8),list(songs.keys()),songs_vec))

    list_of_quiz = [str(x[0])+':'+str(x[1])+','+str(x[2]) for x in songs_name]
    result_song=[]

    sg.theme(THEME)

    layout = [

        [sg.Listbox(list_of_quiz,size=(170,10))],
        [sg.Text(QA + 'angry?',justification='center'), sg.InputText(key='angry')],
        [sg.Text(QA + 'fear?',justification='center'), sg.InputText(key='fear')],
        [sg.Text(QA + 'happy?',justification='center'), sg.InputText(key='happy')],
        [sg.Text(QA + 'sad?',justification='center'), sg.InputText(key='sad')],
        [sg.Text(QA + 'surprise?',justification='center'), sg.InputText(key='surprise')],
        [sg.Text(QA + 'neutral?',justification='center'), sg.InputText(key='neutral')],

        [sg.Button('END')]
    ]

    # Create the Window
    window = sg.Window('We Feel You', layout,location=(0,0),resizable=True).finalize()
    window.maximize()
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == 'END': # if user clicks end
            result_song += [songs_vec[int(values['angry'])], songs_vec[int(values['fear'])], songs_vec[int(values['happy'])],
                            songs_vec[int(values['sad'])], songs_vec[int(values['surprise'])], songs_vec[int(values['neutral'])]]
            break
        if  event == sg.WIN_CLOSED:
            break
    window.close()
    return RESULT_PIC, result_song


def take_picture():
    # Camera Settings
    try:
        video_capture = cv2.VideoCapture(0)
    except:
        video_capture = cv2.VideoCapture(1)

    # init Windows Manager
    sg.theme(THEME)

    # def webcam col
    colwebcam1_layout = [[sg.Text("Camera View", size=(60, 1), justification="center")],
                         [sg.Image(filename="", key="cam1")]]
    colwebcam1 = sg.Column(colwebcam1_layout, element_justification='center')


    colslayout = [colwebcam1]

    rowfooter = [sg.Image(filename="", key="-IMAGEBOTTOM-")]
    layout = [colslayout, rowfooter,[sg.ReadButton('capture')]]

    window = sg.Window("We Feel You", layout,
                       no_titlebar=False, alpha_channel=1, grab_anywhere=False,
                       return_keyboard_events=True, location=(0, 0))
    while True:
        event, values = window.read(timeout=20)

        if event == sg.WIN_CLOSED:
            break

        # get camera frame
        ret, frame = video_capture.read()

        if event=='capture':
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            video_capture.release()
            cv2.destroyAllWindows()
            window.close()
            return frame

        # # update webcam1
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        window["cam1"].update(data=imgbytes)


    video_capture.release()
    cv2.destroyAllWindows()


def sign_in():
    sg.theme(THEME)

    layout = [
        [sg.Text('sign in', justification='center')],
        [sg.Text('user name'), sg.InputText(key='user_name')],
        [sg.Button('sign in')],
    ]
    # Create the Window
    window = sg.Window('We Feel You', layout, location=(0, 0), resizable=True).finalize()
    window.maximize()

    while True:
        event, values = window.read()
        if event=='sign in':
            window.close()
            if not is_user_exist(values['user_name']):
                users_db_maneger.add_user(values['user_name'])
                add_songs(values['user_name'])
                caster = ftu.UserLearner(load=False, user_name=values['user_name'])
                caster.learn_user(data_source=ui_first_time)
            main_window(values['user_name'])
            break
        if event==sg.WIN_CLOSED:
            break
    window.close()


def add_songs(userName):

    sg.theme(THEME)

    layout=[
        [sg.Text('enter the link to the spotify playlist', justification='center'), sg.Multiline(size=(50,4),key='pl_ids')],
        [sg.Button('add')]
    ]

    # Create the Window
    window = sg.Window('We Feel You', layout, location=(0, 0), resizable=True).finalize()
    window.maximize()
    #threads
    adder: threading.Thread
    while True:
        event, values = window.read()
        if event=='add':
            adder = threading.Thread(target=sDB.add_multiple_playlists, args=(values['pl_ids'], userName))
            adder.start()
            adder.join()
            window.close()
            break
        if event==sg.WIN_CLOSED:
            break

    window.close()


def main_window(userName):
    sg.theme(THEME)

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
            face_pic = take_picture()
            pl = fit_playlist(face_pic, user_name=userName)
            webbrowser.open(pl)
        if event=='Add Playlist To DataBase':
            add_songs(userName)
        if event in [sg.WIN_CLOSED, 'done']:
            break
    window.close()


def progress_msg(progress: str, progress_thread: threading.Thread):
    '''
    :param progress: progress name to display
    '''
    sg.theme('BluePurple')

    # adding songs progress animation
    animation_texsts = progress + ['', '.', '..', '...']
    progress_txt = sg.Text(key='progress_txt')

    layout = [
        [progress_txt]
    ]

    window = sg.Window('We Feel You', layout, location=(0, 0), resizable=True).finalize()

    i = 0
    while progress_thread.is_alive():
        event, values = window.read()
        if event==sg.WIN_CLOSED:
            break
        if time.time() - t >= 0.5:  # change the animation each 0.5 seconds
            t = time.time()
            progress_txt.update(progress + animation_texsts[i])
            window.finalize()
            i = (i + 1) % len(animation_texsts)


def init_gui():
    sign_in()


if __name__ == '__main__':
    init_gui()