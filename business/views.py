from django.shortcuts import render
from user_auth.models import *
from business.models import *
from user_auth.decorators import business_required
import csv,io,datetime
from django.contrib import messages

# Create your views here.


@business_required
def collaberate_home(request):
    template = 'business/collaberate_home.html'
    return render(request,template)

@business_required
def coupon_upload(request):
    template = "business/limited_coupons.html"
    if request.method == 'POST':
        csv_file = request.FILES['file']
        banner = request.FILES['banner']
        if not csv_file.name.endswith('.csv'):
            print('mesage_created')
            messages.error(request,'This file is not csv, please upload a csv file')
            return render(request, template)

        coupon_data = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(coupon_data)
        reader = csv.reader(io_string, delimiter = ',')
        header = next(reader)

        if header[0] != 'Coupon code' or header[1] != 'Start date' or header[2] != 'Expiry date' or header[3] != 'Discription' :
            messages.error(request, 'The CSV file is not same as preview file')
            return render(request, template)

        coupon_ids=[]
        for coulmn in reader:
            start_date = coulmn[1] + ' 00:00:00'
            start_date = datetime.datetime.strptime(start_date, '%d-%m-%y %H:%M:%S')
            expiry_date = coulmn[2]+ ' 00:00:00'
            expiry_date = datetime.datetime.strptime(expiry_date, '%d-%m-%y %H:%M:%S')
            coupon = Limited_Offer_Coupons(coupon_code = coulmn[0],start_date = start_date, expiry_date = expiry_date, discription = coulmn[3]).save()
            print("\nCoupon",coupon)
            print(coupon['id'])
            coupon_ids.append(coupon['id'])
        print(coupon_ids)
        created_user = User.objects.get(email=request.session["username"])["id"]
        created_date = datetime.datetime.now()
        LO_instance = Limited_Offer(created_date=created_date,created_user=created_user,offer_count=len(coupon_ids),coupons=coupon_ids).save()
        LO_instance.banner_image.put(banner, content_type='image/jpeg')
        LO_instance.save()
        messages.success(request,'File sucessfully uploaded')
        return render(request,template)
    else:
        return render(request,template)

@business_required
def perminent_coupons(request):
    template = 'business/perminent_coupons.html'
    if request.method == 'POST':
        print('\nrequest\n',request.POST,'\n')
        if 'code' in request.POST and 'banner' in request.FILES and 'discription' in request.POST:
            coupon_code = request.POST['code']
            banner = request.FILES['banner']
            discription = request.POST['discription']
            created_user = User.objects.get(email=request.session["username"])["id"]
            created_date = datetime.datetime.now()
            model_instance = Unlimited_Coupons(coupon_code=coupon_code,created_user=created_user,created_date=created_date,discription=discription ).save()
            model_instance.banner_image.put(banner,content_type='image/jpeg')
            model_instance.save()
            messages.success(request,'Coupon sucessfully added')
            return render(request,template)
        else:
            messages.error(request,'Please fill all the feilds')
            return render(request,template)
    else:
        return render(request,template)