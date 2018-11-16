console.log('loading')

var phenotypes;
var current_pheno;

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
					var data = phenotypes[i];
					// console.log(data)
					html += '<a id="phenotypes" class="list-group-item list-group-item-action waves-effect">';
					html += '<i class="fa fa-pie-chart mr-3"></i>' + data['title'];
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

$(document).on('click', '#phenotypes', phenotype_click);
function phenotype_click() {
	$('#left-panel a').removeClass('active');
	$('#left-panel a').css('color', 'black');
	$(this).addClass('active');
	$(this).css('color', 'white');

	var current = $(this).text();
	console.log(current);
	var data;
	var keys;
	for (var i=0; i<phenotypes.length; i++) {
		data = phenotypes[i];
		keys = Object.keys(data);
		if (data['title'] == current) {
			current_pheno = phenotypes[i];
			break;
		}
	}

	console.log(current_pheno);
	var phenotype_name = current_pheno['title'];

	html = ""
	html += '<p><strong>Phenotype:</strong> ' + phenotype_name + '</p>';
	for (i in current_pheno){
		if (i != 'title')
			html += '<p><strong>'+i+':</strong> ' + current_pheno[i] + '</p>';
	}

	$('#main_panel .card-body').html(html);
	// $('#main_panel').show();
}


function splitAndCap(string) {
	str = string.split('_');
	processedStr = '';
	for (var i=0; i<str.length - 1; i++) {
		processedStr += str[i].charAt(0).toUpperCase() + str[i].slice(1) + ' ';
	}
	processedStr += str[str.length - 1].charAt(0).toUpperCase() + str[str.length - 1].slice(1)
	return processedStr;
}

function getDictContent(dict) {
	content = '';
	for (item in dict) {
		if (item != 'id') {
			name = splitAndCap(item)
			content += '<p><strong>' + name + ':</strong> ' + dict[item] + '</p>';
		}
	}
	return content;
}

$(document).on('click', '#phenotypes', phenotype_click_new);
function phenotype_click_new() {
	var main_container = $('#phenotype_container');

	// refresh card body
	main_container.find('.card-body').empty();

	var details_card = $('#details_card');
	var icd_card = $('#icd_card');
	var medications_card = $('#medications_card');
	var demographics_card = $('#demographics_card');
	var vital_signs_card = $('#vital_signs_card');
	var lab_results_card = $('#lab_results_card');

	details = '<p><strong>Phenotype:</strong> ' + current_pheno['title'] + '</p>';
	details += getDictContent(current_pheno['contributors']);

	icd = '<p><strong>ICD-9 Inclusion:</strong> ' + current_pheno['icd9_inclusion'] + '</p>';
	icd += '<p><strong>ICD-9 Exclusion:</strong> ' + current_pheno['icd9_exclusion'] + '</p>';
	icd += '<p><strong>ICD-10 Inclusion:</strong> ' + current_pheno['icd10_inclusion'] + '</p>';
	icd += '<p><strong>ICD-10 Exclusion:</strong> ' + current_pheno['icd10_exclusion'] + '</p>';

	medications = '<p><strong>Medications:</strong> ' + current_pheno['medications'] + '</p>';

	demographics = getDictContent(current_pheno['demographics']);

	vital_signs = getDictContent(current_pheno['vital_signs']);

	lab_results = getDictContent(current_pheno['lab_results']);

	details_card.children('.card-body').append(details);
	icd_card.children('.card-body').append(icd);
	medications_card.children('.card-body').append(medications);
	demographics_card.children('.card-body').append(demographics);
	vital_signs_card.children('.card-body').append(vital_signs);
	lab_results_card.children('.card-body').append(lab_results);

	$('#phenotype_container').show();
}

function create_histogram() {
	html = '<canvas id="comparison_histogram"></canvas>';
	$('#main_panel .card-body').html(html);
	$('#main_panel').show();

	// Gather phenotype result count
	phenotype_result = {}
	var data, keys, phenotype_name;
	for (var i=0; i<phenotypes.length; i++) {
		data = phenotypes[i];
		phenotype_name = data['title'];
		phenotype_result[phenotype_name] = (i+1)*1000;
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