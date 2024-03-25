from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required

from events.models import Bookings, Contact, Packages, UserProfile


# Create your views here.

def home(request):
    return render(request, 'home.html')





def register(request):
    if request.method == 'POST':
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")
        username = request.POST.get("username")
        department = request.POST.get("department")
        class_year = request.POST.get("class")
        PRN = request.POST.get("PRN")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect("register")
        
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=firstname,
                last_name=lastname
            )
            # Additional fields
            UserProfile.objects.create(
                user=user,
                department=department,
                class_name=class_year,
                prn_number=PRN
            )
            messages.success(request, 'Your account has been created successfully!')
            return redirect("/")
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect("register")
            
    return render(request, "register.html")


def loginuser(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in successfully!') 
            return redirect("/")
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect("login")
    return render(request, "login.html")

# logout user view
@login_required(login_url='/login/')
def logoutuser(request):
        logout(request)
        messages.success(request, 'You have been logged out successfully!')

        return redirect("/")





def about(request):
    return render(request, 'about.html')

@login_required(login_url='/login/')
def contact(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        if name and email and message:
            Contact.objects.create(
                name=name,
                email=email,
                message=message
            )
            messages.success(request, 'Your message has been sent successfully!')
        else:
            messages.error(request, 'All fields are required!')
    return render(request, 'contact.html')






def packages(request):
    packages = Packages.objects.all()
    return render(request, 'packages.html' ,{'packages':packages})

@login_required
def profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = None

    booking_history = Bookings.objects.filter(user=request.user)

    if request.method == 'POST':
        # Update user's first name and last name
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.save()
        messages.success(request, 'Profile updated successfully!')

        # Update UserProfile fields
        if not profile:
            profile = UserProfile(user=request.user)

        profile.department = request.POST.get('department')
        profile.class_name = request.POST.get('class_name')
        profile.prn_number = request.POST.get('prn_number')
        profile.save()
        messages.success(request, 'Profile updated successfully!')

        return redirect('profile')

    context = {'profile': profile, 'booking_history': booking_history}
    return render(request, 'profile.html', context)

@login_required(login_url='/login/')
def book_view(request):
    if request.method == 'POST':
        package_id = request.POST.get('package')
        package = Packages.objects.get(pk=package_id)
        
        # Initialize a dictionary to store selected options
        selected_options = {}

        # Iterate over request.POST to collect selected options
        for key, value in request.POST.items():
            if key != 'package' and value:
                selected_options[key] = value

        # Retrieve additional fields from the form
        name = request.POST.get('name')
        class_year = request.POST.get('class')
        department = request.POST.get('department')
        mobile_number = request.POST.get('mobile_number')
        datetime = request.POST.get('datetime')

        # Create a new Booking object and save it to the database
        booking = Bookings(
            user=request.user,
            package=package,
            options=selected_options,
            name=name,
            class_year=class_year,
            department=department,
            mobile_number=mobile_number,
            datetime=datetime
        )
        booking.save()

        # Redirect to a confirmation page or any other appropriate URL
        return redirect('profile')

    # If the request method is GET, render the book.html template with package options
    packages = Packages.objects.all()
    context = {'packages': packages}
    return render(request, 'book.html', context)


def get_package_options(request, package_id):
    # Retrieve the package object from the database
    package = get_object_or_404(Packages, pk=package_id)

    # Construct a dictionary of options for the package
    options = {
        'venues': package.venue.split(','),
        'themes': package.theme.split(','),
        'games': package.games.split(','),
        'cards': package.cards.split(','),
        'gifts': package.gifts.split(','),
        'food': package.food.split(','),
    }

    # Return the options as JSON response
    return JsonResponse(options)


