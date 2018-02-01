from rize import*
import os
from os import listdir
from os.path import isfile, join

# Color for each primitive type
ROBOT_ACTION = '''"#099ced"'''
CONFIG = '''"#575E75"'''
ROBOT_MODE = '''"#FF4D6A"'''
HUMAN_STATE = '''"#47A8D1"'''

#TODO: reconocer cuando existe una diferencia entre el nombre de la database y la primitiva y mandar mensaje cuando no existe data base para un dropdown: IMPORTANTE

def dict2JSblock(block_name, block_description):
    """
    Define new block from a description, this function can generate more that one block for each JSON definition depending of the primitive type
    """

    # Primitive name
    main_text =  block_description["primitive"]
    # Primitive type
    primitive_type = block_description["type"]
    # User description of the primitive
    description = block_description["description"]

    # New block creator
    d = block_creator(block_name, description)
     # New dummy input
    dummy_input = d.set_input("dummy_input")
    # Set the primitive name
    d.add_text_field(main_text)



    # Set a specific color for each type of primitive
    if primitive_type == "robot_action":
        
        #Add field for main description
        d.add_text_input_field()
        # Add options label
        d.add_text_field("options")
        # Add field for options
        d.add_text_input_field()
        # Add image to open modal
        d.add_configuration_image()
        # Get all fields
        fields_region = d.get_fields()

        # Set color of the block
        block_color = ROBOT_ACTION 
        conf_zone = d.set_block_configuration(block_color,"left", ["primitive"])

    elif primitive_type == "robot_mode":

        fields_region = d.get_fields()
        block_color = ROBOT_MODE
        conf_zone = d.set_block_configuration(block_color,"left", ["primitive"])

    elif primitive_type == "human_state":
        
        #Add field for main description
        d.add_text_input_field()
        # Add image to open modal
        d.add_configuration_image()
        # Get all fields
        fields_region = d.get_fields()
        # Set color of the block
        block_color = HUMAN_STATE
        conf_zone = d.set_block_configuration(block_color,"left", ["human_state"])

    block = d.init + dummy_input + fields_region + conf_zone  + d.final
    blocks = [block]
    names = [block_name]
   
    return blocks,names




# Get list of primitives in some folder
path = "primitives"
onlyfiles = getFiles(path)
print ("Available primitives:" +  str(onlyfiles))

blockly = blockly_files("primitives", "web_libraries/blockly", "rize", "nep_blocks.js")

file_d = open("rize/databases.js","w")
file_d.write("var database = ")
file_d.write("{")

for f in onlyfiles:
    #try:
    name_file =  f.split('.')[0]

    json_data = read_json(path + "/" + f)
    data =json2dict(json_data)
    blocks, names = dict2JSblock(name_file,data)

    # Have the primitive optional parameters
    options = False
    if "options" in data:
        options = True
        
    # Add the blocks to the toolbox and javascript file
    i = 0
    for block in blocks:
        
        name = names[i]
        print 
        print name
        blockly.add_toolbox_xml(name,data['type'])


        # This in order to deal with the 2 version of the action primitives
        c = code_generator(name, name_file, data['type'], options)        
        code =  c.get_code()
        blockly.add_code_generator(code)
        blockly.add_block_definition(block)
        i = i +1

        file_d.write(name_file + ': {"input":{"type":' + '"'+ data['input'] + '",')
        
        if  data['input'] == "dropdown":
            json_data = read_json("databases/" + f)
            values =json2dict(json_data)
            file_d.write('"values":'+   dict2json(values['values']) + "," )
        file_d.write("}, \n")
        if "options" in data:
            file_d.write('"options":'+   dict2json(data['options']) + "," )
        file_d.write("}, \n")
    
file_d.write("}")


    


# TODO: build database
# Get list of database for primitives
"""path = "databases"
onlyfiles = getFiles(path)
print ("Available databases:" +  str(onlyfiles))



file_d = open("rize/databases.js","w")
for f in onlyfiles:
    name_file =  f.split('.')[0]

    # Create 2 blocks for each primitive
    json_data = read_json(path + "/" + f)
    data =json2dict(json_data)
    options = data["options"]
    value =  name_file + ": " + json_data + "\n"
    file_d.write(value) """

blockly.close_files()
file_d.close()         


