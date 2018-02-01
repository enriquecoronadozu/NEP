

class toolbox_creator():
    def __init__(self, custom_blocks):
        """Creates a new blockly toolbox
            
            Parameters
            ----------

            custom_blocks : string 
                XML data of default block definitions
        """
        # Define the starung and final XML definition of the toolbox
        self.js_init = """var toolbox = '<xml id="toolbox" style="display: none">';"""
        self.js_init = self.js_init + custom_blocks  + "\n"
        self.js_final = "toolbox += '</xml>';"
        self.categories = {} # This variabel saves the XML definitions of the blocks in a string 
    
    def add_xml_block(self,block_name,category):
        """ Add a new block definition to the toolbox and set the category
            
            Parameters
            ----------

            block_name : string 
                Name of the block
            category : string 
                Category of the block
        """

        if category in self.categories:
            # Concatenate a block in the XML definition (in a string) of the category
            self.categories[category] = self.categories[category] + "toolbox +='    <block type=" +'"'+ str(block_name) +'"' + "></block>';\n"
        else:
            # Start the XML definition (in a string) of a category
            self.categories[category] = "toolbox +='    <block type=" +'"'+ str(block_name) +'"' + "></block>';\n"
            

    def __add_category(self, category_name, color = "#F62459"):
        category_name = category_name.replace("_", " ")
        value = "toolbox += '" +  '<category name="' + str(category_name) + '"' + ' colour="' +  color + '"' + """>'\n"""
        return value

    def get_output(self):

        blocks = ""

        # Define categories
        for cat in self.categories:
            blocks = blocks + self.__add_category(cat)
            blocks = blocks + self.categories[cat] + """toolbox += '  </category>';\n"""
        
        # Concatenate the XML definitions
        value = self.js_init + blocks + self.js_final  
        return value

