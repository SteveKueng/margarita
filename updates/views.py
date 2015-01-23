from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import json
import os

from operator import itemgetter
from reposadolib import reposadocommon

@login_required
def index(request):
	return render(request, 'updates/index.html')

@login_required
def update_list(request):
	products = reposadocommon.getProductInfo()
	prodlist = []

	for prodid in products.keys():
		if 'title' in products[prodid] and 'version' in products[prodid] and 'PostDate' in products[prodid]:
			prodlist.append({
				'title': products[prodid]['title'],
				'version': products[prodid]['version'],
				'PostDate': products[prodid]['PostDate'],
				'size': products[prodid]['size'],
				'description': get_description_content(products[prodid]['description']),
				'id': prodid,
				'depr': len(products[prodid].get('AppleCatalogs', [])) < 1,
				})
		else:
			print 'Invalid update!'

	sprodlist = sorted(prodlist, key=itemgetter('PostDate'), reverse=True)

	branches = list_branches(request);

	context = {'products': sprodlist,
				'branches': branches}
	return render(request, 'updates/updats_list.html', context)

@login_required
def list_branches(request):
	catalog_branches = reposadocommon.getCatalogBranches()

	# reorganize the updates into an array of branches
	branches = []
	for branch in catalog_branches.keys():
		branches.append({'name': branch, 'products': catalog_branches[branch]}) 

	return branches

def get_description_content(html):
	if len(html) == 0:
		return None

	# in the interest of (attempted) speed, try to avoid regexps
	lwrhtml = html.lower()

	celem = 'p'
	startloc = lwrhtml.find('<' + celem + '>')

	if startloc == -1:
		startloc = lwrhtml.find('<' + celem + ' ')

	if startloc == -1:
		celem = 'body'
		startloc = lwrhtml.find('<' + celem)

		if startloc != -1:
			startloc += 6 # length of <body>

	if startloc == -1:
		# no <p> nor <body> tags. bail.
		return None

	endloc = lwrhtml.rfind('</' + celem + '>')

	if endloc == -1:
		endloc = len(html)
	elif celem != 'body':
		# if the element is a body tag, then don't include it.
		# DOM parsing will just ignore it anyway
		endloc += len(celem) + 3

	return html[startloc:endloc]

@login_required
def dup_apple(branchname):
	catalog_branches = reposadocommon.getCatalogBranches()

	if branchname not in catalog_branches.keys():
		print 'No branch ' + branchname
		return jsonify(result=False)

	# generate list of (non-drepcated) updates
	products = reposadocommon.getProductInfo()
	prodlist = []
	for prodid in products.keys():
		if len(products[prodid].get('AppleCatalogs', [])) >= 1:
			prodlist.append(prodid)

	catalog_branches[branchname] = prodlist

	print 'Writing catalogs'
	reposadocommon.writeCatalogBranches(catalog_branches)
	reposadocommon.writeAllBranchCatalogs()

	return jsonify(result=True)

@login_required
def process_queue(request):
	if request.is_ajax():
	    if request.method == 'POST':
			catalog_branches = reposadocommon.getCatalogBranches()

			data = json.loads(request.body)
			for change in data:
			 	prodId = change['productId']
			 	branch = change['branch']

				if branch not in catalog_branches.keys():
					print 'No such catalog'
					continue
				
				print change

				if change['listed']:
					print "test"
					# if this change /was/ listed, then unlist it
					if prodId in catalog_branches[branch]:
						print 'Removing product %s from branch %s' % (prodId, branch, )
						catalog_branches[branch].remove(prodId)
				else:
					# if this change /was not/ listed, then list it
					if prodId not in catalog_branches[branch]:
						print 'Adding product %s to branch %s' % (prodId, branch, )
						catalog_branches[branch].append(prodId)

			reposadocommon.writeCatalogBranches(catalog_branches)
			reposadocommon.writeAllBranchCatalogs()

	return HttpResponse("OK")

@login_required
def new_branch(request, branchname):
	print branchname
	catalog_branches = reposadocommon.getCatalogBranches()
	if branchname in catalog_branches:
	    reposadocommon.print_stderr('Branch %s already exists!', branchname)
	    return HttpResponse('Branch already exists!')
	catalog_branches[branchname] = []
	reposadocommon.writeCatalogBranches(catalog_branches)

	return HttpResponse("OK")

@login_required
def delete_branch(request, branchname):
    catalog_branches = reposadocommon.getCatalogBranches()
    if not branchname in catalog_branches:
        reposadocommon.print_stderr('Branch %s does not exist!', branchname)
        return

    del catalog_branches[branchname]

    # this is not in the common library, so we have to duplicate code
    # from repoutil
    for catalog_URL in reposadocommon.pref('AppleCatalogURLs'):
        localcatalogpath = reposadocommon.getLocalPathNameFromURL(catalog_URL)
        # now strip the '.sucatalog' bit from the name
        if localcatalogpath.endswith('.sucatalog'):
            localcatalogpath = localcatalogpath[0:-10]
        branchcatalogpath = localcatalogpath + '_' + branchname + '.sucatalog'
        if os.path.exists(branchcatalogpath):
            reposadocommon.print_stdout(
                'Removing %s', os.path.basename(branchcatalogpath))
            os.remove(branchcatalogpath)

    reposadocommon.writeCatalogBranches(catalog_branches)
    
    return HttpResponse("OK")

@login_required
def add_all(request, branchname):
	products = reposadocommon.getProductInfo()
	catalog_branches = reposadocommon.getCatalogBranches()
	
	catalog_branches[branchname] = products.keys()

	reposadocommon.writeCatalogBranches(catalog_branches)
	reposadocommon.writeAllBranchCatalogs()
	
	return HttpResponse("OK")

@login_required
def dup(request, frombranch, tobranch):
	catalog_branches = reposadocommon.getCatalogBranches()

	if frombranch not in catalog_branches.keys() or tobranch not in catalog_branches.keys():
		print 'No branch ' + branchname
		return jsonify(result=False)

	catalog_branches[tobranch] = catalog_branches[frombranch]

	print 'Writing catalogs'
	reposadocommon.writeCatalogBranches(catalog_branches)
	reposadocommon.writeAllBranchCatalogs()

	return HttpResponse("OK")