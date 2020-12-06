from os import name
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail


# Create your views here.

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']



        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id= listing_id, user_id = user_id)
            if has_contacted:
                messages.error(request, 'You have already contacted dude relax')
                return redirect('/listings/' + listing_id)

        contact = Contact(listing=listing, listing_id= listing_id, name= name, email= email, phone= phone, messages = message, user_id = user_id)
        contact.save()

        # send email
        send_mail(
            'Property Listin Inquiry',
            'There has been an inquiry for ' + listing + '. Sign into the admin panel for more info',
            'yourmail@mail.com',
            [realtor_email, 'yourmail@mail.com'],
            fail_silently=True
        )

        messages.success(request, 'your message sent to realtor, we will contact to you soon')
        return redirect('/listings/'+listing_id)

