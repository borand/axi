import axi

d = axi.Device()
d.pen_up_position = 65
d.pen_down_position = 20
d.configure()
d.zero_position()

container = [18, 10]
spacing = 4.5
num_of_cakes = 4.0
rows = 2
columns = int(num_of_cakes / 2)
offset = [container[0] / columns / 2.0, container[1] / rows / 2.0]


for row in range(rows):
    for col in range(columns):
        x = 16 - (col * container[0] / columns + offset[0]) / 2.54
        y = row * (container[1] / rows + offset[1]) / 2.54
        print(f"{row}, {col} = [{x}, {y}]")
        #
        d.goto(0,2)
        d.pen_up()
        d.goto(0,0)
        d.goto(x, y)
        d.pen_down()
        d.goto(0,0)