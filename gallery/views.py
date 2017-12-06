from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.db.models import F, Sum
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

from .models import Picture, Profile, Comment
from .forms import PictureForm, BioForm, ProfilePicForm, MyAuthenticationForm, MyUserCreationForm


def imageClick(request):
	if request.method == 'POST':
		if request.is_ajax():
			if request.user.is_authenticated:
				pk = request.POST.get('pic_id')
				current_user = request.user.profile

				if (" " + str(pk) + " ") not in current_user.likes:
					image_object = get_object_or_404(Picture, pk=pk)
					upordown = int(request.POST.get('upordown'))

					if upordown:
						image_object.upvote += 1
					else:
						image_object.downvote += 1

					image_object.save()
					current_user.likes += (" " + str(pk) + " ")
					current_user.save()
			return HttpResponseRedirect('/')

	elif request.method == 'GET':
		if request.is_ajax():
			img = get_object_or_404(Picture, pk=request.GET.get('pic_id'))
			comments = Comment.objects.values('profile__username', 'profile__pk', 'body').filter(picture = img)
			obj_dict = {'username': img.profile.username, 'upvotes': img.upvote,
			'downvotes': img.downvote, 'url': img.profile.get_absolute_url(), 
			'date' : img.date, 'caption': img.caption, 'comments': list(comments)}
			
			return JsonResponse(obj_dict)

	return None



def addComment(request):
	if request.method == 'POST':
		if request.is_ajax():
			pk = request.POST.get('pic_id')
			image_object = get_object_or_404(Picture, pk=pk)
			text = request.POST.get('comment')
			new_comment = Comment(body=text, picture=image_object, profile=request.user.profile)
			new_comment.save()
			return HttpResponseRedirect('/')

	return None

def addUser(request):
	if request.method == 'POST':
		form = MyUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username = username, password = raw_password)
			login(request, user)
			newUser = Profile(username = username, likes = " ", user=user)
			newUser.save()			
	else:
		form = MyUserCreationForm()
		
	return form

def searchBar(request):
	query = request.GET.get('q')

	if query:
		results = Profile.objects.filter(username__icontains = query)
	else:
		results = None

	return render(request, 'gallery/search.html', {'results': results})

def index(request):
	image_list = Picture.objects.order_by(F('upvote') + F('downvote')).reverse()
	page = request.GET.get('page', 1)
	paginator = Paginator(image_list, 4)

	try:
		images = paginator.page(page)
	except PageNotAnInteger:
		images = paginator.page(1)
	except EmptyPage:
		images = paginator.page(paginator.num_pages)


	return render(request, 'index.html', context={'images': images})

def login_view(request):
	signup_form = addUser(request)
	if request.method == 'POST':
		login_form = MyAuthenticationForm(data=request.POST)

		if login_form.is_valid():
			username = login_form.cleaned_data.get('username')
			raw_password = login_form.cleaned_data.get('password')
			user = authenticate(username = username, password = raw_password)
			login(request, user)
			return HttpResponseRedirect(request.user.profile.get_absolute_url())

		if signup_form.is_valid():
			return HttpResponseRedirect(request.user.profile.get_absolute_url())


	else:
		login_form = MyAuthenticationForm()

	return render(request, "gallery/login.html", {'login_form': login_form, 'signup_form': signup_form})

@login_required
def logout_view(request):
	logout(request)
	return redirect('index')

@login_required
def addphoto(request):
	if request.method == 'POST':
		form = PictureForm(request.POST, request.FILES, user=request.user)
		if form.is_valid():
			form.save()
			return redirect('index')
	else:
		form = PictureForm()
	return render(request, 'gallery/addphoto.html', {'form': form})


def ProfileDetail(request, pk):
	member_object = get_object_or_404(Profile, pk = pk)
	member_pics = Picture.objects.filter(profile = member_object)
	upvotes = (member_pics.aggregate(up_sum=Sum('upvote'))['up_sum'] if 
		member_pics.count() else 0)
	downvotes = (member_pics.aggregate(down_sum=Sum('downvote'))['down_sum']
	 	if member_pics.count() else 0)
	total_votes = upvotes + downvotes 
	correct_member = (0 if not request.user.is_authenticated()
		else request.user.profile == member_object)

	if request.method == 'POST':
		bio_form = BioForm(request.POST)
		profPic_form = ProfilePicForm(request.POST, request.FILES, user=request.user)
		if bio_form.is_valid():
		 	member_object.bio = bio_form.cleaned_data.get('bio_text')
		 	member_object.save()
		 	return HttpResponseRedirect(member_object.get_absolute_url())
		elif profPic_form.is_valid():
			profPic_form.save()
			return HttpResponseRedirect(member_object.get_absolute_url())
	else:
		bio_form = BioForm()
		profPic_form = ProfilePicForm()

	page = request.GET.get('page', 1)
	paginator = Paginator(member_pics, 4)

	try:
		images = paginator.page(page)
	except PageNotAnInteger:
		images = paginator.page(1)
	except EmptyPage:
		images = paginator.page(paginator.num_pages)



	return render(request, 'gallery/profile_detail.html', {'bio_form': bio_form, 'profPic_form':
		profPic_form, 'upvotes': upvotes, 'downvotes' : downvotes, 'total_votes': total_votes, 
		'member': member_object, 'images': images, 'correct_member': correct_member,})
	
class ProfileListView(generic.ListView):
	model = Profile
	paginate_by = 5
		
