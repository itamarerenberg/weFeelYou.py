import pandas as pd

DB_FILE = 'songs'
qa = 'what would you like to listen when you'
songs = ['Someone Like You, Adele', 'All of Me, John Legend', 'Slow Hands, Niall Horan']
songs += ['Only Human, Jonas Brothers', 'Growing Pains, Alessia Cara', 'Survivor, Destiny\'s Child']
songs += ['Havana, Instrumental Version', 'Can\'t Help Falling In Love, Kina Grannis']


def quiz():
    songs=[]
    df = pd.read_csv(DB_FILE)
    calm_songs=df.sort_values(by='calm',ascending=False)
    songs+=[calm_songs.loc[0]['name'],calm_songs.loc[1]['name']]
    energetic_songs = df.sort_values(by='energetic', ascending=False)
    songs+=[energetic_songs.loc[0]['name'], energetic_songs.loc[1]['name']]
    happy_songs = df.sort_values(by='happy', ascending=False)
    songs += [happy_songs.loc[0]['name'], happy_songs.loc[1]['name']]
    sad_songs = df.sort_values(by='sad', ascending=False)
    songs += [sad_songs.loc[0]['name'], sad_songs.loc[1]['name']]
    print(qa, ' happy?')
