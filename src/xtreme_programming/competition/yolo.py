script1 = """
alert("YOLO 1");
"""
script2 = """
alert("YOLO 1");
"""
script3 = """
alert("YOLO 1");
"""

yolo1 = {
    "type": "targeted",
    "script": script1
}

yolo2 = {
    "type": "distributed",
    "script": script2
}

yolo3 = {
    "type": "targeted",
    "script": script3
}

yolos = [yolo1, yolo2, yolo3]
