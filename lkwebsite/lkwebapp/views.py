import sys
from django.shortcuts import render,render_to_response,get_object_or_404
from .models import lkModel,lkModelType
import json
sys.path.append('..')
from .requestUilts.requestModel import requestClass
from django.core.paginator import Paginator
# Create your views here.

def interFaceList(request):
    
    interFaces_all_list=lkModel.objects.all()
    paginator=Paginator(interFaces_all_list,4)
    page_num=request.GET.get('page',1)
    page_of_interFaces=paginator.get_page(page_num)
    currentr_page_number=page_of_interFaces.number

    page_range= [currentr_page_number - 2,currentr_page_number - 1,currentr_page_number,currentr_page_number + 1,currentr_page_number + 2]
    
    page_range=list(range(max(currentr_page_number - 2 ,1),currentr_page_number))+ \
                list(range(currentr_page_number,min(currentr_page_number + 2,paginator.num_pages)+ 1))
    #interFaces=lkModel.objects.all()
    #interFaces=page_of_interFaces.object_list
    if page_range[0] -1 >=2:
        page_range.insert(0,'...')
    if paginator.num_pages -page_range[-1]>=2:
        page_range.append('...')



    if page_range[0]!=1:
        page_range.insert(0,1)
    if page_range[-1]!=paginator.num_pages:
        page_range.append(paginator.num_pages)
    context={}
    context['page_of_interFaces']=page_of_interFaces
    context['page_range']=page_range
    #print(interFaces)
    context['interFaces_type']=lkModelType.objects.all()
    return render(request,'interFace_list.html',locals())
#     return render_to_response('interFace_list.html', context)

def interFaceDetail(request,interFace_pk):
    interFace=get_object_or_404(lkModel,pk=interFace_pk)
    requesParame = request.POST.get('interFaceParame','{"1":"5"}')
    print(requesParame)
    context={}
    context['interFace']=interFace
    q=requestClass()
    result=q.get_rquest_result(interFace.request_url,eval(requesParame))
    context['result']=result
    return render(request,'interFace_detail.html', locals())

def interFaceType(request,interFace_type_pk):
    interFace_type=get_object_or_404(lkModelType,pk=interFace_type_pk)
    interFace=get_object_or_404(lkModel,pk=interFace_type_pk)
    interFaces=lkModel.objects.distinct().filter(model_type=interFace_type)
    requesParame = request.POST.get('interFaceParame','121212')
    if requesParame !='121212' and requesParame !=None:
        try:
            requesParame=eval(requesParame)
        except:
            pass
        print(requesParame)
    context={}
    context['interFaces']=interFaces
    q=requestClass()
    result=q.get_rquest_result(interFace.request_url,requesParame)
    context['result']=result
    return render(request,'interFace_type_detail.html',locals())

