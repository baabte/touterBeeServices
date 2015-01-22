
   function fnTbInitialisation(){
    var resultObj;
      loadTBeeConfig(function(resultObj){    //function call for loading the social feature Object.
      if(Object.keys(resultObj).length!=0){ //checkig for if the resultObj contain any data or not by checking its length
      var mainObj=resultObj[0].tbObj; //copying the resulting object to the variable mainObj
      var elem;
      var elemObj={};
      
      for(key in mainObj){ //looping through resulting object
        
        var innerObj=mainObj[key];
          for(key2 in innerObj.pageData){ //loop inside pagedata object to get the specified page control.
             if(innerObj.pageData[key2].currentPage==window.location.href){ //conditon to check the current page with page inside the object. 
            
            for(key3 in innerObj.pageData[key2].configDataObj){ //looping through the configDatObj to get the page specific data
                var eventType=innerObj.pageData[key2].configDataObj[key3].eventType; //getting the venttype which required to trigger.
                var elemId=innerObj.pageData[key2].configDataObj[key3].elementId;
                var ele=document.getElementById(elemId); //getting the target element by its id.

                elemObj[elemId]=innerObj.pageData[key2].configDataObj[key3];

                  ele.addEventListener(eventType, function(e){//attaching event listener for target element
                      setTimeout(function(){//timeout function to call the actvateSocialFeature ajax function.
                     
                      if(!inIframe()){ //checking the website is loaded inside iframe or not
                          console.log(elemObj[e.target.id]);
                          activateSocialFeature(elemObj[e.target.id]); //calling the activateSocialFeature ajax function by passing element object as its parameter.
                          
                        }

                      }, 0)
                    });
                }
              }
            }
          }

        }
      }); 
    }
    /*loading the social config details at the time of page load.  */  
    setTimeout(function(){ 
      var resultObj;
      fnTbInitialisation(); //calling the function fnTbInitialisation to load the config data from server.
    }, 3000);
     /*end loading the social config details at the time of page load.  */  

    /*Function to detect the url change event to load the config object */
    function hashHandler(){
    this.oldHash = window.location.hash;
    this.Check;

    var that = this;
    var detect = function(){
        if(that.oldHash!=window.location.hash){
             setTimeout(function(){ //loading the social config details at the time of page load.
                
                fnTbInitialisation();
              }, 3000);
            that.oldHash = window.location.hash;
        }
    };
    this.Check = setInterval(function(){ detect() }, 100);
    }
    /*end of Function to detect the url change event to load the config object */
    
    var hashDetection = new hashHandler(); //the event is getting attached here

    /*function to check the website is loaded inside the iframe   */ 
    function inIframe () {
        try {
          return window.self !== window.top;
        } catch (e) {
          return true;
        }
    }
    /*End of function to check the website is loaded inside the iframe   */ 

        //for sending the confirmation message to parent window.
        window.parent.postMessage("loadJSsuccess", "*");
          revStr='';
          elemArr=[];
          outcome={};
        function receiveMessage(e){
            if(e.origin=="http://localhost:9001"){ //checking for origin for security purpose
              document.addEventListener('click', fnClickFreeze);
             
              if(e.data=='freeze'){ //chcking for the message passed from parent window.
                  document.addEventListener('click', fnClickFreeze); //bind the click event when message from parent is 'freeze'.
                 
              }
              else if(e.data=='unfreeze'){
                 
                 document.removeEventListener('click', fnClickFreeze); //unbind the click event when message from parent is 'freeze'.
              }
              
            }
          }

        /*Function to prevent the default behavior while we using in iframe and send the required info from parent site to iframe using postMessage() */
        function fnClickFreeze(e) { //fuction which prevent the default behavior of specifc element which we clicked.
              e.preventDefault();          //to prevent the actual behavior of the page loaded inside iframe window.
              
              outcome.id=e.target.id;     //id attribuete of the clicked element.
              outcome.name=e.target.name; //target name of the clicked element.
              outcome.type=e.target.type;
              outcome.currentPage=window.location.href; //getting the current page location which loaded inside iframe window.
              window.parent.postMessage(JSON.parse(JSON.stringify(outcome)), "*"); //posting the message to the parent window.
              return false; 
        }
        /*End of function here */
       
        //ajax function to load the socila configuration details.
        function loadTBeeConfig(fnCallback){ //to load the Tb config details.
          var objectData; // Receives the objectified results of the JSON request.
          var jsonResultBuffer={};
          var xmlhttp;
          if(window.XMLHttpRequest) {
            xmlhttp = new XMLHttpRequest();
          } else if (window.ActiveXObject) {
            xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
          }

          xmlhttp.open("POST", "http://127.0.0.1:8000/FnLoadTBeeConfig/", true);  //service url
          xmlhttp.setRequestHeader("content-type", "application/json");  
          xmlhttp.setRequestHeader("Accept", "application/json");
          xmlhttp.responseType = 'json';
          xmlhttp.onreadystatechange = function () 
          {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200)  //response of the ajax request.
            {
                jsonResultBuffer = JSON.parse(xmlhttp.response);
                fnCallback(jsonResultBuffer);
            }
          };
          xmlhttp.send(JSON.stringify({'urmId':123,'websiteId':321,'value':'','appId':'','feature':123,'featureType':111}));
          
        };

        //ajax function to activate the social feature.
        function activateSocialFeature(inputObj){
          var objectData; // Receives the objectified results of the JSON request.

          var postedValue=inputObj.content;
          
          if(postedValue!=undefined){ //checking for the value wich is exists or not
                  
                  var searchEles = postedValue.toDOM().children;
                  var actualValue="";

                  for(var i = 0; i < searchEles.length; i++) {
                    
                  if(searchEles[i].tagName.trim() == 'SPAN') {
                    if(searchEles[i].innerText.indexOf('#') >= 1) {         //getting the string straeted with # charecter.
                        var tempSearchId=searchEles[i].innerText;           //string which starts with # charecter
                        var actualSearchId=tempSearchId.substring(tempSearchId.indexOf('#')+1,tempSearchId.length); //replacing the # from the string
                        var ele=document.getElementById(actualSearchId);    //selecting the element whos value needed
                              if(ele.getAttribute('type')=='text'){         //ckecking for element type
                               postedValue =postedValue.replace(new RegExp(tempSearchId,"g"),ele.value); //replacing the actual value with temp string inside the value template.  
                               //actualValue=postedValue.replace(/&nbsp;/g,' '); //replacing '&nbsp;' from the template string 
                               
                               } 
                            }
                      }
                  }
                 
                  inputObj.content=postedValue; //setting the actual contents 
                  //console.log(inputObj.content);
                }

          var xmlhttp;
          if(window.XMLHttpRequest) {
            xmlhttp = new XMLHttpRequest();
          } else if (window.ActiveXObject) {
            xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
          }

          xmlhttp.open("POST", "http://127.0.0.1:8000/FnActivateEvent/", true);
          xmlhttp.setRequestHeader("content-type", "application/json");
          xmlhttp.setRequestHeader("Accept", "application/json");

          xmlhttp.onreadystatechange = function () 
          {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) 
            {
                var jsonResultBuffer = JSON.parse(xmlhttp.responseText);
                
            
            }
          };

          xmlhttp.send(JSON.stringify({'inputObj':inputObj}));
        
        };

        //function prototype for string to dom object convertion
        String.prototype.toDOM=function(){
          var d=document
            ,i
            ,a=d.createElement("div")
            ,b=d.createDocumentFragment();
          a.innerHTML=this;
          while(i=a.firstChild)b.appendChild(i);
          return b;
        };
        //function to push the elemnts into the array
        function spanToArray(html){
          var matches = [];
          
          var searchEles = html.children;

          for(var i = 0; i < searchEles.length; i++) {
            
              if(searchEles[i].tagName == 'SPAN') {
                console.log(searchEles[i].innerText.indexOf('#'));
                  if(searchEles[i].innerText.indexOf('#') == 1) {
                      matches.push(searchEles[i]);
                  }
              }
          }
          
          return matches;
        };

        window.addEventListener('message',receiveMessage); //attaching message listener to recieve the message from parent window

             
