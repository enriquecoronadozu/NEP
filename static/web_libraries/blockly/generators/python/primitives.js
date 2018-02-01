'use strict'
goog.provide('Blockly.Python.primitives');
goog.require('Blockly.Python');

Blockly.Python['animation'] = function(block) {
var text = block.getFieldValue('inp_1');
var options_dic = block.getFieldValue('inp_2');
var code  = '{"primitive":"animation"'+","+ '"input":' + '"' + text + '"'+","+'"options":' + options_dic + '}';
return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Python['human_emotion'] = function(block) {

};

Blockly.Python['human_gesture'] = function(block) {

};

Blockly.Python['rest'] = function(block) {
var text = 'none'
var code  = '["rest",' + '"' + text + '"]';  
return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Python['say'] = function(block) {
var text = block.getFieldValue('inp_1');
var options_dic = block.getFieldValue('inp_2');
var code  = '{"primitive":"say"'+","+ '"input":' + '"' + text + '"'+","+'"options":' + options_dic + '}';
return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Python['wake_up'] = function(block) {
var text = 'none'
var code  = '["wake_up",' + '"' + text + '"]';  
return [code, Blockly.Python.ORDER_NONE];
};