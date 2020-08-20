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

    if request.method == 'POST':                                              #request method is post

        user_form = UserForm(data=request.POST)                               #fetch form
        profile_form = UserProfileForm(data=request.POST)                     #fetch form

        if user_form.is_valid() and profile_form.is_valid():                  #check user is valid or not
            user = user_form.save()                                           #save

            user.set_password(user.password)                                  #passwoed set for user
            user.save()

            profile = profile_form.save(commit=False)                         #for save
            profile.user = user

            profile.save()

            registered = True

        else:
            print user_form.errors, profile_form.errors


    else:
        user_form = UserForm()                                          #display form
        profile_form = UserProfileForm()

    return render(request,
            'blogs/register.html',                                       #redirect in registered page (html)
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):

    if request.method == 'POST':                                                 #user is gged i

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)                #check authenticate

        if user:
            if user.is_active:                                                  #check conditions

                login(request, user)
                return HttpResponseRedirect('/blogs/')                            #redirect on page
            else:
                return HttpResponse("Your blogs account is disabled.")             #if its not active this string will display
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'blogs/login.html', {})                            #return to this page


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
    logout(request)                                     # Since we know the user is logged in, we can now just log them out.
    return HttpResponseRedirect('/blogs/')              #Take the user back to the page

def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)                      #fetch form

        if form.is_valid():                              #check if form is valid
            user_profile = UserProfile.objects.get(user= request.user.id)           #get the UserProfile objects
            blog = form.save(commit=False)                                          #save the form
            blog.created_by = user_profile                                          #update the userprofile id in created_byh idea
            blog.save()                                                             #save

            return index(request)                                                   #take back to index page
        else:
            print form.errors
    else:
        form = BlogForm()                                                            ##use in render a page

    return render(request, 'blogs/add_blog.html', {'form': form})                    #render in this page

def profile(request, alias):

    context_dict = {}                                                               #declare dictionary

    try:
        user_Profile = UserProfile.objects.get(alias=alias)                        #get object from UserProfile
        context_dict['user'] = user_Profile                                        #keu used in html and get the data

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        blogs = blog.objects.filter(created_by=user_Profile.id)                   #getobject from blog
        context_dict['list_blogs'] = blogs

        following = user_Profile.follows.all()                                     #get list of following (to whom loggedin user follows)
        context_dict['following'] = following

        followers = user_Profile.userprofile_set.all()                             #get list of followers
        context_dict['followers'] = followers

        logged_in_userprofile = UserProfile.objects.get(user=request.user.id)      #get the user_id
        context_dict['logged_in_userprofile'] = logged_in_userprofile

        is_following = logged_in_userprofile in followers                          #check logged_in_user is +nt in lkst of following
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
                Blog.created_by = user_profile                                #pdate the userprofile id in created_byh idea
                #print(Blog.body)
                #print("saved")
                Blog.save()                                                  #use to save the blog

                context_dict['blog_body'] = Blog.body                        #get bodytite................??
                context_dict['blog_title'] = Blog.title
                context_dict['blog_slug'] = Blog.slug
                context_dict['blog_id'] = Blog.id

        if request.method == 'POST' and "comment_submit" in request.POST:   #condition when post request is there and form is blogsubmit
            form = Comment_on_blogForm(request.POST)                        #fetch form
            if form.is_valid():
                comment = form.save(commit=False)                           #save form
                comment.blogg = Blog                                        #update the Blog id in blogg
                comment.user = user_profile                                 #update the user_profile id in user
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

        loggedin_userprofile = UserProfile.objects.get(id=loggedin_userprofile_id)  #

        following = loggedin_userprofile.follows.all()                              #userProfiles to whom loggedin user is following

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

def delete_comment(request, comment_id, blog_slug):
    comment = Comment_on_blog.objects.get(id=comment_id)
    comment.delete()
    return redirect('/blogs/blog/' + blog_slug + '/')
