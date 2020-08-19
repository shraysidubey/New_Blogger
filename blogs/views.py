from django.shortcuts import render, redirect
from blogs.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from blogs.forms import BlogForm, Comment_on_blogForm
from blogs.models import UserProfile
from blogs.models import blog, Comment_on_blog
import django.forms.widgets


def index(request):

    context_dict = {'boldmessage': "Comes to world of blogs"}

    if request.user.is_authenticated():
        Profile = UserProfile.objects.get(user=request.user.id)
        context_dict['profile'] = Profile

        followings = Profile.follows.all()
        L = []
        for i in followings:
            L.append(i.id)
        blogs = blog.objects.filter(created_by__in=L)
        context_dict['list_blogs'] = blogs

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

        following = user_Profile.follows.all()
        context_dict['following'] = following

        followers = user_Profile.userprofile_set.all()
        context_dict['followers'] = followers

        logged_in_userprofile = UserProfile.objects.get(user=request.user.id)
        context_dict['logged_in_userprofile'] = logged_in_userprofile

        is_following = logged_in_userprofile in followers
        context_dict['is_following'] = is_following

    except UserProfile.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'blogs/profile.html', context_dict)


def blog_detail(request, blog_slug):

    context_dict = {}                                                    #declared context dict

    try:

        Blog = blog.objects.filter(slug=blog_slug)[0]               #got blog object
        Blog.views = Blog.views +1                                  #increment in views as shown by user
        Blog.save()

        context_dict['blog_body'] = Blog.body                          #added body of blog ....
        context_dict['blog_title'] = Blog.title
        context_dict['blog_slug'] = Blog.slug
        context_dict['blog_views'] = Blog.views
        context_dict['blog_id'] = Blog.id                                  #added bog id
        context_dict['form'] = Comment_on_blogForm()

        user_profile = UserProfile.objects.get(user= request.user.id)               #got user id
        likes = Blog.likedBy.all()                                                  #give list of blogs which are liked
        Does_like = user_profile in likes                                           #check userrofile like
        context_dict['Does_like'] = Does_like

        if request.method == 'DELETE':                         #if request method is "delete" then blog will will be deleted as we click on button
            #print("deleted: ", Blog.title)
            Blog.delete()
            return redirect('/blogs')                             #after deleting redirect into blog page

        if request.method == 'POST' and 'edit_submit' in request.POST:      #condition when post request is there and form is editsubmit
            form = BlogForm(instance=Blog)                                  #this use to fetch the form
            form.fields['title'].widget.attrs['readonly'] = True            #
            context_dict['form'] = form                                     #
            return render(request, 'blogs/edit.html',context_dict)          #after click on edit button it will render on another page

        if request.method == 'POST' and 'blog_submit' in request.POST :     #condition when post request is there and form is blogsubmit
            #print("form is submitted")
            form = BlogForm(request.POST, instance=Blog)                     #use to fetch the form

            if form.is_valid():                                              #check if form is valid
                user_profile = UserProfile.objects.get(user=request.user.id)  #get user id
                Blog = form.save(commit=False)                                #save thr form
                Blog.created_by = user_profile                                #create the connection b/w
                #print(Blog.body)
                #print("saved")
                Blog.save()                                                  #use to save the blog

                context_dict['blog_body'] = Blog.body
                context_dict['blog_title'] = Blog.title
                context_dict['blog_slug'] = Blog.slug
                context_dict['blog_id'] = Blog.id

        if request.method == 'POST' and "comment_submit" in request.POST:   # condition when post request is there and form is blogsubmit
            form = Comment_on_blogForm(request.POST)  # fetch form
            if form.is_valid():
                comment = form.save(commit=False)
                comment.blogg = Blog
                comment.user = user_profile
                print("comment getting saved")
                comment.save()

        comments_on_blog = Comment_on_blog.objects.filter(blogg=Blog.id)
        context_dict['list_of_comments'] = comments_on_blog

    except blog.DoesNotExist:
        print("No such type of Blog is available")
        pass
    # Go render the response and return it to the client.
    return render(request, 'blogs/blog.html', context_dict)

def follow(request, userprofile_id, loggedin_userprofile_id):

    try:
        userprofile = UserProfile.objects.get(id=userprofile_id)

        loggedin_userprofile = UserProfile.objects.get(id=loggedin_userprofile_id)

        following = loggedin_userprofile.follows.all() #userProfiles whom loggedin user is following

        if userprofile in following:
            loggedin_userprofile.follows.remove(userprofile)
        else:
            loggedin_userprofile.follows.add(userprofile)

        return HttpResponseRedirect('/blogs/user/'+ userprofile.alias + '/')

    except UserProfile.DoesNotExist:
        print('DoesNotExist exception')

    return render(request, 'blogs/profile.html')

def like_blog(request, user_id, blog_id):
    try:

        userprofile = UserProfile.objects.get(id=user_id)

        blogs = blog.objects.get(id=blog_id)
        likes = blogs.likedBy.all()


        if userprofile in likes:
            blogs.likedBy.remove(userprofile)
        else:
            blogs.likedBy.add(userprofile)

        return HttpResponseRedirect('/blogs/blog/' + blogs.slug + '/')

    except UserProfile.DoesNotExist:
        print('DoesNotExist exception')
