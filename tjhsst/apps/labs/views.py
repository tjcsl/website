import random
import itertools

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models import Q

from .models import Lab, Course
from .forms import LabForm, LabCreationForm

# Create your views here.

def index(request):
    labs = Lab.objects.all()

    if request.GET.get("q"):
        query = request.GET["q"]
        words = query.split()

        lab_scores = {lab: 0 for lab in labs}
        for word in words:
            for lab in labs.filter(name__contains = word):
                lab_scores[lab] += 2

            for lab in labs.filter(description__contains = word):
                lab_scores[lab] += 1

        labs = sorted((lab for lab in labs if lab_scores[lab] > 0), key = lab_scores.__getitem__)
    else:
        # Order the labs randomly, but store the seed in a session variable so the
        # order won't change if the user reloads the page.
        if "seed" not in request.session:
            request.session["seed"] = random.randint(0, 10000)
        rand_gen = random.Random(request.session["seed"])

        labs = sorted(labs, key = lambda c: rand_gen.random())

    return render(
        request,
        "labs/list.html",
        {
            "labs": [(lab, itertools.zip_longest(lab.prerequisites.all(), lab.recommended.all())) for lab in labs],
            "search_term": request.GET.get("q", ""),
        },
    )

def show(request, lab_url):
    lab = get_object_or_404(Lab, url = lab_url)

    return render(
        request,
        "labs/show.html",
        {
            "lab": lab,
            "can_edit": request.user.is_superuser or request.user in lab.admins.all(),

        },
    )

def show_course(request, course_url):
    course = get_object_or_404(Course, url = course_url)
    required = course.labs_with_prerequisite.all()
    recommended = course.labs_with_recommended.all()
    return render(
        request,
        "labs/courses/show.html",
        {
            "course": course,
            "labs_required_for": required,
            "labs_recommended_for": recommended,
            "labs": recommended.union(required)
        },
    )

def show_courses(request):
    course_urls = request.GET.getlist("courses[]")
    if "submit" in request.GET:
        labs = Lab.objects.filter(Q(prerequisites__url__in = course_urls) | Q(recommended__url__in = course_urls)).distinct()

        lab_scores = {lab: 0 for lab in labs}
        for lab in labs:
            recommended = lab.recommended.all()
            required = lab.prerequisites.all()
            lab_scores[lab] += sum(course.url in course_urls for course in required) / len(required)
            lab_scores[lab] += 0.1 * sum(course.url in course_urls for course in recommended)

        labs = sorted(labs, reverse = True, key = lab_scores.__getitem__)
        return render(
            request,
            "labs/list.html",
            {
                "all_courses": Course.objects.all(),
                "course_urls": course_urls,
                "labs": [(lab, itertools.zip_longest(lab.prerequisites.all(), lab.recommended.all())) for lab in labs],
            }
        )
    else:

        return render(
            request,
            "labs/find/find_by_courses.html",
            {
                "all_courses": Course.objects.all().order_by("nickname"),
                "course_urls": course_urls,
            }
        )

def edit(request, lab_url):
    lab = get_object_or_404(Lab, url = lab_url)
    if request.user.is_authenticated and (request.user.is_superuser or request.user in lab.admins.all()):
        if request.method == "POST":
            form = LabForm(request.POST, request.FILES, instance = lab)
            if form.is_valid():
                form.save()
                return redirect("labs:edit", lab.url)
        else:
            form = LabForm(instance = lab)

        return render(
            request,
            "labs/edit.html",
            {
                "lab": lab,
                "lab_form": form,
            },
        )
    else:
        raise http.Http404

def new(request):
    if request.user.is_authenticated and (request.user.is_teacher or request.user.is_superuser):
        if request.method == "POST":
            form = LabCreationForm(request.POST)
            if form.is_valid():
                lab = form.save()
                return redirect("labs:show", lab.url)
        else:
            form = LabCreationForm()

        return render(
            request,
            "labs/new.html",
            {
                "lab_form": form,
            },
        )
    else:
        raise http.Http404
