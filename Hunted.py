# Import required library
import turtle
import random
##################################### GENISIAS################################


# Create screen
sc = turtle.Screen()
sc.title("Pong game")
sc.bgcolor("white")
sc.setup(width=550, height=550)


# Player
c1 = turtle.Turtle()
c1.speed(0)
c1.shape("circle")
c1.color("red")
c1.shapesize(stretch_wid=2, stretch_len=2)
c1.penup()
c1.goto(0, -200)


# Hunter
p1 = turtle.Turtle()
p1.speed(0)
p1.shape("circle")
p1.color("blue")
p1.shapesize(stretch_wid=2, stretch_len=2)
p1.penup()
p1.goto(0, 200)


# Initialize the score
Player = 0
Computer = 0

# Displays the score
sketch = turtle.Turtle()
sketch.speed(0)
sketch.color("blue")
sketch.penup()
sketch.hideturtle()
sketch.goto(-200, 200)
sketch.write("Computer: 0    Player: 0",
             align="left", font=("Courier", 12, "normal"))

##################################### Functions to move paddles################################

#Player 1 on WASD
##################################




#Player 2 on Arrow keys
##################################

#move p2 up
def p_up():
    y = p1.ycor()
    if y < 250:  # Limit paddle movement
        y += 20
        p1.sety(y)

#move p2 down
def p_down():
    y = p1.ycor()
    if y > -250:  # Limit paddle movement
        y -= 20
        p1.sety(y)

#move p2 left
def p_left():
    x = p1.xcor()
    if x > -250:  # Limit paddle movement
        x -= 20
        p1.setx(x)

#move p2 right
def p_right():
    x = p1.xcor()
    if x < 250:  # Limit paddle movement
        x += 20
        p1.setx(x)



##################################### Set keyboard binding################################


# Keyboard bindings
sc.listen()

sc.onkeypress(p_up, "Up")  # Changed to 'up'
sc.onkeypress(p_down, "Down")  # Changed to 'down'
sc.onkeypress(p_left, "Left")
sc.onkeypress(p_right, "Right")



#define randon numberer
def rando():
    a = random.randint(1, 2)
    if a == 1:
        return 1
    elif a == 2:
        return -1

#create anothe rando number thing, this time for the reflection thing
def floater():
    return random.random() * (-1 - 1)

#create time value and set inital movevment value (a)
tim = 0
a = 1


# Main game loop
while True:
    sc.update()
    
    #time.sleep(0.01)  # Add delay to make game smoother

    #increment tim up 1
    tim += 1



    
    #if computer "hits " the player 1 
    if  c1.xcor() < p1.xcor()+10 and c1.xcor() > p1.xcor()-10 and c1.ycor() > p1.ycor()-10 and c1.ycor() < p1.ycor()+10:
        p1.goto(random.randint(-250, 250),random.randint(-250, 250)) # respawn the ball at a random location
        Computer += 1 #1 up player score
        sketch.clear() #remove old score
        sketch.write("Computer: {}    Player: {}".format(
            Computer, Player), align="left",
            font=("Courier", 12, "normal")) #print new score



    #Check fro win conditions (score >5) and print winner message

    if Computer >= 1:
        fin_tim = tim
        sketch = turtle.Turtle()
        sketch.speed(0)
        sketch.color("red")
        sketch.penup()
        sketch.hideturtle()
        sketch.goto(0, 0)
        sketch.write("Computer WINS\n Time: {}".format(fin_tim),
                     align="center", font=("Courier", 20, "normal"))
    else:
        a = tim /2500
        a = int(a)        

    #Create intelegence for the player 2 sprite



    
    if c1.ycor() < p1.ycor() and c1.xcor() < p1.xcor():#If target y is < p2y: p2y -2
        y = c1.ycor()+ a
        x = c1.xcor() + a
        c1.goto(x,y)
    elif  c1.ycor() > p1.ycor() and c1.xcor() > p1.xcor():#If target y is < p2y: p2y -2
        y = c1.ycor()- a
        x = c1.xcor() - a
        c1.goto(x,y)
    elif  c1.ycor() > p1.ycor() and c1.xcor() < p1.xcor():#If target y is < p2y: p2y -2
        y = c1.ycor()- a
        x = c1.xcor() + a
        c1.goto(x,y)
    elif  c1.ycor() < p1.ycor() and c1.xcor() > p1.xcor():#If target y is < p2y: p2y -2
        y = c1.ycor()+ a
        x = c1.xcor() - a
        c1.goto(x,y)


print("Congratulations your time was: " ,tim)