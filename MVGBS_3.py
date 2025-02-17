# Import required library
import turtle
import random
##################################### GENISIAS################################


# Create screen
sc = turtle.Screen()
sc.title("Pong game")
sc.bgcolor("white")
sc.setup(width=550, height=550)


# Player 1
p1 = turtle.Turtle()
p1.speed(0)
p1.shape("circle")
p1.color("red")
p1.shapesize(stretch_wid=2, stretch_len=2)
p1.penup()
p1.goto(0, -200)


# Player 2
p2 = turtle.Turtle()
p2.speed(0)
p2.shape("circle")
p2.color("blue")
p2.shapesize(stretch_wid=2, stretch_len=2)
p2.penup()
p2.goto(0, 200)


# Ball of circle shape
hit_ball = turtle.Turtle()
hit_ball.speed(10)
hit_ball.shape("triangle")
hit_ball.color("green")
hit_ball.penup()
hit_ball.goto(0, 0)
hit_ball.dx = 10
hit_ball.dy = -10

# Initialize the score
Player_1 = 0
Player_2 = 0

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

#Player 2 on Arrow keys
##################################

#move p2 up
def p2_up():
    y = p2.ycor()
    if y < 250:  # Limit paddle movement
        y += 20
        p2.sety(y)

#move p2 down
def p2_down():
    y = p2.ycor()
    if y > -250:  # Limit paddle movement
        y -= 20
        p2.sety(y)

#move p2 left
def p2_left():
    x = p2.xcor()
    if x > -250:  # Limit paddle movement
        x -= 20
        p2.setx(x)

#move p2 right
def p2_right():
    x = p2.xcor()
    if x < 250:  # Limit paddle movement
        x += 20
        p2.setx(x)



##################################### Set keyboard binding################################


# Keyboard bindings
sc.listen()
sc.onkeypress(p2_up, "Up")  # Changed to 'up'
sc.onkeypress(p2_down, "Down")  # Changed to 'down'
sc.onkeypress(p2_left, "Left")
sc.onkeypress(p2_right, "Right")



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


# Main game loop
while True:
    sc.update()
    
    #time.sleep(0.01)  # Add delay to make game smoother
    
    hit_ball.setx(hit_ball.xcor() + hit_ball.dx) #Initiatw ball x loaction and movement
    hit_ball.sety(hit_ball.ycor() + hit_ball.dy) # Initiat bally movement and positions


    # Creates boarders around the game square and gives randomised.
    if hit_ball.ycor() > 250:
        hit_ball.sety(250)
        hit_ball.dy *= floater()

    if hit_ball.ycor() < -250:
        hit_ball.sety(-250)
        hit_ball.dy *= floater()

    if hit_ball.xcor() < -250:
        hit_ball.setx(-250)
        hit_ball.dx *= floater()

    if hit_ball.xcor() > 250:
        hit_ball.setx(250)
        hit_ball.dx *= floater()



    

        
    #if Player 1 "hits " the ball 
    if hit_ball.xcor() >= p1.xcor()-15 and  hit_ball.xcor() <= p1.xcor()+15 and hit_ball.ycor() >= p1.ycor()-15 and  hit_ball.ycor() <= p1.ycor()+15:
        hit_ball.goto(random.randint(-250, 250),random.randint(-250, 250)) # respawn the ball at a random location
        b = rando()        
        hit_ball.dy *= b #give the ball a random y velocity
        b = rando()
        hit_ball.dx *= b #give the ball a random x velocity
        Player_1 += 1 #1 up player score
        sketch.clear() #remove old score
        sketch.write("Computer: {}    Player: {}".format(
            Player_1, Player_2), align="left",
            font=("Courier", 12, "normal")) #print new score


    #AS ABOVE, JUST FOR PLAYER 2#
    
    if hit_ball.xcor() >= p2.xcor()-15 and  hit_ball.xcor() <= p2.xcor()+15 and hit_ball.ycor() >= p2.ycor()-15 and  hit_ball.ycor() <= p2.ycor()+15: #Ball centre is p2 centre
        hit_ball.goto(random.randint(-250, 250),random.randint(-250, 250)) #reset ball position to middle of screen
        b = rando()
        hit_ball.dy *= b 
        b = rando()
        hit_ball.dx *= b 
        Player_2 += 1 
        sketch.clear()
        sketch.write("Computer: {}    Player: {}".format(
            Player_1, Player_2), align="left",
            font=("Courier", 12, "normal")) 


    #Check fro win conditions (score >5) and print winner message

    if Player_2 >= 5:
        sketch = turtle.Turtle()
        sketch.speed(0)
        sketch.color("blue")
        sketch.penup()
        sketch.hideturtle()
        sketch.goto(0, 0)
        sketch.write("PLAYER WINS",
                     align="center", font=("Courier", 20, "normal"))
        

    if Player_1 >= 5:
        sketch = turtle.Turtle()
        sketch.speed(0)
        sketch.color("red")
        sketch.penup()
        sketch.hideturtle()
        sketch.goto(0, 0)
        sketch.write("Computer WINS",
                     align="center", font=("Courier", 20, "normal"))


    #Create intelegence for the player 2 sprite

    #If function
    a =1

    if p1.ycor() < hit_ball.ycor() and p1.xcor() < hit_ball.xcor():#If target y is < p2y: p2y -2
        y = p1.ycor()+ a
        x = p1.xcor() + a
        p1.goto(x,y)
    elif  p1.ycor() > hit_ball.ycor() and p1.xcor() > hit_ball.xcor():#If target y is < p2y: p2y -2
        y = p1.ycor()- a
        x = p1.xcor() - a
        p1.goto(x,y)
    elif  p1.ycor() > hit_ball.ycor() and p1.xcor() < hit_ball.xcor():#If target y is < p2y: p2y -2
        y = p1.ycor()- a
        x = p1.xcor() + a
        p1.goto(x,y)
    elif  p1.ycor() < hit_ball.ycor() and p1.xcor() > hit_ball.xcor():#If target y is < p2y: p2y -2
        y = p1.ycor()+ a
        x = p1.xcor() - a
        p1.goto(x,y)


"""
    if p1.ycor() < hit_ball.ycor():#If target y is < p2y: p2y -2
        y = p1.ycor()+ 2
        x = p1.xcor()
        p1.goto(y, x)
    elif  p1.ycor() > hit_ball.ycor():     #if ty > p2y: p2y + 2
        y = p1.ycor()- 2
        x = p1.xcor()
        p1.goto(y, x)


    if p1.xcor() < hit_ball.xcor():     #If target y is < p2y: p2y -2
        y = p1.ycor()
        x = p1.xcor() + 2
        p1.goto(y, x)
    elif  p1.xcor() > hit_ball.xcor():     #if ty > p2y: p2y + 2
        y = p1.ycor()
        x = p1.xcor() - 2
        p1.goto(y, x)
    #if tx > p2x: p2x + 2
"""