var queue = []

function addtoqueue(id, branch, listed) {
	// add product to queue list
	queue.push({"productId": id, "branch": branch, "listed": listed});
	
	// disable button
	$("#"+id+'.'+branch).addClass("disabled");

	// increase number on apply button
	var $number = $('#queue');
	$number.html((parseInt($number.html(),10) || 0) + 1);
	//alert(JSON.stringify(queue));
}

function removequeue() {}

function sendqueue() {
	//alert(JSON.stringify(queue));
	$(".loading_modal").show();
	$.ajax({
	    url: '/updates/process_queue/',
	    type: 'POST',
	    contentType: 'application/json; charset=utf-8',
	    data: JSON.stringify(queue),
	    dataType: 'text',
	    success: function(result) {
	        //alert(result.Result);
	        queue = []
	        getdata();
	    }
	});
}

function getdata() {
	var manifestURL = '/updates/update_list/';
	$.get(manifestURL, function(data) {
        $('#data').html(data);
        $(".loading_modal").hide();
        var $number = $('#queue');
		$number.html(0);  
    });
}