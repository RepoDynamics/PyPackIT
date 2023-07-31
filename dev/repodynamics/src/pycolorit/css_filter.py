"""CSS filter generator to convert from black to target hex color.

References
----------
* Code is re-implemented from JavaScript: https://codepen.io/sosuke/pen/Pjoqqp
"""


# Standard libraries
import math
import random


class Color:
    def __init__(self, r, g, b):
        self.set(r, g, b)

    def __str__(self):
        return f"rgb({round(self.r)}, {round(self.g)}, {round(self.b)})"

    def set(self, r, g, b):
        self.r = self.clamp(r)
        self.g = self.clamp(g)
        self.b = self.clamp(b)

    def hue_rotate(self, angle=0):
        angle = angle / 180 * math.pi
        sin = math.sin(angle)
        cos = math.cos(angle)

        self.multiply(
            [
                0.213 + cos * 0.787 - sin * 0.213,
                0.715 - cos * 0.715 - sin * 0.715,
                0.072 - cos * 0.072 + sin * 0.928,
                0.213 - cos * 0.213 + sin * 0.143,
                0.715 + cos * 0.285 + sin * 0.140,
                0.072 - cos * 0.072 - sin * 0.283,
                0.213 - cos * 0.213 - sin * 0.787,
                0.715 - cos * 0.715 + sin * 0.715,
                0.072 + cos * 0.928 + sin * 0.072,
            ]
        )

    def grayscale(self, x=1):
        self.multiply(
            [
                0.2126 + 0.7874 * (1 - x),
                0.7152 - 0.7152 * (1 - x),
                0.0722 - 0.0722 * (1 - x),
                0.2126 - 0.2126 * (1 - x),
                0.7152 + 0.2848 * (1 - x),
                0.0722 - 0.0722 * (1 - x),
                0.2126 - 0.2126 * (1 - x),
                0.7152 - 0.7152 * (1 - x),
                0.0722 + 0.9278 * (1 - x),
            ]
        )

    def sepia(self, x=1):
        self.multiply(
            [
                0.393 + 0.607 * (1 - x),
                0.769 - 0.769 * (1 - x),
                0.189 - 0.189 * (1 - x),
                0.349 - 0.349 * (1 - x),
                0.686 + 0.314 * (1 - x),
                0.168 - 0.168 * (1 - x),
                0.272 - 0.272 * (1 - x),
                0.534 - 0.534 * (1 - x),
                0.131 + 0.869 * (1 - x),
            ]
        )

    def saturate(self, x=1):
        self.multiply(
            [
                0.213 + 0.787 * x,
                0.715 - 0.715 * x,
                0.072 - 0.072 * x,
                0.213 - 0.213 * x,
                0.715 + 0.285 * x,
                0.072 - 0.072 * x,
                0.213 - 0.213 * x,
                0.715 - 0.715 * x,
                0.072 + 0.928 * x,
            ]
        )

    def brightness(self, x=1):
        """
        Adjust the brightness of the color, by applying a linear multiplier.

        Parameters
        ----------
        x : int >= 0
            Linear multiplier, with 0 creating a completely black color, 1 (i.e. 100%) having no effect,
            and values over 1 brightening the color.

        Returns
        -------

        """
        self.multiply([x, 0, 0, 0, x, 0, 0, 0, x])

    def contrast(self, x=1):
        """
        Adjust the contrast of the color.

        Parameters
        ----------
        x : int >= 0
            A value of 0 makes the color grey, 1 (i.e. 100%) has no effect, and values over 1 create a contrast.

        Returns
        -------

        """
        intercept = tuple(127.5 * (1 - x) for i in range(3))
        self.multiply([x, 0, 0, 0, x, 0, 0, 0, x], intercept)

    def clamp(self, value):
        return min(255, max(0, value))

    def multiply(self, matrix, vector=(0, 0, 0)):
        r = self.r * matrix[0] + self.g * matrix[1] + self.b * matrix[2] + vector[0]
        g = self.r * matrix[3] + self.g * matrix[4] + self.b * matrix[5] + vector[1]
        b = self.r * matrix[6] + self.g * matrix[7] + self.b * matrix[8] + vector[2]
        self.set(r, g, b)

    def invert(self, x=1):
        r = (x + self.r / 255 * (1 - 2 * x)) * 255
        g = (x + self.g / 255 * (1 - 2 * x)) * 255
        b = (x + self.b / 255 * (1 - 2 * x)) * 255
        self.set(r, g, b)
        return

    def rgb_to_hsl(self):
        r, g, b = self.r / 255, self.g / 255, self.b / 255
        max_value = max(r, g, b)
        min_value = min(r, g, b)
        h, s, l = 0, 0, (max_value + min_value) / 2
        if max_value != min_value:
            d = max_value - min_value
            s = d / (2 - max_value - min_value) if l > 0.5 else d / (max_value + min_value)
            if max_value == r:
                h = (g - b) / d + (6 if g < b else 0)
            elif max_value == g:
                h = (b - r) / d + 2
            else:
                h = (r - g) / d + 4
            h /= 6
        return h * 100, s * 100, l * 100


class Solver:
    def __init__(self, target_color: Color):
        self.target = target_color
        self.target_hsl = target_color.rgb_to_hsl()

    def solve(self):
        curr_result = {"loss": float("inf")}
        for i in range(100):
            if curr_result["loss"] < 1:
                break
            new_result = self.solve_narrow(self.solve_wide())
            if new_result["loss"] < curr_result["loss"]:
                curr_result = new_result
        return curr_result["values"], curr_result["loss"], self.css(curr_result["values"])

    def solve_wide(self):
        A = 5
        c = 15
        a = [60, 180, 18000, 600, 1.2, 1.2]
        best = {"loss": float("inf")}
        i = 0
        while best["loss"] > 25 and i < 10:
            initial = [50, 20, 3750, 50, 100, 100]
            result = self.spsa(A, a, c, initial, iters=1000)
            if result["loss"] < best["loss"]:
                best = result
            i += 1
        return best

    def solve_narrow(self, result):
        A = result["loss"]
        c = 2
        A1 = A + 1
        a = [0.25 * A1, 0.25 * A1, A1, 0.25 * A1, 0.2 * A1, 0.2 * A1]
        return self.spsa(A, a, c, result["values"], iters=500)

    def spsa(self, A, a, c, values, iters):
        alpha = 1
        gamma = 0.16666666666666666
        best = None
        best_loss = float("inf")
        deltas = [0] * 6
        high_args = [0] * 6
        low_args = [0] * 6
        for k in range(iters):
            ck = c / ((k + 1) ** gamma)
            for i in range(6):
                deltas[i] = 1 if random.random() > 0.5 else -1
                high_args[i] = values[i] + ck * deltas[i]
                low_args[i] = values[i] - ck * deltas[i]
            loss_diff = self.loss(high_args) - self.loss(low_args)
            for i in range(6):
                g = loss_diff / (2 * ck) * deltas[i]
                ak = a[i] / ((A + k + 1) ** alpha)
                values[i] = self.fix(values[i] - ak * g, i)
            loss = self.loss(values)
            if loss < best_loss:
                best = values.copy()
                best_loss = loss
        return {"values": best, "loss": best_loss}

    def fix(self, value, idx):
        max_val = 100
        if idx == 2:  # saturate
            max_val = 7500
        elif idx == 4 or idx == 5:  # brightness or contrast
            max_val = 200

        if idx == 3:  # hue-rotate
            if value > max_val:
                value %= max_val
            elif value < 0:
                value = max_val + value % max_val
        elif value < 0:
            value = 0
        elif value > max_val:
            value = max_val
        return value

    def loss(self, filters):
        color = Color(0, 0, 0)
        color.invert(filters[0] / 100)
        color.sepia(filters[1] / 100)
        color.saturate(filters[2] / 100)
        color.hue_rotate(filters[3] * 3.6)
        color.brightness(filters[4] / 100)
        color.contrast(filters[5] / 100)
        color_hsl = color.rgb_to_hsl()
        return (
            abs(color.r - self.target.r)
            + abs(color.g - self.target.g)
            + abs(color.b - self.target.b)
            + abs(color_hsl[0] - self.target_hsl[0])
            + abs(color_hsl[1] - self.target_hsl[1])
            + abs(color_hsl[2] - self.target_hsl[2])
        )

    def css(self, filters):
        def fmt(idx, multiplier=1):
            return round(filters[idx] * multiplier)

        return (
            f"filter: invert({fmt(0)}%) sepia({fmt(1)}%) saturate({fmt(2)}%) hue-rotate({fmt(3, 3.6)}deg) "
            f"brightness({fmt(4)}%) contrast({fmt(5)}%);"
        )
