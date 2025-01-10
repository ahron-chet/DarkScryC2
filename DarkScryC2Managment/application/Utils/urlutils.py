from enum import Enum
from django.urls import path, include

class SlashBehavior(Enum):
    NONE = "none"
    ONLY = "only"
    BOTH = "both"

def create_path(route_base, view, name=None, slash_behavior=SlashBehavior.BOTH):
    route_base = route_base.strip("/")
    patterns = []

    if slash_behavior == SlashBehavior.NONE:
        patterns.append(path(route_base, view, name=name))
    elif slash_behavior == SlashBehavior.ONLY:
        patterns.append(path(route_base + "/", view, name=name))
    elif slash_behavior == SlashBehavior.BOTH:
        # no slash
        patterns.append(path(route_base, view, name=(f"{name}_no_slash" if name else None)))
        # slash
        patterns.append(path(route_base + "/", view, name=(f"{name}_with_slash" if name else None)))
    else:
        raise ValueError(f"Unknown slash_behavior: {slash_behavior}")

    return patterns

def create_include_path(route_base, urlconf, slash_behavior=SlashBehavior.BOTH):
    route_base = route_base.strip("/")
    patterns = []

    if slash_behavior == SlashBehavior.NONE:
        patterns.append(path(route_base, include(urlconf)))
    elif slash_behavior == SlashBehavior.ONLY:
        patterns.append(path(route_base + "/", include(urlconf)))
    elif slash_behavior == SlashBehavior.BOTH:
        patterns.append(path(route_base, include(urlconf)))
        patterns.append(path(route_base + "/", include(urlconf)))
    else:
        raise ValueError(f"Unknown slash_behavior: {slash_behavior}")

    return patterns
