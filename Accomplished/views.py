from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required()
def done(request):
    return render(request, "Accomplished/done.html")
