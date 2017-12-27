var http = require("http");
var py = require("python-shell");

//Function to host server on port 8081
http.createServer(function(request, response){
	//Create markup for HTML
	response.writeHead(200, {'Content-Type': 'text/html'});
	response.write('<!DOCTYPE html><html><head><title>' + 'TEST SERVICE' + '</title></head>');
	response.write('<body>');
 	
	//Runs script on page load - should preprocess and store in CSV then pull results from file/database
	var analysis = py.run('../symbols/process.py', {args: ['', '', 10]}, function(err, results){
		if(err) throw err;
		
		//Need to fix formatting issues with table
		response.write('<table><tr><th style=>Company</th><th>SMA Cross?</th></tr>');
		
		//Always logs NONE at the end of reading output
		console.log(results);
		for(var i = 0; i < results.length - 1; i++){
			var temp = results[i].split(", ");
			response.write('<tr><td>' + temp[0].substring(1) +  '</td><td>' + temp[1].substring(0, temp[1].length-1) + '</td><tr>');
		}	
		response.write('</table></body></html>');
		response.end();
	});
	

}).listen(8081);

console.log("Server Running on 127.0.0.1:8081");
