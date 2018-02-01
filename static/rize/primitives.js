var current_primitive_options; // Get the inputs from the selected block
var current_primitive_input;

// TODO: code must be changed and generated ----- ???
var html_header;
var html_input;
var html_options;
var html_set =  `&nbsp; <div><button type="button" class="btn btn-info btn-lg" style=" margin-left:80px; float:center; text-align:center;" onclick="primitives.onUpdateOptions()" data-dismiss="modal" >set values</i> </button></div> `
// -----------------
var primitives = {

  onGetHTML: function(current_primitive,type) {
  html_header = `<div class="modal-header"><button type="button" class="close" onclick="rize.onCloseAll()" data-dismiss="modal">&times;</button><h4 class="modal-title">`+type+'</h4></div>';
  html_input = "<label>Input</label>" + primitives.onSetInput(current_primitive);
  if (current_primitive.hasOwnProperty('options'))
  {
    html_options = primitives.onSetOptions(current_primitive.options);
  }
  else{
    html_options =  ""
  }
  return html_header  + html_input  + html_options + html_set
  },

  onSetOptions: function (options)
  {
    var temp_html = "";
    var keys = Object.keys(options);
    for(var i=0;i<keys.length;i++){
        var key = keys[i];
  
        temp_html += "<div><label>" + key + "</label> &nbsp;";
        temp_html += primitives.onFillInput(key, options[key]);
        temp_html += "</div>";
        console.log(key, options[key]);
    }
    console.log(temp_html);
    return temp_html;
  },

  onFillInput: function (input,type)
  {
    try {
        if(type == "string")
        {
          return  '<input class="form-control" id = "option_' + input + '">'
        }
        if(type == "percentage")
        {
          return '<input id="option_' + input + '" type="range" min="0" max="100" value="50" step="2" />'
        }
        if(type == "bool")
        {
          return '<input type="checkbox" id = "option_' + input + '">'
        }
    }
    catch(err) {
            return "";
    }
  },


  onSetInput: function(primitive)
  {
    try {
      if(primitive.input.type == "dropdown")
      {
          return  '<select class="form-control" id = "main_input">' + primitives.onFilldropdown(primitive.input.values);
      } 
      if(primitive.input.type == "string")
      {
        return  '<textarea class="form-control" id = "main_input"></textarea>'
      }
      if(primitive.input.type == "percentage")
      {
        return '<input id="main_input" type="range" min="0" max="100" value="50" step="2" />'
      }
      if(primitive.input.type == "bool")
      {
        return '<input type="checkbox" id="main_input">'
      }
    }
    catch(err) {
            return "";
    }
  },


  onUpdateOptions: function ()
  {
    
      let options = current_primitive.options;
      // TODO: must be generated   ---------
      current_primitive_input = document.getElementById("main_input").value;
      console.log(document.getElementById("main_input"));

      

      current_primitive_options =  {}
      var keys = Object.keys(options);
      console.log(keys)
      for(var i=0;i<keys.length;i++){
          var key = keys[i];
          if(options[key] == "bool")
          {
            current_primitive_options[key] =  document.getElementById("option_"+key).checked;
          }
          else{
            current_primitive_options[key] = document.getElementById("option_"+key).value;
          }
      }
      
      // ------------------------

      //block_selected.setFieldValue(current_primitive_input, "inp_1");
      block_selected.setFieldValue(current_primitive_input, "inp_1");
      block_selected.setFieldValue(JSON.stringify(current_primitive_options), "inp_2");

  },

  onFilldropdown: function(input)
  {

    var listItems = '<option selected="selected" value="0">- Select -</option>';
    for (var i = 0; i < input.length; i++) {
        listItems += "<option value='" + input[i].name + "'>" + input[i].name + "</option>";
    }
    listItems+="</select>";
    return listItems

  }


  /*
    let dropdown = $('#locality-dropdown');
    
    dropdown.empty();
    
    dropdown.append('<option selected="true" disabled>Choose State/Province</option>');
    dropdown.prop('selectedIndex', 0);
    
    const url = 'https://api.myjson.com/bins/7xq2x';

    var $dropdown = $('#locality-dropdown'); 

    $.each(result, function() {
      $dropdown.append($("<option />").val(this.ImageFolderID).text(this.Name));
    });*/

    


}


