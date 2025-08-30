from django.http import JsonResponse
from django.shortcuts import render


def me(request):
    if request.user.is_authenticated:
        p = getattr(request.user, "profile", None)
        return JsonResponse({
            "authenticated": True,
            "user": {
                "id": request.user.id,
                "email": request.user.email,
                "display_name": (getattr(p, "display_name", None) or request.user.get_username()),
                "avatar_url": getattr(p, "avatar_url", ""),
            }
        })
    return JsonResponse({"authenticated": False, "user": None})


def home(request):
    context = {}
    if request.user.is_authenticated:
        p = getattr(request.user, "profile", None)
        context["display_name"] = (getattr(p, "display_name", None) or request.user.get_username())
    return render(request, "home.html", context)
