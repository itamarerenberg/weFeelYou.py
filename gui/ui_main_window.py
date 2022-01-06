import threading
import time

import PySimpleGUI as sg

import fitToUser
from data_base import songs_db_maneger as sDB
from main import *
import webbrowser
import cv2

#todo: לפתוח ישר להוסיף פלייליסט
#רשימה של פלייליסטים
#loading
#רשימה של thread

QA = 'what would you like to listen when you are '
result_pic=[(1, 0, 0, 0, 0, 0, 0),(0, 0, 1, 0, 0, 0, 0),(0,0,0,1,0,0,0),(0, 0, 0, 0, 1, 0, 0),(0, 0, 0, 0, 0, 1, 0),(0, 0, 0, 0, 0, 0, 1)]
K=2


def ui_first_time(user_name):
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
    # df = pd.read_csv(DB_FILE)
    # calm_songs=df.sort_values(by=['calm'],ignore_index=True,ascending=False)
    # func(calm_songs.iloc[0])
    # func(calm_songs.iloc[1])
    #
    # energetic_songs = df.sort_values(by='energetic',ignore_index=True, ascending=False)
    # func(energetic_songs.loc[0])
    # func(energetic_songs.loc[1])
    #
    # happy_songs = df.sort_values(by='happy',ignore_index=True, ascending=False)
    # func(happy_songs.loc[0])
    # func(happy_songs.loc[1])
    #
    # sad_songs = df.sort_values(by='sad',ignore_index=True, ascending=False)
    # func(sad_songs.loc[0])
    # func(sad_songs.loc[1])

    songs_vec=list(songs.values())
    songs_name= list(zip(range(8),list(songs.keys()),songs_vec))

    list_of_quiz = [str(x[0])+':'+str(x[1])+','+str(x[2]) for x in songs_name]
    result_song=[]

    sg.theme('BluePurple')

    layout = [

        [sg.Listbox(list_of_quiz,size=(170,10))],
        [sg.Text(QA + 'angry?',justification='center'), sg.InputText()],
        [sg.Text(QA + 'fear?',justification='center'), sg.InputText()],
        [sg.Text(QA + 'happy?',justification='center'), sg.InputText()],
        [sg.Text(QA + 'sad?',justification='center'), sg.InputText()],
        [sg.Text(QA + 'surprise?',justification='center'), sg.InputText()],
        [sg.Text(QA + 'neutral?',justification='center'), sg.InputText()],

        [sg.Button('END')]
    ]

    # Create the Window
    window = sg.Window('We Feel You', layout,location=(0,0),resizable=True).finalize()
    window.maximize()
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == 'END': # if user closes window or clicks end
            result_song += [songs_vec[int(values[1])], songs_vec[int(values[2])], songs_vec[int(values[3])],
                            songs_vec[int(values[4])], songs_vec[int(values[5])], songs_vec[int(values[6])]]
            break
        if  event == sg.WIN_CLOSED:
            break
    window.close()
    return result_pic, result_song


def take_picture():
    # Camera Settings
    video_capture = cv2.VideoCapture(1)

    # init Windows Manager
    sg.theme("DarkBlue")

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
    sg.theme('BluePurple')
    layout = [
        [sg.Text('sign in', justification='center')],
        [sg.Text('user name'), sg.InputText(key='userName')],
        [sg.Button('sign in')],
    ]
    # Create the Window
    window = sg.Window('We Feel You', layout, location=(0, 0), resizable=True).finalize()
    window.maximize()

    while True:
        event, values = window.read()
        if event=='sign in':
            if is_user_exist(values['userName']):
                window.close()
                main(values['userName'])
            else:
                window.close()
                users_db_maneger.add_user(values['userName'])
                add_songs(values['userName'])
                caster = ftu.userLearner(load=False, userName=values['userName'])
                caster.learn_user(data_source=ui_first_time)
                main(values['userName'])
            break
        if event==sg.WIN_CLOSED:
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


def add_songs(userName):

    sg.theme('BluePurple')

    layout=[
        [sg.Text('enter the link to the spotify playlist', justification='center'), sg.InputText()],
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
            adder = threading.Thread(target=sDB.add_songs_to_db, args=(values[0], userName))
            adder.start()
            adder.join()
            window.close()
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
            face_pic = take_picture()
            pl = fit_playlist(face_pic, userName=userName)
            webbrowser.open(pl)
        if event=='Add Playlist To DataBase':
            add_songs(userName)
        if event in [sg.WIN_CLOSED, 'done']:
            break
    window.close()


if __name__ == '__main__':
    sign_in()