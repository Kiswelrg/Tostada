from django.conf import settings


def printc(info, isList = False, color = None, end = '\n'):
    def printRGB(text):
        def rgb_to_ansi(r, g, b):
            # Convert RGB values to a color index
            index = 16 + (36 * round(r * 5 / 255)) + (6 * round(g * 5 / 255)) + round(b * 5 / 255)
            # Return the ANSI escape sequence
            return f"\033[38;5;{index}m"
        if color:
            # Convert RGB to ANSI color code
            ansi_code = rgb_to_ansi(color[0], color[1], color[2])
            print(f"{ansi_code}{text}\033[0m", end=end)
        else:
            print(text, end=end)
    if settings.VERBOSE:
        if isList:
            for i in info:
                printRGB(i)
            return
        printRGB(info)