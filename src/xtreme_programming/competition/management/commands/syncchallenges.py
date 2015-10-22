import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from ...models import Challenge


class Command(BaseCommand):
    help = 'Synchronizes the database with the puzzle repository'

    def handle(self, *args, **options):

        Challenge.objects.all().delete()

        chals_dir = settings.CHAL_DIR
        chals = [name for name in os.listdir(chals_dir)
                 if os.path.isdir(os.path.join(chals_dir, name))]

        for chal in chals:
            chal_dir = os.path.join(chals_dir, chal)
            json_path = os.path.join(chal_dir, 'chal.json')
            problem_path_en = os.path.join(chal_dir, 'enonce_EN.md')
            problem_path_fr = os.path.join(chal_dir, 'enonce_FR.md')

            with open(json_path, 'r') as fd:
                properties = json.load(fd)

            with open(problem_path_en, 'r') as fd:
                problem_md_en = fd.read()

            with open(problem_path_fr, 'r') as fd:
                problem_md_fr = fd.read()

            created_chal = Challenge(
                length=properties['length'],
                title_EN=properties['title_EN'],
                title_FR=properties['title_FR'],
                description_EN=problem_md_en,
                description_FR=problem_md_fr
            )

            created_chal.save()
            print("Created: %s" % created_chal.title_EN)
