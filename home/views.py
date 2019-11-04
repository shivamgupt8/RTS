from django.shortcuts import render, redirect
from .models import Train, Ticket
from django.template.loader import render_to_string
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from .forms import ticket


# Create your views here.
def starting(request):
    user=request.user
    print("jdcncj")
    return render(request,'home/starting.html',{'user':user})

def trains(request):
    if request.is_ajax():
        print("aaya")
        source = request.POST.get('source',None)
        destination = request.POST.get('destination',None)
        date = request.POST.get('date',None)
        print(source)
        print(destination)
        print(date)
        trains=[]
        ptrains = (Train.objects.filter(source__iexact=source))
        for i in ptrains:
            print(i.destination.upper())
            if(i.destination.upper() == destination.upper()):
                trains.append(i)

        context={'trains':trains}
        html = render_to_string('home/trains.html',context,request=request)
        return JsonResponse({'form': html})

def ticketbook(request,id):
    train = Train.objects.filter(id=id).first()
    return render(request,'home/book.html',{'train':train})

def ticketbk(request,id):
    print("aayay habhah")    
    form = ticket()
    return render(request,'home/tick.html',{'form':form})

def realbook(request,id):
    if request.method == 'POST':
        user=request.user
        train = Train.objects.filter(id=id).first()
        date = request.POST.get('date',None)
        tcount = Ticket.objects.filter(date=date)
        g=0
        seatnos=[]
        for i in range(1,20):
            seatnos.append(0)
        for i in tcount:
                if i.train == train:
                        seatnos[i.seatno]=1;
                        g=g+1
        if(g>=3):
                status = "Waiting List"
                seatno=15
        # return render(request,'home/starting.html')
        else:
                for i in range(1,4):
                    if seatnos[i]==0:
                        seatno=i
                        break
                status = "Confirm"
        o = str(date)
        p = o[0:4]
        p = p + o[5:7]
        p = p + o[8:11]
        z = Ticket.objects.all()
        po = z.count()
        po = str(po)
        print(po)
        pnr = str(train.id)+p+str(user.id)+po
        
        passenger_name = request.POST.get('name',None)
        age = request.POST.get('age',None)
        ticket = Ticket(user=user,
        pnr=pnr,status=status,date=date,train=train,passenger_name=passenger_name,
        age=age,seatno=seatno
        )
        ticket.save()
        print(ticket)
        return redirect('tickt', pnr=pnr)


def tickt(request,pnr):    
    tic = Ticket.objects.filter(pnr=pnr).first()
    print(tic)
    return render(request,'home/ticke.html',{'tic':tic})

def canceltic(request,pnr):
    tic = Ticket.objects.filter(pnr=pnr).first()
    if tic.status == "Confirm":
        print("oihv")
        t = tic.seatno
        seatnos=[]
        tics = Ticket.objects.filter(date=tic.date)
        for ti in tics:
            print(ti.status)
            if ti.status == "Waiting List":
                ti.seatno=t
                ti.status="Confirm"
                ticket = Ticket(user=ti.user,
                pnr=ti.pnr,status="Confirm",date=ti.date,train=ti.train,passenger_name=ti.passenger_name,
                age=ti.age,seatno=t
                )
                ticket.save()
                ti.delete()
                break
    tic.delete()
    return redirect('home-home')

def pnrstatus(request):
    if request.method == 'POST':
        pnr = request.POST.get('pnr',None)
        print(pnr)
        return redirect('tickt', pnr=pnr)
    else :
        return render(request,'home/pnrstatus.html')


def about(request):
    return render(request,'home/about.html')