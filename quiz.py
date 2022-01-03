import pandas as pd

DB_FILE = 'data_base/data/users_songs/songs1.csv'
qa = 'what would you like to listen when you'
list_of_quiz=[]

def quiz():
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


    print(qa, ' angry?')
    [print(x[0],':',x[1],',',x[2]) for x in songs_name]
    song = input('write the song number:')
    result_pic = [(1, 0, 0, 0, 0, 0, 0)]
    result_song = [songs_vec[int(song)]]

    print(qa, ' fear?')
    [print(x[0],':',x[1],',',x[2]) for x in songs_name]
    song = input('write the song number:')
    result_pic += [(0, 0, 1, 0, 0, 0, 0)]
    result_song += [songs_vec[int(song)]]

    print(qa, ' happy?')
    [print(x[0],':',x[1],',',x[2]) for x in songs_name]
    song = input('write the song number:')
    result_pic += [(0,0,0,1,0,0,0)]
    result_song += [songs_vec[int(song)]]

    print(qa, ' sad?')
    [print(x[0],':',x[1],',',x[2]) for x in songs_name]
    song = input('write the song number:')
    result_pic += [(0, 0, 0, 0, 1, 0, 0)]
    result_song += [songs_vec[int(song)]]

    print(qa, ' surprise?')
    [print(x[0],':',x[1],',',x[2]) for x in songs_name]
    song = input('write the song number:')
    result_pic += [(0, 0, 0, 0, 0, 1, 0)]
    result_song += [songs_vec[int(song)]]

    print(qa, ' neutral?')
    [print(x[0],':',x[1],',',x[2]) for x in songs_name]
    song = input('write the song number:')
    result_pic += [(0, 0, 0, 0, 0, 0, 1)]
    result_song += [songs_vec[int(song)]]

    return result_pic,result_song
