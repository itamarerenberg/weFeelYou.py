from fer import FER

detector = FER(mtcnn=True)


def find_dominant_face_emotions(faces_emos):
    '''
    :arg faces_emos: vector of faces emotion
    :return: vector of the emotion vector of the dominant face in the image
    '''
    biggest_box_size = 0
    biggest_face_emos = 0
    for d in faces_emos:
        if d['box'][2] > biggest_box_size:
            biggest_box_size = d['box'][2]
            biggest_face_emos = d['emotions']
    return biggest_face_emos


def getEmotions_manySamples(imgs):
    '''
    :arg imgs: list of images
    :return: average of emotions of the dominant face in the images
    '''
    faces_emotions = []
    for img in imgs:
        faces_emotions += [detector.detect_emotions(img)]
    emo_samples = [find_dominant_face_emotions(emo_sample) for emo_sample in faces_emotions]

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
    :arg img: image of face
    :return: emotions of the dominant face in the image
    '''
    faces_emotions = detector.detect_emotions(img)
    emos = find_dominant_face_emotions(faces_emotions)
    return emos