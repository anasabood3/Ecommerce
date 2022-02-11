from django.contrib.admin.views.decorators import staff_member_required
from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse, reverse_lazy
from django.views.generic import ListView,UpdateView,DeleteView,CreateView
from django.views.generic.base import View

import management
from .forms import *
from store.models import Category, Product, ProductSpecification, ProductType,Offer
from django.contrib import messages

#---------------Listing Items---------------

#List Products
class ProductListView(ListView):
    model = Product
    paginate_by = 2
    context_object_name = 'products'
    template_name = 'management/product_list.html'
    
#List Categories
class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'management/category_list.html'

#List Products
class ProductTypeListView(ListView):
        model = ProductType
        context_object_name = 'product_types'
        template_name = 'management/product_type_list.html'

#List Offers
class OfferListView(ListView):
        model = Offer
        context_object_name = 'offers'
        template_name = 'management/offers_list.html'

#---------------Editing Items---------------
#Category Edit Generic Class Based
class CategoryEditView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'management/edit_category.html'



#Product Edit Class Based
class ProductEditView(View):
    template = 'management/edit_product.html'
    def get(self,request,slug,*args, **kwargs):
        product = get_object_or_404(Product,slug=slug)
        product_form = ProductForm(instance=product)
        specs_formset = ProductSpecsFormset(instance=product,prefix='specs')
        images_formset = ProductImagesFormset(instance=product,prefix='images')
        context = {'product_form':product_form,'specs_formset':specs_formset,'images_formset':images_formset}
        return render(request,self.template,context)

    def post(self,request,slug,*args, **kwargs):
        product = get_object_or_404(Product,slug=slug)
        product_form = ProductForm(request.POST,instance=product)
        specs_formset = ProductSpecsFormset(request.POST,instance=product,prefix='specs')
        images_formset = ProductImagesFormset(request.POST,request.FILES,instance=product,prefix='images')
        if product_form.is_valid() and specs_formset.is_valid() and images_formset.is_valid():
            product_form.save()
            specs_formset.save()
            images_formset.save()
            messages.success(request,"Changes were saved successfully")
            return redirect(product)
        context = {'product_form':product_form,'specs_formset':specs_formset,'images_formset':images_formset}
        return render(request,self.template,context)

class ProductTypeEditView(View):
    template = 'management/product_type_edit.html'
    def get(self,request,product_type_id,*args, **kwargs):
        product_type = get_object_or_404(ProductType,pk=product_type_id)
        product_type_form = ProductTypeForm(instance=product_type)
        specs_formset = ProductTypeFormset(instance=product_type,prefix='specs')
        context = {'product_type_form':product_type_form,'product_specs_formset':specs_formset}
        print("get again")
        return render(request,self.template,context)

    def post(self,request,product_type_id,*args, **kwargs):
        print("post again")
        product_type = get_object_or_404(ProductType,pk=product_type_id)
        product_type_form = ProductTypeForm(request.POST,instance=product_type)
        specs_formset = ProductTypeFormset(request.POST,instance=product_type,prefix='specs')
        if product_type_form.is_valid() and specs_formset.is_valid():
            product_type_form.save()
            specs_formset.save()
            messages.success(request,"Changes were saved successfully")
        context = {'product_type_form':product_type_form,'product_specs_formset':specs_formset}
        return render(request,self.template,context)


#Offer Edit using Generic View
class OfferEditView(UpdateView):
    model = Offer
    form_class = OfferForm
    success_url = reverse_lazy('management:offers')
    template_name = 'management/edit_offer.html'
#---------------Creating Items----------------
#Creat category
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'management/edit_category.html'

    def form_valid(self, form):
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'Category has been successfully added'
        )
        return super().form_valid(form)

#Create product
@staff_member_required
def create_product(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST)
        specs_formset = ProductSpecsFormset(request.POST,instance=product_form.instance,prefix='specs')
        images_formset = ProductImagesFormset(request.POST,request.FILES,instance=product_form.instance,prefix='images')

        if product_form.is_valid():
            if specs_formset.is_valid() and images_formset.is_valid():
                product_form.save()
                specs_formset.save()
                images_formset.save()
                messages.success(request,"Changes were saved successfully")
    else:
        product_form = ProductForm()
        specs_formset = ProductSpecsFormset(prefix='specs')
        images_formset = ProductImagesFormset(prefix='images')
    return render(request, "management/edit_product.html", {"product_form": product_form,'specs_formset':specs_formset,'images_formset':images_formset})


class ProductTypeCreateView(CreateView):
    form_class = ProductTypeForm
    template_name = 'management/product_type_edit.html'

    def get_context_data(self, **kwargs):
        context = super(ProductTypeCreateView, self).get_context_data(**kwargs)
        context['product_specs_formset'] = ProductTypeFormset()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        product_specs_formset = ProductTypeFormset(self.request.POST)
        if form.is_valid() and product_specs_formset.is_valid():
            return self.form_valid(form, product_specs_formset)
        else:
            return self.form_invalid(form, product_specs_formset)
    
    def form_valid(self, form, product_specs_formset):
        self.object = form.save(commit=False)
        self.object.save()
        # saving ProductMeta Instances
        product_specs = product_specs_formset.save(commit=False)
        for meta in product_specs:
            meta.product_type = self.object
            meta.save()
        

        return redirect(reverse("management:product_types"))

    def form_invalid(self, form, product_specs_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  product_meta_formset=product_specs_formset
                                  )
        )

#Create Offer
class OfferCreateView(CreateView):
    model = Offer
    form_class = OfferForm
    template_name = 'management/edit_offer.html'
    success_url = reverse_lazy('management:offers')

    def form_valid(self, form):
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'Offer has been successfully added'
        )
        return super().form_valid(form)

#---------------Deleting Items----------------
#Delete Product
class ProductDeleteView(DeleteView):
    model = Product
    success_url = '/'
    template_name = 'management/delete_item.html'
    def form_valid(self, form):
        messages.add_message(
            self.request, 
            messages.ALERT,
            'Product has been successfully Deleted'
        )
        return super().form_valid(form)

#Delete Category
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'
    template_name = 'management/delete_item.html'
    def form_valid(self, form):
        messages.add_message(
            self.request, 
            messages.ALERT,
            'Category has been successfully Deleted'
        )
        return super().form_valid(form)

#Delete Product Type
class ProductTypeDeleteView(DeleteView):
    model = ProductType
    success_url = '/'
    template_name = 'management/delete_item.html'
    pk_url_kwarg = "product_type_id"
    def form_valid(self, form):
        messages.add_message(
            self.request, 
            messages.ALERT,
            'Category has been successfully Deleted')
        return super().form_valid(form)

class OfferDeleteView(DeleteView):
    model = Offer
    success_url = '/'
    template_name = 'management/delete_item.html'
    def form_valid(self, form):
        messages.add_message(
            self.request, 
            messages.ALERT,
            'Offer has been successfully Deleted')
        return super().form_valid(form)








# ---------------------------------------------------------------------------------------------------
# #Product Edit Function Based
# @staff_member_required
# def edit_product(request,slug):
#     product = get_object_or_404(Product, slug=slug)
#     if request.method == "POST":
#         product_form = ProductForm(request.POST,instance=product)
#         specs_formset = ProductSpecsFormset(request.POST,instance=product,prefix='specs')
#         image_formset = ProductImagesFormset(request.POST,request.FILES,instance=product,prefix='images')
#         if product_form.is_valid() and specs_formset.is_valid() and image_formset.is_valid():
#             product_form.save()
#             specs_formset.save()
#             image_formset.save()
#             messages.success(request,"Changes were saved successfully")
#     else:
#         product_form = ProductForm(instance=product)
#         specs_formset = ProductSpecsFormset(instance=product,prefix='specs')
#         image_formset = ProductImagesFormset(instance=product,prefix='images')
#     return render(request, "management/edit_product.html", {"product_form": product_form,'specs_formset':specs_formset,'image_formset':image_formset})

#Product Edit Generic Class Based
# class ProductEditView(UpdateView):
#     model = Product
#     form_class = ProductForm
#     template_name = 'management/edit_product.html'

#Product Type Create Generic Class Based View

# class ProductTypeCreateView(CreateView):
#     model = ProductType
#     template_name = 'management/edit_product_type.html'
#     form_class = ProductSpecification
#     object = None

#     def get(self, request, *args, **kwargs):
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         product_spec_form = ProductTypeFormset()
#         return self.render_to_response(
#                   self.get_context_data(form=form,
#                                         assignment_question_form=product_spec_form,
#                                         )
#                                      )

#     def post(self, request, *args, **kwargs):
#         """
#         Handles POST requests, instantiating a form instance and its inline
#         formsets with the passed POST variables and then checking them for
#         validity.
#         """
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         product_spec_form = ProductTypeFormset(self.request.POST)
#         if form.is_valid() and product_spec_form.is_valid():
#             return self.form_valid(form, product_spec_form)
#         else:
#             return self.form_invalid(form, product_spec_form)

#     def form_valid(self, form, product_spec_form):
#         """
#         Called if all forms are valid. Creates Assignment instance along with the
#         associated AssignmentQuestion instances then redirects to success url
#         Args:
#             form: Assignment Form
#             assignment_question_form: Assignment Question Form

#         Returns: an HttpResponse to success url

#         """
#         self.object = form.save(commit=False)
#         # pre-processing for Assignment instance here...
#         self.object.save()

#         # saving AssignmentQuestion Instances
#         product_specs = product_spec_form.save(commit=False)
#         for ps in product_specs:
#             #  change the AssignmentQuestion instance values here
#             ps.product = self.object.id
#             ps.save()

#         return HttpResponseRedirect(self.get_success_url())

#     def form_invalid(self, form, product_spec_form):
#         """
#         Called if a form is invalid. Re-renders the context data with the
#         data-filled forms and errors.

#         Args:
#             form: Assignment Form
#             assignment_question_form: Assignment Question Form
#         """
#         return self.render_to_response(
#                  self.get_context_data(form=form,
#                                        product_spec_form=product_spec_form
#                                        )
#         )

