from django.shortcuts import get_object_or_404, redirect, render

from reposadolib import reposadocommon

def update_list(request):
	products = reposadocommon.getProductInfo()
	context = {'test': products}
	return render(request, 'updates/updats_list.html', context)