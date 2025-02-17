# Import required library
import turtle
import random
##################################### GENISIAS################################


# Create screen
sc = turtle.Screen()
sc.title("Pong game")
sc.bgcolor("white")
sc.setup(width=1000, height=1000)


# Player 1
p1 = turtle.Turtle()
p1.speed(0)
p1.shape("circle")
p1.color("red")
p1.shapesize(stretch_wid=2, stretch_len=2)
p1.penup()
p1.goto(0, -400)


# Player 2
p2 = turtle.Turtle()
p2.speed(0)
p2.shape("circle")
p2.color("blue")
p2.shapesize(stretch_wid=2, stretch_len=2)
p2.penup()
p2.goto(0, 400)


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
sketch.goto(-480, 480)
sketch.write("Player 1 : 0    Player 2: 0",
             align="left", font=("Courier", 12, "normal"))

##################################### Functions to move paddles################################

#Player 1 on WASD
##################################

#move p1 up
def p1_up():
    y = p1.ycor()
    if y < 500:  # Limit paddle movement
        y += 20
        p1.sety(y)

#move p1 down
def p1_down():
    y = p1.ycor()
    if y > -500:  # Limit paddle movement
        y -= 20
        p1.sety(y)

#move p1 left
def p1_left():
    x = p1.xcor()
    if x > -500:  # Limit paddle movement# swapped <>
        x -= 20
        p1.setx(x)

#move p1 right
def p1_right():
    x = p1.xcor()
    if x < 500:   # Limit paddle movement# swapped <>
        x += 20
        p1.setx(x)


#Player 2 on Arrow keys
##################################

#move p2 up
def p2_up():
    y = p2.ycor()
    if y < 500:  # Limit paddle movement
        y += 20
        p2.sety(y)

#move p2 down
def p2_down():
    y = p2.ycor()
    if y > -500:  # Limit paddle movement
        y -= 20
        p2.sety(y)

#move p2 left
def p2_left():
    x = p2.xcor()
    if x > -500:  # Limit paddle movement
        x -= 20
        p2.setx(x)

#move p2 right
def p2_right():
    x = p2.xcor()
    if x < 500:  # Limit paddle movement
        x += 20
        p2.setx(x)



##################################### Set keyboard binding################################


# Keyboard bindings
sc.listen()
sc.onkeypress(p1_up, "w")  # Changed to 'w'
sc.onkeypress(p1_down, "s")  # Changed to 's'
sc.onkeypress(p1_left, "a")
sc.onkeypress(p1_right, "d")
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



# Main game loop
while True:
    sc.update()
    
    #time.sleep(0.01)  # Add delay to make game smoother

    hit_ball.setx(hit_ball.xcor() + hit_ball.dx)
    hit_ball.sety(hit_ball.ycor() + hit_ball.dy)

    # Checking borders
    if hit_ball.ycor() > 500:
        hit_ball.sety(500)
        hit_ball.dy *= -1

    if hit_ball.ycor() < -500:
        hit_ball.sety(-500)
        hit_ball.dy *= -1

    if hit_ball.xcor() < -500:
        hit_ball.setx(-500)
        hit_ball.dx *= -1

    if hit_ball.xcor() > 500:
        hit_ball.setx(500)
        hit_ball.dx *= -1

    

    if hit_ball.xcor() == p1.xcor() and  hit_ball.ycor() == p1.ycor():
        hit_ball.goto(random.randint(-250, 250),random.randint(-250, 250))
        b = rando()        
        hit_ball.dy *= b
        b = rando()
        hit_ball.dx *= b
        Player_1 += 1
        sketch.clear()
        sketch.write("Player 1 : {}    Player 2: {}".format(
            Player_1, Player_2), align="left",
            font=("Courier", 12, "normal"))

    
    if hit_ball.xcor() == p2.xcor() and  hit_ball.ycor() == p2.ycor(): #Ball centre is p2 centre
        hit_ball.goto(random.randint(-250, 250),random.randint(-250, 250)) #reset ball position to middle of screen
        b = rando()
        hit_ball.dy *= b #Have ball begin moving left
        b = rando()
        hit_ball.dx *= b #have ball begin moving down
        Player_2 += 1 #add 2 point to player 2 score
        sketch.clear() #delete old score board
        sketch.write("Player 1 : {}    Player 2: {}".format(
            Player_1, Player_2), align="left",
            font=("Courier", 12, "normal")) #update the scoreboard with new info




    if Player_2 >= 6:
        sketch = turtle.Turtle()
        sketch.speed(0)
        sketch.color("blue")
        sketch.penup()
        sketch.hideturtle()
        sketch.goto(0, 0)
        sketch.write("PLAYER 2 WINS",
                     align="center", font=("Courier", 30, "normal"))
        return False

    if Player_1 >= 6:
        sketch = turtle.Turtle()
        sketch.speed(0)
        sketch.color("blue")
        sketch.penup()
        sketch.hideturtle()
        sketch.goto(0, 0)
        sketch.write("PLAYER 1 WINS",
                     align="center", font=("Courier", 30, "normal"))
       resturn False
        
    """
    # player ball collision
    if (hit_ball.xcor() < 500) and \
            (hit_ball.ycor() < p2.ycor() + 10 and hit_ball.ycor() > p2.ycor() - 10) and \
            (hit_ball.xcor() < p2.xcor() + 10 and hit_ball.xcor() > p2.xcor() - 10):
        hit_ball.setx(360)
        hit_ball.dx *= -1

    if (hit_ball.xcor() < -490 and hit_ball.xcor() > -500) and \
            (hit_ball.ycor() < p1.ycor() + 50 and hit_ball.ycor() > p1.ycor() - 50):
        hit_ball.setx(-360)
        hit_ball.dx *= -1
        
     """