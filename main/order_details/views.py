from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Customer, Item, OrderDetail

from django.conf import settings

import json
import os
from django.core.mail import send_mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def order_details_view(request):
    return render(request, 'order_details/order_form.html', {})


def new_user_view(request):
    return render(request, 'order_details/new_user.html', {})


def new_user_loading_view(request):
    pass


def new_user_submit_view(request):
    # check if the user already exists using his phone number
    context = {}
    try:
        # user already exists but is trying to act smart
        ph = request.POST['phone']
        q = Customer.objects.get(phone=ph)
        context['customer'] = q
        m = Item.objects.all()
        context['menu'] = m
        context['is_existing'] = True
        request.session['cust'] = q.name
        request.session['email'] = q.email
        request.session['phone'] = q.phone
        return render(request, 'order_details/order_form.html', context)
    except:
        # user is genuinely visiting the first time
        c = Customer()
        c.name = request.POST['name']
        c.phone = request.POST['phone']
        c.email = request.POST['email']
        c.save()
        m = Item.objects.all()
        context['customer'] = c
        context['menu'] = m
        request.session['cust'] = request.POST['name']
        request.session['email'] = request.POST['email']
        request.session['phone'] = request.POST['phone']
        return render(request, 'order_details/order_form.html', context)

    # context = {}
    # c = Customer()
    # c.name = request.POST['name']
    # c.phone = request.POST['phone']
    # c.email = request.POST['email']
    # c.save()
    # m = Item.objects.all()
    # # context = {
    # #     'customer': c,
    # #     'menu': m,
    # # }
    # context['customer'] = c
    # context['menu'] = m
    # return render(request, 'order_details/order_form.html', context)


def existing_user_check_view(request):
    return render(request, 'order_details/existing_check.html', {})


def is_existing(request):
    context = {}
    # q = Customer.objects.get(phone=ph)
    try:
        ph = request.POST['phone']
        # print(ph)
        # print('hello')
        q = Customer.objects.get(phone=ph)
        # print('hello')
        # print(q)
        context['customer'] = q
        m = Item.objects.all()
        context['menu'] = m
        # print("success")
        context['is_existing'] = False
        request.session['cust'] = q.name
        request.session['email'] = q.email
        request.session['phone'] = q.phone
        return render(request, 'order_details/order_form.html', context)
    except:
        # print('hello2')
        context['is_existing'] = True
        return render(request, 'order_details/new_user.html', context)
        # raise Http404("No MyModel matches the given query.")

    # if q:
    #     context['customer'] = q
    #     m = Item.objects.all()
    #     context['menu'] = m
    #     return render(request, 'order_details/order_form.html', context)
    # else:
    #     return render(request, 'order_details/new_user.html', context)


def order_summary_view(request):
    items = Item.objects.all()
    items_count = items.__len__()
    context = {}
    user_items = []
    total = 0
    for i in range(items_count):
        t = str(i)
        q = 'qty'+str(i)
        if request.POST.get(t, False):
            temp = {
                "name": items[i].name,
                "price": items[i].price,
                "quantity": request.POST.get(q, 1)
            }
            user_items.append(temp)
            q = int(temp["quantity"])
            print('quantity: ', q)

            if q >= 0:
                total = total + (items[i].price * q)
            else :
                total = total + items[i].price
    context["user_items"] = user_items
    context["user_name"] = str(request.session.get('cust'))
    context["total"] = total

    # add transactional data to the database
    add_data(str(request.session.get('phone')), user_items)

    send_email(str(request.session.get('email')), user_items, str(request.session.get('cust')), total)

    return render(request, 'order_details/order_summary.html', context)


# function to add transactional data in the database
def add_data(phone, order_dict_list):
    q = Customer.objects.get(phone=phone)
    my_dict = {
        "order": order_dict_list,
    }
    order = OrderDetail(phone=q, order=json.dumps(my_dict))
    order.save()


def send_email(to_email, body, user_name, total):
    message_body = generate_email_body(body=body, total=total)
    data = []
    with open('apikey.txt') as file:
        for line in file:
            data.append(line.rstrip())
    api_key = data[0]
    message = Mail(
        from_email='amit251098@gmail.com',
        to_emails=to_email,
        subject='Here is your Simply Coffee Order Summary!',
        html_content=message_body)
    try:
        # sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)


def generate_email_body(body, total):
    part1 = '<!DOCTYPE html><html><head></head><body><center><h1>Your Simply Coffee Order Summary</h1><table><thead ><tr> <th style="border: 1px solid black; padding: 10px;">#</th> <th style="border: 1px solid black; padding: 10px;">Item</th> <th style="border: 1px solid black; padding: 10px;">Quantity</th> <th style="border: 1px solid black; padding: 10px;">Price</th> </tr></thead><tbody>'
    part2 = '</tbody></table><h2>Total Payable: '+str(total)+'</h2></div><p>&#169; 2020 Simply Coffee, Inc.</p></center></body></html>'
    rows = ''
    count = 0
    for item in body:
        count = count+1
        new_row = '<tr> <th style="border: 1px solid black; padding: 10px;">'+str(count)+'</th> <td style="border: 1px solid black; padding: 10px;">'+item["name"]+'</td><td style="border: 1px solid black; padding: 10px;">'+item["quantity"]+'</td> <td style="border: 1px solid black; padding: 10px;">'+str(item["price"])+'</td> </tr>'
        rows = rows+new_row
    message = part1+rows+part2
    print(message)
    return message
