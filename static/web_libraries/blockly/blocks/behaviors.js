goog.provide('Blockly.Blocks.behaviors');
goog.require('Blockly.Blocks');

Blockly.Blocks['repeat_until_action'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("Repeat");
      this.appendStatementInput("repeat")
          .setCheck(null);
      this.appendDummyInput()
          .appendField("and stop when finished");
      this.appendStatementInput("actions")
          .setCheck(null);
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#8E44AD");
   this.setTooltip("");
   this.setHelpUrl("");
    }
  };


  Blockly.Blocks['repeat_until_trigger'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("Repeat");
      this.appendStatementInput("repeat")
          .setCheck(null);
      this.appendValueInput("NAME")
          .setCheck(null)
          .appendField("and stop until detected");
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#8E44AD");
   this.setTooltip("");
   this.setHelpUrl("");
    }
  };

  Blockly.Blocks['at_the_same_time'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("At the same time do");
      this.appendStatementInput("act1")
          .setCheck(null);
      this.appendDummyInput()
          .appendField("and do");
      this.appendStatementInput("act2")
          .setCheck(null);
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#8E44AD");
   this.setTooltip("");
   this.setHelpUrl("");
    }
  };

  Blockly.Blocks['keep'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("Keep doing");
      this.appendValueInput("input")
          .setCheck(null);
      this.appendDummyInput()
          .appendField("with")
          .appendField(new Blockly.FieldDropdown([["nao","nao"], ["option","OPTIONNAME"], ["option","OPTIONNAME"]]), "robots");
      this.setPreviousStatement(true, null);
      this.setColour(240);
   this.setTooltip("");
   this.setHelpUrl("");
    }
  };

Blockly.Blocks['until'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Until ");
    this.appendValueInput("trigger")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("is detected");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['do_action'] = {
    init: function() {
      this.appendValueInput("input")
          .setCheck(null)
          .appendField("action");
      this.appendDummyInput()
          .appendField("with robot(s)");
      this.appendValueInput("robots")
          .setCheck(null)
      this.appendDummyInput()
          .appendField(new Blockly.FieldImage(play_image, 16, 16, "*", play_event));
      this.setInputsInline(true);
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#3373CC");
   this.setTooltip("Block used to indicate which human action is used to finish the robot behavior");
   this.setHelpUrl("");
    }
  };


  Blockly.Blocks['while_do'] = {
    init: function() {
      this.appendStatementInput("while")
          .setCheck(null)
          .appendField("While");
      this.appendStatementInput("do")
          .setCheck(null)
          .appendField("do");
      this.setInputsInline(true);
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour(230);
   this.setTooltip("");
   this.setHelpUrl("");
    }
  };


Blockly.Blocks['do_action_with_robot'] = {
    init: function() {
      this.appendValueInput("input")
          .setCheck(null)
          .appendField("action");
      this.appendDummyInput()
          .appendField("with robot(s)")
          .appendField(new Blockly.FieldDropdown([["nao","nao"], ["pepper","pepper"], ["arm","arm"]]), "robot")
          .appendField(new Blockly.FieldImage(play_image, 16, 16, "*",play_event));
      this.setInputsInline(true);
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#3373CC"); //Nice purple #2574A9
   this.setTooltip("Block used to indicate which human action is used to finish the robot behavior");
   this.setHelpUrl("");
    }
  };





Blockly.Blocks['do_sequence'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Do sequence")
        .appendField(new Blockly.FieldTextInput("name"), "behavior_name");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour('#2ABB9B');
 this.setTooltip("Definition of a robot behavior");
 this.setHelpUrl("");
  }
};


Blockly.Blocks['define_sequence'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Sequence")
        .appendField(new Blockly.FieldTextInput("name"), "behavior_name");
    this.appendStatementInput("behavior_code")
        .setCheck("behavior");
    this.setColour('#2ABB9B');
 this.setTooltip("Definition of a robot behavior");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['wait'] = {
	init: function() {
	  this.appendDummyInput()
		  .appendField("Wait")
		  .appendField(new Blockly.FieldTextInput("1"), "time")
		  .appendField("seconds");
	  this.setPreviousStatement(true, null);
	  this.setNextStatement(true, null);
	  this.setColour("#FF3355");
   this.setTooltip("wait a specific time in second after to start a new robot action");
   this.setHelpUrl("");
	}
  };

  Blockly.Blocks['nep_robot_behavior'] = {
	init: function() {
	  this.appendValueInput("robots")
		  .setCheck("robot")
		  .appendField("Behavior:")
		  .appendField(new Blockly.FieldTextInput("name"), "behavior_name");
	  this.appendStatementInput("behavior_code")
		  .setCheck("behavior");
	  this.setColour("#09edcc");
   this.setTooltip("Definition of a robot behavior");
   this.setHelpUrl("");
	}
	};
	

  Blockly.Blocks['nep_rule'] = {
    init: function() {
      this.appendValueInput("NAME")
          .appendField("If detected");
      this.appendStatementInput("DO")
          .setCheck(null)
          .appendField("")
          .appendField("Do:");
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#26C281");
   this.setTooltip("");
   this.setHelpUrl("");
    }
  };

  Blockly.Blocks['nep_run'] = {
	init: function() {
	  this.appendDummyInput()
		  .appendField("Run behavior ")
		  .appendField(new Blockly.FieldTextInput("name"), "name_to_execute");
	  this.setPreviousStatement(true, null);
	  this.setNextStatement(true, null);
	  this.setColour(255);
   this.setTooltip("You need to give the name of the behavior to execute");
   this.setHelpUrl("");
	}
  };

  Blockly.Blocks['rule_exit'] = {
	init: function() {
	  this.appendValueInput("input")
		  .setCheck("state")
		  .appendField("Exit if:");
	  this.setPreviousStatement(true, "behavior");
	  this.setColour("#26C281");
   this.setTooltip("Block used to indicate which human action is used to finish the robot behavior");
   this.setHelpUrl("");
	}
  };

  Blockly.Blocks['nep_set_robots'] = {
	init: function() {
	  this.appendValueInput("robots")
		  .setCheck(null)
		  .appendField("With robot (s)")
		  .appendField(new Blockly.FieldTextInput("nao"), "NAME");
	  this.setPreviousStatement(true, null);
	  this.setNextStatement(true, null);
	  this.setColour(315);
   this.setTooltip("#CF63CF");
   this.setHelpUrl("");
	}
};


Blockly.Blocks['nep_robot_reactive'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Reactive behavior")
        .appendField(new Blockly.FieldTextInput("name"), "behavior_name");
    this.appendStatementInput("behavior_code")
        .setCheck("behavior");
    this.appendDummyInput()
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("priority")
        .appendField(new Blockly.FieldNumber(0), "NAME");
    this.setColour("#06a18b");
 this.setTooltip("Definition of a robot behavior");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['add_reaction'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("Add reaction")
          .appendField(new Blockly.FieldTextInput("name"), "behavior_name");
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#06a18b");
   this.setTooltip("Add a reactive behavior");
   this.setHelpUrl("");
    }
  };



Blockly.Blocks['add_robot'] = {
    init: function() {
      this.appendDummyInput()
          .appendField(new Blockly.FieldDropdown(input_robots["options"]), "robot");
      this.setOutput(true, null);
      this.setColour("#099ced");
   this.setTooltip("");
   this.setHelpUrl("");
    }
  };



Blockly.Blocks['request_response'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Request");
    this.appendStatementInput("request")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("Response");
    this.appendStatementInput("response")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("Fails");
    this.appendStatementInput("fails")
        .setCheck(null);
    this.setInputsInline(false);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour("#099ced");
 this.setTooltip("");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['repeat_until_times'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Repeat")
        .appendField(new Blockly.FieldNumber(2, 1, Infinity, 1), "numeric_input")
        .appendField("times");
    this.appendStatementInput("actions")
        .setCheck(null);
    this.setInputsInline(false);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour("#8E44AD");
 this.setTooltip("");
 this.setHelpUrl("");
  }
};
  

  Blockly.Blocks['main_init'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("Start");
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour(0);
   this.setTooltip("");
   this.setHelpUrl("");
    }
  };
	
  Blockly.Blocks['wait'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("Wait")
          .appendField(new Blockly.FieldNumber(1, 0), "NAME")
          .appendField("seconds");
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour(0);
   this.setTooltip("wait a specific time in second after to start a new robot action");
   this.setHelpUrl("");
    }
  };


  Blockly.Blocks['social_action'] = {
    init: function() {
      this.appendValueInput("sound")
          .setCheck(null)
          .appendField("\"Play sound:\"");
      this.appendValueInput("gesture")
          .setCheck(null)
          .appendField("\"do gesture:\"");
      this.appendValueInput("motion")
          .setCheck(null)
          .appendField("\"do motion:\"");
      this.appendValueInput("feeling")
          .setCheck(null)
          .appendField("\"show feeling:\"");
      this.setInputsInline(true);
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#3373CC");
   this.setTooltip("Definition of a robot behavior");
   this.setHelpUrl("");
    }
  };


 