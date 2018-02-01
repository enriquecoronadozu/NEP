'use strict'
goog.provide('Blockly.Python.behaviors');
goog.require('Blockly.Python');

Blockly.Python['main_init'] = function(block) {
  // TODO: Assemble Python into code variable.
  var code = '\n';
  return code;
};

// DELETE
Blockly.Python['keep'] = function(block) {
  var value_input = Blockly.Python.valueToCode(block, 'input', Blockly.Python.ORDER_ATOMIC);
  var dropdown_robots = block.getFieldValue('robots');
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};

Blockly.Python['repeat_until_action'] = function(block) {
  var statements_repeat = Blockly.Python.statementToCode(block, 'repeat');
  var statements_actions = Blockly.Python.statementToCode(block, 'actions');

  
  //Replace some code
  var repeat_value =  statements_repeat.replace("  r.new_action(","msg1 = r.new_action(")
  repeat_value =  repeat_value.replace(")",',run=False)') 
  var action_value =  statements_actions.replace("  r.new_action(","msg2 = r.new_action(")
  action_value =  action_value.replace(")",',run=False)') 

  var repeat_until_action = "r.repeat_until_action(message_continue = msg1, message_repeat =  msg2)"
  var code = repeat_value  + action_value  + repeat_until_action + '\n';
  return code;


};

Blockly.Python['repeat_until_trigger'] = function(block) {
  var statements_repeat = Blockly.Python.statementToCode(block, 'repeat');
  var value_name = Blockly.Python.valueToCode(block, 'NAME', Blockly.Python.ORDER_ATOMIC);


  var code = '...\n';
  return code;
};

// TODO: improve with mutator
Blockly.Python['at_the_same_time'] = function(block) {

  var statements_act1 = Blockly.Python.statementToCode(block, 'act1');
  var statements_act2 = Blockly.Python.statementToCode(block, 'act2');
  
  //Replace some code
  var while_value =  statements_act1.replace("  r.do_parallel_actions(","msg1 = r.do_parallel_actions(")
  while_value =  while_value.replace(")",',run=False)') 
  var do_value =  statements_act2.replace("  r.do_parallel_actions(","msg2 = r.do_parallel_actions(")
  do_value =  do_value.replace(")",',run=False)') 

  var same_time = "r.at_same_time([msg1,msg2])"
  var code = while_value  + do_value  + same_time + '\n';
  return code;
};

// DELETE
Blockly.Python['until'] = function(block) {
  var value_trigger = Blockly.Python.valueToCode(block, 'trigger', Blockly.Python.ORDER_ATOMIC);
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};

Blockly.Python['do_action'] = function(block) {
    var value_input = Blockly.Python.valueToCode(block, 'input', Blockly.Python.ORDER_NONE);
    var value_robots = Blockly.Python.valueToCode(block, 'robots', Blockly.Python.ORDER_NONE);
    // TODO: Assemble Python into code variable.
    if (value_input == ""){
      value_input = "[]"
    }
    var code = 'r.new_action(' +  value_input  +',' + value_robots  + ')' + '\n';
    var final_code =  code.replace("false","False") //Python format
    return final_code;
  };


  Blockly.Python['do_action_with_robot'] = function(block) {
    var value_input = Blockly.Python.valueToCode(block, 'input', Blockly.Python.ORDER_NONE);
    var number_time = block.getFieldValue('time');
    var dropdown_robot = block.getFieldValue('robot');
    if (value_input == ""){
      value_input = "[]"
    }

    // TODO: Assemble JavaScript into code variable.
    var code = 'r.new_action(' +  value_input  +',["' + dropdown_robot  + '"])' + '\n';
    var final_code =  code.replace("false","False") //Python format
    return final_code;
  };

  Blockly.Python['add_robot'] = function(block) {
    var dropdown_robot = block.getFieldValue('robot');
    var code = '"' + dropdown_robot + '"';
    return [code, Blockly.Python.ORDER_NONE];
  };


  Blockly.Python['define_sequence'] = function(block) {
    var text_behavior_name = block.getFieldValue('behavior_name');
    var statements_behavior_code = Blockly.Python.statementToCode(block, 'behavior_code');
    // TODO: Assemble Python into code variable.
    var code = 'def ' + text_behavior_name + '():' + '\n';
    code += statements_behavior_code;
    code += '  pass' + '\n\n' ;
    return code;
  };


  Blockly.Python['do_sequence'] = function(block) {
    var text_behavior_name = block.getFieldValue('behavior_name');
    // TODO: Assemble Python into code variable.
    var code = text_behavior_name + '() \n';
    return code;
  };


  Blockly.Python['social_action'] = function(block) {
    var value_sound = Blockly.Python.valueToCode(block, 'sound', Blockly.Python.ORDER_NONE);
    var value_body = Blockly.Python.valueToCode(block, 'body', Blockly.Python.ORDER_NONE);
    var value_feel = Blockly.Python.valueToCode(block, 'feel', Blockly.Python.ORDER_NONE);
    // TODO: Assemble Python into code variable.
    var code = 'actions = [' + value_sound + ',' + value_body + ','  +   value_body + ']'   + '\n';
    code += 'r.do_actions(actions)' + '\n';
    return code;
  };

  Blockly.Python['nep_rule'] = function(block) {
    var value_name = Blockly.Python.valueToCode(block, 'NAME', Blockly.Python.ORDER_NONE);
    // TODO: Assemble Python into code variable.
    var n = 0;
    var code , branchCode, conditionCode;
    conditionCode =  'human_action  == "' +  value_name + '"' ;
    branchCode = Blockly.Python.statementToCode(block, 'DO');
    code += (n == 0 ? 'if ' : 'elif ' ) + conditionCode + ':\n'  + branchCode;
    return code;
  };

  Blockly.Python['nep_robot_reactive'] = function(block) {
    var text_behavior_name = block.getFieldValue('behavior_name');
    var value_robots = Blockly.Python.valueToCode(block, 'robots',Blockly.Python.ORDER_NONE);
    var statements_behavior_code = Blockly.Python.statementToCode(block, 'behavior_code');
    var number_name = block.getFieldValue('NAME');
    // TODO: Assemble Python into code variable.
    var code = statements_behavior_code + '\n';
    return code;
  };

  Blockly.Python['repeat_until_times'] = function(block) {
    var number_numeric_input = block.getFieldValue('numeric_input');
    var statements_actions = Blockly.Python.statementToCode(block, 'actions');
    // TODO: Assemble Python into code variable.
    var code =  'for i in range('+ number_numeric_input +'):\n'  + statements_actions  +'\n';
    return code;
  };


  Blockly.Python['wait'] = function(block) {
    var number_name = block.getFieldValue('NAME');
    // TODO: Assemble Python into code variable.
    var code = 'time.sleep ('+ number_name  +')\n';
    return code;
  };

  Blockly.Python['social_action'] = function(block) {
    var value_sound = Blockly.Python.valueToCode(block, 'sound', Blockly.Python.ORDER_ATOMIC);
    var value_gesture = Blockly.Python.valueToCode(block, 'gesture', Blockly.Python.ORDER_ATOMIC);
    var value_motion = Blockly.Python.valueToCode(block, 'motion', Blockly.Python.ORDER_ATOMIC);
    var value_feeling = Blockly.Python.valueToCode(block, 'feeling', Blockly.Python.ORDER_ATOMIC);
    // TODO: Assemble Python into code variable.
    var code = '...\n';
    return code;
  };


