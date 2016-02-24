import os

from django.conf import settings

ATTACK_DIR = os.path.join(settings.BASE_DIR,
                          "competition",
                          "attacks")

DEBUG_ATTACK = None
# DEBUG_ATTACK = os.path.join(ATTACK_DIR, "both", "cursor.js")


yolos = []
for script in os.listdir(ATTACK_DIR):
    with open(os.path.join(ATTACK_DIR, script), 'r') as fd:
        script_content = fd.read()
        attack_meta = {
            "type": "distributed",
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
