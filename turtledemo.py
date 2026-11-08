import random
import time
import turtle
import tkinter.font


school = "ECSU"
subject = "Computer Science"
colors = ("#862633", "dark blue")

screen = turtle.Screen()
screen.title("ECSU Computer Science")
screen.setup(width=0.96, height=0.86)
screen.bgcolor("white")

canvas = screen.getcanvas()
school_font = tkinter.font.Font(
    root=canvas, family="Arial Black", size=100, weight="bold"
)
subject_font = tkinter.font.Font(
    root=canvas, family="Courier New", size=100, weight="bold"
)


def fit_font_width(font, text, target_width, separate_characters=False):
    def measure_width():
        if separate_characters:
            return sum(font.measure(character) for character in text)
        return font.measure(text)

    low, high = 1, max(2, int(target_width * 2))
    while low < high:
        size = (low + high + 1) // 2
        font.configure(size=size)
        if measure_width() <= target_width:
            low = size
        else:
            high = size - 1
    font.configure(size=low)
    return low, measure_width(), font.metrics("linespace")


target_width = screen.window_width() * 0.94
available_height = screen.window_height() * 0.80


def measure_layout(width):
    school_size, school_width, school_height = fit_font_width(
        school_font, school, width, separate_characters=True
    )
    subject_size, subject_width, subject_height = fit_font_width(
        subject_font, subject, width
    )
    line_gap = max(8, max(school_height, subject_height) * 0.06)
    total_height = school_height + line_gap + subject_height
    return (
        school_size,
        school_width,
        school_height,
        subject_size,
        subject_width,
        subject_height,
        line_gap,
        total_height,
    )


layout = measure_layout(target_width)
while layout[-1] > available_height:
    target_width *= 0.9
    layout = measure_layout(target_width)

(
    school_size,
    school_width,
    school_height,
    subject_size,
    subject_width,
    subject_height,
    line_gap,
    total_height,
) = layout

pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.speed("fastest")
pen_y_subject = -total_height / 2
pen_y_school = pen_y_subject + subject_height + line_gap

pen.goto(-school_width / 2, pen_y_school)
for index, letter in enumerate(school):
    pen.color(colors[index % len(colors)])
    letter_width = school_font.measure(letter)
    pen.forward(letter_width / 2)
    pen.write(letter, align="center", font=("Arial Black", school_size, "bold"))
    pen.forward(letter_width / 2)

pen.color("#010101")
pen.goto(0, pen_y_subject)
pen.write(
    subject,
    align="center",
    font=("Courier New", subject_size, "bold"),
)

canvas_width = screen.window_width()
canvas_height = screen.window_height()
rain_step_size = 18
rain_stream_spacing = 20
rain_interval = 16
rain_palette = ("#00ff41", "#00cc33", "#008f11", "#005f0a")
rain_characters = "0123456789ABCDEF"

screen.tracer(0, 0)


def stream_positions(width):
    positions = list(range(-width, width, rain_stream_spacing))
    if not positions:
        positions = [0]
    if positions[-1] != width - 1:
        positions.append(width - 1)
    return positions


def create_stream(x, height):
    trail_length = 8
    stream_speed = random.uniform(28, 82)
    stream_size = random.randint(10, 18)
    items = []
    for age in range(trail_length):
        y = random.randint(-height, 0) - age * rain_step_size
        depth_size = max(8, stream_size + (trail_length - age) // 2)
        item = canvas.create_text(
            x,
            y,
            text=random.choice(rain_characters),
            fill=rain_palette[min(age // 2, len(rain_palette) - 1)],
            font=("Courier New", depth_size, "bold"),
            tags=("rain",),
        )
        items.append(item)
    return {
        "x": x,
        "y": random.randint(-height, 0),
        "speed": stream_speed,
        "size": stream_size,
        "items": items,
    }


streams = [create_stream(x, canvas_height) for x in stream_positions(canvas_width)]
last_frame_time = time.monotonic()


def animate_rain():
    global last_frame_time

    now = time.monotonic()
    dt = min(max(now - last_frame_time, 0.016), 0.05)
    last_frame_time = now

    current_width = canvas.winfo_width()
    current_height = canvas.winfo_height()
    if current_width <= 1:
        current_width = screen.window_width()
    if current_height <= 1:
        current_height = screen.window_height()
    current_width = max(1, current_width)
    current_height = max(1, current_height)
    positions = stream_positions(current_width)

    while len(streams) > len(positions):
        for item in streams.pop()["items"]:
            canvas.delete(item)
    while len(streams) < len(positions):
        streams.append(create_stream(positions[len(streams)], current_height))

    for index, stream in enumerate(streams):
        stream["x"] = positions[index]
        stream["y"] += stream["speed"] * dt

        for age, trail_item in enumerate(stream["items"]):
            trail_y = stream["y"] - age * rain_step_size
            font_size = max(8, stream["size"] + (len(stream["items"]) - age) // 2)
            canvas.coords(trail_item, stream["x"], trail_y)
            if age == 0 or random.random() < 0.5:
                canvas.itemconfigure(
                    trail_item,
                    text=random.choice(rain_characters),
                )
            canvas.itemconfigure(
                trail_item,
                fill=rain_palette[min(age // 2, len(rain_palette) - 1)],
                font=("Courier New", font_size, "bold"),
            )

        if stream["y"] - 8 * rain_step_size > current_height:
            stream["y"] = random.randint(-current_height, -rain_step_size)
            for age, trail_item in enumerate(stream["items"]):
                font_size = max(8, stream["size"] + (len(stream["items"]) - age) // 2)
                canvas.coords(trail_item, stream["x"], stream["y"] - age * rain_step_size)
                canvas.itemconfigure(
                    trail_item,
                    text=random.choice(rain_characters),
                    fill=rain_palette[min(age // 2, len(rain_palette) - 1)],
                    font=("Courier New", font_size, "bold"),
                )

    canvas.tag_lower("rain")
    screen.update()
    screen.ontimer(animate_rain, rain_interval)


animate_rain()
screen.mainloop()