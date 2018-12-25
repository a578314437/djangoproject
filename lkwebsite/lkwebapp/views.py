import sys
from django.shortcuts import render,render_to_response,get_object_or_404
from .models import lkModel,lkModelType
import json
sys.path.append('..')
from .requestUilts.requestModel import requestClass
from django.core.paginator import Paginator
from django.db.models import Count
# Create your views here.

def get_interFace_list_common_data(request,interFaces_all_list):
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
    interFaces_type=lkModelType.objects.annotate(interFace_type_count=Count('lkmodel'))

    # interFaces_type_list=[]
    # for interFace_type in interFaces_type:
    #     interFace_type.interFace_type_count=lkModel.objects.filter(model_type=interFace_type).count()
    #     interFaces_type_list.append(interFace_type)


    context={}

    context['page_of_interFaces']=page_of_interFaces
    context['page_range']=page_range
    # print(page_of_interFaces)
    context['interFaces_type']=interFaces_type
    return context

def interFaceList(request):
    
    interFaces_all_list=lkModel.objects.all()
    context=get_interFace_list_common_data(request,interFaces_all_list)
    # print(interFaces_all_list)
    # paginator=Paginator(interFaces_all_list,4)
    # page_num=request.GET.get('page',1)
    # page_of_interFaces=paginator.get_page(page_num)
    # currentr_page_number=page_of_interFaces.number

    # page_range= [currentr_page_number - 2,currentr_page_number - 1,currentr_page_number,currentr_page_number + 1,currentr_page_number + 2]
    
    # page_range=list(range(max(currentr_page_number - 2 ,1),currentr_page_number))+ \
    #             list(range(currentr_page_number,min(currentr_page_number + 2,paginator.num_pages)+ 1))
    # #interFaces=lkModel.objects.all()
    # #interFaces=page_of_interFaces.object_list
    # if page_range[0] -1 >=2:
    #     page_range.insert(0,'...')
    # if paginator.num_pages -page_range[-1]>=2:
    #     page_range.append('...')

    # if page_range[0]!=1:
    #     page_range.insert(0,1)
    # if page_range[-1]!=paginator.num_pages:
    #     page_range.append(paginator.num_pages)

    
    # context={}

    # context['page_of_interFaces']=page_of_interFaces
    # context['page_range']=page_range
    # # print(page_of_interFaces)
    # context['interFaces_type']=interFaces_type
    #return render(request,'interFace_list.html',locals())
    return render_to_response('interFace_list.html', context)

def interFaceDetail(request,interFace_pk):
    interFace=get_object_or_404(lkModel,pk=interFace_pk)
    data="currentPage=1&pageSize=20&custId=&custName=&orderState=&orderStateName=&orderCode=&effDate=2018-12-01&expDate=2018-12-31&orderIds=&tenantIds=72%2C106%2C110%2C111"
    requesParame = request.POST.get('interFaceParame',data)
    print(requesParame)
    #print(requesParame)
    context={}
    context['interFace']=interFace
    q=requestClass()
    try:
        result=q.get_rquest_result(interFace.request_url,requesParame)
        context['result']=result
    except Exception as e:
        pass
    return render(request,'interFace_detail.html', locals())

def interFaceTypeList(request,interFace_type_pk):
    interFace_type=get_object_or_404(lkModelType,pk=interFace_type_pk)
    interFace=get_object_or_404(lkModel,pk=interFace_type_pk)
    interFaces=lkModel.objects.filter(model_type=interFace_type)

    interFacesType_all_list=interFaces
    context=get_interFace_list_common_data(request,interFacesType_all_list)
    context['interFace_type']=interFace_type
    # paginator=Paginator(interFacesType_all_list,4)
    # page_num=request.GET.get('page',1)
    # page_of_interFaces=paginator.get_page(page_num)
    # currentr_page_number=page_of_interFaces.number
    # page_range= [currentr_page_number - 2,currentr_page_number - 1,currentr_page_number,currentr_page_number + 1,currentr_page_number + 2]
    # page_range=list(range(max(currentr_page_number - 2 ,1),currentr_page_number))+ \
    #             list(range(currentr_page_number,min(currentr_page_number + 2,paginator.num_pages)+ 1))
    # #interFaces=lkModel.objects.all()
    # #interFaces=page_of_interFaces.object_list
    # if page_range[0] -1 >=2:
    #     page_range.insert(0,'...')
    # if paginator.num_pages -page_range[-1]>=2:
    #     page_range.append('...')
    # if page_range[0]!=1:
    #     page_range.insert(0,1)
    # if page_range[-1]!=paginator.num_pages:
        # page_range.append(paginator.num_pages)
    return render_to_response('interFace_type_list.html', context)
    #return render(request,'interFace_type_list.html',locals())

