from os import remove
import mouse
import Helper
MainWindow = Helper.Tk()
Last_Icon = None

A90_templateIcon = Helper.imgPIL.open("a90.png")
A90_templateIcon.resize((100, 100))
A90_template = Helper.ImageTk.PhotoImage(A90_templateIcon)
bigA90_templIcon = Helper.imgPIL.open("A-90.png")
bigA90_templIcon.resize((200, 200))
A90scream_templateIcon = Helper.imgPIL.open("A-90_SCREAMER.png")
A90scream_templateIcon.resize((755, 755))
A90scream_template = Helper.ImageTk.PhotoImage(A90scream_templateIcon)
Hand_templateIcon = Helper.imgPIL.open("red_hand.png").convert("RGBA")
Hand_templateIcon.resize((100, 100))
Hand_template = Helper.ImageTk.PhotoImage(Hand_templateIcon)
CoinIcon_template = Helper.imgPIL.open("Gold.png").convert("RGBA")
def A90_Download():
    Helper.SetMusic("Ransom Timer.mp3")
    global Last_Icon
    MainWindow.config(bg="#820000")
    MainWindow.geometry(Helper.GetCenter(Helper.ScreenSize()[0], Helper.ScreenSize()[1]))
    Last_Icon.destroy()
    def GenerateHand():
        hand = Helper.Label(MainWindow, image=Hand_template, bg="#820000")
        hand.place(x=Helper.GeneratePositionOfCenterOnlyXY(100, 100)[0], y=Helper.GeneratePositionOfCenterOnlyXY(100, 100)[1])
        hand.image_ref = Hand_template
    def stop():
        MainWindow.config(bg="white")
        MainWindow.geometry(Helper.GetCenter(800, 500))
        Last_Icon.destroy()
    timeHand = 25
    for i in range(1, 100):
        MainWindow.after(timeHand, GenerateHand)
        timeHand+=25
    MainWindow.after(2500, stop)
def A90_screamer():
    global Last_Icon
    global MainWindow
    MainWindow.destroy()
    MainWindow=Helper.Tk()
    MainWindow.config(bg="#820000")
    MainWindow.attributes("-transparentcolor", "white")
    MainWindow.attributes("-topmost", True)
    MainWindow.attributes("-fullscreen", True)
    global A90scream_template
    A90scream_template = Helper.ImageTk.PhotoImage(A90scream_templateIcon)
    Last_Icon = Helper.Label(MainWindow, image=A90scream_template, bg="#820000")
    Last_Icon.pack(ipadx=400, ipady=400)
    Last_Icon.image_ref = A90scream_template
    Helper.SetMusic("A-90_JUMPSCARE.mp3", 1.4)
    def temp():
        MainWindow.destroy()
    MainWindow.after(1500, temp)
def BadEnd():
    A90_screamer()
def A90_normal(long):
    global Last_Icon
    MainWindow.config(bg="red")
    MainWindow.geometry(Helper.GetCenter(Helper.ScreenSize()[0], Helper.ScreenSize()[1]))
    Last_Icon.destroy()
    Last_Icon = Helper.Label(MainWindow, image=A90_template, bg="red")
    Last_Icon.place(x=Helper.GetCenterOnlyXY(100,100)[0], y=Helper.GetCenterOnlyXY(100,100)[1])
    Last_Icon.image_ref = A90_template
    def temp():
        MainWindow.config(bg="white")
        MainWindow.geometry(Helper.GetCenter(100, 100))
        Last_Icon.destroy()
    if long==True: MainWindow.after(3000, temp)
    else: MainWindow.after(300, temp)
def RedHand():
    global Last_Icon
    MainWindow.geometry(Helper.GetCenter(100, 100))
    Last_Icon.destroy()
    Last_Icon = Helper.Label(MainWindow, image=Hand_template, bg="white")
    Last_Icon.pack(anchor="center")
    Last_Icon.image_ref = Hand_template
coinsGet = 500
def Main():
    Helper.imgPIL.new(
        'RGB', (128, 128), color=(255, 255, 255)
    ).save(
        'ransom', format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])

    global MainWindow
    MainWindow.destroy()
    MainWindow = Helper.Tk()
    MainWindow.title("RANSOM")
    MainWindow.geometry("600x450")
    MainWindow.attributes("-toolwindow", False)
    MainWindow.iconbitmap("ransom.ico")
    MainWindow.config(bg="red")
    MainWindow.protocol("WM_WINDOW_DESTROY", BadEnd)
    title1 = Helper.Label(MainWindow, bg="red", fg="white", text="YOUR FILES", font="Arial 35 bold")
    title1.place(x=250, y=30)
    title2 = Helper.Label(MainWindow, bg="red", fg="white", text="HAVE BEEN", font="Arial 35 bold")
    title2.place(x=250, y=90)
    title3 = Helper.Label(MainWindow, bg="red", fg="white", text="ENCRYPTED", font="Arial 35 bold")
    title3.place(x=250, y=150)
    a90_template = Helper.ImageTk.PhotoImage(bigA90_templIcon)
    a90Icon = Helper.Label(MainWindow, image=a90_template, bg="red")
    a90Icon.place(x=0, y=20)
    warnRansomFone = Helper.Frame(MainWindow, bg="black", relief="solid", bd=7, highlightbackground="white", highlightcolor="white", highlightthickness=5)
    warnRansomFone.place(x=12.5, y=220, width=575, height=120)
    warnRansom1 = Helper.Label(warnRansomFone, bg="black", fg="white", font="Arial 18 bold", text="IF YOU DONT PAY THIS RANSOM BEFORE")
    warnRansom1.place(x=25, y=0)
    warnRansom2 = Helper.Label(warnRansomFone, bg="black", fg="white", font="Arial 18 bold", text="THE TIME ENDS, YOUR FILES WILL BE")
    warnRansom2.place(x=35, y=30)
    warnRansom3 = Helper.Label(warnRansomFone, bg="black", fg="red", font="Arial 18 bold", text="UNRECOVERABLE BY ANY MEANS")
    warnRansom3.place(x=55, y=60)
    a90Icon.image_ref = a90_template
    CoinsFone = Helper.Frame(MainWindow, bg="black", relief="solid", bd=7, highlightbackground="white", highlightcolor="white", highlightthickness=5)
    CoinsFone.place(x=12.5, y=350, width=575 / 2 - 90, height=85)
    CoinsCount = Helper.Label(CoinsFone, bg="black", fg="#FFFF98", font="Arial 40 bold", text="500")
    CoinsCount.place(x=5, y=0)
    MainWindow.CoinsCount = CoinsCount
    CoinIcon = Helper.ImageTk.PhotoImage(CoinIcon_template)
    CoinIconCount = Helper.Label(CoinsFone, image=CoinIcon, bg="black")
    CoinIconCount.place(x=115, y=5)
    CoinIconCount.image_ref = CoinIcon
    TimeFone = Helper.Frame(MainWindow, bg="red", relief="solid", highlightcolor="white", highlightthickness=5)
    TimeFone.place(x=25 + 575 / 2 - 90, y=350, width=575 / 2 + 75, height=85)
    TimeTitle = Helper.Label(TimeFone, bg="red", fg="black", font="Arial 44 bold", text="TIME:")
    TimeTitle.place(x=5, y=0)
    TimerObject = Helper.Label(TimeFone, bg="red", fg="black", font="Arial 44 bold", text="01:15")
    TimerObject.place(x=180, y=0)
    second = 75
    def GetCoin():
        coinsDialog = Helper.tkinter.filedialog.askopenfilename()
        if coinsDialog:
            if isinstance(coinsDialog, str):
                coinsDialog = [coinsDialog]
            global coinsGet
            for coin in coinsDialog:
                if Helper.path.basename(coin) == ".gold":
                    coinsGet-=100
                    Helper.SetSound("DroppedMoney.mp3")
                    CoinsCount.config(text=str(coinsGet))
                    remove(coin)
        if coinsGet<=0:
            Helper.pygame.mixer.music.stop()
            Helper.GoodEnd()
            return
        GetCoin()
    def TimerFunc():
        nonlocal second
        second-=1
        readyTimerText=""
        if second>=60 and second-60>=10: readyTimerText="01:"+str(second-60)
        elif second>=60 and second-60<10: readyTimerText="01:0"+str(second-60)
        elif second<60 and second != 0:
            readyTimerText="00:"+str(second)
            if second == 2:
                Helper.Desktop.EnabledIcons(False)
            if second < 10: readyTimerText="00:0"+str(second)
        else:
            global coinsGet
            coinsGet = 0
            BadEnd()
            return
        TimerObject.config(text=readyTimerText)
        MainWindow.after(1000, TimerFunc)
    MainWindow.after(1000, TimerFunc)
    Helper.RansomWindows(MainWindow)
    GetCoin()
trapped = False
def awakeMain(event):
    global trapped
    trapped = True
    Helper.mouse.unhook_all()
    Helper.SetMusic("A-90_JUMPSCARE.mp3", 1.4)
    A90_normal(True)
    MainWindow.after(1500, A90_Download)
    MainWindow.after(4500, Main)
    Helper.Desktop.EnabledIcons(True)
def isTrapped():
    Helper.mouse.unhook_all()
    if trapped == False: MainWindow.destroy()
def Start():
    RedHand()
    MainWindow.after(300, A90_normal, (False))
    MainWindow.after(100, Helper.mouse.hook, (awakeMain))
    MainWindow.after(700, isTrapped)
def Awake():
    global Last_Icon
    MainWindow.attributes("-transparentcolor", "white")
    MainWindow.attributes("-topmost", True)
    MainWindow.wm_overrideredirect(True)
    MainWindow.geometry(Helper.GeneratePositionOfCenter(100, 100))
    MainWindow.resizable(False, False)
    Last_Icon = Helper.Label(MainWindow, image=A90_template, bg="white")
    Last_Icon.pack(anchor="center")
    Last_Icon.image_ref = A90_template
    Helper.SetSound("Warning.mp3")
    MainWindow.after(500, Start)
    MainWindow.mainloop()
try:
    Awake()
except BaseException as e: pass
finally:
    Helper.Desktop.EnabledIcons(False)
    mouse.unhook_all()
    Helper.Desktop.comtypes.CoUninitialize()
