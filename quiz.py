import pandas as pd

DB_FILE = 'songs1.csv'
qa = 'what would you like to listen when you'



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

    songs_name= list(songs.keys())

    print(qa, ' angry?')
    print(songs_name)
    song = input('copy and paste here:')
    result_pic = [(1, 0, 0, 0, 0, 0, 0)]
    result_song = [songs[song]]

    print(qa, ' fear?')
    print(songs_name)
    song = input('copy and paste here:')
    result_pic += [(0, 0, 1, 0, 0, 0, 0)]
    result_song += [songs[song]]

    print(qa, ' happy?')
    print(songs_name)
    song = input('copy and paste here:')
    result_pic += [(0,0,0,1,0,0,0)]
    result_song += [songs[song]]

    print(qa, ' sad?')
    print(songs_name)
    song = input('copy and paste here:')
    result_pic += [(0, 0, 0, 0, 1, 0, 0)]
    result_song += [songs[song]]

    print(qa, ' surprise?')
    print(songs_name)
    song = input('copy and paste here:')
    result_pic += [(0, 0, 0, 0, 0, 1, 0)]
    result_song += [songs[song]]

    print(qa, ' neutral?')
    print(songs_name)
    song = input('copy and paste here:')
    result_pic += [(0, 0, 0, 0, 0, 0, 1)]
    result_song += [songs[song]]

    return result_pic, result_song


if __name__ == '__main__':
    pass