# application/views/base.py
import json
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from pydantic import ValidationError
from .schema_manager import SchemaManager
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from pydantic import ValidationError
from .schema_manager import SchemaManager


class BaseAsyncView(View):
    """
    A base class-based view that:
      1) Forces login by default (unless override).
      2) If usecsrf=False, disables CSRF protection for this view.
      3) If a schema_class is provided, parses/validates JSON body
         and attaches it to request.validated_data.
      4) Minimizes blocking by making dispatch() async.
    """
    login_required = True
    usecsrf = False
    schema_class: SchemaManager = None  # set this to a Pydantic model class if you want validation

    @classmethod
    def as_view(cls, **initkwargs):
        """
        Overriding as_view to apply a method_decorator:
        - Applies login_required if login_required=True.
        - Applies csrf_exempt if usecsrf=False.
        """
        view = super().as_view(**initkwargs)

        # Disable CSRF if usecsrf is False
        if not cls.usecsrf:
            view = csrf_exempt(view)
        
        # Enforce login_required if set
        if cls.login_required:
            view = login_required(view)

        return view

    async def dispatch(self, request, *args, **kwargs):
        """
        Async dispatch with schema validation.
        """
        if request.method in ("POST", "PUT", "PATCH") and self.schema_class:
            try:
                raw_body = request.body
                body_data = json.loads(raw_body.decode('utf-8') or '{}')
                # Validate using the Pydantic schema
                validated = self.schema_class(**body_data)
                # Attach validated data to request
                request.validated_data = validated
            except (json.JSONDecodeError, ValidationError) as exc:
                return JsonResponse({"error": str(exc)}, status=400)

        # Proceed with normal dispatch
        return await super().dispatch(request, *args, **kwargs)
