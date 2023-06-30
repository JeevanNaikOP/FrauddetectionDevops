from django.shortcuts import render
from .forms import FraudDetectionForm
import sweetify
import os
import json
import requests

# Create your views here.
def index(request):
    form = FraudDetectionForm()
    
    return render(request,'index.html',{'form': form})

def result(request):
    sweetify.DEFAULT_OPTS = {
    'showConfirmButton': True,
    'timer': 2500,
    'allowOutsideClick': True,
    'confirmButtonText': 'OK',
}
    header = {
            'Content-Type': 'application/json',
        }
    
    user = request.POST.get('input1')
    amount = request.POST.get('input2')
    usechip = request.POST.get('input3')
    card = request.POST.get('input4')
    merchantName = request.POST.get('input5')
    errors = request.POST.get('input6')
    merchntState = request.POST.get('input7')
    merchantCity = request.POST.get('input8')
    zip = request.POST.get('input9')
    mcc = request.POST.get('input10')
    form = FraudDetectionForm()
    
    base_url = 'https://192.86.32.113:19443/frauddetectiondevopsapi/param?'
    end_url= base_url+'Zip='+zip+'&MerchantXName='+merchantName+'&User='+user+'&ErrorsX='+errors+'&MCC='+mcc+'&Card='+card+'&MerchantXCity='+merchantCity+'&MerchantXState='+merchntState+'&UseXChip='+usechip+'&Amount='+amount

    response_scoring = requests.post(end_url, auth=('ibmuser', 'ibmuser'), headers=header,verify=False)

    json_out = (json.loads(response_scoring.text))

    prediction = json_out['MODELOUT']['MODELOUP']['PREDICTION']
    prob1 = json_out['MODELOUT']['MODELOUP']['PROBABILITY'][0]
    prob2 = json_out['MODELOUT']['MODELOUP']['PROBABILITY'][1]
    scoring_ID = json_out['MODELOUT']['MODELOUP']['RES_ID']

    return render(request,'result.html',{'form': form, 'user_profile':user,'mcc':mcc, 'amount': amount,'useChip':str(usechip), 'card': card,
                                            'merchantName':merchantName,'errors':errors,'merchantState':merchntState,
                                            'merchantCity':merchantCity, 'zip':zip, 'endpoint':scoring_ID, 
                                            'prediction':prediction,'prob1':prob1,'prob2':prob2})


