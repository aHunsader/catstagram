$('document').ready(attachEventHandlers);

function attachEventHandlers() {
	$('img.like, .overlay-pic').dblclick(voteClick);
	$('img.like, .overlay-pic').hover(showRG, hideRG);
	$('img.post').click(popupClick);
	$('form[name="addComment"]').submit(addComment);
}

function showRG(event){
	$('.overlay-pic').show();
}
function hideRG(event){
	$('.overlay-pic').hide();
}

function voteClick(event){
	var num = $('img.like').attr("id");
	var source = $('img.like').attr("src");
	var token = $('meta[name="_token"]').attr('content');
	var ycoord = event.pageY - $('img.like').offset().top;
	var height = $('img.like').height();
	var type = ycoord < height/2 ? 1 : 0;

	$.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type))
                xhr.setRequestHeader("X-CSRFToken", token)
        }
    });

	$.ajax({
		url: '/imageClick/',
		method: 'POST',
		data: {
			pic_id: num,
			upordown: type,
		},
		success: function(data){
			display_popup(num, source);
		},
	});
}


function popupClick(event){
	console.log("ya");
	var num = this.id;
	var source = $(this).attr("src");
	display_popup(num, source);
}

function display_popup(num, source){
	$(".like").attr({"id": num, "src": source});
	$.ajax({
		url: '/imageClick/',
		method: 'GET',
		dataType: 'JSON',
		data: {
			pic_id: num,
		},
		complete: function(data){
			$("#ViewPic").modal('show');
			var response = data.responseJSON;
			var title = "<a href=\"" + response.url + "\">" + 
				response.username + "</a>";
			$('.date').html(response.date);
			$('.upvotes').html(response.upvotes);
			$('.downvotes').html(response.downvotes);
			$('.modal-title').html(title);
			$('.caption').html(response.caption);
			if(response.caption == "")
				$('p.caption').css('display', "none")

			var comments = "";
			var i;
			for(i in response.comments)
				comments += ("<div class=\"well well-sm\"> <a href=\"/" + 
					response.comments[i].profile__pk + "\">" + response.comments[i].profile__username + 
					"</a>" + ": " + response.comments[i].body + "</div>");
			if(comments == "")
				comments = "<p>There are no comments to show at this time.</p>";
			$('.comments').html(comments);
		},
	});
}

function addComment(event){
	event.preventDefault();
	var num = $(".like").attr('id');
	var token = $('meta[name="_token"]').attr('content');
	var source = $(".like").attr('src');
	var comment = $("#new_comment").val();

	$.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type))
                xhr.setRequestHeader("X-CSRFToken", token)
        }
    });

	$.ajax({
		url: '/addComment/',
		method: 'POST',
		data: {
			pic_id: num,
			comment: comment,
		},
		success: function(data){
			display_popup(num, source);
			$("#new_comment").val('');
		},
	});
}

$('document').ready(function(){
	var infinite = new Waypoint.Infinite({
		element: $('.infinite-container')[0],
		offset: 'bottom-in-view',
		onAfterPageLoad: function(){attachEventHandlers();},
	});
});
		

