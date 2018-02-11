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
var selectedType={typeId:"0",typeDesc:"",typeCode:"",typeLevel:0};
var checkCodeResponse=false;
var checkDescResponse=false;

function pageLoadAction(){
	//run first time when page is loaded
	//with appropriate data from the server
	var select1 = document.getElementById("typeSelector");
	document.getElementById("startOverButton").disabled=true;
	document.getElementById("finishButton").disabled=true;
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

function loadSelectTypes(main,typeList){
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
	if (main) {
		opt.innerHTML = "Add New Category/Type";
	}
	else {
		opt.innerHTML = "Add Sub-Type";
	}
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
//check value of selected type, if it is 1 display the add type form
	if (selectedId=="1"){
		addNewTypeAction();
		document.getElementById("startOverButton").disabled=false;
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
			typeCode : selectedCode,
			typeLevel: selectedLevel
		};
		selectedType=vSelectedType;
		setBCArray(selectedId,selectedText);
		document.getElementById("startOverButton").disabled=false;
		document.getElementById("finishButton").disabled=false;
		//this loop is to check if the data already exists in local cache
		var notFound=true;
		for (ctr in typeListArray){
			if (typeListArray[ctr].ParentId==selectedId){
				typeList = typeListArray[ctr].typeList;
			    //remove entries from the current select
			    removeSelectEntries();
			    //add new sub type entries to the current select 
			    loadSelectTypes(false,typeList);
			    //set focus on the select 
				notFound=false;
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
			    		var typeListArrayEntry={ParentId:selectedId,
			    					level:typeListFrmSvr[0].level,
		    		              	typeList:typeListFrmSvr};
					   	typeListArray.push(typeListArrayEntry);
			    	}
			      //remove entries from the current select
			      removeSelectEntries();
			      //add new sub type entries to the current select 
			      loadSelectTypes(false,typeListFrmSvr);
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
	selectedType={typeId:"0",typeDesc:"",typeCode:"",typeLevel:0};
	loadSelectTypes(true,typeListArray[0].typeList);
	deactivateAddTypeSection();
	deactivateProductForm();
	document.getElementById("finishButton").disabled=true;
}

function setBCArray(selectedId, selectedText){
	var bcIndex=typeBCArray.length;
	var bcEntry = 
    {
		index:bcIndex,
		sId:selectedType.typeId,
		sTxt:selectedType.typeDesc,
		sCode:selectedType.typeCode,
		sLevel:selectedType.typeLevel
	};
	typeBCArray.push(bcEntry);
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
	document.getElementById("noneLabel").hidden=false;
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
	console.log("pressed Index is");
	console.log(sIndex);
	var BCArray=typeBCArray.slice(0,sIndex+1);
	selectedId=BCArray[sIndex].sId;
	console.log("selected Id is ");
	console.log(selectedId);
	selectedType = 
	{
		typeId:BCArray[sIndex].sId,
		typeDesc:BCArray[sIndex].sTxt,
		typeCode:BCArray[sIndex].sCode,
		typeLevel:BCArray[sIndex].sLevel
	};
	console.log(selectedType.typeDesc);
	//remove the extra crumbs
	for(ctr=sIndex+1; ctr<=typeBCArray.length-1;ctr++){
		var parent = document.getElementById("typeBC");
		var child = document.getElementById("typeCrumb"+ctr);
		parent.removeChild(child);
	}
	//reset the BC array to reflect the current changes
	typeBCArray=BCArray;
	
	//reload the list
	for (ctr in typeListArray){
		console.log("loop")
		console.log(ctr);
		console.log(typeListArray[ctr].ParentId);
		console.log(selectedId);
		if (typeListArray[ctr].ParentId==selectedId){
			typeList = typeListArray[ctr].typeList;
			console.log(typeList[0]);
		    //remove entries from the current select
		    removeSelectEntries();
		    //add new sub type entries to the current select 
		    loadSelectTypes(false,typeList);
		    break;
		}
	}
}
  
function addTypeAct(){
	//validate inputs make sure values are not duplicated in main arrays
	//send an ajax post request to the server
	//need the parentKey id to
    // all ok proceed to send request to post new value
	//need to change the next section
	var selectedId=selectedType.typeId;
	var newDesc = document.getElementById("typeDescription");
	var newCode = document.getElementById("typeCode")
	var xhttp = new XMLHttpRequest();
	var requestString="parentId=";
	requestString=requestString.concat(selectedId);
	requestString=requestString.concat("&Desc=");
	requestString=requestString.concat(newDesc.value.trim());
	requestString=requestString.concat("&Code=");
	requestString=requestString.concat(newCode.value.trim());
	console.log("AddType");
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
				var typeListArrayEntry={ParentID:selectedId,
    					level:typeListFrmSvr[0].level,
		              	typeList:typeListFrmSvr};
				typeListArray.push(typeListArrayEntry);
			}
			//remove entries from the current select
	    	removeSelectEntries();
	    	//add new sub type entries to the current select 
	    	loadSelectTypes(false,typeListFrmSvr);
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
	var divEle=document.getElementById("div"+elm.trim()+"Msg");
	var pEle=document.getElementById("p"+elm.trim()+"Msg");
	pEle.innerHTML=err;
	if (!isVisible(divEle)){
		divEle.hidden=false;
	}
}

function checkDescAct(){
	var selectedId=selectedType.typeId;
	console.log("checkDesc");
 	console.log(selectedId);
	var newDesc = document.getElementById("typeDescription");
	var submitButton=document.getElementById("submitAddTypeFormButton");
	newDescValue=newDesc.value.trim();
	if (newDescValue.length==0){
		displayError("Desc",
		"Error: Description can't be blank");
	 refocus(newDesc);
	}
	else{
		var requestString="checkDesc?parentId=";
		requestString=requestString.concat(selectedId);
		requestString=requestString.concat("&Desc=");
		requestString=requestString.concat(newDescValue);
		var xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function (){
			 if (this.readyState == 4 && this.status == 200){
				 	var svrResponse= JSON.parse(this.responseText);
				 	var responseType=svrResponse.response;
				 	
				 	if (responseType=="true"){
						checkDescResponse=true;
						if (checkCodeResponse) {
							submitButton.disabled=false;
						}
						errorDiv=document.getElementById("divDescMsg");
						if (isVisible(errorDiv)) {
							errorDiv.hidden=true;
						}
					}
				 	else if (responseType=="false"){
						console.log("error: duplicate description");
						displayError("Desc",
						"Error: Duplicate Description under this parent type");
						refocus(newDesc);
					}
			 }
			 else if (this.readyState == 4 && this.status == 500){
				 displayError("Desc",
					"Server Error: Unable to check value");
				 refocus(newDesc);
			 }
		};
		xhttp.open("GET",requestString, true);
		xhttp.send();
	}
}

function checkCodeAct(){
	var selectedId=selectedType.typeId;
	var newCode = document.getElementById("typeCode");
	var submitButton=document.getElementById("submitAddTypeFormButton");
	newCodeValue=newCode.value.trim();
	if (newCodeValue.length<3){
		displayError("Code",
		"Error: Code can't be blank or less than 3 alphanumeric digits");
	 refocus(newCode);
	}
	else{
		var requestString="checkCode?parentId=";
		requestString=requestString.concat(selectedId);
		requestString=requestString.concat("&Code=");
		requestString=requestString.concat(newCodeValue);
		var xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function (){
			 if (this.readyState == 4 && this.status == 200){
				 	var svrResponse= JSON.parse(this.responseText);
				 	var responseType=svrResponse.response;
				 	console.log("checkCode");
				 	console.log(responseType);
				 	if (responseType=="true"){
						checkCodeResponse=true;
						if (checkDescResponse) {
							submitButton.disabled=false;
						}
						errorDiv=document.getElementById("divCodeMsg");
						if (isVisible(errorDiv)) {
							errorDiv.hidden=true;
						}
					}
				 	else if (responseType=="false"){
						console.log("error: duplicate code");
						displayError("Code",
								"Error: Duplicate Code under this parent type");
						refocus(newCode);
					}
			 }
			 else if (this.readyState == 4 && this.status == 500){
				 displayError("Code",
					"Server Error: Unable to check value");
				 refocus(newCode);
			 }
		};
		xhttp.open("GET",requestString, true);
		xhttp.send();
	}
}

function addNewTypeAction(){
	//deactivate the select control to enable activating the add 
	//subtype form
	deactivateSelectSection();
	document.getElementById("finishButton").disabled=true;
	resetTypeForm();
	//remove breadcrumb if still displaying on this level
	//show the add types form
	//enable the elements of the form
	activateAddTypeSection("Add SubType");
}

function cancelNewTypeButtonAction(){
	deactivateAddTypeSection();
	activateSelectSection();
	document.getElementById("typeSelector").selectedIndex=0;
	document.getElementById("finishButton").disabled=true;
}

function activateSelectSection(){
	document.getElementById("typeSelector").disabled=false;
}

function deactivateAddTypeSection(){
	document.getElementById("typeDescription").disabled=true;
	document.getElementById("typeCode").disabled=true;
	document.getElementById("addTypeForm").style.display="none";
}

function deactivateSelectSection(){
	document.getElementById("typeSelector").disabled=true;
}

function activateAddTypeSection(buttonString){
	document.getElementById("addTypeForm").style.display="";
	document.getElementById("typeDescription").disabled=false;
	document.getElementById("typeCode").disabled=false;
}

function activateProductForm(){
	document.getElementById("divFormProduct").classList.remove('disabled');
	document.getElementById("divFormProduct").classList.add('enabled');
	resetProductForm();
}

function deactivateProductForm(){
	document.getElementById("divFormProduct").classList.remove('enabled');
	document.getElementById("divFormProduct").classList.add('disabled');
}

function resetProductForm(){
	document.getElementById("pName").value="";
	document.getElementById("pSku").value="";
	document.getElementById("prodDesc").value="";
	document.getElementById("1attrValue").value="";
	document.getElementById("2attrValue").value="";
	document.getElementById("3attrValue").value="";
	document.getElementById("4attrValue").value="";
	document.getElementById("prodImageDesc").value="";
}

function resetTypeForm(){
	document.getElementById("typeDescription").value="";
	document.getElementById("typeCode").value="";
}

function generateSKU() {
	//go thru breadcrumbs and make a SKU, set the SKU
}

function finishButtonAct(){
	activateProductForm();
	document.getElementById("fieldsProduct").disabled=false;
	generateSKU();
}

function attrDescBtnAct(index){
	elementName=index+"attrDesc";
	document.getElementById(elementName).readOnly=false;
}

function attrValueSet(index){
	eleName=index+"attrValue";
	ele=document.getElementById(eleName);
	refocus(ele);
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


function setBCArray1(selectedId,selectedText){
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
