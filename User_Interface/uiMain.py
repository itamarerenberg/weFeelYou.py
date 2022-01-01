import tkinter as tk
from tkinter import filedialog, Text
import os
from tkhtmlview import HTMLLabel

root = tk.Tk()
apps = []
html = '''<iframe src='https://open.spotify.com/embed/playlist/37i9dQZF1E39XsLkxWRLiM?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture'></iframe>'''
# def addApp():
#
#     for widget in frame.winfo_children():
#         widget.destroy()
#
#
#     filename = filedialog.askopenfilename(initialdir="/", title="Select File",
#                                           filetypes=(("executables", ".exe"), ("all files", "*.*")))
#     apps.append(filename)
#     print(filename)
#     for app in apps:
#         label = tk.Label(frame, text=app, bg="gray")
#         label.pack()
#
#
# def runApps():
#     for app in apps:
#         os.startfile(app)
#
#
# canvas = tk.Canvas(root, height=500, width=500, bg='#263D42')
# canvas.pack()
#
# frame = tk.Frame(root, bg='white')
# frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
#
# openFile = tk.Button(root, text="open file", padx=10, pady=5, fg='white', bg='#263D42', command=addApp)
# openFile.pack()
#
# runApps = tk.Button(root, text="run apps", padx=10, pady=5, fg='white', bg='#263D42', command=runApps)
# runApps.pack()

my_label = HTMLLabel(root, html=html)

my_label.pack()

root.mainloop()
#<iframe src="https://open.spotify.com/embed/playlist/37i9dQZF1E39XsLkxWRLiM?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>