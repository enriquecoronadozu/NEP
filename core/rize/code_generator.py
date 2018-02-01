class code_generator:
    
    def __init__(self, block_name, primitive_name, primitive_type, options):
        self.new_line = "\n"
        self.init = "Blockly.Python['" + str(block_name) + "'] = function(block) {" + self.new_line
        self.text_input = ""
        self.block_input = ""
        self.code_value = ""
        self.final = ""


        #TODO improve
        if primitive_type == "robot_action":
            self.text_input = "var text = block.getFieldValue('inp_1');" + self.new_line
            if options:
                self.text_input = self.text_input + "var options_dic = block.getFieldValue('inp_2');" + self.new_line
            
            coma = '+","+' 
            dictionary_start =   "var code  = '{"
            primitive_field = '"primitive":"' +  str(primitive_name) + '"' + "'"
            input_field = """ '"input":' + '"' + text + '"'"""
            option_feld = """'"options":' + options_dic + '}';"""

            self.code_value = dictionary_start + primitive_field + coma + input_field + coma + option_feld + self.new_line

            #self.code_value = '''var code  = '{"''' + str(primitive_name) + '''":' + '"' + text + '", "options":' + options_dic + '}'; ''' + self.new_line
            self.final = "return [code, Blockly.Python.ORDER_NONE];"

        if primitive_type == "robot_mode":
            self.text_input = "var text = 'none'" + self.new_line
            self.code_value = '''var code  = '["''' + str(primitive_name) + '''",' + '"' + text + '"]';  ''' + self.new_line 
            self.final = "return [code, Blockly.Python.ORDER_NONE];"


    def get_code(self):
        return self.init + self.text_input +  self.block_input + self.code_value +  self.final + self.new_line + "};"
