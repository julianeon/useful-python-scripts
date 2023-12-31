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
    ("https://ronaldsvilcins.com/2020/12/10/programming-quotes/", "white", "blue"),
    ("There are only two kinds of programming languages: \nthose people always complain about \nand those nobody uses.\n- Bjarne Stroustrup", "black", "white"),
    ("If you optimize everything, you will always be unhappy.\n- Donald Knuth", "black", "white"),
    ("Measuring programming progress by lines of code \nis like measuring aircraft building progress by weight.\n-Bill Gates", "black", "white"),
    ("If you've chosen the right data structures \nand organized things well, \nthe algorithms will almost always be self-evident.\n- Rob Pike", "black", "orange"),
    ("Talk is cheap. Show me the code.\n- Linus Torvalds", "black", "yellow"),
)

for i, (string, color_b, color_t) in enumerate(tarr):
    fname = f"poly_{i}.png"
    make_image(string, fname, color_b, color_t)

subprocess.run(["convert", "-delay", "300", "poly_*", "output.gif"])

print("GIF created successfully as output.gif.")
