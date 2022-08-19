from django.shortcuts import render

# Create your views here.

def inputdata(request):
    return render(request, 'program/inputdata.html')

def result(request):
    lis = []
    lis.append(request.GET['a'])
    lis.append(request.GET['b'])

    
    sum = 0
    for l in lis:
        sum += int(l)
    ans = sum

    context = {'ans':ans, 'lis':lis}

    return render(request, 'program/result.html', context)
    