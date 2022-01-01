import PySimpleGUI as sg
import pandas as pd

DB_FILE = 'songs1.csv'
QA = 'what would you like to listen when you are '
result_pic=[(1, 0, 0, 0, 0, 0, 0),(0, 0, 1, 0, 0, 0, 0),(0,0,0,1,0,0,0),(0, 0, 0, 0, 1, 0, 0),(0, 0, 0, 0, 0, 1, 0),(0, 0, 0, 0, 0, 0, 1)]

def ui_first_time():
    songs={}
    def func(row):
        songs[row['name']+row['artists']]=[row['calm'],row['energetic'],row['happy'],row['sad']]
    df = pd.read_csv(DB_FILE)
    calm_songs=df.sort_values(by=['calm'],ignore_index=True,ascending=False)
    func(calm_songs.iloc[0])
    func(calm_songs.iloc[1])

    energetic_songs = df.sort_values(by='energetic',ignore_index=True, ascending=False)
    func(energetic_songs.loc[0])
    func(energetic_songs.loc[1])

    happy_songs = df.sort_values(by='happy',ignore_index=True, ascending=False)
    func(happy_songs.loc[0])
    func(happy_songs.loc[1])

    sad_songs = df.sort_values(by='sad',ignore_index=True, ascending=False)
    func(sad_songs.loc[0])
    func(sad_songs.loc[1])

    songs_vec=list(songs.values())
    songs_name= list(zip(range(8),list(songs.keys()),songs_vec))

    list_of_quiz = [str(x[0])+':'+str(x[1])+','+str(x[2]) for x in songs_name]
    result_song=[]

    sg.theme('BluePurple')

    layout = [

        [sg.Listbox(list_of_quiz,size=(170,10))],
        [sg.Text(QA + 'angry?'), sg.InputText()],
        [sg.Text(QA + 'fear?'), sg.InputText()],
        [sg.Text(QA + 'happy?'), sg.InputText()],
        [sg.Text(QA + 'sad?'), sg.InputText()],
        [sg.Text(QA + 'surprise?'), sg.InputText()],
        [sg.Text(QA + 'neutral?'), sg.InputText()],

        [sg.Button('END')]
    ]

    # Create the Window
    window = sg.Window('We Feel You', layout,location=(0,0),resizable=True).finalize()
    window.maximize()
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'END': # if user closes window or clicks end
            result_song += [songs_vec[int(values[1])], songs_vec[int(values[2])], songs_vec[int(values[3])],
                            songs_vec[int(values[4])], songs_vec[int(values[5])], songs_vec[int(values[6])]]
            break

    window.close()
    return result_pic, result_song
