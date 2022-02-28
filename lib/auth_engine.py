from apps.api.services.user_service import User
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect

_user = User()


class AuthenticationBackend:
    """
    Authenticate througt parse auth engine.
    """
    user_model = get_user_model()

    def authenticate(self, request, username=None, password=None):
        credentials = {"username": username, "password": password}

        user = _user.login(data=credentials)

        if user:
            if user["isAdmin"]:
                request.session['user_info'] = user
                return self.get_or_create_user(request, credentials, user)

            messages.error(request, "Vous n'êtes pas autorisé !")
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        else:
            messages.error(request, "Error lors de l'authentification, merci de reessayer SVP !")
            return None

    def get_or_create_user(self, request, credentials, user_info):
        username = credentials["username"]
        new_user = {}

        try:
            new_user = self.user_model.objects.get(username__exact=username)
        except self.user_model.DoesNotExist as e:
            new_user = self.user_model(username=username)
            new_user.last_name = user_info.get("lastName", "")
            new_user.first_name = user_info.get("firstName", "")
            new_user.email = user_info.get("email", "")
            new_user.is_active = user_info.get("accountIsActive", "")
            new_user.is_staff = True
            new_user.save()
        finally:
            messages.success(request, "Connexion réussie !")
            return self.get_user(new_user.id)

    def get_user(self, user_id):
        try:
            return self.user_model.objects.get(pk=user_id)
        except self.user_model.DoesNotExist:
            return None
