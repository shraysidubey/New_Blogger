from django.shortcuts import render
from blogs.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from blogs.forms import BlogForm
from blogs.models import UserProfile
from blogs.models import blog

def index(request):

    context_dict = {'boldmessage': "Comes to world of blogs"}

    if request.user.is_authenticated():
        Profile = UserProfile.objects.get(user=request.user.id)
        context_dict['profile'] = Profile

    return render(request, 'blogs/index.html', context_dict)

def register(request):

    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

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

    return render(request,
            'blogs/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:

                login(request, user)
                return HttpResponseRedirect('/blogs/')
            else:
                return HttpResponse("Your blogs account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:

        return render(request, 'blogs/login.html', {})

def some_view(request):
    if not request.user.is_authenticated():
        return HttpResponse("You are logged in.")
    else:
        return HttpResponse("You are not logged in.")

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/blogs/')


def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)

        if form.is_valid():
            user_profile = UserProfile.objects.get(user= request.user.id)
            blog = form.save(commit=False)
            blog.created_by = user_profile
            blog.save()

            return index(request)
        else:
            print form.errors
    else:
        form = BlogForm()

    return render(request, 'blogs/add_blog.html', {'form': form})

def profile(request, alias):

    context_dict = {}

    try:

        user_Profile = UserProfile.objects.get(alias=alias)
        context_dict['user'] = user_Profile


        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        blogs = blog.objects.filter(created_by=user_Profile.id)
        context_dict['list_blogs'] = blogs


    except UserProfile.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'blogs/profile.html', context_dict)


def blog_detail(request, blog_slug):

    context_dict = {}

    try:

        Blog = blog.objects.filter(slug=blog_slug)[0]

        context_dict['blog_body'] = Blog.body
        context_dict['blog_title'] = Blog.title

    except blog.DoesNotExist:
        pass

        print("No such type of Blog is availble")
    # Go render the response and return it to the client.
    return render(request, 'blogs/blog.html', context_dict)
