from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import SignUpForm, RequestForm, NotationForm, UserProfileForm
from .models import Notation, Friendship, UserProfile
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("notion:main"))
        else:
            print(form.errors)
    else:
        form = SignUpForm()

    return render(request, "registration/sign_up.html", {"form": form})


class MainView(View):
    @method_decorator(login_required(login_url="/login/"))
    def get(self, request):
        form = RequestForm()
        return render(request, 'main_app/main.html', {'form': form})

    def post(self, request):
        form = RequestForm(request.POST)
        try:
            if form.is_valid():
                user_input = form.cleaned_data['user_input']
                is_public = form.cleaned_data['is_public']
                tag_notion = form.cleaned_data['tag_notion']
                topic_notion = form.cleaned_data['topic_notion']
                with transaction.atomic():
                    notion = Notation(author=request.user, content=user_input, is_public=is_public, tag_notion=tag_notion, topic_notion=topic_notion)
                    notion.save()

                return HttpResponseRedirect(reverse("main_app:get_todo", args=(notion.id,)))

                return render(request, 'main_app/main.html', {'form': form})
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return render(request, 'main_app/main.html', {'form': form})


@login_required(login_url="/login/")
def get_notion(request, notion_id):
    notion = get_object_or_404(Notation, pk=notion_id)
    context = {"notion": notion}
    return render(request, "main_app/page.html", context)


@login_required(login_url="/login/")
def get_list_notions(request):
    notions = Notation.objects.filter(author=request.user).order_by("-id")
    context = {"notions": notions}
    return render(request, "main_app/notions.html", context)


@login_required(login_url="/login/")
def delete_notion(request, notion_id):
    notion = Notation.objects.get(pk=notion_id)
    if request.method == "POST":
        if request.user == notion.author:
            notion.delete()
            return redirect(reverse("notion:get_notions"))

    context = {'main_app': notion}
    return render(request, 'main_app/notion_confirm_delete.html', context)


@login_required(login_url="/login/")
def update_notion(request, notion_id):
    notion = get_object_or_404(Notation, pk=notion_id, author=request.user)  # Получаем заметку с проверкой авторства
    if request.method == "POST":
        form = NotationForm(request.POST, instance=notion)  # Инициализация формы с текущими данными заметки
        if form.is_valid():
            form.save()  # Сохранение изменений в заметке
            return redirect(reverse("notion:get_notion", args=(notion_id,)))
    else:
        form = NotationForm(instance=notion)  # Форма для редактирования заметки

    context = {'form': form, 'notion': notion}
    return render(request, 'main_app/notion_update.html', context)  # Шаблон для обновления заметки


@login_required(login_url="/login/")
def delete_notion(request, notion_id):
    notion = Notation.objects.get(pk=notion_id)
    if request.method == "POST":
        if request.user == notion.author:
            notion.delete()
            return redirect(reverse("notion:get_notions"))

    context = {'main_app': notion}
    return render(request, 'main_app/notion_confirm_delete.html', context)


@login_required(login_url="/login/")
def get_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {"user": user}
    return render(request, "main_app/profile.html", context)


@login_required
def update_profile_pic(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('notion:get_profile', user_id=request.user.id)
    else:
        form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'main_app/update_profile_pic.html', {'form': form})


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()


@login_required(login_url="/login/")
def add_friend(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)
    request.user.add_friend(friend)
    return HttpResponseRedirect(...)


@login_required(login_url="/login/")
def remove_friend(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)
    request.user.remove_friend(friend)
    return HttpResponseRedirect(...)


@login_required(login_url="/login/")
def list_friends(request):
    friends = request.user.get_friends()
    return render(request, 'friends_list.html', {'friends': friends})


@login_required(login_url="/login/")
def friend_notations(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)
    notations = request.user.get_friend_notations(friend)
    return render(request, 'friend_notations.html', {'notations': notations})


def add_friend(user, friend):
    Friendship.objects.create(user=user, friend=friend)


def remove_friend(user, friend):
    Friendship.objects.filter(user=user, friend=friend).delete()


def get_friends(user):
    return User.objects.filter(friends__user=user)


def get_friend_notations(friend):
    return Notation.objects.filter(author=friend, is_public=True)