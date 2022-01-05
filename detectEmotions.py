from fer import FER


detector = FER(mtcnn=True)


def find_biggest_face_emotions(faces_emos):
    # find the emotions of the biggest face in the picture
    biggest_box_size = 0
    biggest_face_emos = 0
    for d in faces_emos:
        if d['box'][2] > biggest_box_size:
            biggest_box_size = d['box'][2]
            biggest_face_emos = d['emotions']
    return biggest_face_emos


def getEmotions_manySamples(imgs):
    '''
    Args: imgs: list of images
    :return: emotions of the biggest face in the picture
    '''
    faces_emotions = []
    for img in imgs:
        faces_emotions += [detector.detect_emotions(img)]
    emo_samples = [find_biggest_face_emotions(emo_sample) for emo_sample in faces_emotions]
    # find the emotions of the biggest face in the picture
    for i in range(len(emo_samples) - 1):
        for emo in emo_samples[0].keys():
            emo_samples[i + 1][emo] += emo_samples[i][emo]
    avrg_emo = emo_samples[-1]
    for emo in emo_samples[0]:
        avrg_emo[emo] /= len(emo_samples)
    return avrg_emo


def getEmotions(img):
    '''
    :return: emotions of the biggest face in the picture
    '''
    faces_emotions = detector.detect_emotions(img)
    emos = find_biggest_face_emotions(faces_emotions)
    # find the emotions of the biggest face in the picture
    return emos