from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView,CreateView,FormView,View,UpdateView,ListView,DetailView
from REMS.models import *
from REMS.forms import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q 
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

#decorators 

def signin_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.warning(request,'please login first')
            return redirect('login')
    return inner

dec=[signin_required,never_cache]

class LoginView(FormView):
    template_name='login.html'
    form_class=LoginForm
    def post(self,request):
        form_data=LoginForm(data=request.POST)
        if form_data.is_valid():
            uname=form_data.cleaned_data.get('username')
            pswd=form_data.cleaned_data.get('password')
            user=authenticate(request,username=uname,password=pswd)
            if user:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,'Invalid username or password')
                return render(request,'login.html',{'form':form_data})
        return render(request,'login.html',{'form':form_data})

class SignupView(CreateView):
    template_name='signup.html'
    form_class=RegForm
    success_url=reverse_lazy('login')
    def form_valid(self,form):
        messages.success(self.request,'Registration successfull')
        return super().form_valid(form)
    def form_invalid(self,form):
        messages.error(self.request,'Registration failed')
        return super().form_invalid(form)
    
def logoutview(request,*args,**kwargs):
    logout(request)
    return redirect('login')



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfileModel.objects.create(user=instance)


@method_decorator(decorator=dec,name='dispatch')
class HomeView(View):
    def get(self,request):
        profile = ProfileModel.objects.get(user=self.request.user)
        property = Property.objects.exclude(user=profile)
        return render(request,'home.html',{'profile':profile,'property':property})
    
    def post(self, request):
        form = SearchForm(data=request.POST)  # Use the form to get the data
        properties = Property.objects.all()
        query = None
        
        if form.is_valid():
            query = form.cleaned_data['search']
            print(query)  # Debug line to check the query

            if query:
                 properties = properties.filter(
                    Q(address__icontains=query) |
                    Q(city=query) |
                    Q(state=query) |
                    Q(country=query)
                )
            print(f"Properties Found: {properties.count()}")
        context = {
            'profile': ProfileModel.objects.get(user=self.request.user),
            'property': properties,
            'form': form,  # Include the form in the context
            'query': query
        }
        return render(request, 'home.html', context)

dec  
def category(request,**kwargs):
    data=Property.objects.filter(category=kwargs.get('cat'))
    context = {
            'profile': ProfileModel.objects.get(user=request.user),
            'property': data,
        }
    return render(request, 'home.html', context)



@method_decorator(decorator=dec,name='dispatch')
class AddProperty(LoginRequiredMixin, CreateView):
    form_class = PropertyForm
    template_name = 'add_property.html'
    success_url = reverse_lazy('home')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = ProfileModel.objects.get(user=self.request.user)  # Add the ProfileModel instance to context
        return context

    def form_valid(self, form):
        profile = ProfileModel.objects.get(user=self.request.user)
        form.instance.user = profile
        return super().form_valid(form)

@method_decorator(decorator=dec,name='dispatch')
class ProfileView(View):
    def get(self,request):
        user=request.user
        profile=ProfileModel.objects.get(user=user)
        property=Property.objects.filter(user=profile)
        total=property.count()
        return render(request,'profile.html',{'profile':profile,'post':property,'total':total})

@method_decorator(decorator=dec,name='dispatch')
class UpdateProfileView(View):
    def get(self,request,**kwargs):
        id=kwargs.get('id')
        profile=ProfileModel.objects.get(id=id)
        form=ProfileForm(initial={'first_name':profile.user.first_name,'last_name':profile.user.last_name,'email':profile.user.email,'username':profile.user.username,'profile_pic':profile.profile_pic,'bio':profile.bio,'phone':profile.phone})
        return render(request,'updateprofile.html',{'profile':profile,'form':form})
        
    def post(self,request,**kwargs):
        pid=kwargs.get('id')
        profile=ProfileModel.objects.get(id=pid)
        form_data=ProfileForm(data=request.POST,files=request.FILES)
        if form_data.is_valid():
            profile_pic=form_data.cleaned_data.get('profile_pic')
            username=form_data.cleaned_data.get('username')
            bio=form_data.cleaned_data.get('bio')
            first_name=form_data.cleaned_data.get('first_name')
            last_name=form_data.cleaned_data.get('last_name')
            email=form_data.cleaned_data.get('email')
            phone=form_data.cleaned_data.get('phone')
            profile.profile_pic=profile_pic
            profile.user.username=username
            profile.bio=bio
            profile.user.first_name=first_name
            profile.user.last_name=last_name
            profile.user.email=email
            profile.phone=phone
            profile.save()
            return redirect('profile')
        return render(request,'updateprofile.html',{'form':form_data})


@method_decorator(decorator=dec,name='dispatch')
class PropertyDetailView(DetailView):
    template_name="property_details.html"
    queryset=Property.objects.all()
    context_object_name='property'
    pk_url_kwarg="id"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = ProfileModel.objects.get(user=self.request.user)  # Add the ProfileModel instance to context
        return context

dec
def SaveView(request,**kwargs):
    pid=kwargs.get('id')
    property=Property.objects.get(id=pid)
    property.saved_users.add(request.user)
    return redirect('savelist')


@method_decorator(decorator=dec,name='dispatch')
class SaveList(ListView):
    template_name = 'saved_property.html'
    context_object_name = 'property'

    def get_queryset(self):
        return Property.objects.filter(saved_users=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = ProfileModel.objects.get(user=self.request.user)  # Add the ProfileModel instance to context
        return context

dec  
def RemoveSave(request,**kwargs):
    pid=kwargs.get('id')
    property=Property.objects.get(id=pid)
    property.saved_users.remove(request.user)
    return redirect('savelist')

dec
@login_required
def chat_view(request,id):
    # Get the property and the owner of the property
    receiver = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            message = Message(
                sender=request.user,
                receiver=receiver,
                content=content
            )
            message.save()
            return redirect('chat', id=id)
    else:
        form = MessageForm()

    # Get the messages between the current user and the property owner
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=receiver)) |
        (Q(sender=receiver) & Q(receiver=request.user))
    ).order_by('time')
    re=ProfileModel.objects.get(user=receiver)
    se=ProfileModel.objects.get(user=request.user)
    context = {
        'property': property,
        'messages': messages,
        'form': form,
        'receiver': receiver,
        're': re,
        'se': se,
        'profile':se

    }

    return render(request, 'chat.html', context)

dec
@login_required
def chat_list_view(request):
    # Get messages for the logged-in user
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).distinct()

    # Extract unique users involved in the messages
    user_ids = set()
    for message in messages:
        user_ids.add(message.sender.id)
        user_ids.add(message.receiver.id)
    if request.user.id in user_ids:
        user_ids.remove(request.user.id)
    # Fetch profile models for the unique user IDs
    users = ProfileModel.objects.filter(user__id__in=user_ids).distinct()
    profile=ProfileModel.objects.get(user=request.user)


    context = {
        'users': users,
        'profile': profile,
    }

    return render(request, 'chat_list.html', context)


@method_decorator(decorator=dec,name='dispatch')
class EditProperty(UpdateView):
    template_name='edit_property.html'
    form_class=PropertyForm
    pk_url_kwarg='id'
    queryset=Property.objects.all()
    success_url=reverse_lazy('profile')


@method_decorator(decorator=dec,name='dispatch')
class DeleteProperty(View):
    def get(self,request,**kwargs):
        id=kwargs.get('id')
        data=Property.objects.get(id=id)
        data.delete()
        return redirect('profile')
    
@method_decorator(decorator=dec,name='dispatch')
class ProfiletouserView(View):
    def get(self,request,**kwargs):
        id=kwargs.get('id')
        profile=ProfileModel.objects.get(user=request.user)
        property=Property.objects.get(id=id)
        profile2=property.user
        post=Property.objects.filter(user=property.user)
        print(post)
        total=post.count()
        context = {
        'profile': profile,
        'profile2': profile2,
        'post': post,
        'total': total,
    }
        return render(request,'profile_to_user.html', context)
