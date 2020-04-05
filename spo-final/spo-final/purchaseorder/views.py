from django.shortcuts import render
from .models import order
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from datetime import datetime
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from pathlib import Path

# Create your views here.

def home(response):
     context = {
        'orders': order.objects.all()
     }
     return render(response, 'purchaseorder/home.html', context)


def about(response):

    return render(response, 'purchaseorder/about.html',{'title': 'About'})


class orderListView(ListView):
    model = order
    template_name = 'purchaseorder/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'orders'
    ordering = ['-date_ordered']


class orderDetailView(UserPassesTestMixin,DetailView):
    model = order

    def test_func(self):
        order = self.get_object()
        if self.request.user == order.author:
            return True
        elif self.request.user.is_supervisor:
            return True
        elif self.request.user.is_purchasing:
            return True
        else:
            return False


class orderCreateView(CreateView):
    model = order
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class orderUpdateView(UserPassesTestMixin, UpdateView):
    model = order
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        order = self.get_object()
        if self.request.user == order.author:
            return True
        elif self.request.user.is_supervisor:
            return True
        elif self.request.user.is_purchasing:
            return True
        else:
            return False


class orderDeleteView(UserPassesTestMixin, DeleteView):
    model = order
    success_url = '/'
    def test_func(self):
        order = self.get_object()
        if self.request.user == order.author:
            return True
        elif self.request.user.is_supervisor:
            return True
        elif self.request.user.is_purchasing:
            return True
        else:
            return False

class orderApproveView(UserPassesTestMixin, DetailView):
    model = order
    #model.approve()
    def test_func(self):
        order = self.get_object()
        if self.request.user == order.author:
            return False
        elif self.request.user.is_supervisor and not order.approved:
            # set status to signed
            order.approved = True
            order.dateApproved = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            order.approvedBy = str(self.request.user.username)

            # create a signature to verify the signing
            key = RSA.importKey(open('supervisor.pem').read())
            h = SHA256.new(order.content)
            signer = PKCS1_v1_5.new(key)
            order.signedSupervisor = signer.sign(h)
            #save changes
            order.save(update_fields=['approved','dateApproved','approvedBy', 'signedSupervisor'])
            return True
        else:
            return False

class orderPurchaseView(UserPassesTestMixin, DetailView):
    model = order
    
    def test_func(self):
        order = self.get_object()
        if self.request.user == order.author:
            return False
        elif self.request.user.is_purchasing and not order.purchased:
            # Set signed status
            order.purchased = True
            order.datePurchased = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            order.purchasedBy = str(self.request.user.username)

            # create a signature to verify the signing 
            key = RSA.importKey(open('purchasing.pem').read())
            h = SHA256.new(order.content)
            signer = PKCS1_v1_5.new(key)
            order.signedPurchase = signer.sign(h)

            #save changes, django convention
            order.save(update_fields=['purchased','datePurchased', 'purchasedBy', 'signedPurchase'])
            return True
        else:
            return False
