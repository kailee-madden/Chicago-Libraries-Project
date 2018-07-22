function results_table(json) {
	console.log(json)
	var tab = $("<table>").attr("class", "table table-hover").append(
		$("<thead>").append(
			$("<tr>").append(
				$("<th>").text("Library Name"),
				$("<th>").text("Address"),
				$("<th>").text("Hours")
			)
		)
	);
	
	var tbody = $("<tbody>")
	tab.append(tbody)
	
	for (i in json['data']) {
		tbody.append(
			$("<tr>").attr("data-library_id", json['data'][i]['library_id']).append(
				$("<td>").text(json['data'][i]['name']),
				$("<td>").text(json['data'][i]['address']),
				$("<td>").text(json['data'][i]['hours'])
			).click(function(){
			get_details($(this).attr("data-library_id"))
			})
		)
	}
	$("#results_col").empty().append(tab)
}

function start_search() {
	var lib_name = $("#name").val();
	$.get("/search", {"name":lib_name}, results_table);
}

function display_details(json) {
	var udiv = $("<div>").append(
		$("<p>").text(json['data']['description'])
	)
	var ldiv = $("<div>").append(
		
		$("<table>").append(
			
		$("<tr>").append(
		$("<th>").text("Library Name"),
		$("<td>").text(json["data"]["name"])
		),
		
		$("<tr>").append(
		$("<th>").text("Address"),
		$("<td>").text(json["data"]["address"])
		),
		
		$("<tr>").append(
		$("<th>").text("City"),
		$("<td>").text(json["data"]["city"])
		),
		
		$("<tr>").append(
		$("<th>").text("State"),
		$("<td>").text(json["data"]["state"])
		),
		
		$("<tr>").append(
		$("<th>").text("Zipcode"),
		$("<td>").text(json["data"]["zipcode"])
		),
		
		$("<tr>").append(
		$("<th>").text("Hours"),
		$("<td>").text(json["data"]["hours"])
		),
		
		$("<tr>").append(
		$("<th>").text("Phone Number"),
		$("<td>").text(json["data"]["phone_number"])
		),
		
		$("<tr>").append(
		$("<th>").text("Website"),
		$("<td>").append(
			$("<a>").attr(
				"href", json["data"]["website"]
			).text(
				json["data"]["website"]
			)
		)
		)
	)
);

	$("#detail_header").text(json['data']['name']);
	$("#detail_body").append(udiv, ldiv);
	$("#details").modal();
}


function get_details(id) {
	//$.get("/detail", {"library_id": id}, display_details)
	$("#details").load("/detailhtml", {"library_id": id}, function(){$("#details").modal()})
}

$(document).ready(function(){

	$("#form1").submit(function(event){
		event.preventDefault();
		start_search();
	});
})

