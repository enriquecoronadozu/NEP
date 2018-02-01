goog.provide('Blockly.Blocks.primitives');
goog.require('Blockly.Blocks');


Blockly.Blocks["animation"] = {
init: function() {
	this.appendDummyInput()
		.appendField("animation")
		.appendField(new Blockly.FieldTextInput("edit"), "inp_1")
		.appendField("options")
		.appendField(new Blockly.FieldTextInput("edit"), "inp_2")
		.appendField(new Blockly.FieldImage(configuration_image, 16, 16, "*", edit_primitive))		;
	this.setColour("#099ced");
	this.setOutput(true,['primitive']);

	this.setTooltip("Perform some complex animation movement");
 	this.setHelpUrl("");
}};

Blockly.Blocks["human_emotion"] = {
init: function() {
	this.appendDummyInput()
		.appendField("human emotion")
		.appendField(new Blockly.FieldTextInput("edit"), "inp_1")
		.appendField(new Blockly.FieldImage(configuration_image, 16, 16, "*", edit_primitive))		;
	this.setColour("#47A8D1");
	this.setOutput(true,['human_state']);

	this.setTooltip("Imitate an animal or character");
 	this.setHelpUrl("");
}};

Blockly.Blocks["human_gesture"] = {
init: function() {
	this.appendDummyInput()
		.appendField("human gesture")
		.appendField(new Blockly.FieldTextInput("edit"), "inp_1")
		.appendField(new Blockly.FieldImage(configuration_image, 16, 16, "*", edit_primitive))		;
	this.setColour("#47A8D1");
	this.setOutput(true,['human_state']);

	this.setTooltip("Imitate an animal or character");
 	this.setHelpUrl("");
}};

Blockly.Blocks["rest"] = {
init: function() {
	this.appendDummyInput()
		.appendField("rest")
		;
	this.setColour("#FF4D6A");
	this.setOutput(true,['primitive']);

	this.setTooltip("Put the robot in a rest state");
 	this.setHelpUrl("");
}};

Blockly.Blocks["say"] = {
init: function() {
	this.appendDummyInput()
		.appendField("say")
		.appendField(new Blockly.FieldTextInput("edit"), "inp_1")
		.appendField("options")
		.appendField(new Blockly.FieldTextInput("edit"), "inp_2")
		.appendField(new Blockly.FieldImage(configuration_image, 16, 16, "*", edit_primitive))		;
	this.setColour("#099ced");
	this.setOutput(true,['primitive']);

	this.setTooltip("Say something with the robot");
 	this.setHelpUrl("");
}};

Blockly.Blocks["wake_up"] = {
init: function() {
	this.appendDummyInput()
		.appendField("wake up")
		;
	this.setColour("#FF4D6A");
	this.setOutput(true,['primitive']);

	this.setTooltip("Turn on the robot from a rest state");
 	this.setHelpUrl("");
}};