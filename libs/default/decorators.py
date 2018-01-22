from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied, ValidationError
from GamesRetro import settings
from functools import wraps


def validate_formulary(view):
    @wraps(view)
    def _wrapped_view(controller, request, formulary, *args, **kwargs):
        print("entrando no validade")
        """ request via ajax verifiy need settings.DEBUG=True for running view tests."""
        form = formulary(request.POST)
        form.request = request
        print("Chego no form.is_valid()?")
        if not form.is_valid():
            print("Passei do form_valid")
            if 'id' in request.POST:
                print("existe id no POST")
                controller.object = form.get_object(int(request.POST['id']))
                print("Consegui pegar")
            else:
                print("Nao possuo id")
                controller.object = form.get_object()
                print("passei do controller1")
        else:
            print("N passei no form is valid")
            if 'id' in request.POST:
                print("existe id no POST")
                controller.object = form.get_object(int(request.POST['id']))
                print("passei do controller2")
            else:
                print("Nao possuo id")
                controller.object = form.get_object()
                print("passei do controller3")
        print("VEJA O OBJETO CRIADO:",controller.object)
        controller.get_exceptions(controller.object, form)
        return view(controller, request, formulary, *args, **kwargs)
    return _wrapped_view


def request_ajax_required(view):
    @wraps(view)
    def _wrapped_view(controller, request, formulary=None, *args, **kwargs):
        """ request via ajax verifiy need settings.DEBUG=True for running view tests."""
        if request.is_ajax() or settings.DEBUG:
            controller.start_process(request)
            controller.request = request
            if formulary is None:
                return view(controller, request, *args, **kwargs)
            else:
                return view(controller, request, formulary, *args, **kwargs)
        else:
            raise PermissionDenied()
    return _wrapped_view


def request_get_required(view):
    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        if request.method == 'GET':
            return view(request, *args, **kwargs)
        else:
            raise PermissionDenied()
    return _wrapped_view


def request_post_required(view):
    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        if request.method == 'POST':
            return view(request, *args, **kwargs)
        else:
            raise PermissionDenied()
    return _wrapped_view