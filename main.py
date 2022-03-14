import random
import numpy as np
import matplotlib.pyplot as plt
from manim import *

class Bezier(Scene):
    def construct(self):
        # Load data points from an external file into a file variable
        file = open('econData.txt', 'r')
        # Load all lines from 'file' into a variable called lines
        lines = file.readlines()

        # A function that generates random integer in the range between 0 and 25
        # this is used to chose one of the data points from every month of data,
        # where each month contains approximately 25 data points.
        def generateRandomNumber():
            return random.randrange(0, 25)

        # A function to parse data from the lines variable into an array
        def loadData(lines):
            # An array for the parsed data
            data = []
            # A helper array used to append arrays into the 'data' array
            arr = []
            # An array used to store a pair of data (a stock value and date)
            pair = []
            # A variable to itterate over the loaded lines
            i = 0
            # A string to store a number that is currently being parsed
            number = ""

            # Iterate through all of the loaded lines up untill the end of the lines,
            # if the end is reached store the loaded data into the 'data' array.
            # Otherwise keep on loading characters into the number string, until a
            # 'tab' character is reached. If a 'tab' character was reached it means
            # that the stock value was loaded and the next character until the end of
            # the line will be the chracter of the coresponding date.
            for line in lines:
                if i < 31:
                    for char in line:
                        if char == '\t':
                            pair.append(number)
                            number = ""
                        elif char != '\n':
                            number += char
                    pair.append(float(number))
                    arr.append(pair)
                    pair = []
                    number = ""
                    i += 1
                else:
                    data.append(arr)
                    arr = []
                    i = 0
            
            return data

        # A function to randomly choose a data point from each month of data
        def getData( data ):
            values = []
            for i in range(0, len(data)):
                values.append(data[i][generateRandomNumber()])
            return values

        # A function to parse a date of the format of dd/mm/yyyy into a sing number
        # representing the number of days passed since 1/26/2021
        def dateToCoordinates( date ):
            date_values = date.split("/")
            coordinate = (int(date_values[0]) - 1) * 30
            coordinate += (int(date_values[1]))
            if int(date_values[2]) == 2022:
                coordinate += 330
            return float(coordinate)

        # The BÉZIER INTERPOLATION ALGORITHM
        def bezierPoints(points, n):
            # Create a matrix for the system of 9 equations
            # Insert in the matrix the first line corresponding to the first equation
            # (2a0 + a1 = ...)
            M = np.zeros( (n) )
            M[0] = 2
            M[1] = 1
            # Fill in the coefficients of the next 7 intermediate equations 
            # (ai + 4ai+1 + ai+2 = ..., i=0,...,6)
            # Fill a diagonal with the number 4
            arr = np.zeros( (n-2, n))
            np.fill_diagonal(arr[:, 1:], 4)
            # Fill two other diagonals with the number 1
            np.fill_diagonal(arr[:, 2:], 1)
            np.fill_diagonal(arr[:, 0:], 1)
            # Add the coefficients to the matrix of coefficients M
            M = np.vstack([M, arr])
            # Fill in the coefficients of the last equation
            # (7a8 + 2a7 = ...)
            arr = np.zeros( (n) )
            arr[n-2] = 2
            arr[n-1] = 7
            arr[n-3] = 0
            # Also append it into the matrix M
            M = np.vstack([M, arr])

            # Create a vector from the 10 given points P0 through P9
            # Fill the points from the first equation
            # (... = V0 + 2V1)
            P = np.array(points[0] + 2*points[1])
            # Fill in the points from the intermediate 7 equations
            # (... = 4Vi+1 + 2Vi+2, i=0,...,6)
            P = np.vstack([P, [4*points[i+1] + 2*points[i+2] for i in range(n-2)]])
            # Fill in the points from the last equation
            # (... = 8V8 +V9)
            P = np.vstack([P, [8*points[n-1] + points[n]]])
            
            # Solve the system of 9 equations:
            #               2a0 + a1 = V0 + 2V1
            #       ai +4ai+1 + ai+2 = 4Vi+1 + 2Vi+2, i = 0, ..., 6
            #              7a8 + 2a7 = 8V8 + V9
            # Described using matrix notation as:
            #       [2 1 0 0 0 0 0 0 0] [a0]        [V0 + 2V1]
            #       [1 4 1 0 0 0 0 0 0] [a1]        [4V1 + 2V2]
            #       [0 1 4 1 0 0 0 0 0] [a2]        [4V2 + 2V3]
            #       [0 0 1 4 1 0 0 0 0] [a3]        [4V3 + 2V4]
            #       [0 0 0 1 4 1 0 0 0] [a4]    =   [4V4 + 2V5]
            #       [0 0 0 0 1 4 1 0 0] [a5]        [4V5 + 2V6]
            #       [0 0 0 0 0 1 4 1 0] [a6]        [4V6 + 2V7]
            #       [0 0 0 0 0 0 1 4 1] [a7]        [4V7 + 2V8]
            #       [0 0 0 0 0 0 0 2 7] [a8]        [8V8 + V9]
            # Using a built-in function of the 'numpy' library to solve
            # this system of equations for a0 through a8 and storing
            # these values into an array 'a' 
            a = np.linalg.solve(M, P)
            # Calculating values of b based on the solved values of a, as
            # described by
            #       bi = 2Vi+1 − ai+1, i=0,...,7
            #       b8 = (V9 + a8)/2
            b = np.array([2*points[i+1] - a[i+1] for i in range(n-1)])
            b = np.vstack([b, [(a[n-1]+points[n])/2]])

            return a, b

        # Load all data
        data = loadData(lines)
        # Chose 1 data point from each month worth of data  
        values = getData(data)

        # Parse date format into number of days after 1/26/2021
        for items in values:
            items[0] = dateToCoordinates(items[0])

        # Create a numpy array from the parsed dates and stock values
        points = np.array(values)
        # Print the data
        print(points)
        
        # Separate the loaded data points into their x and y coordinates
        x, y = points[:, 0], points[:, 1]


        # CONFIGURE THE GRAPHICS OF THE FIGURE PRODUCED
        # Cet the background color
        self.camera.background_color = WHITE
        # Configure axes
        axes = Axes(
            x_range=[0, 350, 50],
            y_range=[min(y)-0.01, max(y)+0.01, 0.01],
            x_length=9,
            y_length=6,
            axis_config={
                "color": GREEN,
                "font_size": 24},
            x_axis_config={
                "numbers_to_include": np.arange(0, 350, 50),
                "numbers_with_elongated_ticks": np.arange(0, 350, 50),
                "decimal_number_config": {"num_decimal_places":0, "color": BLACK},
                "label_direction": DOWN,
            },
            y_axis_config={
                "numbers_to_include": np.arange(min(y)-0.01, max(y)+0.01, 0.01),
                "decimal_number_config": {"color": BLACK},
                "label_direction":LEFT,
            },
        )

        # Add labels to axes
        x_label = Text(
            "Days  after  1/26/2021", font_size=20, color=BLACK
        ).move_to(axes)
        y_label = Text(
            "Stock  value  (USD)", font_size=20, color=BLACK
        ).move_to(axes)
        y_label.rotate(PI/2)
        y_label.shift(LEFT*5.2).shift(UP/2)
        x_label.shift(DOWN*3)

        # Graph the 10 initial data points P0 through P9
        for i in range(len(points)):
            dot = Dot(
                axes.coords_to_point(x[i], y[i]), color=BLACK, radius=0.06
            ).shift(UP/2)
            self.add(dot)

        # Obtain the contorl points a and b for the 9 bézier curve of the
        # bézier interpolation
        a, b = bezierPoints(points, len(points)-1)
        # Extract the x and y coordinates of the control points a and b
        ax, ay = a[:, 0], a[:, 1]
        bx, by = b[:, 0], b[:, 1]

        # Use the calculated control points together with the initial given
        # points to plot the 9 bézier curve of the bézier interpolation
        bezierCurves = VGroup()
        for i in range(len(points)-1):
            vertices = [
                axes.coords_to_point(x[i], y[i], 0),
                axes.coords_to_point(ax[i], ay[i], 0),
                axes.coords_to_point(bx[i], by[i], 0),
                axes.coords_to_point(x[i+1], y[i+1], 0)
            ]
            curve = CubicBezier(
                vertices[0], vertices[1], vertices[2], vertices[3]
            ).set_color(BLUE)
            bezierCurves.add(curve)
        
        # Display all of the graphics
        plotC = VGroup(axes, bezierCurves).shift(UP/2)
        labels = VGroup(x_label, y_label)
        self.add(plotC, labels)

