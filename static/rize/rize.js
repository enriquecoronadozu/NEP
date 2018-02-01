// rize.js
var rize = {

        // ------------------------------------ onConnectRobot -----------------------------------
        // Description: Get robot parameters from the form and launch the robot node

        onConnectRobot: function() {
            default_robot_type = document.getElementById("type_robot_simple").value;
            console.log("Default robot changed to: " + default_robot_type);
            default_robot_name = document.getElementById("name_robot").value;
            console.log("New name of the default robot: " + default_robot_name);
            default_robot_ip =  document.getElementById("ip_robot_simple").value + document.getElementById("last_ip_simple").value 
            console.log("IP cahnged to: " +  default_robot_ip);
            var node_name = default_robot_type + "_action";
            console.log("IP of the robot: " + default_robot_ip);
            var json = {"action":"launch_action", "node_name":node_name, "robot_name":default_robot_name, "robot_ip":default_robot_ip }
            console.log(JSON.stringify(json));
            //POST the text to the server
            $.ajax({
                    type : "POST",
                    url : url_var,
                    contentType: "application/json; charset=utf-8",
                    data : JSON.stringify(json),
                    dataType : "json"
                });
        },


        // ------------------------------------ onStopCode -----------------------------------
        // Description: Set message to kill cognitibe node
        onStopCode: function() {
             // Action to do by the server
            var json = {"action":"stop", "input":"main"}
            console.log(JSON.stringify(json));
            $.ajax({
                    type : "POST",
                    url : url_var,
                    contentType: "application/json; charset=utf-8",
                    data : JSON.stringify(json),
                    dataType : "json"
                });
                
        },

        // -------------------------------- LoadInitBlocks ---------------------------------
        // Description: Load a initial workspace when the interface is loaded 
        loadInitBlocks: function(){
            $.ajax({
                'url' : 'interface/init_block.xml',   // init_block will be loaded whn the interface starts
                'dataType' : 'text',
                'cache' : false,
                'success' : function(xml){
                    xml = Blockly.Xml.textToDom(xml);
                    WORKSPACE.clear();
                    Blockly.Xml.domToWorkspace(xml, WORKSPACE);
                }
            });
        },

        //  ------------------------------------- onRunCode ------------------------------------
        //  Description: This function is used to send the code to the server.
        // The message sended have the next format:
        // "run&" +  code, where "run" is a string that will indicate to the server that the action to be done is to run code
        // & is used as a delimiter in the server. The code is extracted from the workspaceToCode function.

        onRunCode: function () {
            // Get the code from the blocks 
            var code = Blockly.Python.workspaceToCode(WORKSPACE);
        
            code = default_code + code
            // See the code in the console (for example the Chorme console)
            console.log(code);
        
            // Action to do by the server
            var json = {"action":"run", "input":code}
            console.log(JSON.stringify(json));
            $.ajax({
                    type : "POST",
                    url : url_var,
                    contentType: "application/json; charset=utf-8",
                    data : JSON.stringify(json),
                    dataType : "json"
                });
        },

        // ---------------------------- doUndo -----------------------
        // Description: recover workspace (before action)
        doUndo: function(){
            WORKSPACE.undo(false);
        },

        
        // ---------------------------- doRedo-----------------------
        // Description: recover workspace (after action)

        doRedo: function(){
            WORKSPACE.undo(true);
        },


        // ------------------------------------------ onSeeCode ----------------------------------------------
        // Description: See the code generated in the modal CodeModal
        onSeeCode: function(){
            
            Blockly.Python.INFINITE_LOOP_TRAP = null;
            var source_code = Blockly.Python.workspaceToCode(WORKSPACE);
                    
            source_code = default_code + source_code //Import defualt libraries
            source_code = source_code.replace(/ /g, '&nbsp;');
            source_code = source_code.replace(/\n/g, '<br />');
            source_code = '<div style="font-weight:bold; text-align: left;" >' + source_code + '</div>';

            source_code = '<h3> Code </h3> ' +  source_code;


            $('.show_code').html(source_code);
            rize.code_openNav()
            
        },

        onAutoSaveProject: function () {
          if (current_project_defined == false){
              rize.onServerSave("default")
             }
            else{
              rize.onServerSave(project_name, "auto")
            }
        },

        onServerSave: function(name, how){
             // Get the code from the blocks 
             var code = Blockly.Python.workspaceToCode(WORKSPACE);
             code = default_code + code
         
             // See the code in the console (for example the Chorme console)
             console.log(code);
 
             // Transform the block in a xml format
             var xml = Blockly.Xml.workspaceToDom(WORKSPACE);
             // Tranform a xml text in a more redeable xml text
             xml = Blockly.Xml.domToPrettyText(xml);
             console.log(xml);
 
            if (how == "user")
            {
              var save_json = {"action":"save", "code":code, "xml":xml, "name":name, "how":"user"}
            }
            else
            {
              var save_json = {"action":"save", "code":code, "xml":xml, "name":name, "how":"auto"}
            }
         
             // Action to do by the server
 
             console.log(JSON.stringify(save_json));
             $.ajax({
                     type : "POST",
                     url : url_var,
                     contentType: "application/json; charset=utf-8",
                     data : JSON.stringify(save_json),
                     dataType : "json"
                 });
        },

        //  ------------------------------------- onSaveProject ------------------------------------
        // Description: This function is used to send the xml and pthon code of the current project

        onSaveProject: function () {

          if (current_project_defined == false){

            swal({
              title:'Save project as',
              text: "Name of your new project",
              input: "text",
              showCancelButton: true,
              showLoaderOnConfirm: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: 'Save new project',
              preConfirm: function (text) {
                return new Promise(function (resolve, reject) {
                  setTimeout(function() {
                    if (text === '') {
                      swal.showValidationError(
                        'This name is not valid'
                      )
                    }
                    else{
                      current_project_defined =  true;
                      project_name = text
                      console.log("New project request: " + project_name);
                      rize.onServerSave(project_name, "user");

                    }
                    resolve()
                  }, 1000)
                })
              },
              allowOutsideClick: false
            }).then(function (result) {
              if (result.value) {
                swal({
                  type: 'success',
                  title: 'New project created!',
                  html: 'Project name: ' + project_name 
                })
              }
            })

          }
          else{
              rize.onServerSave(project_name, "user");
            }
      },

        // ------------------------------- onSaveBlocklyXML -------------------------
        // Description: Save Blockly programs in XML
        onSaveBlocklyXML: function(){
            
            
            // Transform the block in a xml format
            var xml = Blockly.Xml.workspaceToDom(WORKSPACE);
            // Tranform a xml text in a more redeable xml text
            xml = Blockly.Xml.domToPrettyText(xml);
            console.log(xml);
            // Save a file
            Download.save(xml,"blocks.xml");
        
            // Save the python code --- TODO: in other button
            Blockly.Python.INFINITE_LOOP_TRAP = null;
            var code = Blockly.Python.workspaceToCode(WORKSPACE);
            code = default_code + code
            console.log(code);
        
            Download.save(code,"code.py");
        
        },

        // Update selector with a list od projects
        onLoadProject: function() {

          var json = {"action":"load", "name":project_name}
          console.log("Load" + project_name)
          $.ajax({
            'type' : "POST",
            'url' : url_var,
            'contentType': "application/json; charset=utf-8",
            'data' : JSON.stringify(json),
            'dataType' : "json",
            'success' : function(projects){
              
              list_projects = projects['projects']
              console.log(list_projects)


                  var oldSel = $('.project_selector').get(0);
              
                  while (oldSel.options.length > 0) {
                      oldSel.remove(oldSel.options.length - 1);
                  }
              
              
                  for (i = 0; i < list_projects.length; i++)
                  {
                      var opt = document.createElement('option');
              
                      opt.text = list_projects[i]
                      opt.value = list_projects[i]
              
                      oldSel.add(opt, null);
                  }
              
              rize.load_openNav()
            }
            
          });
        },

        // --------------------------------------- onNewProject ---------------------------------------
        // Description: Create a new project

        onNewProject: function() {     
        
            swal({
                title: 'Warning: The progress not saved will be delated',
                text: "Name of your new project",
                input: "text",
                type: 'warning',
                showCancelButton: true,
                showLoaderOnConfirm: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Create new project',
                preConfirm: function (text) {
                  return new Promise(function (resolve, reject) {
                    setTimeout(function() {
                      if (text === '') {
                        swal.showValidationError(
                          'This name is not valid'
                        )
                      }
                      else{
                        current_project_defined =  true;
                        project_name = text
                        console.log("New project request: " + project_name);
                        rize.onServerSave(project_name, "user");
                      }
                      resolve()
                    }, 1000)
                  })
                },
                allowOutsideClick: false
              }).then(function (result) {
                if (result.value) {
                  swal({
                    type: 'success',
                    title: 'New project created!',
                    html: 'Project name: ' + project_name 
                  })
                }
              })

        },

        // --------------------------------------- onClearWorkspace  ---------------------------------------
        // Description: Clear all blockly workspace
        onClearWorkspace:function (){
                WORKSPACE.clear();
        },


        // ---------------------------------------- openNav -------------------------------------------

        openNav:function () {
          rize.oncloseAll()
          document.getElementById("my_right_sidenav").style.width = "100px";
          document.getElementById("main").style.marginRight = "100px";
          onresize();
          Blockly.svgResize(WORKSPACE);
          input_robots={"options": [["nao", "nao"]]}
        },

      // ---------------------------------------- closeNav -------------------------------------------
      
      closeNav:function () {
          document.getElementById("my_right_sidenav").style.width = "0";
          document.getElementById("main").style.marginRight = "30px";
          onresize();
          Blockly.svgResize(WORKSPACE);
      },


      // ---------------------------------------- button_openNav -------------------------------------------

            button_openNav:function () {
              rize.onCloseAll()
              document.getElementById("my_button_sidenav").style.width = "620px";
            },
      
      // ---------------------------------------- button_closeNav -------------------------------------------
            
            button_closeNav:function () {
                document.getElementById("my_button_sidenav").style.width = "0";
            },


    // ---------------------------------------- code_openNav -------------------------------------------

          code_openNav:function () {
            rize.onCloseAll()
            document.getElementById("code_sidenav").style.width = "80%";
          },
    
    // ---------------------------------------- code_closeNav -------------------------------------------
          
          code_closeNav:function () {
              document.getElementById("code_sidenav").style.width = "0";
          },
                      
                

            

      // ---------------------------------------- connect_openNav -------------------------------------------

      connect_openNav:function () {
        rize.onCloseAll()
        document.getElementById("connect_sidenav").style.width = "300px";
        document.getElementById("main").style.marginRight = "300px";
        onresize();
        Blockly.svgResize(WORKSPACE);
      },

      // ---------------------------------------- connect_closeNav -------------------------------------------
      
      connect_closeNav:function () {
          document.getElementById("connect_sidenav").style.width = "0";
          document.getElementById("main").style.marginRight = "30px";
          onresize();
          Blockly.svgResize(WORKSPACE);
      },
                
          
        

            // ---------------------------------------- load_openNav -------------------------------------------

            load_openNav:function () {
              rize.onCloseAll()
              document.getElementById("load_sidenav").style.width = "250px";
              document.getElementById("main").style.marginRight = "270px";
              onresize();
              Blockly.svgResize(WORKSPACE);
            },
      
            // ---------------------------------------- load_closeNav -------------------------------------------
            
            load_closeNav:function () {
                document.getElementById("load_sidenav").style.width = "0";
                document.getElementById("main").style.marginRight = "30px";
                onresize();
                Blockly.svgResize(WORKSPACE);
            },


            // ---------------------------------------- primitive_openNav -------------------------------------------

            primitive_openNav:function () {
                rize.closeNav()
                document.getElementById("primitive_sidenav").style.width = "250px";
                document.getElementById("main").style.marginRight = "270px";
                onresize();
                Blockly.svgResize(WORKSPACE);
              },
                  
            // ---------------------------------------- primitive_closeNav -------------------------------------------
                        
            primitive_closeNav:function (html_val) {
                document.getElementById("primitive_sidenav").style.width = "0";
                document.getElementById("main").style.marginRight = "30px";
                onresize();
                Blockly.svgResize(WORKSPACE);
            },


        // ----------------------------------- Load XML blocks ---------------------------------------------



               // Clear the workspace and add the blocks from an XML file
        onXML2Workspace: function(file_load){
        $.ajax({
            'url' : file_load,
            'dataType' : 'text',
            'cache' : false,
            'success' : function(xml){
                //Load project
                xml = Blockly.Xml.textToDom(xml);
                WORKSPACE.clear();
                Blockly.Xml.domToWorkspace(xml, WORKSPACE);
                //Update name of the project
                current_project_defined = true;
            }});
          },

          onRecover:function()
          {
                    var e = document.getElementById("project_load");
                    var name_folder = e.options[e.selectedIndex].value;
                    if (name_folder == "")
                    {
                      name_folder =  "default"
                    }
                    var file_load =  "static/projects/" + String(name_folder) + "/recover_blocks.xml";
                    rize.onXML2Workspace(file_load);
                    project_name = name_folder

          },

          onLoad: function ()
          {
                    var e = document.getElementById("project_load");
                    var name_folder = e.options[e.selectedIndex].value;
                    var file_load =  "static/projects/" + String(name_folder) + "/blocks.xml";
                    rize.onXML2Workspace(file_load);
                    project_name = name_folder

          },

          onCloseAll: function()
          {
            rize.button_closeNav()
            rize.closeNav()
            rize.load_closeNav()
            rize.primitive_closeNav()
            rize.connect_closeNav()
            rize.code_closeNav()
          },

}
                      
                
            