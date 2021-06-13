from django.shortcuts import render,redirect
from django.contrib.auth.models import auth,User
from .models import Admin,Train,AppUser,Transaction
from django.contrib import messages
from .forms import updateTrainsForm
from django.forms import formset_factory
from django.conf import settings
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def Welcome(request):
    return render(request,"Welcome.html")
def AdminLogin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        Admin_cred=Admin.objects.all()
        for user in Admin_cred:
            if username==user.username:
                if password==user.password:
                    Train_data = Train.objects.all().order_by("starttime")
                    return render(request,"AdminOptions.html",{"name":user.name,"Train_data":Train_data})
                else:
                    messages.add_message(request, messages.INFO, 'Invalid credentials')

    return render(request,"AdminLogin.html")
def AdminOptions(request):
    Train_data = Train.objects.all().order_by("starttime")
    return render(request,"AdminOptions.html",{"Train_data":Train_data})

def UpdateTrains(request):
    Train_data = Train.objects.all().order_by("starttime")
    if request.method=='POST':
        id=request.POST["trainid"]
        name=request.POST["trainname"]
        status=request.POST["status"]
        source=request.POST["source"]
        dest=request.POST["destination"]
        start=request.POST["starttime"]
        end=request.POST["endtime"]
        totalseats=request.POST.get("totalseats")
        filled=request.POST.get("filled")
        
        if totalseats!=None and filled!=None:
            try:
                train=Train.objects.get(trainid=id)
                train.trainid=id
                train.trainname=name
                train.status=status
                train.source=source
                train.destination=dest
                train.starttime=start
                train.endtime=end
                train.totalseats=totalseats
                train.filled=filled
                train.save()
            except:
                train=Train()
                train.trainid=id
                train.trainname=name
                train.status=status
                train.source=source
                train.destination=dest
                train.starttime=start
                train.endtime=end
                train.totalseats=totalseats
                train.filled=filled
                train.save()

        
    return render(request,"UpdateTrains.html",{"Train_data":Train_data})

def AddAdmin(request):
    if request.method=='POST':
        passwd = request.POST['password']
        confpwd = request.POST['confirmpassword']
        if passwd == confpwd:
                new_admin=Admin()
                new_admin.name= request.POST.get('name')
                new_admin.username= request.POST.get('username')
                new_admin.password= request.POST.get('password')
                new_admin.save()
                messages.add_message(request, messages.INFO, 'ADDED ADMIN SUCCESSFULLY!!')
                
                return render(request, 'AddAdmin.html')  
        else:
            messages.add_message(request, messages.INFO, 'Password missmatch!!')

    return render(request,"AddAdmin.html")

def UserLogin(request):
    if request.method=="POST":
        username = request.POST["username"]
        passwd = request.POST["password"]
        try:
            user = AppUser.objects.get(username=username)
            if user!=None:
                if user.username==username and user.password==passwd:
                    Traindata = Train.objects.filter(status="Running")
                    return render(request,"Trainlist.html",{"Traindata":Traindata})
                else:
                    messages.add_message(request, messages.INFO, 'Invalid credentials')
        except Exception as e:
            print(e)
            messages.add_message(request, messages.INFO,"Your account doesn't exist.")

        return render(request,"UserLogin.html")

    else:
        return render(request,"UserLogin.html")


def UserRegister(request):
    if request.method=='POST':
        try:
            email=request.POST['email']
            user = AppUser.objects.get(email=email)
            if user!=None:
                messages.add_message(request,messages.INFO,"Email already exists!")
        except:
            try:
                username = request.POST["username"]
                user = AppUser.objects.get(username=username)
                if user!=None:
                    messages.add_message(request,messages.INFO,"Username Already Taken!")
            except:
                password=request.POST["password"]
                confpassword=request.POST["confirmpassword"]
                if password==confpassword:
                    user=AppUser()
                    user.name=request.POST["name"]
                    user.username=request.POST["username"]
                    user.password=password
                    user.email=request.POST["email"]
                    user.phone=request.POST["phonenumber"]
                    user.save()
                    messages.add_message(request, messages.INFO, 'User Registered!! Login now')
                else:
                    messages.add_message(request, messages.INFO, 'Password missmatch!!')

    return render(request,"UserRegistration.html")


def Trainlist(request):
        Traindata = Train.objects.filter(status="Running")
        return render(request,"Trainlist.html",{"Traindata":Traindata})
def BookTickets(request):
    Traindata = Train.objects.filter(status="Running")
    if request.method=="POST":
        id=request.POST.get("trainid")
        no_of_seats=request.POST.get("seats")
        print(id,no_of_seats)
        try:
            train = Train.objects.get(trainid=id)
            return render(request,"Payment.html",{"id":id,"no_of_seats":no_of_seats})
        except Exception as e:
            messages.add_message(request,messages.INFO,"Train Doesn't Exist!")


    return render(request,"BookTickets.html",{"Traindata":Traindata})
def Payment(request):
     return render(request,"Payment.html")



def initiate_payment(request):
    transaction = Transaction.objects.create(made_by=user, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'payments/redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'Callback.html', context=received_data)
        return render(request, 'Callback.html', context=received_data)
