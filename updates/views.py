from django.shortcuts import get_object_or_404, redirect, render

from reposadolib import reposadocommon

def update_list(request):
	branches = reposadocommon.getCatalogBranches()
	context = {'test': branches}
	return render(request, 'updates/updats_list.html', context)