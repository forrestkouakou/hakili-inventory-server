from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core import signing
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from apps.user.forms import CreatePasswordForm
from apps.user.token import account_activation_token

User = get_user_model()


class ActivateAccountView(TemplateView):
    template_name = "user/activate_account.html"

    def get(self, request, *args, **kwargs):
        uidb64, token = self.kwargs.get("uidb64", None), self.kwargs.get("token", None)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        encoded_id = signing.dumps({"id": uidb64, "token": token})

        if user is not None and user.email_confirmed is False and account_activation_token.check_token(user, token):
            data = {"user": user, "email": user.email, "user_hash": encoded_id}
            form = CreatePasswordForm(initial=data)
            context = {
                "page_name": "activate_account",
                "user": user,
                "form": form,
                "page_title": _("Account activation"),
                "page_info": _("Account activation")
            }

            return TemplateResponse(request, self.template_name, context)

        context = {
            "page_name": "activate_account",
            "user": user,
            "page_title": _("Account activation"),
            "page_info": _("Account activation")
        }
        return TemplateResponse(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = CreatePasswordForm(request.POST)
        if form.is_valid():
            try:
                user_hash = request.POST.get("user_hash", None)
                user_id = signing.loads(user_hash)
                decoded_id = force_str(urlsafe_base64_decode(user_id["id"]))
                user = User.people.user_list().get(id=decoded_id)
                if user.email == request.POST.get("email", None):
                    user.set_password(request.POST.get("password2"))
                    user.email_confirmed = True
                    user.is_active = True
                    user.save()
                return render(request, "user/activate_account.html", {"is_activated": "Is activated"})
                return JsonResponse(request.path_info)
                return HttpResponseRedirect(request.path_info)
            except (TypeError, ValueError, OverflowError, KeyError, User.DoesNotExist):
                messages.error(request, _("User not found"))
                return render(request, "user/activate_account.html", {"form": form})
        else:
            return render(request, "user/activate_account.html", {"form": form})
            # messages.error(request, _("An error occured"))
            # data = {self.kwargs["uidb64"], self.kwargs["token"]}
            # return self.get(request, data)
