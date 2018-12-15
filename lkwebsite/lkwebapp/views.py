import sys
from django.shortcuts import render,render_to_response,get_object_or_404
from .models import lkModel,lkModelType
import json
sys.path.append('..')
from .requestUilts.requestModel import requestClass

# Create your views here.

def interFaceList(request):
    interFaces=lkModel.objects.all()
    interFaces_type=lkModelType.objects.all()
    print(interFaces_type)
    context={}
    context['interFaces']=interFaces
    print(interFaces)
    context['interFaces_type']=interFaces_type
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

