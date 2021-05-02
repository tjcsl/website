from django.core.validators import RegexValidator
from django.db import models


# Create your models here.
class Lab(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    url = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9_\-]+$",
                message="Only alphanumeric, dashes, and underscores allowed",
            )
        ],
    )

    image = models.ImageField(upload_to="lab_photos/", null=True, blank=True)

    description = models.CharField(
        max_length=5000, default="This lab page has not yet been filled out."
    )
    link = models.CharField(max_length=200, blank=True)

    prerequisites = models.ManyToManyField("Course", related_name="labs_with_prerequisite")
    recommended = models.ManyToManyField("Course", related_name="labs_with_recommended", blank=True)
    admins = models.ManyToManyField("users.User", related_name="labs")

    def __str__(self):
        return self.name


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    description = models.CharField(max_length=5000)
    image = models.ImageField(upload_to="project_photos/", null=True, blank=True)

    authors = models.ManyToManyField("users.User", related_name="senior_projects_authored")
    labs = models.ManyToManyField("Lab", related_name="senior_projects_sponsored")

    def __str__(self):
        return "{}: {}".format(self.display_labs(), self.name)

    def display_labs(self):
        return " ,".join([lab.name for lab in self.labs.all()])

    def display_authors(self):
        return " ,".join(["{} {}".format(a.first_name, a.last_name) for a in self.authors.all()])


class Testimonial(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(
        "users.User",
        related_name="testimonials_written",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    lab = models.ForeignKey("Lab", related_name="testimonials_set", on_delete=models.CASCADE)
    content = models.CharField(max_length=5000)

    def __str__(self):
        return "{}: {}...".format(self.lab, self.content[:40])


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    nickname = models.CharField(max_length=50, unique=True, null=True, blank=True)
    url = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9_\-]+$",
                message="Only alphanumeric, dashes, and underscores allowed",
            )
        ],
    )

    @property
    def nickname_or_name(self):
        return self.nickname or self.name

    def __str__(self):
        if self.nickname and self.nickname != self.name:
            return "{} ({})".format(self.nickname, self.name)
        else:
            return self.name
