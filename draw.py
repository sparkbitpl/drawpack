import os
import sys
from colors import *
from svg import *

INDENT_LIMIT = 3

# Dimensions in pixels
MARGIN = 20
PACKAGE_NAME_BOX_HEIGHT = 20
PACKAGE_NAME_BOX_WIDTH = 190
PACKAGE_WIDTH = 250
PACKAGE_HEIGHT = 50
IMAGE_WIDTH = 1200

CHILD_HEIGHT = PACKAGE_NAME_BOX_HEIGHT + PACKAGE_HEIGHT


def small_box(name, x, y, indent, base_color):
    return box(name, x, y, PACKAGE_WIDTH, PACKAGE_HEIGHT, indent, base_color)


def box(name, x, y, width, height, indent, base_color):
    color = get_color(base_color, indent)
    return SVG_BOX.format(x, y, PACKAGE_NAME_BOX_WIDTH, PACKAGE_NAME_BOX_HEIGHT, x + 4, y + 14, name,
                          x, y + PACKAGE_NAME_BOX_HEIGHT, width, height, color)


def go(path, x, y, max_x, indent, base_color):
    if indent >= MAX_INDENT:
        return "", y
    dir_list = os.listdir(path)
    result = ""
    cur_y = y
    cur_x = x
    with_children_list = []
    without_children_list = []
    for item in dir_list:
        test_path = os.path.join(path, item)
        if os.path.isdir(test_path) and item != "test":
            if has_children(test_path, indent):
                with_children_list.append(item)
            else:
                without_children_list.append(item)
    sorted_list = with_children_list + without_children_list
    i = 0
    for item in sorted_list:
        test_path = os.path.join(path, item)
        if has_children(test_path, indent):
            children_svg, max_y_children = go(test_path, x + MARGIN, cur_y + PACKAGE_NAME_BOX_HEIGHT + MARGIN,
                                              max_x - 2 * MARGIN, indent + 1, base_color)
            box_svg = box(item, x, cur_y, max_x, max_y_children - cur_y - MARGIN, indent, base_color) + "\n"
            result += box_svg + children_svg
            cur_y = max_y_children + MARGIN
        else:
            result += small_box(item, cur_x, cur_y, indent, base_color)
            cur_x += PACKAGE_WIDTH + MARGIN
            if cur_x + PACKAGE_WIDTH > max_x and i < len(sorted_list) - 1:
                cur_x = x
                cur_y += CHILD_HEIGHT + MARGIN
            else:
                if i == len(sorted_list) - 1:
                    cur_y += CHILD_HEIGHT + MARGIN
        i += 1
    return result, cur_y


def has_children(path, indent):
    if indent >= MAX_INDENT - 1:
        return False
    dir_list = os.listdir(path)
    for item in dir_list:
        test_path = os.path.join(path, item)
        if os.path.isdir(test_path):
            return True
    return False


if len(sys.argv) <= 3:
    print "Usage <script> path max_indent base_color [main package prefix]"
    exit(-1)
MAX_INDENT = int(sys.argv[2])

if MAX_INDENT > INDENT_LIMIT:
    print "maximum 3 indentation levels supported"
    exit(-1)

baseColor = sys.argv[3]

if len(sys.argv) == 5:
    prefix = sys.argv[4]
    MAX_INDENT += 1
    text, maxY = go(sys.argv[1], 2 * MARGIN, PACKAGE_NAME_BOX_HEIGHT + 2 * MARGIN, IMAGE_WIDTH - 4 * MARGIN, 1,
                    baseColor)
    text = box(prefix, MARGIN, MARGIN, IMAGE_WIDTH - 2 * MARGIN, maxY - 2 * MARGIN, 0, baseColor) + text
else:
    text, maxY = go(sys.argv[1], MARGIN, MARGIN, IMAGE_WIDTH - 2 * MARGIN, 0, baseColor)

print SVG_HEADER.format(maxY + MARGIN)
print text
print SVG_TRAILER
