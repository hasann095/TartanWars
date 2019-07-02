from Tkinter import *
import time
import random
import winsound

def mousePressed(event):
    global root

    print event.x
    print event.y

    #This block of code is used to detect if the start button is pressed and incorporates the background music into the game, which activates after you press the start button,
    if event.x <= 550 and event.x >= 350 and event.y <= 400 and event.y >= 300 and canvas.data.Instructions == False and canvas.data.Startflag == False:
        canvas.data.Instructions = True
        winsound.PlaySound(canvas.data.bgmusic,winsound.SND_FILENAME|winsound.SND_ASYNC|winsound.SND_LOOP)
        redrawAll()

    #This starts the game from the instructions menu when the user clicks on the GO! button
    if canvas.data.Instructions == True and event.x >= 540 and event.x <= 680 and event.y >= 450 and event.y <= 500:
        canvas.data.Instructions = False
        canvas.data.Startflag = True

    #This activates the redo course button which restarts the game with the same professor
    if (canvas.data.win == True or canvas.data.lose == True) and event.x >= 310 and event.y >= 40 and event.x <= 390 and event.y <= 65:
        canvas.data.win = False
        canvas.data.lose = False
        canvas.data.healthbar1 = 250
        canvas.data.healthbar2 = 250
        canvas.data.movementa = 0
        canvas.data.movementb = 0

    #This activates the new course button which restarts the game with a different professor    
    if (canvas.data.win == True or canvas.data.lose == True) and event.x >= 410 and event.y >= 40 and event.x <= 490 and event.y <= 65:
        canvas.data.win = False
        canvas.data.lose = False
        canvas.data.healthbar1 = 250
        canvas.data.healthbar2 = 250
        canvas.data.movementa = 0
        canvas.data.movementb = 0
        canvas.data.level = random.randint(0,8)

    #This operates the exit button which closes the application
    if (canvas.data.win == True or canvas.data.lose == True) and event.x >= 510 and event.y >= 40 and event.x <= 590 and event.y <= 65:
        winsound.PlaySound(None, winsound.SND_FILENAME)
        root.destroy()
    
def keyPressed(event):
    global root
    
    #This block of code is used to move the player model in the canvas, while staying inside a range that approximates the left end of the screen to a bit farther than the mid of the screen
    if event.keysym == "Left" and canvas.data.playerx + canvas.data.movementa > 0:
        canvas.data.movementa -= 25
    elif event.keysym == "Right" and canvas.data.playerx + canvas.data.movementa < 500:
        canvas.data.movementa += 25

    #This block of code is for detecting when the user presses the punch buttons A or D. It makes a punch flag true which further activates the punch mechanisms in timerfired() 
    if event.char == "a":
        canvas.data.punchA = True
        canvas.data.punchAFlag = True
    if event.char == "d":
        canvas.data.punchB = True
        canvas.data.punchBFlag = True

    #If you press escape, it ends the canvas window and the background
    if event.keysym=="Escape":
        winsound.PlaySound(None, winsound.SND_FILENAME)
        root.destroy()
    
    redrawAll()

def timerFired(previousTime):
    currentTime = time.time()
    dt = currentTime - previousTime

    #This ensures that whatever animations take place, only take place when the game has been started, i.e. the start flag has been made true
    if(canvas.data.Startflag == True):
        punchprobability = 0

        #The hopflag is used to make the models hop up and down in repetition on their respective x-axis, in order to portray how boxers behave in a fight
        if canvas.data.hopflag == False and canvas.data.lose == False and canvas.data.win == False:
            canvas.data.hop -= 5
            canvas.data.hopflag = True
        elif canvas.data.hopflag == True and canvas.data.lose == False and canvas.data.win == False:
            canvas.data.hop += 5
            canvas.data.hopflag = False

        #This is the animation part of the punches by the model of the player. Punches A and B represent the punches by buttons a and d respectively. Basically, they check if the punch flag is
        #True, in the event of which, the cooridnates of the arms and boxing gloves increases to simulate a punch, and then the flag is made false, which produces the reverse of the former mentioned.
        if canvas.data.punchA == True and canvas.data.lose == False and canvas.data.win == False:
            while canvas.data.puncha != -40:
                canvas.data.puncha -= 5
                canvas.data.punchaa += 6
            canvas.data.punchA = False
        elif canvas.data.punchA == False and canvas.data.lose == False and canvas.data.win == False:
            while canvas.data.puncha != 0:
                canvas.data.puncha += 5
                canvas.data.punchaa -= 6

        if canvas.data.punchB == True and canvas.data.lose == False and canvas.data.win == False:
            while canvas.data.punchb != -50:
                canvas.data.punchb -= 5
                canvas.data.punchbb += 6
            canvas.data.punchB = False
        elif canvas.data.punchB == False and canvas.data.lose == False and canvas.data.win == False:
            while canvas.data.punchb != 0:
                canvas.data.punchb += 5
                canvas.data.punchbb -= 6

        #This detects if a punch by the player reaches the face of the opponent, and if so, it reduces the health of the opponent by 10
        if (canvas.data.playerx + 210 + canvas.data.movementa + canvas.data.punchaa) >= canvas.data.opponentx + canvas.data.movementb + 250 and canvas.data.win == False and canvas.data.lose == False and 375 + canvas.data.healthbar2 < 875 and (canvas.data.punchAFlag == True or canvas.data.punchBFlag == True):
            canvas.data.healthbar2 += 10
            canvas.data.punchAFlag = False
            canvas.data.punchBFlag = False

        #This is the part of the code that randomizes the movement of th opponent
        if canvas.data.opponentx + 300 + canvas.data.movementb > 500 and canvas.data.opponentx + 300 + canvas.data.movementb < 900 and canvas.data.win == False and canvas.data.healthbar2 + 375 < 875 and canvas.data.lose == False:
            canvas.data.movementb += random.randint(-20,20)
        elif canvas.data.opponentx + 300 + canvas.data.movementb < 500 and canvas.data.win == False and canvas.data.lose == False:
            canvas.data.movementb += 30
        elif canvas.data.opponentx + 300 + canvas.data.movementb > 900 and canvas.data.win == False and canvas.data.lose == False:
            canvas.data.movementb -= 30
        

        #punchprobability detects a 1 in 7 chance of the opponent punching the player
        punchprobability = random.randint(0,50)
        if punchprobability%7 == 0 and canvas.data.lose == False and canvas.data.win == False:
            canvas.data.opponentPunchAFlag = True
            canvas.data.opponentPunchA = True
        elif punchprobability%7 == 1 and canvas.data.lose == False and canvas.data.win == False:
            canvas.data.opponentPunchBFlag = True
            canvas.data.opponentPunchB = True

        if canvas.data.opponentPunchA == True and canvas.data.lose == False and canvas.data.win == False:
            while canvas.data.punchoa != -40:
                canvas.data.punchoa -= 5
                canvas.data.punchoaa -= 6
            canvas.data.opponentPunchA = False
        elif canvas.data.opponentPunchA == False and canvas.data.lose == False and canvas.data.win == False:
            while canvas.data.punchoa != 0:
                canvas.data.punchoa += 5
                canvas.data.punchoaa += 6

        if canvas.data.opponentPunchB == True and canvas.data.lose == False and canvas.data.win == False:
            while canvas.data.punchob != -40:
                canvas.data.punchob -= 5
                canvas.data.punchobb -= 6
            canvas.data.opponentPunchB = False
        elif canvas.data.opponentPunchB == False and canvas.data.lose == False and canvas.data.win == False:
            while canvas.data.punchob != 0:
                canvas.data.punchob += 5
                canvas.data.punchobb += 6

        if (canvas.data.opponentx - 125 + canvas.data.movementb - canvas.data.punchoa) <= canvas.data.playerx + canvas.data.movementa and canvas.data.win == False and canvas.data.lose == False and canvas.data.healthbar1 > 0  and (canvas.data.opponentPunchAFlag == True or canvas.data.opponentPunchBFlag == True):
            canvas.data.healthbar1 -= 10
            canvas.data.opponentPunchAFlag = False
            canvas.data.opponentPunchBFlag = False

        #This detects if the player has won or lost, and makes a respective flag true. It also stops all actions of movement of the player and the opponent
        elif canvas.data.healthbar2 >= 500:
            canvas.data.movementb = 0
            canvas.data.win = True
        elif canvas.data.healthbar1 <= 0:
            canvas.data.movementb = 0
            canvas.data.lose = True

        if canvas.data.lose == True or canvas.data.win == True:
            canvas.data.movementb += 10

    redrawAll()
    canvas.after(100, timerFired, currentTime)

def model(x,y):
    #left leg
    canvas.create_polygon(x + canvas.data.movementa, y+300 + canvas.data.hop,
                          x+25 + canvas.data.movementa, y+350 + canvas.data.hop,
                          x + canvas.data.movementa, y+550 + canvas.data.hop,
                          x+35 + canvas.data.movementa, y+550 + canvas.data.hop,
                          x+60 + canvas.data.movementa, y+350 + canvas.data.hop,
                          x+35 + canvas.data.movementa, y+300 + canvas.data.hop, fill="#161616", outline="black")
    #right leg
    canvas.create_polygon(x+55 + canvas.data.movementa, y+300 + canvas.data.hop,
                          x+80 + canvas.data.movementa, y+350 + canvas.data.hop,
                          x+55 + canvas.data.movementa, y+550 + canvas.data.hop,
                          x+90 + canvas.data.movementa, y+550 + canvas.data.hop,
                          x+115 + canvas.data.movementa, y+350 + canvas.data.hop,
                          x+90 + canvas.data.movementa, y+300 + canvas.data.hop, fill="#161616", outline="black")
    #right arm
    canvas.create_polygon(x+70 + canvas.data.movementa, y+100 + canvas.data.hop,
                          x+150 + canvas.data.movementa, y+150 + canvas.data.hop + canvas.data.puncha,
                          x+175 + canvas.data.movementa + canvas.data.punchaa, y+100 + canvas.data.hop,
                          x+185 + canvas.data.movementa + canvas.data.punchaa, y+150 + canvas.data.hop,
                          x+150 + canvas.data.movementa, y+175 + canvas.data.hop + canvas.data.puncha,
                          x+80 + canvas.data.movementa, y+150 + canvas.data.hop, fill="#161616", outline="black")
    #mainbody
    canvas.create_image(x+70 + canvas.data.movementa, y+180 + canvas.data.hop,image=canvas.data.scottiebody)
    #left arm
    canvas.create_polygon(x + canvas.data.movementa, y+100 + canvas.data.hop,
                          x+50 + canvas.data.movementa, y+150 + canvas.data.hop + canvas.data.punchb,
                          x+75 + canvas.data.movementa + canvas.data.punchbb, y+125 + canvas.data.hop,
                          x+85 + canvas.data.movementa + canvas.data.punchbb, y+150 + canvas.data.hop,
                          x+50 + canvas.data.movementa, y+175 + canvas.data.hop + canvas.data.punchb,
                          x + canvas.data.movementa, y+150 + canvas.data.hop, fill="#161616", outline="black")
    #left hand
    canvas.create_image(x+210 + canvas.data.movementa + canvas.data.punchaa, y+108 + canvas.data.hop, image=canvas.data.leftglove)
    #right hand
    canvas.create_image(x+125 + canvas.data.movementa + canvas.data.punchbb, y+108 + canvas.data.hop, image=canvas.data.rightglove)

def opponent(x,y):

    head = canvas.data.professors[canvas.data.level]
    
    #left leg
    canvas.create_polygon(x+385 + canvas.data.movementb, y+250 + canvas.data.hop,
                          x+360 + canvas.data.movementb, y+350 + canvas.data.hop,
                          x+385 + canvas.data.movementb, y+550 + canvas.data.hop,
                          x+350 + canvas.data.movementb, y+550 + canvas.data.hop,
                          x+325 + canvas.data.movementb, y+350 + canvas.data.hop,
                          x+350 + canvas.data.movementb, y+250 + canvas.data.hop, fill="white", outline="black")
    #right leg
    canvas.create_polygon(x+330 + canvas.data.movementb, y+250 + canvas.data.hop,
                          x+305 + canvas.data.movementb, y+350 + canvas.data.hop,
                          x+330 + canvas.data.movementb, y+550 + canvas.data.hop,
                          x+295 + canvas.data.movementb, y+550 + canvas.data.hop,
                          x+270 + canvas.data.movementb, y+350 + canvas.data.hop,
                          x+295 + canvas.data.movementb, y+250 + canvas.data.hop, fill="white", outline="black")
    #left arm
    canvas.create_polygon(x+330 + canvas.data.movementb, y+100 + canvas.data.hop,
                          x+235 + canvas.data.movementb, y+150 + canvas.data.hop + canvas.data.punchoa,
                          x+210 + canvas.data.movementb + canvas.data.punchoaa, y+100 + canvas.data.hop,
                          x+200 + canvas.data.movementb + canvas.data.punchoaa, y+150 + canvas.data.hop,
                          x+235 + canvas.data.movementb, y+175 + canvas.data.hop + canvas.data.punchoa,
                          x+330 + canvas.data.movementb, y+150 + canvas.data.hop, fill="#0099ff", outline="#004d80")
    #body
    canvas.create_image(x+350 + canvas.data.movementb, y+180 + canvas.data.hop,image=canvas.data.opponentb)
    #head
    canvas.create_image(x+335 + canvas.data.movementb, y+50 + canvas.data.hop,image=head)
    #right arm
    canvas.create_polygon(x+404 + canvas.data.movementb, y+110 + canvas.data.hop,
                          x+325 + canvas.data.movementb, y+150 + canvas.data.hop+ canvas.data.punchob,
                          x+300 + canvas.data.movementb+ canvas.data.punchobb, y+125 + canvas.data.hop,
                          x+290 + canvas.data.movementb+ canvas.data.punchobb, y+150 + canvas.data.hop,
                          x+325 + canvas.data.movementb, y+175 + canvas.data.hop+ canvas.data.punchob,
                          x+398 + canvas.data.movementb, y+160 + canvas.data.hop, fill="#0099ff", outline="#004d80")
    #right hand
    canvas.create_image(x+166 + canvas.data.movementb + canvas.data.punchoa, y+108 + canvas.data.hop,image=canvas.data.Orightglove)
    #left hand
    canvas.create_image(x+250 + canvas.data.movementb + canvas.data.punchob, y+108 + canvas.data.hop,image=canvas.data.Oleftglove)

def redrawAll():
    canvas.delete(ALL)

    canvas.create_image(450,350, image=canvas.data.arena)
    canvas.create_image(450,610, image=canvas.data.ring)

    #Creates the basic menu screen with the logo and the start button
    if canvas.data.Instructions == False and canvas.data.Startflag == False:
        canvas.create_image(450,150, image=canvas.data.logo)
        canvas.create_image(450, 350, image=canvas.data.start)

    #Creates the Instructions screen
    if canvas.data.Instructions == True:
        canvas.create_rectangle(120, 140,
                                780, 600, fill = "light blue", outline = "blue")
        canvas.create_rectangle(130, 150,
                                770, 590, fill = "#87CEFA", outline="light blue")
        canvas.create_text(450, 143, text="Instructions", font=("AR JULIAN", 50), anchor=N, fill = "#148da7")
        canvas.create_line(450, 230,
                           450, 560, fill = "#598E92", width = 5, dash=(5,1,2,1), dashoff=3)
        canvas.create_image(180, 250, image=canvas.data.Akey, anchor=NW)
        canvas.create_image(330, 251, image=canvas.data.Dkey, anchor=NW)
        canvas.create_image(175, 325, image=canvas.data.Punch, anchor=NW)
        canvas.create_image(325, 320, image=canvas.data.Kick, anchor=NW)
        canvas.create_image(215, 440, image=canvas.data.Leftkey, anchor=NW)
        canvas.create_image(215 + 85, 440, image=canvas.data.Rightkey, anchor=NW)
        canvas.create_text(200, 510, text="Strafe Left", font=30, anchor=NW)
        canvas.create_text(290, 510, text="Strafe Right", font=30, anchor=NW)
        canvas.create_rectangle(535, 445,
                                685, 505, fill="#F0E68C", outline="#F0E68C")
        canvas.create_rectangle(540, 450,
                                680, 500, fill="orange", outline="#F0E68C")
        canvas.create_text(610, 475, text="GO!", font= 60)
        canvas.create_text(165, 570, text="Disclaimer: This game was made purely with fun intentions. We do not advocate violence against professors.", anchor=NW)

    #Creates the models of the fighters as well as the healthbars  
    if canvas.data.Startflag == True:
        canvas.create_rectangle(25-5, 40-5,
                                275 + 5, 60 + 5, fill="light blue", outline="blue")
        canvas.create_rectangle(25, 40,
                                275 - (250 - canvas.data.healthbar1), 60, fill="red", outline="pink")
        canvas.create_rectangle(625 - 5, 40 - 5,
                                875 + 5, 60 + 5, fill="light blue", outline="blue")
        canvas.create_rectangle(900 - 25, 40,
                                900 - 275 - (250 - canvas.data.healthbar2), 60, fill = "red", outline = "pink")
        
        model(canvas.data.playerx, canvas.data.playery)
        opponent(canvas.data.opponentx, canvas.data.opponenty)

    #Makes the Win message when the player wins
    if canvas.data.win == True or canvas.data.healthbar2 <= 0:
        canvas.create_text(425, 100,
                           text="You Got An A!!", font=("Times New Roman", 36), fill="orange", anchor=N)
        
    #Makes the Lose message when the player loses
    if canvas.data.lose == True or canvas.data.healthbar1 <= 0:
        canvas.create_text(425, 100,
                           text="You Got An R!!", font=("Times New Roman", 36), fill="orange", anchor=N)

    if canvas.data.lose == True or canvas.data.win == True:
        canvas.create_rectangle(310, 40,
                                390, 65, fill="orange")
        canvas.create_text(315, 45, text = "Redo Course", anchor=NW)
        canvas.create_rectangle(410, 40,
                                490, 65, fill="orange")
        canvas.create_text(415, 45, text = "New Course", anchor=NW)
        canvas.create_rectangle(510, 40,
                                590, 65, fill="orange")
        canvas.create_text(540, 45, text = "Exit", anchor=NW)

def init():

    #These contain the entire initial values in the game which include setting of all the flags as false, the healthbars to be 250 in value, the movements to be equal to zero and to import the sounds and pictures of the professors
    canvas.data.Startflag = False
    canvas.data.healthbar1 = 250
    canvas.data.healthbar2 = 250
    canvas.data.bgmusic = "sounds/JohnCena.wav"
    canvas.data.endbutton = False
    canvas.data.Instructions = False
    canvas.data.hop = 0
    canvas.data.hopflag = False

    canvas.data.level = random.randint(0,8)
    
    canvas.data.movementa = 0

    canvas.data.movementb = 0

    canvas.data.lose = False
    canvas.data.win = False

    canvas.data.puncha = 0
    canvas.data.punchaa = 0
    canvas.data.punchA = False
    canvas.data.punchAFlag = False

    canvas.data.punchb = 0
    canvas.data.punchbb = 0
    canvas.data.punchB = False
    canvas.data.punchBFlag = False

    canvas.data.opponentPunchA = False
    canvas.data.opponentPunchAFlag = False
    canvas.data.punchoa = 0
    canvas.data.punchoaa = 0

    canvas.data.opponentPunchB = False
    canvas.data.opponentPunchBFlag = False
    canvas.data.punchob = 0
    canvas.data.punchobb = 0

    canvas.data.opponentPunchBFlag = False

    canvas.data.playerx = 100
    canvas.data.playery = 250
    canvas.data.opponentx = 300
    canvas.data.opponenty = 250

    canvas.data.arena = PhotoImage(file="images/arena.gif")
    canvas.data.ring = PhotoImage(file="images/ring.gif")
    canvas.data.logo = PhotoImage(file="images/logo.gif")
    canvas.data.start = PhotoImage(file="images/start.gif")
    canvas.data.Akey=PhotoImage(file="images/Akey.gif")
    canvas.data.Dkey=PhotoImage(file="images/Dkey.gif")
    canvas.data.Leftkey=PhotoImage(file="images/Leftkey.gif")
    canvas.data.Rightkey=PhotoImage(file="images/Rightkey.gif")
    canvas.data.Punch=PhotoImage(file="images/Punch.gif")
    canvas.data.Kick=PhotoImage(file="images/Kick.gif")
    canvas.data.scottiebody=PhotoImage(file="images/scottiebody.gif")
    canvas.data.opponentb=PhotoImage(file="images/opponent.gif")
    canvas.data.leftglove=PhotoImage(file="images/leftglove.gif")
    canvas.data.rightglove=PhotoImage(file="images/rightglove.gif")
    canvas.data.Oleftglove=PhotoImage(file="images/Oleftglove.gif")
    canvas.data.Orightglove=PhotoImage(file="images/Orightglove.gif")
    
    canvas.data.oliver=PhotoImage(file="professors/oliver.gif")
    canvas.data.dan=PhotoImage(file="professors/dan.gif")
    canvas.data.dudley=PhotoImage(file="professors/dudley.gif")
    canvas.data.eric=PhotoImage(file="professors/eric.gif")
    canvas.data.fossati=PhotoImage(file="professors/fossati.gif")
    canvas.data.houda=PhotoImage(file="professors/houda.gif")
    canvas.data.reilly=PhotoImage(file="professors/reilly.gif")
    canvas.data.silvia=PhotoImage(file="professors/silvia.gif")
    canvas.data.mitchel=PhotoImage(file="professors/mitchel.gif")

    canvas.data.professors=[canvas.data.dan, canvas.data.reilly, canvas.data.silvia,  canvas.data.eric, canvas.data.mitchel,  canvas.data.dudley, canvas.data.houda, canvas.data.fossati, canvas.data.oliver]
    pass

def run():
    global canvas
    global root
    root = Tk()
    canvas = Canvas(root, width=900, height=900, bg="black")
    canvas.pack()
    root.canvas = canvas.canvas = canvas
    class MyModel: pass
    canvas.data = MyModel()
    init()
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    timerFired(time.time())
    root.mainloop()

run()
