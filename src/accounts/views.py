"""
Django views for user authentication and profile management.

This module provides API endpoints and web views for user authentication,
including a REST API endpoint for checking authentication status and a home view
with Google OAuth integration.
"""

from django.http import JsonResponse
from django.shortcuts import render


def me(request):
    """
    API endpoint to get current user's authentication status and profile data.

    Returns JSON with user information if authenticated, or authentication status
    if not authenticated. This endpoint is used by frontend applications to
    determine the current user's state.

    Args:
        request: Django HttpRequest object.

    Returns:
        JsonResponse: Contains authentication status and user data if authenticated.
            Example authenticated response:
            {
                "authenticated": True,
                "user": {
                    "id": 1,
                    "email": "user@example.com",
                    "display_name": "John Doe",
                    "avatar_url": "https://example.com/avatar.jpg"
                }
            }

            Example unauthenticated response:
            {
                "authenticated": False,
                "user": None
            }
    """
    if request.user.is_authenticated:
        p = getattr(request.user, "profile", None)
        return JsonResponse(
            {
                "authenticated": True,
                "user": {
                    "id": request.user.id,
                    "email": request.user.email,
                    "display_name": (
                        getattr(p, "display_name", None) or request.user.get_username()
                    ),
                    "avatar_url": getattr(p, "avatar_url", ""),
                },
            }
        )
    return JsonResponse({"authenticated": False, "user": None})


def home(request):
    """
    Home page view with Google OAuth integration.

    Displays the main landing page with different content based on authentication status.
    For authenticated users, shows their profile information and logout option.
    For anonymous users, shows Google OAuth login button.

    Args:
        request: Django HttpRequest object.

    Returns:
        HttpResponse: Rendered home.html template with appropriate context.
    """
    context = {}
    if request.user.is_authenticated:
        p = getattr(request.user, "profile", None)
        context["display_name"] = (
            getattr(p, "display_name", None) or request.user.get_username()
        )
    return render(request, "home.html", context)
