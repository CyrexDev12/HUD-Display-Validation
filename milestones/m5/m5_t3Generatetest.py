# Milestone 5 - Generate Randomized missing element test 
import tkinter as tk
import math
import random

# -------------------
# Display Settings
# -------------------

WIDTH = 900
HEIGHT = 900

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

RADIUS = 350

ROTATION_SPEED = 1.0

angle = 0

# -------------------
# Failure Injection
# -------------------

FAILURE_MODE = random.choice([
    "NONE",
    "MINOR",
    "MAJOR"
])

elements = [
    "COMPASS_RING",
    "TICK_MARKS",
    "CARDINALS",
    "DEGREE_LABELS",
    "BEARING1",
    "BEARING2",
    "GREEN_NAV",
    "CYAN_NAV",
    "AIRCRAFT"
]

if FAILURE_MODE == "MINOR":
    failed = random.sample(elements, 2)

elif FAILURE_MODE == "MAJOR":
    failed = random.sample(elements, 5)

else:
    failed = []

SHOW_COMPASS_RING = "COMPASS_RING" not in failed
SHOW_TICK_MARKS = "TICK_MARKS" not in failed
SHOW_CARDINALS = "CARDINALS" not in failed
SHOW_DEGREE_LABELS = "DEGREE_LABELS" not in failed
SHOW_BEARING_LINE_1 = "BEARING1" not in failed
SHOW_BEARING_LINE_2 = "BEARING2" not in failed
SHOW_GREEN_NAV = "GREEN_NAV" not in failed
SHOW_CYAN_NAV = "CYAN_NAV" not in failed
SHOW_AIRCRAFT_SYMBOL = "AIRCRAFT" not in failed

print("\n===== FAILURE CONFIGURATION =====")
print(f"Mode: {FAILURE_MODE}")
print(f"Failed Elements: {failed}")
print("=================================\n")

# -------------------
# Window Setup
# -------------------

root = tk.Tk()
root.title("BFD Randomized Failure Test")

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="black",
    highlightthickness=0
)

canvas.pack()


def polar_to_xy(radius, degrees):

    rad = math.radians(degrees)

    x = CENTER_X + radius * math.cos(rad)
    y = CENTER_Y + radius * math.sin(rad)

    return x, y


def draw_arrow(x, y, angle_deg, color):

    size = 20

    a = math.radians(angle_deg)

    tip_x = x + size * math.cos(a)
    tip_y = y + size * math.sin(a)

    left_x = x + size * math.cos(a + 2.5)
    left_y = y + size * math.sin(a + 2.5)

    right_x = x + size * math.cos(a - 2.5)
    right_y = y + size * math.sin(a - 2.5)

    canvas.create_polygon(
        tip_x,
        tip_y,
        left_x,
        left_y,
        right_x,
        right_y,
        fill=color,
        outline=color
    )


def draw():

    global angle

    canvas.delete("all")

    # -------------------
    # Compass Ring
    # -------------------

    if SHOW_COMPASS_RING:

        canvas.create_oval(
            CENTER_X - RADIUS,
            CENTER_Y - RADIUS,
            CENTER_X + RADIUS,
            CENTER_Y + RADIUS,
            outline="white",
            width=2
        )

    # -------------------
    # Tick Marks
    # -------------------

    if SHOW_TICK_MARKS:

        for deg in range(0, 360, 5):

            draw_angle = deg + angle

            outer_x, outer_y = polar_to_xy(
                RADIUS,
                draw_angle
            )

            tick_len = 25 if deg % 30 == 0 else 10

            inner_x, inner_y = polar_to_xy(
                RADIUS - tick_len,
                draw_angle
            )

            canvas.create_line(
                inner_x,
                inner_y,
                outer_x,
                outer_y,
                fill="white",
                width=2
            )

    # -------------------
    # Cardinal Directions
    # -------------------

    if SHOW_CARDINALS:

        labels = [
            ("N", -90),
            ("E", 0),
            ("S", 90),
            ("W", 180)
        ]

        for text, base_angle in labels:

            x, y = polar_to_xy(
                RADIUS - 55,
                base_angle + angle
            )

            canvas.create_text(
                x,
                y,
                text=text,
                fill="white",
                font=("Arial", 28, "bold")
            )

    # -------------------
    # Degree Labels
    # -------------------

    if SHOW_DEGREE_LABELS:

        for deg in range(0, 360, 30):

            x, y = polar_to_xy(
                RADIUS - 100,
                deg + angle
            )

            canvas.create_text(
                x,
                y,
                text=str(deg),
                fill="white",
                font=("Arial", 16)
            )

    # -------------------
    # Bearing Line 1
    # -------------------

    if SHOW_BEARING_LINE_1:

        bearing1 = angle + 20

        x1, y1 = polar_to_xy(280, bearing1)
        x2, y2 = polar_to_xy(280, bearing1 + 180)

        canvas.create_line(
            x1, y1,
            x2, y2,
            fill="white",
            width=4
        )

        draw_arrow(
            x1,
            y1,
            bearing1,
            "white"
        )

        draw_arrow(
            x2,
            y2,
            bearing1 + 180,
            "white"
        )

    # -------------------
    # Bearing Line 2
    # -------------------

    if SHOW_BEARING_LINE_2:

        bearing2 = angle + 110

        x1, y1 = polar_to_xy(240, bearing2)
        x2, y2 = polar_to_xy(240, bearing2 + 180)

        canvas.create_line(
            x1, y1,
            x2, y2,
            fill="white",
            width=3
        )

        draw_arrow(
            x1,
            y1,
            bearing2,
            "white"
        )

        draw_arrow(
            x2,
            y2,
            bearing2 + 180,
            "white"
        )

    # -------------------
    # Green Nav Symbol
    # -------------------

    if SHOW_GREEN_NAV:

        nav_x, nav_y = polar_to_xy(
            RADIUS - 35,
            angle + 140
        )

        canvas.create_polygon(
            nav_x,
            nav_y - 18,
            nav_x - 18,
            nav_y + 18,
            nav_x + 18,
            nav_y + 18,
            fill="lime",
            outline="lime"
        )

    # -------------------
    # Cyan Nav Symbol
    # -------------------

    if SHOW_CYAN_NAV:

        nav_x, nav_y = polar_to_xy(
            RADIUS - 25,
            angle + 320
        )

        canvas.create_oval(
            nav_x - 8,
            nav_y - 8,
            nav_x + 8,
            nav_y + 8,
            outline="cyan",
            width=3
        )

    # -------------------
    # Aircraft Symbol
    # -------------------

    if SHOW_AIRCRAFT_SYMBOL:

        canvas.create_line(
            CENTER_X - 60,
            CENTER_Y,
            CENTER_X + 60,
            CENTER_Y,
            fill="lime",
            width=4
        )

        canvas.create_line(
            CENTER_X,
            CENTER_Y - 40,
            CENTER_X,
            CENTER_Y + 50,
            fill="lime",
            width=4
        )

        canvas.create_polygon(
            CENTER_X,
            CENTER_Y - 55,
            CENTER_X - 10,
            CENTER_Y - 35,
            CENTER_X + 10,
            CENTER_Y - 35,
            outline="lime",
            fill=""
        )

        canvas.create_oval(
            CENTER_X - 8,
            CENTER_Y - 8,
            CENTER_X + 8,
            CENTER_Y + 8,
            outline="cyan",
            width=3
        )

    # -------------------
    # Rotation Mode
    # -------------------

    angle -= ROTATION_SPEED   # CCW

    root.after(
        16,
        draw
    )


draw()

root.mainloop()