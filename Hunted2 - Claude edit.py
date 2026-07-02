# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 11:07:38 2026

@author: MattCust
"""
import turtle
import random
import time
import math
 
# ── Constants ──────────────────────────────────────────────────────────────────
W, H            = 700, 700
HALF            = 280
WALL            = 270
PLAYER_SPEED    = 5
BASE_HUNTER     = 0.8
SPEED_RAMP      = 0.00075      # faster ramp (was 0.0002)
POWERUP_INT     = 350
ROUNDS          = 3
TICK_SLEEP      = 0.016
 
# Obstacle settings
OBS_COUNT       = 4
OBS_MIN_LIFE    = 300
OBS_MAX_LIFE    = 600
OBS_WARN        = 80
OBS_SPAWN_GAP   = 180
OBS_HALF        = 22          # half-size for collision (double the old ~11)
 
# Bonus hunter
BONUS_HUNTER_DUR = 300        # ticks the extra hunter sticks around
 
# Token effect durations (ticks)
DUR_FREEZE       = 180
DUR_SPEED_BOOST  = 240
DUR_SLOW         = 240
 
# Palette
BG              = "#080810"
GRID_COL        = "#12122A"
PLAYER_COL      = "#00F5D4"
HUNTER_COL      = "#FF4D6D"
BONUS_COL       = "#FF9020"
TOKEN_COL       = "#FFE66D"
OBS_COL         = "#7B2FBE"
OBS_WARN_COL    = "#FF8800"
TEXT_COL        = "#E0E0FF"
DIM_COL         = "#2A2A4A"
DANGER_COL      = "#FF4D6D"
SAFE_COL        = "#00F5D4"
FREEZE_COL      = "#A0C4FF"
SLOW_COL        = "#FF88FF"
BOOST_COL       = "#88FF88"
 
# ── Token definitions ──────────────────────────────────────────────────────────
# Each entry: (key, label, colour, description shown to player)
TOKENS = [
    ("freeze_hunter",   "❄ FREEZE HUNTER",      "#A0C4FF", "Hunter frozen!"),
    ("freeze_player",   "❄ FREEZE YOU",          "#FF88FF", "You are frozen!"),
    ("boost_player",    "⚡ SPEED BOOST",         "#88FF88", "Speed boost!"),
    ("slow_player",     "🐢 SLOWED",              "#FFAA44", "You are slowed!"),
    ("boost_hunter",    "⚡ HUNTER BOOST",        "#FF6644", "Hunter sped up!"),
    ("slow_hunter",     "🐢 HUNTER SLOWED",       "#AAFFCC", "Hunter slowed!"),
    ("teleport_player", "✦ RANDOM TELEPORT",      "#FF44FF", "You teleported!"),
    ("swap_teleport",   "⇄ SWAP TELEPORT",        "#FFFF44", "Positions swapped!"),
    ("extra_hunter",    "☠ EXTRA HUNTER",         "#FF2200", "Extra hunter!"),
]
 
# ── Screen ─────────────────────────────────────────────────────────────────────
sc = turtle.Screen()
sc.title("HUNTER  ·  Survive as long as you can")
sc.bgcolor(BG)
sc.setup(width=W, height=H)
sc.tracer(0)
 
# ── Grid ───────────────────────────────────────────────────────────────────────
def draw_grid():
    t = turtle.Turtle()
    t.hideturtle(); t.speed(0); t.pensize(1); t.color(GRID_COL)
    for x in range(-HALF, HALF + 1, 40):
        t.penup(); t.goto(x, -HALF); t.pendown(); t.goto(x, HALF)
    for y in range(-HALF, HALF + 1, 40):
        t.penup(); t.goto(-HALF, y); t.pendown(); t.goto(HALF, y)
    t.pensize(3); t.color(DIM_COL)
    t.penup(); t.goto(-HALF, -HALF); t.pendown()
    t.goto(HALF, -HALF); t.goto(HALF, HALF)
    t.goto(-HALF, HALF); t.goto(-HALF, -HALF)
    t.penup()
 
draw_grid()
 
# ── Sprite factory ─────────────────────────────────────────────────────────────
def make_sprite(shape, color, x, y, sw=1.0, sl=1.0):
    t = turtle.Turtle()
    t.speed(0); t.shape(shape); t.color(color)
    t.shapesize(sw, sl); t.penup(); t.goto(x, y)
    return t
 
player       = make_sprite("circle",   PLAYER_COL,  0, -150, 1.0, 1.0)
hunter       = make_sprite("triangle", HUNTER_COL,  0,  150, 1.2, 1.2)
token_sprite = make_sprite("circle",   TOKEN_COL,   9999, 9999, 0.7, 0.7)
# Bonus hunter — hidden until activated
bonus_hunter = make_sprite("triangle", BONUS_COL,   9999, 9999, 1.0, 1.0)
 
# ── Obstacle class ─────────────────────────────────────────────────────────────
class Obstacle:
    def __init__(self):
        # Doubled shapesize (was 1.4 → 2.8 gives roughly 2× visual area)
        self.t        = make_sprite("square", OBS_COL, 9999, 9999, 2.8, 2.8)
        self.active   = False
        self.life     = 0
        self.max_life = 0
        self.x = self.y = 0
 
    def spawn(self, x, y):
        self.x, self.y = x, y
        self.max_life  = random.randint(OBS_MIN_LIFE, OBS_MAX_LIFE)
        self.life      = self.max_life
        self.active    = True
        self.t.color(OBS_COL)
        self.t.goto(x, y)
 
    def tick(self):
        if not self.active:
            return
        self.life -= 1
        if self.life <= OBS_WARN:
            self.t.color(OBS_WARN_COL if (self.life // 8) % 2 == 0 else OBS_COL)
        if self.life <= 0:
            self.hide()
 
    def hide(self):
        self.active = False
        self.t.goto(9999, 9999)
 
    def blocks(self, x2, y2):
        if not self.active:
            return False
        return abs(x2 - self.x) < OBS_HALF + 10 and abs(y2 - self.y) < OBS_HALF + 10
 
obstacles = [Obstacle() for _ in range(OBS_COUNT)]
 
# ── HUD turtles ────────────────────────────────────────────────────────────────
hud    = turtle.Turtle(); hud.speed(0);    hud.penup(); hud.hideturtle()
bar    = turtle.Turtle(); bar.speed(0);    bar.penup(); bar.hideturtle()
flash  = turtle.Turtle(); flash.speed(0);  flash.penup(); flash.hideturtle()
effect = turtle.Turtle(); effect.speed(0); effect.penup(); effect.hideturtle()
pause_t= turtle.Turtle(); pause_t.speed(0);pause_t.penup(); pause_t.hideturtle()
 
# ── Input ──────────────────────────────────────────────────────────────────────
keys   = {"Up": False, "Down": False, "Left": False, "Right": False}
paused = [False]   # list so lambda can mutate it
 
def toggle_pause():
    paused[0] = not paused[0]
    if paused[0]:
        pause_t.color(TEXT_COL)
        pause_t.goto(0, 20)
        pause_t.write("PAUSED\nSPACE to resume",
                      align="center", font=("Courier", 24, "bold"))
    else:
        pause_t.clear()
 
sc.listen()
for k in keys:
    sc.onkeypress(  lambda key=k: keys.__setitem__(key, True),  k)
    sc.onkeyrelease(lambda key=k: keys.__setitem__(key, False), k)
sc.onkeypress(toggle_pause, "space")
 
# ── Helpers ────────────────────────────────────────────────────────────────────
def dist(a, b):
    return math.hypot(a.xcor() - b.xcor(), a.ycor() - b.ycor())
 
def dist_xy(x1, y1, x2, y2):
    return math.hypot(x1 - x2, y1 - y2)
 
def clamp(v, lo, hi):
    return max(lo, min(hi, v))
 
def safe_pos(clear_px=100):
    for _ in range(300):
        x = random.randint(-WALL + 40, WALL - 40)
        y = random.randint(-WALL + 40, WALL - 40)
        if dist_xy(x, y, player.xcor(), player.ycor()) < clear_px:
            continue
        if any(o.active and dist_xy(x, y, o.x, o.y) < OBS_HALF * 3 for o in obstacles):
            continue
        return x, y
    return random.randint(-100, 100), random.randint(-100, 100)
 
def flash_message(msg, color=TEXT_COL, duration=1.2, size=26):
    flash.clear(); flash.color(color)
    flash.goto(0, 20)
    flash.write(msg, align="center", font=("Courier", size, "bold"))
    sc.update(); time.sleep(duration); flash.clear()
 
def show_effect(msg, color):
    effect.clear(); effect.color(color)
    effect.goto(0, -60)
    effect.write(msg, align="center", font=("Courier", 14, "bold"))
 
# ── Movement ───────────────────────────────────────────────────────────────────
def move_player(speed_mult=1.0):
    x, y   = player.xcor(), player.ycor()
    step   = PLAYER_SPEED * speed_mult
    nx, ny = x, y
    if keys["Up"]:    ny += step
    if keys["Down"]:  ny -= step
    if keys["Left"]:  nx -= step
    if keys["Right"]: nx += step
    nx = clamp(nx, -WALL, WALL)
    ny = clamp(ny, -WALL, WALL)
    bx = any(o.blocks(nx, y)  for o in obstacles)
    by = any(o.blocks(x,  ny) for o in obstacles)
    player.goto(x if bx else nx, y if by else ny)
 
def move_hunter_sprite(spr, speed):
    hx, hy = spr.xcor(), spr.ycor()
    px, py = player.xcor(), player.ycor()
    angle  = math.atan2(py - hy, px - hx)
    nx = hx + speed * math.cos(angle)
    ny = hy + speed * math.sin(angle)
    if any(o.blocks(nx, ny) for o in obstacles):
        if not any(o.blocks(nx, hy) for o in obstacles):
            ny = hy
        elif not any(o.blocks(hx, ny) for o in obstacles):
            nx = hx
        else:
            perp = angle + math.pi / 2
            nx = hx + speed * math.cos(perp)
            ny = hy + speed * math.sin(perp)
    spr.goto(clamp(nx, -WALL, WALL), clamp(ny, -WALL, WALL))
    spr.setheading(math.degrees(angle))
 
# ── Token effect applicator ────────────────────────────────────────────────────
def apply_token(key, state):
    label = next(t[1] for t in TOKENS if t[0] == key)
    col   = next(t[2] for t in TOKENS if t[0] == key)
    msg   = next(t[3] for t in TOKENS if t[0] == key)
    show_effect(msg, col)
 
    if key == "freeze_hunter":
        state["frozen_hunter"] = DUR_FREEZE
    elif key == "freeze_player":
        state["frozen_player"] = DUR_FREEZE
    elif key == "boost_player":
        state["boost_player"]  = DUR_SPEED_BOOST
    elif key == "slow_player":
        state["slow_player"]   = DUR_SLOW
    elif key == "boost_hunter":
        state["boost_hunter"]  = DUR_SPEED_BOOST
    elif key == "slow_hunter":
        state["slow_hunter"]   = DUR_SLOW
    elif key == "teleport_player":
        x, y = safe_pos(0)
        player.goto(x, y)
    elif key == "swap_teleport":
        px, py = player.xcor(), player.ycor()
        hx, hy = hunter.xcor(), hunter.ycor()
        player.goto(hx, hy)
        hunter.goto(px, py)
    elif key == "extra_hunter":
        if not state["bonus_active"]:
            bx, by = safe_pos(200)
            bonus_hunter.goto(bx, by)
            bonus_hunter.color(BONUS_COL)
            state["bonus_active"] = True
            state["bonus_ticks"]  = BONUS_HUNTER_DUR
 
# ── HUD ────────────────────────────────────────────────────────────────────────
def draw_hud(tick, h_speed, state, round_num, best):
    hud.clear()
    secs = tick // 60
    hud.color(TEXT_COL)
    hud.goto(-HALF + 8, HALF - 28)
    hud.write(f"ROUND {round_num}/{ROUNDS}    TIME  {secs}s",
              align="left", font=("Courier", 12, "bold"))
    hud.color(DIM_COL)
    hud.goto(HALF - 8, HALF - 28)
    hud.write(f"BEST  {best}s", align="right", font=("Courier", 12, "normal"))
    hud.color(HUNTER_COL)
    hud.goto(-HALF + 8, -HALF + 12)
    hud.write(f"HUNTER  {h_speed:.2f}", align="left", font=("Courier", 10, "normal"))
 
    # Active effect pills
    pill_x = -HALF + 8
    pill_y = HALF - 52
    active_effects = []
    if state["frozen_hunter"] > 0:
        active_effects.append((f"❄H {state['frozen_hunter']//60+1}s", FREEZE_COL))
    if state["frozen_player"] > 0:
        active_effects.append((f"❄P {state['frozen_player']//60+1}s", SLOW_COL))
    if state["boost_player"]  > 0:
        active_effects.append((f"⚡P {state['boost_player']//60+1}s",  BOOST_COL))
    if state["slow_player"]   > 0:
        active_effects.append((f"🐢P {state['slow_player']//60+1}s",   SLOW_COL))
    if state["boost_hunter"]  > 0:
        active_effects.append((f"⚡H {state['boost_hunter']//60+1}s",  DANGER_COL))
    if state["slow_hunter"]   > 0:
        active_effects.append((f"🐢H {state['slow_hunter']//60+1}s",   SAFE_COL))
    if state["bonus_active"]:
        active_effects.append((f"☠ {state['bonus_ticks']//60+1}s",    BONUS_COL))
    for label, col in active_effects:
        hud.color(col)
        hud.goto(pill_x, pill_y)
        hud.write(label, align="left", font=("Courier", 10, "bold"))
        pill_x += 110
        if pill_x > HALF - 60:
            pill_x  = -HALF + 8
            pill_y -= 18
 
def draw_danger_bar(d):
    bar.clear()
    ratio = clamp(1 - d / 300, 0, 1)
    bw    = int(ratio * (HALF * 2 - 20))
    bx    = -HALF + 10
    by    = -HALF + 4
    bar.pensize(6)
    bar.color(DIM_COL); bar.goto(bx, by); bar.pendown(); bar.forward(HALF*2-20); bar.penup()
    col = SAFE_COL if ratio < 0.5 else (TOKEN_COL if ratio < 0.75 else DANGER_COL)
    bar.color(col);    bar.goto(bx, by); bar.pendown(); bar.forward(bw);         bar.penup()
 
# ── Round runner ───────────────────────────────────────────────────────────────
def run_round(round_num, best):
    # Reset sprites
    player.goto(0, -150); player.color(PLAYER_COL)
    hunter.goto(0,  150); hunter.color(HUNTER_COL)
    bonus_hunter.goto(9999, 9999)
    token_sprite.goto(9999, 9999)
    for o in obstacles:
        o.hide()
 
    # Per-round mutable state
    state = {
        "frozen_hunter": 0,
        "frozen_player": 0,
        "boost_player":  0,
        "slow_player":   0,
        "boost_hunter":  0,
        "slow_hunter":   0,
        "bonus_active":  False,
        "bonus_ticks":   0,
    }
 
    tick          = 0
    token_timer   = POWERUP_INT
    obs_timer     = OBS_SPAWN_GAP
    caught        = False
 
    flash_message(f"ROUND {round_num}", TEXT_COL, duration=0.6, size=24)
    flash_message("SURVIVE!", PLAYER_COL, duration=0.5, size=28)
 
    while not caught:
        t0 = time.time()
 
        # ── Pause check ───────────────────────────────────────────────────
        if paused[0]:
            sc.update()
            time.sleep(0.05)
            continue
 
        sc.update()
        tick += 1
 
        h_speed = BASE_HUNTER + tick * SPEED_RAMP
 
        # ── Tick down all effect counters ─────────────────────────────────
        for key in ("frozen_hunter","frozen_player","boost_player",
                    "slow_player","boost_hunter","slow_hunter"):
            if state[key] > 0:
                state[key] -= 1
 
        # Bonus hunter countdown
        if state["bonus_active"]:
            state["bonus_ticks"] -= 1
            if state["bonus_ticks"] <= 0:
                state["bonus_active"] = False
                bonus_hunter.goto(9999, 9999)
 
        # ── Hunter colours reflect status ─────────────────────────────────
        if state["frozen_hunter"] > 0:
            hunter.color(FREEZE_COL)
        elif state["slow_hunter"] > 0:
            hunter.color(SLOW_COL)
        elif state["boost_hunter"] > 0:
            hunter.color("#FF0000")
        else:
            hunter.color(HUNTER_COL)
 
        # Player colour reflects status
        if state["frozen_player"] > 0:
            player.color(FREEZE_COL)
        elif state["slow_player"] > 0:
            player.color(SLOW_COL)
        elif state["boost_player"] > 0:
            player.color(BOOST_COL)
        else:
            player.color(PLAYER_COL)
 
        # ── Token spawn ───────────────────────────────────────────────────
        token_timer -= 1
        if token_timer <= 0:
            x, y = safe_pos(60)
            # Pick random token and colour the sprite accordingly
            chosen_token = random.choice(TOKENS)
            token_sprite.color(chosen_token[2])
            token_sprite.goto(x, y)
            token_timer = POWERUP_INT + random.randint(-80, 80)
 
        # Player collects token
        if dist(player, token_sprite) < 20:
            chosen_key = next(
                t[0] for t in TOKENS if t[2] == token_sprite.pencolor()
                or True  # colour matching unreliable — just pick by stored var
            )
            apply_token(chosen_token[0], state)
            token_sprite.goto(9999, 9999)
 
        # ── Obstacle lifecycle ─────────────────────────────────────────────
        obs_timer -= 1
        for o in obstacles:
            o.tick()
        if obs_timer <= 0:
            free = [o for o in obstacles if not o.active]
            if free:
                x, y = safe_pos(100)
                free[0].spawn(x, y)
            obs_timer = OBS_SPAWN_GAP + random.randint(-40, 40)
 
        # ── Move player ───────────────────────────────────────────────────
        if state["frozen_player"] > 0:
            pass   # can't move
        elif state["boost_player"] > 0:
            move_player(speed_mult=2.0)
        elif state["slow_player"] > 0:
            move_player(speed_mult=0.4)
        else:
            move_player(speed_mult=1.0)
 
        # ── Move hunters ──────────────────────────────────────────────────
        if state["frozen_hunter"] == 0:
            eff = h_speed
            if state["boost_hunter"] > 0:
                eff *= 2.0
            elif state["slow_hunter"] > 0:
                eff *= 0.35
            move_hunter_sprite(hunter, eff)
 
        if state["bonus_active"]:
            move_hunter_sprite(bonus_hunter, h_speed * 0.85)
 
        # ── Caught check ──────────────────────────────────────────────────
        if dist(player, hunter) < 22:
            caught = True
        if state["bonus_active"] and dist(player, bonus_hunter) < 20:
            caught = True
 
        draw_hud(tick, h_speed, state, round_num, best)
        draw_danger_bar(dist(player, hunter))
        effect.clear() if tick % 120 == 0 else None
 
        elapsed = time.time() - t0
        if elapsed < TICK_SLEEP:
            time.sleep(TICK_SLEEP - elapsed)
 
    return tick // 60
 
# ── Match ──────────────────────────────────────────────────────────────────────
scores = []
best   = 0
 
for rnd in range(1, ROUNDS + 1):
    survived = run_round(rnd, best)
    scores.append(survived)
    if survived > best:
        best = survived
    flash_message("CAUGHT!", DANGER_COL, duration=0.8, size=32)
    flash_message(f"Survived  {survived}s", TEXT_COL, duration=1.0, size=20)
    if survived == best and rnd > 1:
        flash_message("NEW BEST!", TOKEN_COL, duration=0.9, size=22)
 
# ── End screen ─────────────────────────────────────────────────────────────────
hud.clear(); bar.clear(); flash.clear(); effect.clear()
total = sum(scores)
hud.color(TEXT_COL)
hud.goto(0, 90)
hud.write("GAME OVER", align="center", font=("Courier", 32, "bold"))
hud.color(PLAYER_COL)
hud.goto(0, 40)
hud.write(f"Best round: {best}s    Total: {total}s",
          align="center", font=("Courier", 16, "normal"))
hud.color(DIM_COL)
for i, s in enumerate(scores):
    hud.goto(0, 0 - i * 26)
    hud.write(f"Round {i+1}:  {s}s", align="center", font=("Courier", 13, "normal"))
hud.goto(0, -20 - ROUNDS * 26)
hud.write("close window to exit", align="center", font=("Courier", 9, "normal"))
sc.update()
 
print(f"\nMatch complete! Round times: {scores}")
print(f"Best: {best}s  |  Total: {total}s")
turtle.done()