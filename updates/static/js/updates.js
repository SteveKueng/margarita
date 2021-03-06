
var queue = [];
var queueId = 0;

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (settings.type == 'POST' || settings.type == 'PUT' || settings.type == 'DELETE') {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    }
});

function addtoqueue(id, branch, listed) {
	// add product to queue list
	queue.push({"id": queueId, "productId": id, "branch": branch, "listed": listed});
	
	// change button
	$("#"+id+'.'+branch).replaceWith( "<button id=\""+ id +"\" onclick='removequeue(\""+ id +"\", \""+ branch +"\", \""+ listed +"\", \""+queueId+"\")' class=\"btn btn-sm "+branch+" btn-info\"><span class=\"glyphicon glyphicon-plus\" aria-hidden=\"true\"></span> Queued</button>" );


	// increase number on apply button
	var $number = $('#queue');
	$number.html((parseInt($number.html(),10) || 0) + 1);
	// alert(JSON.stringify(queue));
	queueId = queueId + 1;
}

function removequeue(id, branch, listed, index) {
	// remove product from queue list
	findAndRemove(queue, "id", index);

	// change button
	if (listed == "true") {
    	$("#"+id+'.'+branch).replaceWith( "<button id=\""+ id +"\" onclick='addtoqueue(\""+ id +"\", \""+ branch +"\", \""+ listed +"\")' class=\"btn btn-sm "+branch+" btn-success\"><span class=\"glyphicon glyphicon-ok\" aria-hidden=\"true\"></span> Listed</button>" );
	} else {
		$("#"+id+'.'+branch).replaceWith( "<button id=\""+ id +"\" onclick='addtoqueue(\""+ id +"\", \""+ branch +"\")' class=\"btn btn-sm "+branch+" btn-default\"><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span> Unlisted</button>" );
	}

	// increase number on apply button
	var $number = $('#queue');
	$number.html((parseInt($number.html(),10) || 0) - 1);
	//alert(JSON.stringify(queue));
}

function sendqueue() {
	// alert(JSON.stringify(queue));
	$(".loading_modal").show();
	$.ajax({
	    url: '/updates/process_queue/',
	    type: 'POST',
	    contentType: 'application/json; charset=utf-8',
	    data: JSON.stringify(queue),
	    dataType: 'text',
	    success: function(result) {
	        // alert(result.Result);
	        queue = [];
	        queueId = 0;
	        getdata();
	    }
	});
}

function getdata() {
	$(".loading_modal").show();

	cookie = getCookie("hidecommonly");
	if(cookie == "true") {
		$('#icon').replaceWith('<a href="#" id="icon" onclick="hidecommonly();"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span> Unhide commonly updates</a>');
	} else {
		$('#icon').replaceWith('<a href="#" id="icon" onclick="hidecommonly();"><span class="glyphicon glyphicon-ok" aria-hidden="true"></span> Hide commonly updates</a>');
	}

	var manifestURL = '/updates/update_list/';
	$.get(manifestURL, function(data) {
        $('#data').html(data);
        $(".loading_modal").hide();
        var $number = $('#queue');
		$number.html(0);  
    });

}

function addall(branchname) {
	$(".loading_modal").show();
	$.ajax({
	    url: '/updates/add_all/'+branchname+'/',
	    type: 'POST',
	    contentType: 'application/json; charset=utf-8',
	    success: function(result) {
	        queue = [];
	        queueId = 0;
	        getdata();
	    }
	});
}

function copybranch(from, to) {
	$(".loading_modal").show();
	$.ajax({
	    url: '/updates/dup/'+from+'/'+to+'/',
	    type: 'POST',
	    contentType: 'application/json; charset=utf-8',
	    success: function(result) {
	        queue = [];
	        queueId = 0;
	        getdata();
	    }
	});
}

function deletebranch(branchname) {
	$(".loading_modal").show();
	$.ajax({
	    url: '/updates/delete_branch/'+branchname+'/',
	    type: 'POST',
	    contentType: 'application/json; charset=utf-8',
	    success: function(result) {
	        queue = [];
	        queueId = 0;
	        getdata();
	    }
	});
}

function findAndRemove(obj, prop, val) {
    var c, found=false;
    for(c in obj) {
        if(obj[c][prop] == val) {
            found=true;
            break;
        }
    }
    if(found){
        queue.splice(c,1);
    }
}

function showDiscr(element) {
	if($(element).find('.hidden').length != 0) {
		$(element).children(".well").removeClass("hidden");
	} else {
		$(element).children(".well").addClass("hidden");
	}
}

function newbranch(branch) {
	if(branch != "") {
		$(".loading_modal").show();
	$.ajax({
	    url: '/updates/new_branch/'+branch+'/',
	    type: 'POST',
	    contentType: 'application/json; charset=utf-8',
	    success: function(result) {
	        queue = [];
	        queueId = 0;
	        getdata();
	    }
	});
	}
	
	$('#branch-name').val('');
}

function hidecommonly() {
	cookie = getCookie("hidecommonly");
	if(cookie == "true") {
		document.cookie="hidecommonly=false";
	} else {
		document.cookie="hidecommonly=true";
	}
	getdata();
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
    }
    return "";
}