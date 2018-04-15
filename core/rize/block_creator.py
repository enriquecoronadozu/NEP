class block_creator:
    def __init__(self, block_name, description):
        """
            Class used to create JavaScript definitions of primitives blocks

            Parameters
            ----------
            block_name : string
                Name of the behavior block
            
            block_description : dictionary
                User-friendly description of what the block will do 
        """
        
        # New line string definition
        self.new_line = "\n"

        # Get block info
        self.block_name = block_name
        self.block_description = description

        # Set initial and final JavaScript code.
        self.init = 'Blockly.Blocks["'+ self.block_name + '"] = {' + self.new_line + 'init: function() {' + self.new_line
        self.final =  '\n\tthis.setTooltip("'+ str(self.block_description) + '");' + self.new_line + ' \tthis.setHelpUrl("");' + self.new_line + '}};'

        # Fields of the block 
        self.fields = ""

        # Counter: Number of inputs
        self.inp_num = 0

    def set_input(self, input_type):
        """ Add a new input region to the block

            Parameters
            ----------
            input_type : string
                Type of input that will be added. It can be "dummy_input" or "value_input"

            Returns
            ----------
            
            block_input : string
                Block input JavaScript code
        """
        
        if input_type == "dummy_input":
            block_input = '\tthis.appendDummyInput()' + self.new_line
        if input_type == "value_input":
            block_input = '\tthis.appendValueInput("block_input")' + self.new_line + '\t\t.setCheck("primitive")' + self.new_line
        return block_input   

    def add_dropdown_field(self,text):

        """ Add a new dropdown field to the block

            Parameters
            ----------
            text : string
                Type of input that will be added. It can be "dummy_input" or "value_input"

            Returns
            ----------
            
            block_input : string
                Block input JavaScript code
        """

                
        value = '\t\t.appendField(new Blockly.FieldDropdown(input_' + text + '["options"]), "drop_input" )' + self.new_line
        self.fields = self.fields +  value
                
        
        
    def add_text_field(self,text):
        """
            Add a text field (Label) to the block. The user can not change this label.

            Parameters
            ----------
            text : string
                Text to add to the field

        """
        value = '\t\t.appendField("' + text + '")' + self.new_line
        self.fields = self.fields +  value

    def add_configuration_image(self):
        """
        Add button image which executes the function edit_primitive Javascript function (can be defined by the developer).
        """
        value = '\t\t.appendField(new Blockly.FieldImage(configuration_image, 16, 16, "*", edit_primitive))'
        self.fields = self.fields +  value 

    def add_text_input_field(self, default_text = "edit"):
        """
            Add a textbox field, which user can fill.

            Parameters
            ----------
            default_text : string
                Default text shown in the input 

        """
        self.inp_num = self.inp_num + 1
        value ='\t\t.appendField(new Blockly.FieldTextInput("' + str(default_text) + '"), "inp_' + str(self.inp_num)+ '")' +  self.new_line
        self.fields = self.fields +  value

    def get_fields(self):
        """ Return all fields definitions
        """
        if self.fields != "":
            value =  self.fields + "\t\t;" + self.new_line
        return value


    def set_block_configuration(self,block_color,connections, allowed_types =  ["primitive", "statement", "behavior"] ):
        """
            Define the block configuration zone (color of the block, outputs and allowed connections types)

            Parameters
            ----------
            color : int
                color value
                
            connection : string
                connection type of the block, can be "top_down" or "left"

            allowed_types: list of strings
                this parameter defines which blocks inputs/outputs types can be connected this block

        """

        color = '\tthis.setColour(' + str(block_color) + ');'+ self.new_line

        if (connections == "top_down"):
            connection = '\tthis.setPreviousStatement(true,' + str(allowed_types) +');' + self.new_line + '\tthis.setNextStatement(true, ["primitive", "statement", "behavior"]);' + self.new_line
        elif (connections == "left"):
            connection = '\tthis.setOutput(true,'+ str(allowed_types) +');' + self.new_line

        conf_zone = color + connection
        return conf_zone
