from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from myapp.models import MarketPrice,ServiceRequest,UploadBlueprints,BookRequest,ContractorRequest,SaleHouse, HouseImage,Labour,UserLogin,UserProfile, UserRegistration,ContractorInfo  # and others as needed
import random

def index(request):
    return render(request,'index.html')

def admin_dashboard(request):
    return render(request,'admin_dashboard.html')

def labour_dashboard(request):
    return render(request,'labour_dashboard.html')

def contractor_dashboard(request):
    return render(request,'contractor_dashboard.html')

def user_dashboard(request):
    return render(request,'user_dashboard.html')


from django.contrib.auth import logout


def logout_view(request):
    logout(request)   # Django logout
    request.session.flush()   # clear session
    messages.success(request, "Logged out successfully.")
    return redirect('login')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('email')  # assuming email is the username
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)  # logs in the user
            request.session['username'] = username  # ✅ SET SESSION HERE

            # Optional: fetch user type (if using UserLogin table)
            try:
                user_type = UserLogin.objects.get(username=username).utype
                if user_type == 'contractor':
                    return redirect('contractor_dashboard')
                elif user_type == 'labour':
                    return redirect('labour_dashboard')
                elif user_type == 'user':
                    return redirect('user_dashboard')
                else:
                    return redirect('admin_dashboard')
            except UserLogin.DoesNotExist:
                messages.warning(request, "User type not found.")
                return redirect('login')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')

    return render(request, 'login.html')


def reg(request):
    if request.method == "POST":
        user_type = 'user'
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        city = request.POST.get('city')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'reg.html', {'error': 'Passwords do not match!'})

        if User.objects.filter(username=email).exists():
            return render(request, 'reg.html', {'error': 'Email is already registered!'})

        # Step 1: Create the Django User
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )

        # Step 2: Save additional user profile info
        UserRegistration.objects.create(
            user=user,  # This is a User object now
            first_name=first_name,
            last_name=last_name,
            city=city,
            address=address,
            pincode=pincode,
            contact=contact
        )

        #Step 3: Save role-specific login info (optional)
        UserLogin.objects.create(
            username=email,
            password=make_password(password1),
            utype=user_type
        )

        UserProfile.objects.create(
            user=user
        )

        return render(request, 'reg.html', {'success': 'Thank you for the registration!'})

    return render(request, 'reg.html')



def add_contractor(request):
    if request.method == 'POST':
        contractor_name = request.POST.get('contractor_name')
        experience = request.POST.get('experience')
        city = request.POST.get('city')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        document = request.FILES.get('document')

        ContractorInfo.objects.create(
            contractor_name=contractor_name,
            experience=experience,
            city=city,
            address=address,
            contact=contact,
            email=email,
            document=document
        )

        return render(request, 'add_contractor.html', {'success': 'Registered successfully!'})
    return render(request,'add_contractor.html')


def contractor_view(request):
    udata=ContractorInfo.objects.all()
    return render(request,'contractor_view.html',{'udata':udata})

def add_labour(request):
    if request.method == "POST":
        Labour.objects.create(
            labour_head=request.POST.get('labour_head'),
            city=request.POST.get('city'),
            address=request.POST.get('address'),
            number_of_workers=request.POST.get('number_of_workers'),
            mobile_no=request.POST.get('mobile_no')
        )
        return render(request, 'add_labour.html', {'success': 'Labour details registered successfully!'})

    return render(request, 'add_labour.html')

def labour_view(request):
    udata = Labour.objects.all()
    return render(request,'labour_view.html',{'udata':udata})






def estimation(request, house):
    if request.method == 'POST':
        bhk_type = request.POST.get('bhk')
        size = request.POST.get('size')

        try:
            size = int(size)
        except (TypeError, ValueError):
            return render(request, 'estimation.html', {
                'house': house,
                'error': 'Invalid size. Please enter a valid number.'
            })

        # Randomly generate realistic cost per sqft
        rates = {
            'foundation': random.randint(180, 250),
            'walls': random.randint(120, 180),
            'plastering': random.randint(80, 120),
            'painting': random.randint(60, 100),
            'cement_per_sqft': random.randint(40, 70),
            'tiles': random.randint(100, 150),
        }

        breakdown = {
            'Foundation': rates['foundation'] * size,
            'Walls': rates['walls'] * size,
            'Plastering': rates['plastering'] * size,
            'Painting': rates['painting'] * size,
            'Cement': rates['cement_per_sqft'] * size,
            'Tiles': rates['tiles'] * size,
        }

        total_cost = sum(breakdown.values())

        context = {
            'bhk_type': bhk_type,
            'size': size,
            'total_cost': total_cost,
            'rates': rates,
            'breakdown': breakdown
        }
        return render(request, 'estimate_result.html', context)

    return render(request, 'estimation.html', {'house': house})




def vr_view(request, bhk_type):
    bhk_type = bhk_type.upper()

    if bhk_type == '1BHK':
        model_type = '1bhk_flat.glb'
    elif bhk_type == '2BHK':
        model_type = '2bhk_flat_interior.glb'
    elif bhk_type == '3BHK':
        model_type = '3bhk_villa.glb'
    else:
        model_type = '2bhk_flat_interior.glb'  # Default

    return render(request, 'vr_view.html', {'model_type': model_type,'bhk_type':bhk_type})




def sale_house(request):
    username = request.session.get('username')

    if not username:
        messages.error(request, "You must be logged in to post a house.")
        return redirect('login')

    if request.method == "POST":
        images = request.FILES.getlist('images')

        if not images:
            return render(request, 'sales_house.html', {'username': username, 'error': 'Please upload at least one image.'})

        house = SaleHouse.objects.create(
            house_type=request.POST.get('house_type'),
            area=request.POST.get('area'),
            city=request.POST.get('city'),
            address=request.POST.get('address'),
            facilities=request.POST.get('facilities'),
            cost=request.POST.get('cost'),
            sale_status=request.POST.get('sale_status'),
            added_by=username
        )

        for image in images:
            HouseImage.objects.create(house=house, image=image)

        return render(request, 'sales_house.html', {
            'username': username,
            'msg': 'Created Successfully'
        })

    return render(request, 'sales_house.html', {'username': username})



def sale_house_view(request):
    houses = SaleHouse.objects.all().prefetch_related('images')  # Optimized fetch
    return render(request, 'sale_house_view.html', {'houses': houses})


def sale_house_del(request,pk):
    data=SaleHouse.objects.get(id=pk)
    data.delete()
    return redirect('sales_house_view')


def contra_req_view(request):
    uid=request.session['username']
    udata = ServiceRequest.objects.filter(contractor=uid).values()
    return render(request, 'contra_req_view.html', {'udata': udata})

def book_request_view(request):
    username=request.session['username']
    userdict = BookRequest.objects.filter(contractor=username).values()
    return render(request, 'book_request_view.html', {'udata': userdict})

def update_sale_status(request,pk):
    if request.method=="POST":
        status=request.POST.get('status')
        BookRequest.objects.filter(id=pk).update(sale_status=status)
        return redirect('book_request_view')
    return render(request,'update_sale_status.html')

def market_price(request):
    if request.method=="POST":
        raw_material=request.POST.get('material_name')
        company_name = request.POST.get('company_name')
        uom = request.POST.get('uom')
        cost = request.POST.get('cost')
        size = request.POST.get('size')

        MarketPrice.objects.create(raw_material=raw_material,company_name=company_name,uom=uom,cost=cost,size=size)
        return render(request,'market_price.html',{'msg':'added successfully'})

    return render(request,'market_price.html')


def view_contractors(request):
    data=ContractorInfo.objects.all()
    return render(request,'view_contractors.html',{'data':data})

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from datetime import date

def service_request(request, pk):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    contractor_info = get_object_or_404(ContractorInfo, id=pk)
    contractor_email = contractor_info.email

    if request.method == "POST":
        message = request.POST.get('message')
        ServiceRequest.objects.create(
            user_id=username,
            contractor=contractor_email,
            message=message,
            request_date=date.today(),
            request_status='pending'
        )
        messages.success(request, 'Request has been sent successfully.')
        return redirect('service_request', pk=pk)

    return render(request, 'service_request.html', {'contractor': contractor_info})


def service_status_view(request):
    username=request.session['username']
    data=ServiceRequest.objects.filter(user_id=username).values()
    return render(request,'service_status_view.html',{'data':data})




def house_book_request(request, pk):
    username = request.session.get('username')

    if not username:
        messages.error(request, "Please log in to book a house.")
        return redirect('login')  # Update to your actual login route

    # Get the SaleHouse instance
    house = get_object_or_404(SaleHouse, id=pk)
    contractor = house.added_by

    # Check if the user already made a booking request
    if BookRequest.objects.filter(house=house, user=username).exists():
        messages.info(request, "You have already sent a request for this house.")
    else:
        # Pass the house instance, not the ID
        BookRequest.objects.create(house=house, user=username, contractor=contractor)
        messages.success(request, "Request has been sent successfully.")

    return redirect('sale_house_view_u')



def sale_house_view_u(request):
    data=SaleHouse.objects.all()
    return render(request, 'sale_house_view_u.html', {'houses': data})


def book_request_status(request):
    username=request.session['username']
    data=BookRequest.objects.filter(user=username).values()
    return render(request,'book_request_status.html',{'udata':data})


def market_price_view_u(request):
    data=MarketPrice.objects.all()
    return render(request,'market_price_view_u.html',{'data':data})

def market_price_view(request):
    data=MarketPrice.objects.all()
    return render(request,'market_price_view.html',{'data':data})


def upload_blue_print(request):
    if request.method == "POST":
        construction_type = request.POST.get('construction_type')
        blueprint_title = request.POST.get('blueprint_title')
        approx_cost = request.POST.get('approx_cost')
        image_1 = request.FILES.get('image_1')
        image_2 = request.FILES.get('image_2')

        UploadBlueprints.objects.create(
            construction_type=construction_type,
            blueprint_title=blueprint_title,
            approx_cost=approx_cost,
            image_1=image_1,
            image_2=image_2
        )

        return render(request, 'upload_blue_print.html', {'msg': 'Blueprint uploaded successfully'})

    return render(request, 'upload_blue_print.html')


def upload_blue_print_view(request):
    data=UploadBlueprints.objects.all()
    return render(request,'upload_blue_print_view.html',{'data':data})


def blueprint_del(request,pk):
    data=UploadBlueprints.objects.get(id=pk)
    data.delete()
    return redirect('upload_blue_print_view')


def labours_view(request):
    data=Labour.objects.all()
    return render(request,'labours_view.html',{'data':data})


def contractor_del(request,pk):
    data=ContractorInfo.objects.get(id=pk)
    email=data.email
    n=UserLogin.objects.get(email=email)
    n.delete()
    data.delete()
    return redirect('contractor_view')

def labour_del(request,pk):
    data=Labour.objects.get(id=pk)
    data.delete()
    return redirect('labour_view')

def market_del(request,pk):
    data=MarketPrice.objects.get(id=pk)
    data.delete()
    return redirect('market_price_view')




def update_service_status(request,pk):
    if request.method=="POST":
        reply = request.POST.get('reply')
        ServiceRequest.objects.filter(id=pk).update(reply=reply)
        return redirect('contra_req_view')
    return render(request,'update_service_status.html')

