const PythonShell = require('python-shell');
const json = `[
	{
		"project":{
		"name" : "Bayshore-A",
		"start" : "04192018",
		"end": "08212018",
		"workdays":["M","T","W","Th","F"],
		"budget":"400",
		"location":{
			"street1":"231, 1st cross",
			"street2":"Suite 2",
			"city":"Long Beach",
			"state":"CA",
			"postal":"20134",
			"country":"USA"
			}
		},
		"bundles":{
		"name" : "Mechanical",
		"phases" : "Origination",
		"activities":{
			"name":"Pile Installation",
			"contractor": "Arraycon",
			"total_planned_hours":"",
			"total_planned_units":"",
			"planned_start":"",
			"planned_end":"",
			"actual_start":"",
			"actual_end":"",
			"unit": {
				"name": "Rows"
			},
			"material": "Material"
			},
		"activities":{
			"name":"Torque Row Installed",
			"contractor": "Sacramento Drilling",
			"total_planned_hours":"",
			"total_planned_units":"",
			"planned_start":"",
			"planned_end":"",
			"actual_start":"",
			"actual_end":"",
			"unit": {
				"name": "piles"
			},
			"material": "Material"
			}
		},
		"bundles":{
		"name" : "Electrical",
		"phases" : "Origination",
		"activities":{
			"name":"LGH",
			"contractor": "GKM",
			"total_planned_hours":"",
			"total_planned_units":"",
			"planned_start":"",
			"planned_end":"",
			"actual_start":"",
			"actual_end":"",
			"unit": {
				"name": "Rows"
			},
			"material": "Material"
			},
		"activities":{
			"name":"LA",
			"contractor": "SK",
			"total_planned_hours":"",
			"total_planned_units":"",
			"planned_start":"",
			"planned_end":"",
			"actual_start":"",
			"actual_end":"",
			"unit": {
				"name": "piles"
			},
			"material": "Material"
			}
		},
		"contractors":[{
			"name":"Arraycon",
			"email": "arraycon@gmail.com",
			"phone":"6461241234",
			"primary_contact":"6461234567"
		}],
		"materials":[{
			"name":"",
			"planned_delivery": "",
			"actual_delivery":"",
			"unit_cost":""
		}],
		"incidents":[{
			"date":"",
			"type": "IncidentType",
			"class":"IncidentClass",
			"contractor":"Contractor"
		}]
}]`;
const options = {
    mode: 'text',
    pythonPath: 'C:/Users/Lakshmi Damodara/AppData/Local/Continuum/anaconda3/python.exe'
};
var pyshell = new PythonShell('structuralDataLoader.py', options);
pyshell.send(json);
//Lakshmi TODO: needs to return parsing error codes
/*
separate error codes for the following conditions:
1) Invalid JSON
2) Unexpected field value
3) Database field validation error (length is too long)
4) Business rule failure (adding an existing activity)
5) Unknown error type
Also please provide location of the error (line number in the input file or row in spreadsheet)
*/
pyshell.on('message', function (message) {
    // received a message sent from the Python script (a simple "print" statement)
    console.log(message);
  });

  // end the input stream and allow the process to exit
  pyshell.end(function (err,code,signal) {
    if (err) throw err;
    console.log('The exit code was: ' + code);
    console.log('The exit signal was: ' + signal);
    console.log('finished');
    console.log('finished');
  });