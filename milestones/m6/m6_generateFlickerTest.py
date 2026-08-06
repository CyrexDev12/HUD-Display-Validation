# Milestone 4 - Realistic BFD Rendering Fault Test

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
# Fault Injection
# -------------------

FAULT_TYPES = [
    "bearing1_arrow",
    "bearing2_arrow",
    "bearing1_half",
    "bearing2_half",
    "cardinal",
    "degree_label",
    "green_nav",
    "cyan_nav"
]

current_fault = None
fault_parameter = None
fault_frames_remaining = 0

frames_until_next_fault = random.randint(180, 480)

# -------------------
# Window Setup
# -------------------

root = tk.Tk()
root.title("BFD Realistic Flicker Test")

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


def update_fault_injection():

    global current_fault
    global fault_parameter
    global fault_frames_remaining
    global frames_until_next_fault

    if current_fault is not None:

        fault_frames_remaining -= 1

        if fault_frames_remaining <= 0:

            current_fault = None
            fault_parameter = None
            frames_until_next_fault = random.randint(180, 480)

        return

    frames_until_next_fault -= 1

    if frames_until_next_fault <= 0:

        current_fault = random.choice(FAULT_TYPES)

        if current_fault == "cardinal":

            fault_parameter = random.choice(
                ["N", "E", "S", "W"]
            )

        elif current_fault == "degree_label":

            fault_parameter = random.choice(
                list(range(0, 360, 30))
            )

        elif current_fault in (
            "bearing1_arrow",
            "bearing2_arrow"
        ):

            fault_parameter = random.choice(
                ["head1", "head2"]
            )

        elif current_fault in (
            "bearing1_half",
            "bearing2_half"
        ):

            fault_parameter = random.choice(
                ["first", "second"]
            )

        fault_frames_remaining = random.randint(1, 5)


def draw():

    global angle

    update_fault_injection()

    canvas.delete("all")

    # -------------------
    # Compass Ring
    # -------------------

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

    labels = [
        ("N", -90),
        ("E", 0),
        ("S", 90),
        ("W", 180)
    ]

    for text, base_angle in labels:

        if (
            current_fault == "cardinal"
            and text == fault_parameter
        ):
            continue

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

    for deg in range(0, 360, 30):

        if (
            current_fault == "degree_label"
            and deg == fault_parameter
        ):
            continue

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

    bearing1 = angle + 20

    x1, y1 = polar_to_xy(
        280,
        bearing1
    )

    x2, y2 = polar_to_xy(
        280,
        bearing1 + 180
    )

    if (
        current_fault == "bearing1_half"
        and fault_parameter == "first"
    ):

        canvas.create_line(
            CENTER_X,
            CENTER_Y,
            x2,
            y2,
            fill="white",
            width=4
        )

    elif (
        current_fault == "bearing1_half"
        and fault_parameter == "second"
    ):

        canvas.create_line(
            CENTER_X,
            CENTER_Y,
            x1,
            y1,
            fill="white",
            width=4
        )

    else:

        canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill="white",
            width=4
        )

    if not (
        current_fault == "bearing1_arrow"
        and fault_parameter == "head1"
    ):
        draw_arrow(
            x1,
            y1,
            bearing1,
            "white"
        )

    if not (
        current_fault == "bearing1_arrow"
        and fault_parameter == "head2"
    ):
        draw_arrow(
            x2,
            y2,
            bearing1 + 180,
            "white"
        )

    # -------------------
    # Bearing Line 2
    # -------------------

    bearing2 = angle + 110

    x1b, y1b = polar_to_xy(
        240,
        bearing2
    )

    x2b, y2b = polar_to_xy(
        240,
        bearing2 + 180
    )

    if (
        current_fault == "bearing2_half"
        and fault_parameter == "first"
    ):

        canvas.create_line(
            CENTER_X,
            CENTER_Y,
            x2b,
            y2b,
            fill="white",
            width=3
        )

    elif (
        current_fault == "bearing2_half"
        and fault_parameter == "second"
    ):

        canvas.create_line(
            CENTER_X,
            CENTER_Y,
            x1b,
            y1b,
            fill="white",
            width=3
        )

    else:

        canvas.create_line(
            x1b,
            y1b,
            x2b,
            y2b,
            fill="white",
            width=3
        )

    if not (
        current_fault == "bearing2_arrow"
        and fault_parameter == "head1"
    ):
        draw_arrow(
            x1b,
            y1b,
            bearing2,
            "white"
        )

    if not (
        current_fault == "bearing2_arrow"
        and fault_parameter == "head2"
    ):
        draw_arrow(
            x2b,
            y2b,
            bearing2 + 180,
            "white"
        )

    # -------------------
    # Green Nav Symbol
    # -------------------

    if current_fault != "green_nav":

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

    if current_fault != "cyan_nav":

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
    # Fixed Aircraft Symbol
    # -------------------

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

    # angle += ROTATION_SPEED   # CCW
    # angle -= ROTATION_SPEED   # CW

    root.after(16, draw)


draw()

root.mainloop()