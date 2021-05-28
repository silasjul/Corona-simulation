import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from PIL import ImageTk,Image
import time
import random
import math
n = int(input("Number of people in simulation: ")) # Number of people in the simulation

class Person(object):
    # Constructor: creates a new person/agent
    def __init__(self, canvas, x, y):

        # Initialize the persons attributrs
        self.x = x
        self.y = y
        self.canvas = canvas

        self.dx = 0
        self.dy = 0
        self.deathTimer = None
        self.alive = True
        self.infected = False
        self.direction = "left"
        self.spreadTracker = 0
        self.directionTracker = random.randint(5, 15)
        self.windowSize = 975

        # Change parameters for different results
        self.infectionRadius = 35 # Spread 'reach'
        self.infectiousTime = 20 # Time they can spread virus
        self.infectiousChance = 30 # % chance to get infected within the spread reach per frame
    
    # Loads images
    def infectedPicture(self):
        self.infectedImg = ImageTk.PhotoImage(Image.open("C:/Users/silas/OneDrive/2.g/SO6/Simulation/Billeder/infected.png"))
        self.idinfected = self.canvas.create_image(self.x, self.y, anchor=NW, image=self.infectedImg)
    def deadPicture(self):
        self.deadImg = ImageTk.PhotoImage(Image.open("C:/Users/silas/OneDrive/2.g/SO6/Simulation/Billeder/dead.png"))
        self.iddead = self.canvas.create_image(self.x, self.y, anchor=NW, image=self.deadImg)


    def move(self):
        # Tracks the walkingdirection and makes sure they don't turn rapidly, but moves "smoothly" in random directions
        if self.directionTracker == 0:
            self.dx = random.choice([-0.5, 0.5])
            self.dy = random.choice([-0.5, 0.5])
            self.directionTracker = random.randint(20, 50)
        elif not self.alive:
            self.dx = 0
            self.dy = 0
        else:
            self.directionTracker -= 1

        # Tracks recent walking direction
        if self.dx < 0:
            self.direction = "left"
        else:
            self.direction = "right"

        # Move all images "attatched" to the person:
        self.canvas.move(self.idleft, self.dx, self.dy)
        self.canvas.move(self.idright, self.dx, self.dy)
        self.canvas.move(self.idinfected, self.dx, self.dy)
        self.canvas.move(self.iddead, self.dx, self.dy)

        # Hides/shows depending on direction
        if self.direction == "left":
            self.canvas.itemconfigure(self.idleft, state="normal")
            self.canvas.itemconfigure(self.idright, state="hidden")
        else:
            self.canvas.itemconfigure(self.idleft, state="hidden")
            self.canvas.itemconfigure(self.idright, state="normal")
        
        # Show infected overlay
        if self.infected:
            self.canvas.itemconfigure(self.idinfected, state="normal")
        else:
            self.canvas.itemconfigure(self.idinfected, state="hidden")

        # Show dead picture
        if not self.alive:
            self.canvas.itemconfigure(self.iddead, state="normal")
            self.canvas.itemconfigure(self.idinfected, state="hidden")
            self.canvas.itemconfigure(self.idleft, state="hidden")
            self.canvas.itemconfigure(self.idright, state="hidden")

        else:
            self.canvas.itemconfigure(self.iddead, state="hidden")
        
        # New Coordinates:
        self.x = self.x + self.dx
        self.y = self.y + self.dy

        # Colissiondetection:
        # Keeps them withing the window
        if self.x > self.windowSize:
            self.x -= 5
        if self.x < 0:
            self.x += 5
        if self.y > self.windowSize:
            self.y -= 5
        if self.y < 225:
            self.y += 5

    # Checks if the person is close to an infected and calls the infect method if True
    def check_infected(self, persons):
        for person in persons:
            if self.infected == False and person.infected == True and person.alive == True:
                d = math.sqrt(((self.x - person.x)**2 + (self.y - person.y)**2))

                if d < self.infectionRadius:
                    if random.randint(0,100) < self.infectiousChance:
                        self.infect()
                        person.spreadTracker += 1

    # Infects a person with corona
    def infect(self):
        self.infected = True
        self.deathTimer = time.time()

    # Kills a person after a certain time has passed
    def spreadTime(self):
        if self.infected and self.deathTimer != None:
            if time.time() - self.deathTimer > self.infectiousTime:
                self.alive = False


class BagWomen(Person):
    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        BagWomen.paint(self)

    def paint(self):
        self.BagWomenImgLeft = ImageTk.PhotoImage(Image.open("C:/Users/silas/OneDrive/2.g/SO6/Simulation/Billeder/BagWomenLeft.png"))
        self.BagWomenImgRight = ImageTk.PhotoImage(Image.open("C:/Users/silas/OneDrive/2.g/SO6/Simulation/Billeder/BagWomenRight.png"))
        self.idleft = self.canvas.create_image(self.x, self.y, anchor=NW, image=self.BagWomenImgLeft)
        self.idright = self.canvas.create_image(self.x, self.y, anchor=NW, image=self.BagWomenImgRight)
        Person.infectedPicture(self)
        Person.deadPicture(self)

class BusinessMan(Person):
    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        BusinessMan.paint(self)

    def paint(self):
        self.BusinessManImgLeft = ImageTk.PhotoImage(Image.open("C:/Users/silas/OneDrive/2.g/SO6/Simulation/Billeder/BusinessManLeft.png"))
        self.BusinessManImgRight = ImageTk.PhotoImage(Image.open("C:/Users/silas/OneDrive/2.g/SO6/Simulation/Billeder/BusinessManRight.png"))
        self.idleft = self.canvas.create_image(self.x, self.y, anchor=NW, image=self.BusinessManImgLeft)
        self.idright = self.canvas.create_image(self.x, self.y, anchor=NW, image=self.BusinessManImgRight)
        Person.infectedPicture(self)
        Person.deadPicture(self)

class CapBoy(Person):
    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        CapBoy.paint(self)

    def paint(self):
        self.CapBoyImgLeft = ImageTk.PhotoImage(Image.open("C:/Users/silas/OneDrive/2.g/SO6/Simulation/Billeder/CapBoyLeft.png"))
        self.CapBoyImgRight = ImageTk.PhotoImage(Image.open("C:/Users/silas/OneDrive/2.g/SO6/Simulation/Billeder/CapBoyRight.png"))
        self.idleft = self.canvas.create_image(self.x, self.y, anchor=NW, image=self.CapBoyImgLeft)
        self.idright = self.canvas.create_image(self.x, self.y, anchor=NW, image=self.CapBoyImgRight)
        Person.infectedPicture(self)
        Person.deadPicture(self)

class OldSackOfShit(Person):
    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        OldSackOfShit.paint(self)

    def paint(self):
        self.OldSackOfShitImgLeft = ImageTk.PhotoImage(Image.open("C:/Users/silas/OneDrive/2.g/SO6/Simulation/Billeder/OldSackOfShitLeft.png"))
        self.OldSackOfShitImgRight = ImageTk.PhotoImage(Image.open("C:/Users/silas/OneDrive/2.g/SO6/Simulation/Billeder/OldSackOfShitRight.png"))
        self.idleft = self.canvas.create_image(self.x, self.y, anchor=NW, image=self.OldSackOfShitImgLeft)
        self.idright = self.canvas.create_image(self.x, self.y, anchor=NW, image=self.OldSackOfShitImgRight)
        Person.infectedPicture(self)
        Person.deadPicture(self)

class SkoleBums(Person):
    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        SkoleBums.paint(self)

    def paint(self):
        self.SkoleBumsImgLeft = ImageTk.PhotoImage(Image.open("C:/Users/silas/OneDrive/2.g/SO6/Simulation/Billeder/SkoleBumsLeft.png"))
        self.SkoleBumsImgRight = ImageTk.PhotoImage(Image.open("C:/Users/silas/OneDrive/2.g/SO6/Simulation/Billeder/SkoleBumsRight.png"))
        self.idleft = self.canvas.create_image(self.x, self.y, anchor=NW, image=self.SkoleBumsImgLeft)
        self.idright = self.canvas.create_image(self.x, self.y, anchor=NW, image=self.SkoleBumsImgRight)
        Person.infectedPicture(self)
        Person.deadPicture(self)

class WhiteWomen(Person):
    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        WhiteWomen.paint(self)

    def paint(self):
        self.WhiteWomenImgLeft = ImageTk.PhotoImage(Image.open("C:/Users/silas/OneDrive/2.g/SO6/Simulation/Billeder/WhiteWomenLeft.png"))
        self.WhiteWomenImgRight = ImageTk.PhotoImage(Image.open("C:/Users/silas/OneDrive/2.g/SO6/Simulation/Billeder/WhiteWomenRight.png"))
        self.idleft = self.canvas.create_image(self.x, self.y, anchor=NW, image=self.WhiteWomenImgLeft)
        self.idright = self.canvas.create_image(self.x, self.y, anchor=NW, image=self.WhiteWomenImgRight)
        Person.infectedPicture(self)
        Person.deadPicture(self)

class Worker(Person):
    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        Worker.paint(self)

    def paint(self):
        self.WorkerImgLeft = ImageTk.PhotoImage(Image.open("C:/Users/silas/OneDrive/2.g/SO6/Simulation/Billeder/WorkerLeft.png"))
        self.WorkerImgRight = ImageTk.PhotoImage(Image.open("C:/Users/silas/OneDrive/2.g/SO6/Simulation/Billeder/WorkerRight.png"))
        self.idleft = self.canvas.create_image(self.x, self.y, anchor=NW, image=self.WorkerImgLeft)
        self.idright = self.canvas.create_image(self.x, self.y, anchor=NW, image=self.WorkerImgRight)
        Person.infectedPicture(self)
        Person.deadPicture(self)


class App(object):
    def __init__(self, master):

        # Create the canvas on which the agents are drawn
        self.time = time.time()
        self.master = master
        self.windowSize = 975
        self.infectedPeople = 10 # ammount of people to be infected at start
        self.endPrint = True
        self.firstWrite = True
        self.r0 = 0
        self.canvas = tk.Canvas(self.master, width=self.windowSize, height=self.windowSize,background='white')
        self.canvas.pack()
        self.sickDead = False

        # Create a reset button for the simulation
        self.but_reset = ttk.Button(master, text="Reset", command=self.init_sim)
        self.but_reset.pack(side=tk.BOTTOM)
        

        # Start / init the simulation
        self.init_sim()

        self.master.after(1, self.update)

    def update(self):

        # Update / move each agent
        for person in self.persons:
            person.move()
            person.check_infected(self.persons)
            person.spreadTime()

        # Count number of infected people
        ni = 0
        infectedPeople = 0
        ipl = []
        for p in self.persons:
            if p.infected:
                infectedPeople += 1

                # Basic reproduction number r0 calc
                if p.spreadTracker == 0:
                    ipl.append(0)
                else:
                    ipl.append(p.spreadTracker/(time.time()-p.deathTimer)*(p.infectiousTime-(time.time()-p.deathTimer))+p.spreadTracker)
                if p.alive:
                    ni += 1

        # If all sick are dead quit program     
        totalr = 0
        avrr0 = []
        for i in ipl:
            totalr += i
        self.r0 = totalr / len(ipl)
        avrr0.append(totalr / len(ipl))
        
        totalavrr0 = 0
        #print(ni, self.endPrint)
        if ni == 0 and self.endPrint:
            print("Sick are dead!")
            for i in avrr0:
                totalavrr0 += i
            print("Average r0:", totalavrr0 / len(avrr0))
            self.sickDead = True
            self.endPrint = False
            #root.quit()
        if not self.sickDead: 
            print("Currenctly infected:", ni, "  Time:", round(time.time() - self.time, ndigits=2), "  Total infected:", infectedPeople, "  r0:", round(self.r0, ndigits=2))

        # Append time and infected count to a txt-file
        self.timePast = round(time.time() - self.time, ndigits=2)
        if ni < n and not self.sickDead:
            fileInfected = open("C:/Users/silas/OneDrive/2.g/SO6/Simulation/Infected.txt", "a")
            fileTime = open("C:/Users/silas/OneDrive/2.g/SO6/Simulation/Time.txt", "a")
            if self.firstWrite:
                fileInfected.truncate(0)
                fileTime.truncate(0)
            fileInfected.write(str(ni)+"\n")
            fileTime.write(str(self.timePast)+"\n")
            self.firstWrite = False


        self.master.after(1, self.update)


    # Start / init simulation (clear all agents and create new ones)
    def init_sim(self):
        self.canvas.delete('all')

        # Prints background image anchored from the top left corner in pos (0, 0)
        self.backgroundImg = ImageTk.PhotoImage(Image.open("C:/Users/silas/OneDrive/2.g/SO6/Simulation/Billeder/LordSilasTown.png"))
        self.canvas.create_image(0, 0, anchor=NW, image=self.backgroundImg)
        self.firstWrite = True
        self.time = time.time()

        self.persons = []
        self.count = 0
        for i in range(n):
            x = random.randint(0,self.windowSize)
            y = random.randint(0,self.windowSize)
            people = [BagWomen(self.canvas, x, y), BusinessMan(self.canvas, x, y), CapBoy(self.canvas, x, y), OldSackOfShit(self.canvas, x, y), SkoleBums(self.canvas, x, y), WhiteWomen(self.canvas, x, y), Worker(self.canvas, x, y)]
            p = random.choice(people)
            if self.count <= self.infectedPeople:
                p.infect()
                self.count += 1

            self.persons.append(p)
        
        self.canvas.pack()

        
# Create the Tkinter application and run it
root = tk.Tk()
app = App(root)
root.mainloop()