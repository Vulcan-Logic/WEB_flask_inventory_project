/**
 *addType.js contains script to make addType HTML page UI function 
 *properly
 */

 /* initially tested with
  * var typeListFrmSvr = '[]';
  * var typeListFrmSvr = '[{"typeId":1, "typeDesc":"Pot","typeCode":"Pot"},' 
  * +'{"typeId":2, "typeDesc":"Dome","typeCode":"Dom"},' +
     '{"typeId":3, "typeDesc":"Other","typeCode":"Oth"}]';
*/

//this has the form = [{parentId:0,typeList:json List}] 
var typeListArray =[];
//this has the form = [{Id:0,typeList:Array of sub-types under this type}] 
var typeBCArray=[];
var selectedType={typeId:"",typeDesc:"",typeCode:""};

function pageLoadAction(){
	//run first time when page is loaded
	//with appropriate data from the server
	var select1 = document.getElementById("typeSelector");
	if (select1.length>2){
		var tTypeArray=[];
		for (ctr=2; ctr<select1.length ; ctr++){
			taEntry={
				key:select1[ctr].value.trim(),
				typeDefinition:select1[ctr].innerHTML.trim(),
				typeCode:select1[ctr].getAttribute('data-value').trim(),
				typeLevel:select1[ctr].getAttribute('data-value2').trim()
			};
			tTypeArray.push(taEntry);
		}
		var tlaEntry={
				ParentId:"0",
				level:0,
				typeList:tTypeArray
		};
		typeListArray.push(tlaEntry);
		deactivateAddTypeSection();
		select1.selectedIndex=0;
	}
	else{
		//empty type List on load
		//no entries at level 0 also 
		//disable the type selector
		decativateSelectSection();
		//show the add types form
		//enable the elements of the form
		activateAddTypeSection("Add Main Type");
	}
}

function loadSelectTypes(typeList){
// create select control	
	var divSel = document.getElementById("divSel");
	var select1 = document.createElement("select");
	var atr11 = document.createAttribute('name');
	atr11.value = "typeSelector";
	var atr12 = document.createAttribute('id');
	atr12.value="typeSelector";
	var atr13 = document.createAttribute('onChange');
	atr13.value="typeSelectorAction()";
	select1.setAttributeNode(atr11);
	select1.setAttributeNode(atr12);
	select1.setAttributeNode(atr13);
	divSel.appendChild(select1);
//add none option	
	var opt = document.createElement('option');
	var atr = document.createAttribute('data-value');
	atr.value = "0";
	var atr1 = document.createAttribute('data-value2');
	atr1.value="0";
	var atr2 = document.createAttribute('selected');
	atr2.value="true";
	opt.value = "0";
	opt.innerHTML = "None Selected";
	opt.setAttributeNode(atr);
	opt.setAttributeNode(atr1);
	opt.setAttributeNode(atr2);
	select1.appendChild(opt);
//add add-subtypes option	
	var opt = document.createElement('option');
	var atr = document.createAttribute('data-value');
	atr.value = "1";
	var atr1 = document.createAttribute('data-value2');
	atr1.value = "1";
	opt.value = "1";
	opt.innerHTML = "Add Sub-Type";
	opt.setAttributeNode(atr);
	opt.setAttributeNode(atr1);
	select1.appendChild(opt);
//add all category types fetched from server
	if (typeList.length!=0) {	
		console.log(typeList.length);
		for (ctr in typeList){
			var opt = document.createElement('option');
			var atr1 = document.createAttribute('data-value');
			atr1.value = typeList[ctr].typeCode;
			var atr2 = document.createAttribute('data-value2');
			atr2.value=typeList[ctr].typeLevel;
			opt.value = typeList[ctr].key;
			opt.innerHTML = typeList[ctr].typeDefinition;
			opt.setAttributeNode(atr1);
			opt.setAttributeNode(atr2);
			select1.appendChild(opt);
		 }
	} 
}

function typeSelectorAction(){
	//fired when value in type select box is changed
	var sel = document.getElementById('typeSelector');
	var selected = sel.options[sel.selectedIndex];
	var selectedCode = selected.getAttribute('data-value').trim();
	var selectedLevel = selected.getAttribute('data-value2').trim();
	var selectedId=selected.value.trim();
	var selectedText=selected.innerHTML.trim();
//convert types to ing	
	selectedLevel=Number(selectedLevel);
//check value of selected type, if it is 1 display the add type form
	if (selectedId=="1"){
		addNewTypeAction(selectedLevel);
	}
	//check if selected Id is 0, if so display the none label
	else if (selectedId=="0") {
		removeBC(selectedLevel);
	} 
	else if ((selectedType.typeId!=selectedId) && (selectedId!=0)) {
		//value other than none selected in select type
		var vSelectedType = 
		{
			typeId :  selectedId,
			typeDesc : selectedText,
			typeCode : selectedCode
		};
		selectedType=vSelectedType;
		setBCArray(selectedId,selectedText);
		//this loop is to check if the data already exists in local cache
		var notFound=true;
		for (ctr in typeListArray){
			if (typeListArray[ctr].ParentId==selectedId){
				typeList = typeListArray[ctr].typeList;
			    //remove entries from the current select
			    removeSelectEntries();
			    //add new sub type entries to the current select 
			    loadSelectTypes(typeList);
			    //set focus on the select 
				notFound=false;
				currentLevel=typeListArray[ctr].level;
			}
		}
		if (notFound) {
			//parentKey has not been found in local array 
			requestString='getTypeList?kId='+selectedId;
			//prepare request and send to server
			//get data back and display
			var xhttp = new XMLHttpRequest();
			xhttp.onreadystatechange = function (){
				//called when server results are returned
			    if (this.readyState == 4 && this.status == 200){
			     //get the type List from the server
			    	var dataFrmSvr = JSON.parse(this.responseText);
			    	if (dataFrmSvr.count==0){
			    		console.log("0 records returned");
			    		var typeListFrmSvr=[];
			    	} else {
			    		console.log("records returned");
			    		console.log(dataFrmSvr.count);
			    		var typeListFrmSvr=JSON.parse(dataFrmSvr.list);
			    		var typeListArrayEntry={parentID:selectedId,
			    					level:typeListFrmSvr[0].level,
		    		              	typeList:typeListFrmSvr};
					   	typeListArray.push(typeListArrayEntry);
			    	}
			      //remove entries from the current select
			      removeSelectEntries();
			      //add new sub type entries to the current select 
			      loadSelectTypes(typeListFrmSvr);
			    } else if (this.readyState == 4 && this.status == 500){
			    	//to do........
			    	//display error alert
			    	alert("server error in fetching data");
			    	startOverAction();
			    }
			};
			xhttp.open("GET",requestString, true);
			xhttp.send();
		}
	}
}

function removeSelectEntries(){
	var divSel = document.getElementById("divSel");
	var select1 = document.getElementById("typeSelector");
	divSel.removeChild(select1);
}

function startOverAction(){
	resetBC();
	removeSelectEntries();
	selectedType={typeId:0,typeDesc:"",typeCode:""};
	loadSelectTypes(typeListArray[0].typeList);
}

function setBCArray(selectedId,selectedText){
	var level=-1;
	for (ctr in typeListArray){
		var typeList=typeListArray[ctr].typeList;
		for (ctr2 in typeList){
			if (Number(typeList[ctr2].key)==Number(selectedId)){
			level=typeListArray[ctr].level;
			}	
		}
	}
	var newBCArray=[];
	var bcIndex=typeBCArray.length;
	if ((level==bcIndex) || (bcIndex==0)){
		var bcEntry = 
		    {
				index:bcIndex,
				sId:selectedType.typeId,
				sTxt:selectedType.typeDesc,
				sCode:selectedType.typeCode
			};
		typeBCArray.push(bcEntry);
	}
	else {
		if (level<bcIndex){
			for (ctr=0; ctr<=level; ctr++){
				if (ctr==level){
					var bcEntry = 
				    {
						index:bcIndex,
						sId:selectedType.typeId,
						sTxt:selectedType.typeDesc,
						sCode:selectedType.typeCode
					};
					newBCArray.push(bcEntry);
				}
				else{
					newBCArray.push(typeBCArray[ctr]);
				}
			}
			typeBCArray=newBCArray;
			}
	}
	showBC();
}

function resetBC(){
	typeBCArray=[];
	//remove old breadcrumbs
	var bcDiv=document.getElementById("bcDiv");
	var child = document.getElementById("typeBC");
	bcDiv.removeChild(child);
	var ol = document.createElement('ol');
	var atr = document.createAttribute('class');
	atr.value="breadcrumb";
	ol.setAttributeNode(atr);
	var atr1 = document.createAttribute('id');
	atr1.value="typeBC";
	ol.setAttributeNode(atr1);
	bcDiv.appendChild(ol);
	var att = document.createAttribute('hidden');
	att.value="true";
	bcDiv.setAttributeNode(att);
	var noneLabel = document.getElementById("noneLabel");
	var attr = noneLabel.getAttributeNode("hidden");
	noneLabel.removeAttributeNode(attr);
	document.getElementById("startOverButton").disabled=true;
}

function removeBC(selectedLevel){
	if (typeBCArray.length>0){
		if ((typeBCArray.length-1)==selectedLevel){
			if((typeBCArray.length-1)>0){
				typeBCArray.pop();
				showBC();
			}
			else{
				typeBCArray.pop();
				var bcDiv=document.getElementById("bcDiv");
				var att = document.createAttribute('hidden');
				att.value="true";
				bcDiv.setAttributeNode(att);
				var noneLabel = document.getElementById("noneLabel");
				var attr = noneLabel.getAttributeNode("hidden");
				noneLabel.removeAttributeNode(attr);
				document.getElementById("startOverButton").disabled=true;
			}
		}
	}
}

function showBC(){
	var bcDiv=document.getElementById("bcDiv");
	if (!isVisible(bcDiv)){
		// hide the none label and 
		// unhide the bcDiv.
		var noneLabel=document.getElementById("noneLabel");
		var att = document.createAttribute('hidden');
		att.value="true";
		noneLabel.setAttributeNode(att);
		var attr = bcDiv.getAttributeNode("hidden");
		bcDiv.removeAttributeNode(attr);
		document.getElementById("startOverButton").disabled=false;
	}
//remove old breadcrumbs
	var bcDiv=document.getElementById("bcDiv");
	var child = document.getElementById("typeBC");
	bcDiv.removeChild(child);
//add new bread crumbs from array
	var ol = document.createElement('ol');
	var atr = document.createAttribute('class');
	atr.value="breadcrumb";
	ol.setAttributeNode(atr);
	var atr1 = document.createAttribute('id');
	atr1.value="typeBC";
	ol.setAttributeNode(atr1);
	bcDiv.appendChild(ol);
// Display all contents of the BC array on the bread crumb div
	var bcBar=document.getElementById("typeBC");
	for (ctr in typeBCArray){
		bcEntry=typeBCArray[ctr];
		var opt = document.createElement('li');
		var atr = document.createAttribute('id');
		atr.value="typeCrumb"+bcEntry.index;
		opt.setAttributeNode(atr);
		
		var opt1 = document.createElement('a');
		var atr1 = document.createAttribute('href');
		atr1.value = "#";
		opt1.setAttributeNode(atr1);
		
		var atr2 = document.createAttribute('onClick');
		atr2.value = "typeBCAction(" + bcEntry.index + ")";
		opt1.setAttributeNode(atr2);
		
		var atr3 = document.createAttribute('data-value');
		atr3.value = bcEntry.sId;
		opt1.setAttributeNode(atr3);
		
		var opt2=document.createElement('span');
		opt2.innerHTML = bcEntry.sTxt;
		
		opt1.appendChild(opt2);
		opt.appendChild(opt1);
		bcBar.appendChild(opt);
	}
}

function typeBCAction(sIndex){
	//reset the array
	var BCArray=typeBCArray.slice(0,sIndex+1);
	selectedId=BCArray[sIndex].sId;
	selectedType = 
	{
		typeId:BCArray[sIndex].sId,
		typeDesc:BCArray[sIndex].sTxt,
		typeCode:BCArray[sIndex].sCode
	};
	//remove the extra crumbs
	for(ctr=sIndex+1; ctr<=typeButtonArray.length-1;ctr++){
		var parent = document.getElementById("typeBC");
		var child = document.getElementById("typeCrumb"+ctr);
		parent.removeChild(child);
	}
	//reset the BC array to reflect the current changes
	typeBCArray=BCArray;
	
	//reload the list
	for (ctr in typeListArray){
		if (typeListArray[ctr].parentId==selectedId){
			typeList = typeListArray[ctr].typeList;
		    //remove entries from the current select
		    removeSelectEntries();
		    //add new sub type entries to the current select 
		    loadSelectTypes(typeList);
		}
	}
}
  
function postForAddProduct(selectedId,newDesc,newCode){
	//validate inputs make sure values are not duplicated in main arrays
	//send an ajax post request to the server
	//need the parentKey id to
    // all ok proceed to send request to post new value
	//need to change the next section
	var xhttp = new XMLHttpRequest();
	var requestString="parentId=";
	requestString=requestString.concat(selectedId);
	requestString=requestString.concat("&Desc=");
	requestString=requestString.concat(newDesc.value.trim());
	requestString=requestString.concat("&Code=");
	requestString=requestString.concat(newCode.value.trim());
	console.log("request string is " + requestString);
	xhttp.open("POST", "insertType", true);
	xhttp.onreadystatechange =  function(){
		if (this.readyState == 4 && this.status == 200){
			var dataFrmSvr = JSON.parse(this.responseText);
			//prepare newTypeList
			var typeListFrmSvr=JSON.parse(dataFrmSvr.list);
			//see if parentId is already in typeListArray
			var notFound=true;
			for (ctr in typeListArray){
				if (typeListArray[ctr].ParentId==selectedId){
					//parentId exists in typeListArray reset typeList
					typeListArray[ctr].typeList=typeListFrmSvr;
					notFound=false;
				}
			}
			//parentID does not exist in typeListArray, add a new entry
			if (notFound){
				var typeListArrayEntry={parentID:selectedId,
    					level:typeListFrmSvr[0].level,
		              	typeList:typeListFrmSvr};
				typeListArray.push(typeListArrayEntry);
			}
			//remove entries from the current select
	    	removeSelectEntries();
	    	//add new sub type entries to the current select 
	    	loadSelectTypes(typeListFrmSvr);
	    	deactivateAddTypeSection();
	    	activateSelectSection();
		}
		else if (this.readyState == 4 && this.status == 500) {
			displayError("divType","ERROR:in adding new type in server")
		}
	};
	xhttp.setRequestHeader("Content-type", 
			               "application/x-www-form-urlencoded");
	xhttp.send(requestString); 
}

function displayError(elm,err){
	var ele=document.getElementById(elm);
	var eleMsg=document.getElementById(elm.trim()+"Msg");
	eleMsg.innerHTML=err;
	if (!isVisible(ele)){
		var attr = eleMsg.getAttributeNode("hidden");
		eleMsg.removeAttributeNode(attr);
	}
}

function checkField(field,parentId){
	//error codes
	//0 OK field value not found in database
	//-1 field is blank
	//-2 field value is in database
	//-3 server error
	var ele = document.getElementById(field);
	//check if input is blank
	if (ele.value.trim().length==0)return(-1);
	//input is not blank
	else {
		if (field=="typeDescription") 
			var requestString="checkDesc?parentId=" + 
					parentId + "&desc=" + ele.value.trim();
		else 
			var requestString="checkCode?parentId=" + 
					parentId + "&code=" + ele.value.trim();
	//not blank send ajax request and check response
		var xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function (){
			 if (this.readyState == 4 && this.status == 200){
			    	if (Number(this.responseText)==1) return(-2);	
			 }
			 else if (this.readyState == 4 && this.status == 500)return(-3);
		};
		xhttp.open("GET",requestString, true);
		xhttp.send();
	}
	console.log("returning 0 from checkField");
	return(0);
}

function submitAddTypeAct(){
	var selectedId=selectedType.typeId;
	var newDesc = document.getElementById("typeDescription");
	var newCode = document.getElementById("typeCode");
	if (checkField("typeDescription",selectedId)==0 &&
			checkField("typeCode",selectedId)==0){
		console.log("posting insert request");
		postForAddProduct(selectedId,newDesc,newCode);	
	}
	else if (checkField("typeDescription",selectedId)==-2){
		console.log("error: duplicate description");
		displayError("divDesc",
				"Duplicate Description under this parent type");
		refocus(newDesc);
		return(false);
	}
	else if (checkField("typeCode",selectedId)==-2) {
		console.log("error: duplicate code");
		displayError("divCode", "Duplicate Code under this parent type");
		refocus("newCode");
		return(false);
	}
}


function addNewTypeAction(selectedLevel){
	//deactivate the select control to enable activating the add 
	//subtype form
	removeBC(selectedLevel);
	deactivateSelectSection();
	//remove breadcrumb if still displaying on this level
	//show the add types form
	//enable the elements of the form
	activateAddTypeSection("Add SubType");
}

function cancelNewTypeButtonAction(){
	deactivateAddTypeSection();
	activateSelectSection();
	document.getElementById("typeSelector").selectedIndex=0;
}

function activateSelectSection(){
	document.getElementById("typeSelector").disabled=false;
}

function deactivateAddTypeSection(){
	document.getElementById("typeDescription").disabled=true;
	document.getElementById("typeCode").disabled=true;
	document.getElementById("submitAddTypeFormButton").disabled=true;
	document.getElementById("addTypeForm").style.display="none";
}

function deactivateSelectSection(){
	document.getElementById("typeSelector").disabled=true;
}

function activateAddTypeSection(buttonString){
	document.getElementById("addTypeForm").style.display="";
	document.getElementById("typeDescription").disabled=false;
	document.getElementById("typeCode").disabled=false;
	document.getElementById("submitAddTypeFormButton").disabled=false;
}

function isVisible (ele) {
	console.log(ele);
    var style = window.getComputedStyle(ele);   
    return  style.width !== 0 &&
    style.height !== 0 &&
    style.opacity !== 0 &&
    style.display!=='none' &&
    style.visibility!== 'hidden';
}

function refocus(elm) {
    setTimeout(go, 0);
    function go() {
        elm.focus();
    }
}


//obsolete
function checkCode(){
	var newCode = document.getElementById("typeCode");
	console.log("New Code is:");
	console.log(newCode.value);
	var continu=true;
	var codeMsg=document.getElementById("divCodeMsg");
	for (ctr in typeListArray){
		if (typeListArray[ctr].ParentId==selectedType.typeId){
			var typeList = typeListArray[ctr].typeList; 
			for (ctr2 in typeList){
				console.log(typeList[ctr2].typeCode.toLowerCase());
				console.log(newCode.value.toLowerCase());
				console.log((typeList[ctr2].typeCode.toLowerCase().trim() ==
				  			newCode.value.toLowerCase().trim()))
				if (typeList[ctr2].typeCode.toLowerCase().trim() ==
				  			newCode.value.toLowerCase().trim()){
					console.log("this is equal");
					
					continu=false;
					break;
				} 
			}
		}
		if (!continu){
			break;
		}
	}
	console.log("length");
	console.log(newCode.value.trim().length);
	if (newCode.value.trim().length==0){
		document.getElementById("codeMsg").innerHTML=
			"ERROR: Code can't be blank";
		var attr = codeMsg.getAttributeNode("hidden");
			codeMsg.removeAttributeNode(attr);
		continu=false;
	}
	if (!continu){
		refocus(newCode);
	} else {
		if (isVisible(codeMsg)){
			codeMsg.style.display="none";
		}
	}
}
