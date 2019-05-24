from django.shortcuts import reverse
from django.urls import NoReverseMatch

def set_search_field_vars(request):
    app_name = request.resolver_match.app_name
    if app_name == "home":
        return {}
    try:
        search_url = reverse(app_name + ":index")
    except NoReverseMatch:
        return {}
    else:
        return {
            "search_url": search_url,
            "search_name": app_name,
        }

