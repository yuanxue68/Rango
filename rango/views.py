from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from datetime import datetime

from rango.models import Category,Page
from rango.forms import CategoryForm,PageForm

def index(request):
	category_list = Category.objects.order_by("-likes")[:5]
	top_pages_list = Page.objects.order_by("-views")[:5]
	context_dict={"categories":category_list,
					"top_pages_list":top_pages_list}

	visits=request.session.get('visits')
	if not visits:
		visits=1
	reset_last_visit_time=False

	last_visit=request.session.get('last_visit')
	if(last_visit):
		last_visit_time=datetime.strptime(last_visit[:-7],"%Y-%m-%d %H:%M:%S")

		if(datetime.now()-last_visit_time).seconds>0:
			visits=visits+1
			reset_last_visit_time=True
	else:
		reset_last_visit_time=True
		
	if(reset_last_visit_time):
		request.session['last_visit']=str(datetime.now())
		request.session['visits']=visits
	context_dict['visits']=visits
	return render(request,'rango/index.html',context_dict)
	
def about(request):
	print "hello"
	return render(request,'rango/about.html')

def category(request,category_name_slug):
	context_dict={}
	try:
		category=Category.objects.get(slug=category_name_slug)
		context_dict['category_name']=category.name

		pages=Page.objects.filter(category=category)
		context_dict['pages']=pages
		context_dict['category']=category
		context_dict['category_name_url']=category_name_slug

	except Category.DoesNotExist:
		pass

	return render(request,'rango/category.html',context_dict)

@login_required
def add_category(request):
	if request.method=="POST":
		form=CategoryForm(request.POST)

		if(form.is_valid()):
			form.save(commit=True)
			return index(request)
		else:
			print form.errors

	else:
		form=CategoryForm()

	return render(request,'rango/add_category.html',{'form':form})

@login_required
def add_page(request,category_name_slug):
	try:
		cat=Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		cat=None
	if(request.method=="POST"):
		form=PageForm(request.POST)
		if form.is_valid():
			if cat:
				page=form.save(commit=False)
				page.category=cat
				page.views=0;
				page.save()
				return category(request,category_name_slug)
		else:
			print form.errors
	else:
		form=PageForm()

	context_dict={'form':form,'category':cat}

	return render(request,'rango/add_page.html',context_dict)


@login_required
def restricted(request):
	return render(request,'rango/restricted.html',{})

def get_category_list(max_results=0, starts_with=''):
	print "hello2"
	cat_list = []
	if starts_with:
		cat_list = Category.objects.filter(name__istartswith=starts_with)

	if max_results > 0:
		if len(cat_list) > max_results:
			cat_list = cat_list[:max_results]

	return cat_list

def suggest_category(request):
	print "hello"
	cat_list = []
	starts_with = ''
	if request.method == 'GET':
		starts_with = request.GET['suggestion']

	cat_list = get_category_list(8, starts_with)
	#print cat_list

	return render(request, 'rango/category_list.html', {'categories': cat_list })
