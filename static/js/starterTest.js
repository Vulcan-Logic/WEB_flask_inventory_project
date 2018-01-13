/**
 * 
 */


function pageLoadAction(){
	requestString='getStarterTypesJSON';
	//prepare request and send to server
	//get data back and display
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function (){
		//called when server results are returned
		console.log("in function callback");
		console.log(this.readyState);
		console.log(this.status);
	    if (this.readyState == 4 && this.status == 200){
	     //get the type List from the server
	   		console.log("in this branch");
	    	var typeListFrmSvr = JSON.parse(this.responseText);
	    	console.log(typeof(typeListFrmSvr));
	    	console.log(typeListFrmSvr);
	    	console.log(typeListFrmSvr.length);
	    	for (ctr in typeListFrmSvr){
	    		document.getElementById("result").innerHTML+=
	    			typeListFrmSvr[ctr].typeDefinition + " " + "<br />";
	    	}
	    	
/*
	     	var typeListArrayEntry={parentID:selectedId,
			              typeList:[]};
	    	typeListArray.push(typeListArrayEntry);
*/		    	
	      //remove entries from the current select
	      //removeSelectEntries();
	      //add new sub type entries to the current select 
	      //loadSelectType(typeListFrmSvr);
	      //
	    } else if (this.readyState == 4 && this.status == 500){
	    	/*
	    	if (window.confirm("Server Error in fetching data\n"+ 
	    			"Press OK to retry")
	    			== true){
	    		typeSelectorAction();
	    	}*/
	    	console.log("and in this branch too");
	    }
	};
	xhttp.open("GET",requestString, true);
	xhttp.send();
	
	
	
	}