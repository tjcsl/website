#!/bin/bash
cd "$(dirname "$(dirname "$0")")"
pipenv run ./manage.py shell -c "$(echo -e 'from tjhsst.apps.labs.models import Course\nfor course in Course.objects.filter(nickname = None):\n  course.nickname = course.name; course.save()')"

