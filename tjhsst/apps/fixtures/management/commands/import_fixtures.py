import json
import os

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from ....clubs.models import Category, Club, Keyword
from ....labs.models import Course, Lab


class Command(BaseCommand):
    help = (
        "Imports fixtures (lab/club information) from the given directory. Does NOT delete "
        "existing objects under any circumstances, and tries to avoid modifying them unnecessarily."
    )

    def add_arguments(self, parser):
        parser.add_argument("dname", help="The name of the directory to import the fixtures from")

    def handle(self, *args, **options):
        dname = options["dname"]

        if not os.path.exists(dname):
            raise CommandError("{!r} does not exist; aborting".format(dname))

        if not os.path.isdir(dname):
            raise CommandError("{!r} is not a directory; aborting".format(dname))

        with open(os.path.join(dname, "club_data.json"), "r") as f_obj:
            club_info = json.load(f_obj)

        with open(os.path.join(dname, "lab_data.json"), "r") as f_obj:
            lab_info = json.load(f_obj)

        image_dir = os.path.join(dname, "images")

        self.stdout.write("Importing club fixtures...")

        for category_url, category_name in club_info["categories"].items():
            category = Category.objects.get_or_create(
                url=category_url, defaults={"name": category_name}
            )[0]
            category.name = category_name
            category.save()

        for keyword_url, keyword_name in club_info["keywords"].items():
            keyword = Keyword.objects.get_or_create(
                url=keyword_url, defaults={"name": keyword_name}
            )[0]
            keyword.name = keyword_name
            keyword.save()

        for club_url, club_data in club_info["clubs"].items():
            # The "defaults" here should ONLY contain required fields without default values. We set
            # everything else later.
            club = Club.objects.get_or_create(url=club_url, defaults={"name": club_data["name"]})[0]

            # If you are adding a field here, make sure to allow for the field not existing -- i.e.
            # use club_data.get("...") instead of club_data["..."]. Otherwise importing old fixtures
            # without those fields will fail.
            club.name = club_data["name"]
            club.description = club_data["description"]
            club.activity_id = club_data["activity_id"]
            club.link = club_data["link"]
            if club_data["category"] is None:
                club.category = None
            else:
                club.category = Category.objects.get(url=club_data["category"])
            club.keywords.set(Keyword.objects.filter(url__in=club_data["keywords"]))

            if club_data["image"]:
                with open(os.path.join(image_dir, club_data["image"]), "rb") as f_obj:
                    club.image.save(club_data["image"], File(f_obj))

            club.save()

        self.stdout.write("Importing lab fixtures...")

        for course_url, course_data in lab_info["courses"].items():
            course = Course.objects.get_or_create(
                url=course_url, defaults={"name": course_data["name"]}
            )[0]
            course.name = course_data["name"]
            course.nickname = course_data["nickname"]
            course.save()

        for lab_url, lab_data in lab_info["labs"].items():
            # The "defaults" here should ONLY contain required fields without default values. We set
            # everything else later.
            lab = Lab.objects.get_or_create(url=lab_url, defaults={"name": lab_data["name"]})[0]

            # If you are adding a field here, make sure to allow for the field not existing -- i.e.
            # use lab_data.get("...") instead of lab_data["..."]. Otherwise importing old fixtures
            # without those fields will fail.
            lab.name = lab_data["name"]
            lab.description = lab_data["description"]
            lab.link = lab_data["link"]
            lab.prerequisites.set(Course.objects.filter(url__in=lab_data["prerequisites"]))
            lab.recommended.set(Course.objects.filter(url__in=lab_data["recommended"]))

            if lab_data["image"]:
                with open(os.path.join(image_dir, lab_data["image"]), "rb") as f_obj:
                    lab.image.save(lab_data["image"], File(f_obj))

            lab.save()
