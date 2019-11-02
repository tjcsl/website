import json
import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from ....clubs.models import Category, Club, Keyword
from ....labs.models import Course, Lab


class Command(BaseCommand):
    help = "Exports fixtures (lab/club information) to the given directory"

    def add_arguments(self, parser):
        parser.add_argument("dname", help="The name of the directory to save the fixtures to")

    def handle(self, *args, **options):
        dname = options["dname"]

        if os.path.exists(dname):
            raise CommandError("{!r} exists; aborting".format(dname))

        os.mkdir(dname)

        club_images = []

        self.stdout.write("Generating club fixtures...")
        clubs = {}
        for club in Club.objects.all():
            if club.image.name:
                club_images.append(club.image.name)

            clubs[club.url] = {
                "name": club.name,
                "image": club.image.name,
                "description": club.description,
                "activity_id": club.activity_id,
                "link": club.link,
                "category": (club.category.url if club.category is not None else None),
                "keywords": [keyword.url for keyword in club.keywords.all()],
            }

        categories = dict(Category.objects.values_list("url", "name"))
        keywords = dict(Keyword.objects.values_list("url", "name"))

        lab_images = []

        self.stdout.write("Generating lab fixtures...")
        labs = {}
        for lab in Lab.objects.all():
            if lab.image.name:
                lab_images.append(lab.image.name)

            labs[lab.url] = {
                "name": lab.name,
                "image": lab.image.name,
                "description": lab.description,
                "link": lab.link,
                "prerequisites": [course.url for course in lab.prerequisites.all()],
                "recommended": [course.url for course in lab.recommended.all()],
            }

        courses = {
            course.url: {"name": course.name, "nickname": course.nickname}
            for course in Course.objects.all()
        }

        self.stdout.write("Serializing fixtures as JSON...")
        club_data = {"clubs": clubs, "categories": categories, "keywords": keywords}
        lab_data = {"labs": labs, "courses": courses}

        with open(os.path.join(dname, "club_data.json"), "w") as f_obj:
            json.dump(club_data, f_obj)

        with open(os.path.join(dname, "lab_data.json"), "w") as f_obj:
            json.dump(lab_data, f_obj)

        image_dir = os.path.join(dname, "images")

        self.stdout.write("Copying club images...")
        for name in club_images:
            copy_name = os.path.join(image_dir, name)
            os.makedirs(os.path.dirname(copy_name), exist_ok=True)
            shutil.copy(os.path.join(settings.MEDIA_ROOT, name), copy_name)

        self.stdout.write("Copying lab images...")
        for name in lab_images:
            copy_name = os.path.join(image_dir, name)
            os.makedirs(os.path.dirname(copy_name), exist_ok=True)
            shutil.copy(os.path.join(settings.MEDIA_ROOT, name), copy_name)
