from toolbox_creator import*
from rize import*

class blockly_files:
    """
        Write and save the javascript files needed to define a blockly enviroment

        Parameters
        ----------

        name_files: string
            name of the blockly files (block definition and code generator)
        path_blockly: string
            path where the blockly library is saved
        path_toolbox: string
            path where the toolbox definition will be saved a used to define the blockly enviroment
        default_blocks:string
            path + name + extension of the javascript file that has a default toolbox description (developer specific blocks)
    """
    def __init__(self, name_files, path_blockly, path_toolbox, default_blocks):
        # Files to save primitives and the toolbox
        self.file_b = open(path_blockly + "/blocks/" + name_files + ".js","w")
        self.file_g = open(path_blockly + "/generators/python/" + name_files + ".js","w")
        self.file_t = open(path_toolbox + "/toolbox.js","w") # Envrioment toolbox description



        self.file_d = open(path_toolbox + "/databases.js","w")
        self.file_d.write("var database = ")
        self.file_d.write("{")


        file_ct = open(default_blocks, "r") 
        custom_blocks =  file_ct.read() 
        self.toolbox = toolbox_creator(custom_blocks)

        blocks_init = "goog.provide('Blockly.Blocks." + name_files + "');\ngoog.require('Blockly.Blocks');\n"
        generator_init = "'use strict'\ngoog.provide('Blockly.Python."+ name_files +"');\ngoog.require('Blockly.Python');"
        self.file_b.write(blocks_init)
        self.file_g.write(generator_init)

    def add_code_generator(self,code):
        """ Add the code that will be generated the a block
        
            Parameters
            ----------

            code:string
                javascript and python code to be added
        """
        self.file_g.write("\n\n") 
        self.file_g.write(code)

        
    def add_block_definition(self,block):
        """ Add the javascript block definition
        
            Parameters
            ----------

            block:string
                javascript that define the design, inputs and outputs of a block
        """

        self.file_b.write("\n\n") 
        self.file_b.write(block)

    def add_toolbox_xml(self,name,block_type):
        """ This function add a new block description to a XML file that define the blockly toolbox.
        """
        self.toolbox.add_xml_block(name,block_type)

    def add_database(self, name_file, data):
        """ Add database values for each primitive
        
            Parameters
            ----------

            name_file: string
                Name of the file that describes the primitive

            data:dictionary
                dictionary with the description of the primitive
        """

        self.file_d.write(name_file + ': {"input":{"type":' + '"'+ data['input'] + '",')
        
        if  data['input'] == "dropdown":
            try:
                json_data = read_json("databases/" + name_file + ".json")
                values =json2dict(json_data)
                self.file_d.write('"values":'+   dict2json(values['values']) + "," )
                
            except:
                print ("No database javascript file for primitive: " + data["primitive"])
        self.file_d.write("},")

        

        # This options values will be readed by Javascript to generate the form based interfaces
        if "options" in data:
            self.file_d.write('"options":'+   dict2json(data['options'])  )
        self.file_d.write("}, \n")
        

    def close_files(self):
        """ This function close the files created, code generators, toolbox and blocks.
        """
        self.file_d.write("}")
        self.file_t.write(self.toolbox.get_output())
        self.file_t.close()
        self.file_b.close()
        self.file_g.close()
        self.file_d.close()  
       

