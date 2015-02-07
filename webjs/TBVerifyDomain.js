        window.addEventListener('load', verifyDomain);
        function verifyDomain(){ //to load the Tb config details.
          //alert(window.location.hostname);
          
          var objectData; // Receives the objectified results of the JSON request.
          var jsonResultBuffer={};
          var xmlhttp;
          if(window.XMLHttpRequest) {
            xmlhttp = new XMLHttpRequest();
          } else if (window.ActiveXObject) {
            xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
          }

          xmlhttp.open("POST", "http://127.0.0.1:8000/FnVerifyDomain/", true);  //service url
          xmlhttp.setRequestHeader("content-type", "application/json");  
          xmlhttp.setRequestHeader("Accept", "application/json");
          xmlhttp.responseType = 'json';
          xmlhttp.onreadystatechange = function () 
          {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200)  //response of the ajax request.
            {
                    if(xmlhttp.response!="success"){ //checking for status updated in db or not
                    var source   = document.getElementById("entry-template").innerHTML; //getting the html content for handle bar
                    var template = Handlebars.compile(source); //compile the content
                     var theData={data:'Your Domain Name successully verified',img:'http://localhost:8000/files/otherImages/verified.png'};
                    var html=template(theData);
                     document.getElementById("div").innerHTML=(html);
                     window.parent.postMessage("verified", "*");
               }
              else{
                    var source   = document.getElementById("entry-template").innerHTML;
                    var template = Handlebars.compile(source);
                    var theData={data:'Sorry!! Please try again',img:'http://localhost:8000/files/otherImages/failed.png'};
                    var html=template(theData);
                    document.getElementById("div").innerHTML=(html);
                    window.parent.postMessage("verified", "*");
              }
            }
          };
          xmlhttp.send(JSON.stringify({'domainUrl':'http://localhost:9000'}));
          
        };