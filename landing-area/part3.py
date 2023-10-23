import math
import time
import terminalio
import displayio
import busio    
import board
from adafruit_display_text import label
import adafruit_displayio_ssd1306
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.line import Line

# init displays
displayio.release_displays()

# init i2c
sda_pin = board.GP14
scl_pin = board.GP15
i2c = busio.I2C(scl_pin, sda_pin)

# init display part 2
display_bus = displayio.I2CDisplay(i2c, device_address=0x3d, reset=board.GP21)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# create the display group
splash = displayio.Group()

# add base and coordinate axes
splash.append(Circle(64, 32, 3, outline=0xFFFFFF))
splash.append(Line(0, 32, 128, 32, 0xFFFFFF))
splash.append(Line(64, 0, 64, 64, 0xFFFFFF))
area_label = label.Label(terminalio.FONT, x=5, y=5, text="")
# splash.append(Triangle(5, 5, 30, 30, 10, 30, outline=0xFFFFFF))
splash.append(area_label)
landing_area_display = None

# send display group to screen
display.show(splash)

def validate_input(input_string: str): # return false on error or an array of the form [x, y] on success
    try:
        input_parts = input_string.split(",")
    except ValueError:
        return False
    if len(input_parts) != 2: # we expect an x and a y coordinate
        return False
    try:
        result = [float(part) for part in input_parts] # turn the strings in input_parts into floats
        return result
    except ValueError: # if something wasn't a float
        return False

def get_area(p1, p2, p3): # adapted from https://stackoverflow.com/questions/59597399
    area = 0.5 * (p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0]
                  * (p1[1] - p2[1]))
    return abs(area)

def do_triangle(vertex_1, vertex_2, vertex_3):
    global landing_area_display
    area = get_area(vertex_1, vertex_2, vertex_3)
    print(f"The area of the triangle with vertices ({vertex_1[0]},{vertex_1[1]}), ({vertex_2[0]},{vertex_2[1]}), ({vertex_3[0]},{vertex_3[1]}) is {area} square km.")
    area_label.text = f"{area:.2f}km2" # set the text that shows on the display
    if landing_area_display is not None: # if we already have a triangle, get rid of it
        splash.pop()
    landing_area_display = Triangle(int(vertex_1[0])+64, 32-int(vertex_1[1]), int(vertex_2[0])+64, 32-int(vertex_2[1]), int(vertex_3[0])+64, 32-int(vertex_3[1]), outline=0xFFFFFF)
    splash.append(landing_area_display) # show this triangle
    return area

def get_centroid(vertex_1, vertex_2, vertex_3):
    # the centroid is just the average of the points
    return [(vertex_1[0]+vertex_2[0]+vertex_3[0])/3, (vertex_1[1]+vertex_2[1]+vertex_3[1])/3]

input_triangles = [['-2,-30','-19,-8','-44,-18'],['7,-14','60,-7','33,-6'],['5,5','-8,9','0,-6'],['63,30','60,19','29,16']]
triangle_distances = {}
closest_distance = float('inf')

for i, input_triangle in enumerate(input_triangles):
    vertexes = []
    for j, point_str in enumerate(input_triangle):
        vertexes.append(validate_input(point_str))
        if not vertexes[j]:
            raise ValueError("Error in input! Check that everything is set up properly.")
    triangle_area = do_triangle(*vertexes)
    triangle_centroid = get_centroid(*vertexes)
    triangle_distance = math.sqrt(triangle_centroid[0]**2 + triangle_centroid[1]**2)
    triangle_distances[triangle_distance] = vertexes
    # Only set a new closest triangle if it's big enough
    if triangle_area > 100 and closest_distance > triangle_distance:
        closest_distance = triangle_distance
    time.sleep(1)
best_triangle = triangle_distances[closest_distance]
do_triangle(*best_triangle)

print(f"The closest landing area larger than 100 km2 has vertices ({best_triangle[0][0]}, {best_triangle[0][1]}), ({best_triangle[1][0]}, {best_triangle[1][1]}), ({best_triangle[2][0]}, {best_triangle[2][1]}). The area is {get_area(*best_triangle)} km2 and the centroid is {closest_distance} km away from base.")
while True:
    pass # block forever to keep display showing triangle