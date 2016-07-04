def get_color(base_color, indent):
    color = {
        "green": {
            0: "#e6ffe6",
            1: "#ccffcc",
            2: "#8cd98c",
            3: "#53c653"
        },
        "yellow": {
            0: "#fff5cc",
            1: "#ffe066",
            2: "#ffd11a",
            3: "#e6b800"
        },
        "blue": {
            0: "#e6f5ff",
            1: "#b3e0ff",
            2: "#66c2ff",
            3: "#33adff"
        }
    }
    return color.get(base_color).get(indent)
