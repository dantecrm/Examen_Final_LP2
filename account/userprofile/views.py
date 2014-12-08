# coding: utf-8
from django.shortcuts import redirect, render, render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import FormView
from django.views.generic.list import ListView
from .forms import UserForm, UserProfileForm
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import UserProfile
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate, logout

# @method_decorator(permission_required('profil.list_profil'))
def Usuarios(request):
    usuarios = User.objects.all()
    titulo = "Página de usuarios registrados"
    return render_to_response('userprofile/usuarios.html', {'usuarios':usuarios, 'titulo':titulo},
                              context_instance=RequestContext(request))
def register(request):
    context = RequestContext(request)
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render_to_response(
            'userprofile/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render_to_response('userprofile/login.html', {}, context)


@login_required(login_url='/login')
def Cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')

class UserProfileList(ListView):
    template_name = 'userprofile/user_profile_list.html'
    model = UserProfile

class UserProfileDetail(DeleteView):
    template_name = 'userprofile/user_profile_detail.html'
    model = UserProfile
    @method_decorator(permission_required('userprofile.view_profil'))
    def dispatch(self, *args, **kwargs):
        return super(UserProfileDetail, self).dispatch(*args, **kwargs)

# class UserProfileCreate(CreateView):
#     template_name = 'userprofile/user_profile_create.html'
#     model = UserProfile
#     form_class = UserProfileForm

#     @method_decorator(permission_required('userprofile.add_profil'))
#     def dispatch(self, *args, **kwargs):
#         return super(UserProfileCreate, self).dispatch(*args, **kwargs)
#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         # self.object.picture = self.request.FILES
#         self.object.save()
#         return redirect(self.object)


class UserProfileUpdate(UpdateView):
    template_name = 'userprofile/user_profile_create.html'
    model = UserProfile
    form_class = UserProfileForm

    @method_decorator(permission_required('userprofile.change_profil'))
    def dispatch(self, *args, **kwargs):
        return super(UserProfileUpdate, self).dispatch(*args, **kwargs)

class UserProfileDelete(DeleteView):
    model = UserProfile
    @method_decorator(permission_required('userprofile.delete_profil'))
    def dispatch(self, *args, **kwargs):
        return super(UserProfileDelete, self).dispatch(*args, **kwargs)
    def get_success_url(self):
        return reverse('user_profile_list')
