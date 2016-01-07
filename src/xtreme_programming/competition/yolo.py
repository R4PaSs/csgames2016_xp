import os

from django.conf import settings

ATTACK_DIR = os.path.join(settings.BASE_DIR,
                          "competition",
                          "attacks")

DEBUG_ATTACK = None
# DEBUG_ATTACK = os.path.join(ATTACK_DIR, "both", "zoom.js")


yolos = []
for script in os.listdir(os.path.join(ATTACK_DIR, "both")):
    with open(os.path.join(ATTACK_DIR, "both", script), 'r') as fd:
        script_content = fd.read()
        attack_meta = {
            "type": "distributed",
            "script": script_content,
            "name": script[:-3]
        }
        yolos.append(attack_meta)

        attack_meta = {
            "type": "targeted",
            "script": script_content,
            "name": script[:-3]
        }
        yolos.append(attack_meta)


for script in os.listdir(os.path.join(ATTACK_DIR, "distributed")):
    with open(os.path.join(ATTACK_DIR, "distributed", script), 'r') as fd:
        script_content = fd.read()
        attack_meta = {
            "type": "distributed",
            "script": script_content,
            "name": script[:-3]
        }
        yolos.append(attack_meta)


for script in os.listdir(os.path.join(ATTACK_DIR, "targeted")):
    with open(os.path.join(ATTACK_DIR, "targeted", script), 'r') as fd:
        script_content = fd.read()
        attack_meta = {
            "type": "targeted",
            "script": script_content,
            "name": script[:-3]
        }
        yolos.append(attack_meta)


if DEBUG_ATTACK:
    with open(DEBUG_ATTACK, 'r') as fd:
        script_content = fd.read()
        attack_meta = {
            "type": "distributed",
            "script": script_content,
            "name": script[:-3]
        }
    yolos = [attack_meta]
