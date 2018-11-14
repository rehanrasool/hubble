console.log('loading')

var phenotypes;

$("#search_button").click(function(){
	console.log('loaded hubble')
	var output = $("#search_query").val();
	if (output.length == 0) {
		console.log("empty")	
	}
	console.log(output)
	var data = {'search': output}

	$.ajax({
			url: '/lookup',
			data: JSON.stringify(data),
			type: 'POST',
			success: function(response) {
				console.log('got response')
				phenotypes = response;
				console.log(phenotypes);

				// create left-panel
				html = ""
				for (var i=0; i<phenotypes.length; i++) {
					var obj = jQuery.parseJSON(phenotypes[i]);
					var keys = Object.keys(obj);
					html += '<a id="phenotypes" class="list-group-item list-group-item-action waves-effect">';
					html += '<i class="fa fa-pie-chart mr-3"></i>' + keys[0];
					html += '</a>';
				}

				$('#left-panel').html(html);
				$('#left-panel').show();

				// create histogram
				create_histogram();

			},
			error: function(error) {
				console.log('got error')
				console.log(error);
			},
			dataType: "json",
			contentType: 'application/json;charset=UTF-8',
	});

})

// popovers Initialization
$(function() {
    $('[data-toggle="popover"]').popover()
})

$(document).on('click', '#phenotypes', onClick);
function onClick() {
	$('#left-panel a').removeClass('active');
	$('#left-panel a').css('color', 'black');
	$(this).addClass('active');
	$(this).css('color', 'white');

	var current = $(this).text();
	console.log(current);
	var current_pheno;
	var obj;
	var keys;
	for (var i=0; i<phenotypes.length; i++) {
		obj = jQuery.parseJSON(phenotypes[i]);
		keys = Object.keys(obj);
		if (keys[0] == current) {
			console.log(phenotypes[i]);
			current_pheno = phenotypes[i];
			break;
		}
	}

	var phenotype_name = keys[0];
	fields = Object.keys(obj[phenotype_name]);
	console.log(fields)

	html = ""
	html += '<p><strong>Phenotype:</strong> ' + phenotype_name + '</p>';
	for (var i=0; i<fields.length; i++) {
		html += '<p><strong>'+fields[i]+':</strong> ' + obj[phenotype_name][fields[i]] + '</p>';
	}
	$('#main_panel .card-body').html(html);
	// $('#main_panel').show();
}


function create_histogram() {
	html = '<canvas id="comparison_histogram"></canvas>';
	$('#main_panel .card-body').html(html);
	$('#main_panel').show();

	// Gather phenotype result count
	phenotype_result = {}
	var obj, keys, phenotype_name;
	for (var i=0; i<phenotypes.length; i++) {
		obj = jQuery.parseJSON(phenotypes[i]);
		keys = Object.keys(obj);
		phenotype_name = keys[0];
		fields = Object.keys(obj[phenotype_name]);
		phenotype_result[phenotype_name] = parseInt(obj[phenotype_name]['Result'][0]);
		// console.log(fields);
	}
	// console.log(phenotype_result);
	// console.log(Object.keys(phenotype_result))
	// console.log(Object.values(phenotype_result))

	// Construct histogram
	var ctx = document.getElementById("comparison_histogram").getContext('2d');
	var comparison_histogram = new Chart(ctx, {
	    type: 'bar',
	    data: {
	        labels: Object.keys(phenotype_result),
	        datasets: [{
	            label: '# of Patients',
	            data: Object.values(phenotype_result),
	            backgroundColor: [
	                'rgba(255, 99, 132, 0.2)',
	                'rgba(54, 162, 235, 0.2)',
	                'rgba(255, 206, 86, 0.2)',
	                'rgba(75, 192, 192, 0.2)',
	                'rgba(153, 102, 255, 0.2)',
	                'rgba(255, 159, 64, 0.2)'
	            ],
	            borderColor: [
	                'rgba(255,99,132,1)',
	                'rgba(54, 162, 235, 1)',
	                'rgba(255, 206, 86, 1)',
	                'rgba(75, 192, 192, 1)',
	                'rgba(153, 102, 255, 1)',
	                'rgba(255, 159, 64, 1)'
	            ],
	            borderWidth: 1
	        }]
	    },
	    options: {
	        scales: {
	            yAxes: [{
	                ticks: {
	                    beginAtZero: true
	                }
	            }]
	        }
	    }
	});
}


// //pie
// var ctxP = document.getElementById("pieChart").getContext('2d');
// var myPieChart = new Chart(ctxP, {
//     type: 'pie',
//     data: {
//         labels: ["Red", "Green", "Yellow", "Grey", "Dark Grey"],
//         datasets: [{
//             data: [300, 50, 100, 40, 120],
//             backgroundColor: ["#F7464A", "#46BFBD", "#FDB45C", "#949FB1", "#4D5360"],
//             hoverBackgroundColor: ["#FF5A5E", "#5AD3D1", "#FFC870", "#A8B3C5", "#616774"]
//         }]
//     },
//     options: {
//         responsive: true,
//         legend: false
//     }
// });


// //line
// var ctxL = document.getElementById("lineChart").getContext('2d');
// var myLineChart = new Chart(ctxL, {
//     type: 'line',
//     data: {
//         labels: ["January", "February", "March", "April", "May", "June", "July"],
//         datasets: [{
//                 label: "My First dataset",
//                 backgroundColor: [
//                     'rgba(105, 0, 132, .2)',
//                 ],
//                 borderColor: [
//                     'rgba(200, 99, 132, .7)',
//                 ],
//                 borderWidth: 2,
//                 data: [65, 59, 80, 81, 56, 55, 40]
//             },
//             {
//                 label: "My Second dataset",
//                 backgroundColor: [
//                     'rgba(0, 137, 132, .2)',
//                 ],
//                 borderColor: [
//                     'rgba(0, 10, 130, .7)',
//                 ],
//                 data: [28, 48, 40, 19, 86, 27, 90]
//             }
//         ]
//     },
//     options: {
//         responsive: true
//     }
// });


// //radar
// var ctxR = document.getElementById("radarChart").getContext('2d');
// var myRadarChart = new Chart(ctxR, {
//     type: 'radar',
//     data: {
//         labels: ["Eating", "Drinking", "Sleeping", "Designing", "Coding", "Cycling", "Running"],
//         datasets: [{
//             label: "My First dataset",
//             data: [65, 59, 90, 81, 56, 55, 40],
//             backgroundColor: [
//                 'rgba(105, 0, 132, .2)',
//             ],
//             borderColor: [
//                 'rgba(200, 99, 132, .7)',
//             ],
//             borderWidth: 2
//         }, {
//             label: "My Second dataset",
//             data: [28, 48, 40, 19, 96, 27, 100],
//             backgroundColor: [
//                 'rgba(0, 250, 220, .2)',
//             ],
//             borderColor: [
//                 'rgba(0, 213, 132, .7)',
//             ],
//             borderWidth: 2
//         }]
//     },
//     options: {
//         responsive: true
//     }
// });

// //doughnut
// var ctxD = document.getElementById("doughnutChart").getContext('2d');
// var myLineChart = new Chart(ctxD, {
//     type: 'doughnut',
//     data: {
//         labels: ["Red", "Green", "Yellow", "Grey", "Dark Grey"],
//         datasets: [{
//             data: [300, 50, 100, 40, 120],
//             backgroundColor: ["#F7464A", "#46BFBD", "#FDB45C", "#949FB1", "#4D5360"],
//             hoverBackgroundColor: ["#FF5A5E", "#5AD3D1", "#FFC870", "#A8B3C5", "#616774"]
//         }]
//     },
//     options: {
//         responsive: true
//     }
// });