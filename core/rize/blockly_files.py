from toolbox_creator import*

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
            path + name + extension of the javascript file with the definition of new type of blocks defined by the user
    """
    def __init__(self, name_files, path_blockly, path_toolbox, default_blocks):
        # Files to save primitives and the toolbox
        self.file_b = open(path_blockly + "/blocks/" + name_files + ".js","w")
        self.file_g = open(path_blockly + "/generators/python/" + name_files + ".js","w")
        self.file_t = open(path_toolbox + "/toolbox.js","w")
        file_ct = open(default_blocks, "r") 
        custom_blocks =  file_ct.read() 
        self.toolbox = toolbox_creator(custom_blocks)

        blocks_init = "goog.provide('Blockly.Blocks." + name_files + "');\ngoog.require('Blockly.Blocks');\n"
        generator_init = "'use strict'\ngoog.provide('Blockly.Python."+ name_files +"');\ngoog.require('Blockly.Python');"
        self.file_b.write(blocks_init)
        self.file_g.write(generator_init)

    def add_code_generator(self,code):
        """ Add the code generated of a block
        
            Parameters
            ----------

            code:string
                javascript and python code to be added
        """
        self.file_g.write("\n\n") 
        self.file_g.write(code)

        
    def add_block_definition(self,block):
        """ Add the code generated of a block
        
            Parameters
            ----------

            block:string
                javascript that define the design, inputs and outputs of a block
        """

        self.file_b.write("\n\n") 
        self.file_b.write(block)

    def close_files(self):
        """ Close the files created. This function need to be executed after defining all the elements (blocks, generators and toolbox).
        """
        self.file_t.write(self.toolbox.get_output())
        self.file_t.close()
        self.file_b.close()
        self.file_g.close()

    def add_toolbox_xml(self,name,block_type):
        self.toolbox.add_xml_block(name,block_type)