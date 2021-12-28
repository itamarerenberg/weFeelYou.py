import heapq
import math


class songKnn:
    dist = 0
    song_id = ''

    def __init__(self, song_id, dist):
        self.dist = dist
        self.song_id = song_id

    def __lt__(self, other):
        return self.dist < other.dist

    def __le__(self, other):
        return self.dist <= other.dist

    def __gt__(self, other):
        return self.dist > other.dist

    def __ge__(self, other):
        return self.dist >= other.dist


def cosine_similarity(v1, v2):
    a = sum([x1*x2 for x1, x2 in zip(v1, v2)])
    b = math.sqrt(sum([x1**2 for x1 in v1]) * sum([x2**2 for x2 in v2]))
    return a/b


def calc_dist(v1, v2):
    return sum([(i1 - i2)**2 for i1, i2 in zip(list(v1), v2)])


def calcFitness(songs, mood_vec):
    '''
    :param songs: list of tupels like (song_id, emo_vec)
    :param mood_vec: the vector to find the distances to
    :return: list of songKnn objects with calculated distances
    '''
    songknns = []
    for s in songs:
        songknns.append(songKnn(s[0], cosine_similarity(s[1], mood_vec)))
    return songknns


def knn(k, songs, mood_vec):
    '''
    :param k: no. of songs to return
    :param songs: list of tuples like (song_id, emo_vec)
    :param mood_vec: the emotion vector
    :return: list of the k song_ids with the nearest emotion_vector to emo_vec
    '''
    songKnns = calcFitness(songs, mood_vec)
    return [song.song_id for song in heapq.nlargest(k, songKnns)]


# songs = [('1', [0, 0, 0, 0]), ('2', [1, 1, 1, 1]), ('4', [4, 4, 4, 4]), ('3', [3, 3, 3, 3])]
# s = [0, 0, 0, 0]
#
# print(knn(3, songs, s))


