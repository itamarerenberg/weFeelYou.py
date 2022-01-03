
import cv2
import PySimpleGUI as sg

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
            return frame

        # # update webcam1
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        window["cam1"].update(data=imgbytes)


    video_capture.release()
    cv2.destroyAllWindows()
