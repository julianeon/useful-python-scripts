import subprocess

def make_image(text, output_filename, cbackground, cforeground):
    # Set the background color, text color, and font
    background = cbackground
    text_color = cforeground
    font = "Helvetica"
    font_size = 48

    # Create a command to generate the image in-memory
    convert_command = [
        "convert",
        "-size", "1600x900",
        "-background", background,
        "-fill", text_color,
        "-font", font,
        "-pointsize", str(font_size),
        "-gravity", "center",
        f"label:{text}",
        output_filename
    ]

    # Execute the command to generate the image directly
    subprocess.run(convert_command)

    print(f"Image created successfully as {output_filename}.")

tarr = (
    ("Rob Pike's 5 Rules of Programming", "white", "blue"),
    ("You can't tell \nwhere a program is going to spend its time.", "black", "white"),
    ("Measure. \nDon't tune for speed until you've measured.", "black", "yellow"),
    ("Fancy algorithms are slow \nwhen n is small - and n is usually small.", "black", "white"),
    ("Fancy algorithms are buggier than simple ones.", "black", "white"),
    ("Data dominates. \nIf you've chosen the right data structures, \nand organized things well, \nthe algorithms will almost always be self-evident.", "black", "orange"),
)

for i, (string, color_b, color_t) in enumerate(tarr):
    fname = f"poly_{i}.png"
    make_image(string, fname, color_b, color_t)


