/**
 * @license
 * Visual Blocks Editor
 *
 * Copyright 2017 Google Inc.
 * https://developers.google.com/blockly/
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

 /**
 * @fileoverview Tests for Blockly.Events
 * @author marisaleung@google.com (Marisa Leung)
 */
'use strict';

goog.require('goog.testing');
goog.require('goog.testing.MockControl');

var mockControl_;
var workspace;

function eventTest_setUp() {
  workspace = new Blockly.Workspace();
  mockControl_ = new goog.testing.MockControl();
}

function eventTest_setUpWithMockBlocks() {
  eventTest_setUp();
  Blockly.defineBlocksWithJsonArray([{
    'type': 'field_variable_test_block',
    'message0': '%1',
    'args0': [
      {
        'type': 'field_variable',
        'name': 'VAR',
        'variable': 'item'
      }
    ],
  }]);
}

function eventTest_tearDown() {
  mockControl_.$tearDown();
  workspace.dispose();
}

function eventTest_tearDownWithMockBlocks() {
  eventTest_tearDown();
  delete Blockly.Blocks.field_variable_test_block;
}

function test_abstract_constructor_block() {
  eventTest_setUpWithMockBlocks();
  setUpMockMethod(mockControl_, Blockly.utils, 'genUid', null, '1');
  var block = new Blockly.Block(workspace, 'field_variable_test_block');
  var event = new Blockly.Events.Abstract(block);
  assertUndefined(event.varId);
  checkExactEventValues(event, {'blockId': '1', 'workspaceId': workspace.id,
    'group': '', 'recordUndo': true});
  eventTest_tearDownWithMockBlocks();
}

function test_abstract_constructor_variable() {
  eventTest_setUpWithMockBlocks();
  setUpMockMethod(mockControl_, Blockly.utils, 'genUid', null, '1');
  var variable = workspace.createVariable('name1', 'type1', 'id1');
  var event = new Blockly.Events.Abstract(variable);
  assertUndefined(event.blockId);
  checkExactEventValues(event, {'varId': 'id1',
    'workspaceId': workspace.id, 'group': '', 'recordUndo': true});
  eventTest_tearDownWithMockBlocks();
}

function test_abstract_constructor_null() {
  eventTest_setUpWithMockBlocks();
  var event = new Blockly.Events.Abstract(null);
  assertUndefined(event.blockId);
  assertUndefined(event.workspaceId);
  checkExactEventValues(event, {'group': '', 'recordUndo': true});
  eventTest_tearDownWithMockBlocks();
}

function checkCreateEventValues(event, block, ids, type) {
  var expected_xml = Blockly.Xml.domToText(Blockly.Xml.blockToDom(block));
  var result_xml = Blockly.Xml.domToText(event.xml);
  assertEquals(expected_xml, result_xml);
  isEqualArrays(ids, event.ids);
  assertEquals(type, event.type);
}

function checkDeleteEventValues(event, block, ids, type) {
  var expected_xml = Blockly.Xml.domToText(Blockly.Xml.blockToDom(block));
  var result_xml = Blockly.Xml.domToText(event.oldXml);
  assertEquals(expected_xml, result_xml);
  isEqualArrays(ids, event.ids);
  assertEquals(type, event.type);
}

function checkExactEventValues(event, values) {
  var keys = Object.keys(values);
  for (var i = 0, field; field = keys[i]; i++) {
    assertEquals(values[field], event[field]);
  }
}

function test_create_constructor() {
  eventTest_setUpWithMockBlocks();
  setUpMockMethod(mockControl_, Blockly.utils, 'genUid', null, ['1']);
  var block = new Blockly.Block(workspace, 'field_variable_test_block');
  var event = new Blockly.Events.Create(block);
  checkCreateEventValues(event, block, ['1'], 'create');
  eventTest_tearDownWithMockBlocks();
}

function test_blockCreate_constructor() {
  // expect that blockCreate behaves the same as create.
  eventTest_setUpWithMockBlocks();
  setUpMockMethod(mockControl_, Blockly.utils, 'genUid', null, ['1']);
  var block = new Blockly.Block(workspace, 'field_variable_test_block');
  var event = new Blockly.Events.BlockCreate(block);
  checkCreateEventValues(event, block, ['1'], 'create');
  eventTest_tearDownWithMockBlocks();
}

function test_delete_constructor() {
  eventTest_setUpWithMockBlocks();
  setUpMockMethod(mockControl_, Blockly.utils, 'genUid', null, ['1']);
  var block = new Blockly.Block(workspace, 'field_variable_test_block');
  var event = new Blockly.Events.Delete(block);
  checkDeleteEventValues(event, block, ['1'], 'delete');
  eventTest_tearDownWithMockBlocks();
}

function test_blockDelete_constructor() {
  eventTest_setUpWithMockBlocks();
  setUpMockMethod(mockControl_, Blockly.utils, 'genUid', null, ['1']);
  var block = new Blockly.Block(workspace, 'field_variable_test_block');
  var event = new Blockly.Events.BlockDelete(block);
  checkDeleteEventValues(event, block, ['1'], 'delete');
  eventTest_tearDownWithMockBlocks();
}

function test_change_constructor() {
  eventTest_setUpWithMockBlocks();
  setUpMockMethod(mockControl_, Blockly.utils, 'genUid', null, ['1']);
  var block = new Blockly.Block(workspace, 'field_variable_test_block');
  var event = new Blockly.Events.Change(block, 'field', 'VAR', 'item', 'item2');
  checkExactEventValues(event, {'element': 'field', 'name': 'VAR',
    'oldValue': 'item', 'newValue': 'item2', 'type': 'change'});
  eventTest_tearDownWithMockBlocks();
}

function test_blockChange_constructor() {
  eventTest_setUpWithMockBlocks();
  setUpMockMethod(mockControl_, Blockly.utils, 'genUid', null, ['1']);
  var block = new Blockly.Block(workspace, 'field_variable_test_block');
  var event = new Blockly.Events.BlockChange(block, 'field', 'VAR', 'item',
    'item2');
  checkExactEventValues(event, {'element': 'field', 'name': 'VAR',
    'oldValue': 'item', 'newValue': 'item2', 'type': 'change'});
  eventTest_tearDownWithMockBlocks();
}

function test_move_constructorCoordinate() {
  // Expect the oldCoordinate to be set.
  eventTest_setUpWithMockBlocks();
  setUpMockMethod(mockControl_, Blockly.utils, 'genUid', null, ['1', '2']);
  var block1 = new Blockly.Block(workspace, 'field_variable_test_block');
  var coordinate = new goog.math.Coordinate(3,4);
  block1.xy_ = coordinate;

  var event = new Blockly.Events.Move(block1);
  checkExactEventValues(event, {'oldCoordinate': coordinate,
    'type': 'move'});
  eventTest_tearDownWithMockBlocks();
}

function test_move_constructoroldParentId() {
  // Expect the oldParentId to be set but not the oldCoordinate to be set.
  eventTest_setUpWithMockBlocks();
  setUpMockMethod(mockControl_, Blockly.utils, 'genUid', null, ['1', '2']);
  var block1 = new Blockly.Block(workspace, 'field_variable_test_block');
  var block2 = new Blockly.Block(workspace, 'field_variable_test_block');
  block1.parentBlock_ = block2;
  block1.xy_ = new goog.math.Coordinate(3,4);

  var event = new Blockly.Events.Move(block1);
  checkExactEventValues(event, {'oldCoordinate': undefined,
    'oldParentId': '2', 'type': 'move'});
  block1.parentBlock_ = null;
  eventTest_tearDownWithMockBlocks();
}

function test_blockMove_constructorCoordinate() {
  // Expect the oldCoordinate to be set.
  eventTest_setUpWithMockBlocks();
  setUpMockMethod(mockControl_, Blockly.utils, 'genUid', null, ['1', '2']);
  var block1 = new Blockly.Block(workspace, 'field_variable_test_block');
  var coordinate = new goog.math.Coordinate(3,4);
  block1.xy_ = coordinate;

  var event = new Blockly.Events.BlockMove(block1);
  checkExactEventValues(event, {'oldCoordinate': coordinate,
    'type': 'move'});
  eventTest_tearDownWithMockBlocks();
}

function test_blockMove_constructoroldParentId() {
  // Expect the oldParentId to be set but not the oldCoordinate to be set.
  eventTest_setUpWithMockBlocks();
  setUpMockMethod(mockControl_, Blockly.utils, 'genUid', null, ['1', '2']);
  var block1 = new Blockly.Block(workspace, 'field_variable_test_block');
  var block2 = new Blockly.Block(workspace, 'field_variable_test_block');
  block1.parentBlock_ = block2;
  block1.xy_ = new goog.math.Coordinate(3,4);

  var event = new Blockly.Events.BlockMove(block1);
  checkExactEventValues(event, {'oldCoordinate': undefined,
    'oldParentId': '2', 'type': 'move'});
  block1.parentBlock_ = null;
  eventTest_tearDownWithMockBlocks();
}

function test_varCreate_constructor() {
  eventTest_setUp();
  var variable = workspace.createVariable('name1', 'type1', 'id1');
  var event = new Blockly.Events.VarCreate(variable);
  checkExactEventValues(event, {'varName': 'name1', 'varType': 'type1',
    'type': 'var_create'});
  eventTest_tearDown();
}

function test_varCreate_toJson() {
  eventTest_setUp();
  var variable = workspace.createVariable('name1', 'type1', 'id1');
  var event = new Blockly.Events.VarCreate(variable);
  var json = event.toJson();
  var expectedJson = ({type: "var_create", varId: "id1", varType: "type1",
    varName: "name1"});

  assertEquals(JSON.stringify(expectedJson), JSON.stringify(json));
  eventTest_tearDown();
}

function test_varCreate_fromJson() {
  eventTest_setUp();
  var variable = workspace.createVariable('name1', 'type1', 'id1');
  var event = new Blockly.Events.VarCreate(variable);
  var event2 = new Blockly.Events.VarCreate(null);
  var json = event.toJson();
  event2.fromJson(json);

  assertEquals(JSON.stringify(json), JSON.stringify(event2.toJson()));
  eventTest_tearDown();
}

function test_varCreate_runForward() {
  eventTest_setUp();
  var json = {type: "var_create", varId: "id1", varType: "type1",
    varName: "name1"};
  var event = Blockly.Events.fromJson(json, workspace);
  assertNull(workspace.getVariableById('id1'));
  event.run(true);
  checkVariableValues(workspace, 'name1', 'type1', 'id1');
  eventTest_tearDown();
}

function test_varCreate_runBackwards() {
  eventTest_setUp();
  var variable = workspace.createVariable('name1', 'type1', 'id1');
  var event = new Blockly.Events.VarCreate(variable);
  assertNotNull(workspace.getVariableById('id1'));
  event.run(false);
  assertNull(workspace.getVariableById('id1'));
  eventTest_tearDown();
}

function test_varDelete_constructor() {
  eventTest_setUp();
  var variable = workspace.createVariable('name1', 'type1', 'id1');
  var event = new Blockly.Events.VarDelete(variable);
  checkExactEventValues(event, {'varName': 'name1', 'varType': 'type1',
    'varId':'id1', 'type': 'var_delete'});
  eventTest_tearDown();
}

function test_varDelete_toJson() {
  eventTest_setUp();
  var variable = workspace.createVariable('name1', 'type1', 'id1');
  var event = new Blockly.Events.VarDelete(variable);
  var json = event.toJson();
  var expectedJson = ({type: "var_delete", varId: "id1", varType: "type1",
    varName: "name1"});

  assertEquals(JSON.stringify(expectedJson), JSON.stringify(json));
  eventTest_tearDown();
}

function test_varDelete_fromJson() {
  eventTest_setUp();
  var variable = workspace.createVariable('name1', 'type1', 'id1');
  var event = new Blockly.Events.VarDelete(variable);
  var event2 = new Blockly.Events.VarDelete(null);
  var json = event.toJson();
  event2.fromJson(json);

  assertEquals(JSON.stringify(json), JSON.stringify(event2.toJson()));
  eventTest_tearDown();
}

function test_varDelete_runForwards() {
  eventTest_setUp();
  var variable = workspace.createVariable('name1', 'type1', 'id1');
  var event = new Blockly.Events.VarDelete(variable);
  assertNotNull(workspace.getVariableById('id1'));
  event.run(true);
  assertNull(workspace.getVariableById('id1'));
  eventTest_tearDown();
}

function test_varDelete_runBackwards() {
  eventTest_setUp();
  var json = {type: "var_delete", varId: "id1", varType: "type1",
    varName: "name1"};
  var event = Blockly.Events.fromJson(json, workspace);
  assertNull(workspace.getVariableById('id1'));
  event.run(false);
  checkVariableValues(workspace, 'name1', 'type1', 'id1');
  eventTest_tearDown();
}

function test_varRename_constructor() {
  eventTest_setUp();
  var variable = workspace.createVariable('name1', 'type1', 'id1');
  var event = new Blockly.Events.VarRename(variable, 'name2');
  checkExactEventValues(event, {'varId': 'id1', 'oldName': 'name1',
    'newName': 'name2', 'type': 'var_rename'});
  eventTest_tearDown();
}

function test_varRename_toJson() {
  eventTest_setUp();
  var variable = workspace.createVariable('name1', 'type1', 'id1');
  var event = new Blockly.Events.VarRename(variable, 'name2');
  var json = event.toJson();
  var expectedJson = ({type: "var_rename", varId: "id1", oldName: "name1",
    newName: "name2"});

  assertEquals(JSON.stringify(expectedJson), JSON.stringify(json));
  eventTest_tearDown();
}

function test_varRename_fromJson() {
  eventTest_setUp();
  var variable = workspace.createVariable('name1', 'type1', 'id1');
  var event = new Blockly.Events.VarRename(variable, '');
  var event2 = new Blockly.Events.VarRename(null);
  var json = event.toJson();
  event2.fromJson(json);

  assertEquals(JSON.stringify(json), JSON.stringify(event2.toJson()));
  eventTest_tearDown();
}

function test_varRename_runForward() {
  eventTest_setUp();
  var variable = workspace.createVariable('name1', 'type1', 'id1');
  var event = new Blockly.Events.VarRename(variable, 'name2');
  event.run(true);
  assertNull(workspace.getVariable('name1'));
  checkVariableValues(workspace, 'name2', 'type1', 'id1');
  eventTest_tearDown();
}

function test_varBackard_runForward() {
  eventTest_setUp();
  var variable = workspace.createVariable('name1', 'type1', 'id1');
  var event = new Blockly.Events.VarRename(variable, 'name2');
  event.run(false);
  assertNull(workspace.getVariable('name2'));
  checkVariableValues(workspace, 'name1', 'type1', 'id1');
  eventTest_tearDown();
}

function test_events_filter() {
  eventTest_setUpWithMockBlocks();
  var block1 = workspace.newBlock('field_variable_test_block', '1');
  var events = [
    new Blockly.Events.BlockCreate(block1),
    new Blockly.Events.BlockMove(block1),
    new Blockly.Events.BlockChange(block1, 'field', 'VAR', 'item', 'item1'),
    new Blockly.Events.Ui(block1, 'click')
  ];
  var filteredEvents = Blockly.Events.filter(events, true);
  assertEquals(4, filteredEvents.length);  // no event should have been removed.
  // test that the order hasn't changed
  assertTrue(filteredEvents[0] instanceof Blockly.Events.BlockCreate);
  assertTrue(filteredEvents[1] instanceof Blockly.Events.BlockMove);
  assertTrue(filteredEvents[2] instanceof Blockly.Events.BlockChange);
  assertTrue(filteredEvents[3] instanceof Blockly.Events.Ui);
}

function test_events_filterForward() {
  eventTest_setUpWithMockBlocks();
  var block1 = workspace.newBlock('field_variable_test_block', '1');
  var events = [
    new Blockly.Events.BlockCreate(block1),
  ];
  helper_addMoveEvent(events, block1, 1, 1);
  helper_addMoveEvent(events, block1, 2, 2);
  helper_addMoveEvent(events, block1, 3, 3);
  var filteredEvents = Blockly.Events.filter(events, true);
  assertEquals(2, filteredEvents.length);  // duplicate moves should have been removed.
  // test that the order hasn't changed
  assertTrue(filteredEvents[0] instanceof Blockly.Events.BlockCreate);
  assertTrue(filteredEvents[1] instanceof Blockly.Events.BlockMove);
  assertEquals(3, filteredEvents[1].newCoordinate.x);
  assertEquals(3, filteredEvents[1].newCoordinate.y);
  eventTest_tearDownWithMockBlocks();
}

function test_events_filterBackward() {
  eventTest_setUpWithMockBlocks();
  var block1 = workspace.newBlock('field_variable_test_block', '1');
  var events = [
    new Blockly.Events.BlockCreate(block1),
  ];
  helper_addMoveEvent(events, block1, 1, 1);
  helper_addMoveEvent(events, block1, 2, 2);
  helper_addMoveEvent(events, block1, 3, 3);
  var filteredEvents = Blockly.Events.filter(events, false);
  assertEquals(2, filteredEvents.length);  // duplicate event should have been removed.
  // test that the order hasn't changed
  assertTrue(filteredEvents[0] instanceof Blockly.Events.BlockCreate);
  assertTrue(filteredEvents[1] instanceof Blockly.Events.BlockMove);
  assertEquals(1, filteredEvents[1].newCoordinate.x);
  assertEquals(1, filteredEvents[1].newCoordinate.y);
  eventTest_tearDownWithMockBlocks();
}

function test_events_filterDifferentBlocks() {
  eventTest_setUpWithMockBlocks();
  var block1 = workspace.newBlock('field_variable_test_block', '1');
  var block2 = workspace.newBlock('field_variable_test_block', '2');
  var events = [
    new Blockly.Events.BlockCreate(block1),
    new Blockly.Events.BlockMove(block1),
    new Blockly.Events.BlockCreate(block2),
    new Blockly.Events.BlockMove(block2)
  ];
  var filteredEvents = Blockly.Events.filter(events, true);
  assertEquals(4, filteredEvents.length);  // no event should have been removed.
  eventTest_tearDownWithMockBlocks();
}

function test_events_mergeMove() {
  eventTest_setUpWithMockBlocks();
  var block1 = workspace.newBlock('field_variable_test_block', '1');
  var events = [];
  helper_addMoveEvent(events, block1, 0, 0);
  helper_addMoveEvent(events, block1, 1, 1);
  var filteredEvents = Blockly.Events.filter(events, true);
  assertEquals(1, filteredEvents.length);  // second move event merged into first
  assertEquals(1, filteredEvents[0].newCoordinate.x);
  assertEquals(1, filteredEvents[0].newCoordinate.y);
  eventTest_tearDownWithMockBlocks();
}

function test_events_mergeChange() {
  eventTest_setUpWithMockBlocks();
  var block1 = workspace.newBlock('field_variable_test_block', '1');
  var events = [
    new Blockly.Events.Change(block1, 'field', 'VAR', 'item', 'item1'),
    new Blockly.Events.Change(block1, 'field', 'VAR', 'item1', 'item2')
  ];
  var filteredEvents = Blockly.Events.filter(events, true);
  assertEquals(1, filteredEvents.length);  // second change event merged into first
  assertEquals('item', filteredEvents[0].oldValue);
  assertEquals('item2', filteredEvents[0].newValue);
  eventTest_tearDownWithMockBlocks();
}

function test_events_mergeUi() {
  eventTest_setUpWithMockBlocks();
  var block1 = workspace.newBlock('field_variable_test_block', '1');
  var block2 = workspace.newBlock('field_variable_test_block', '2');
  var block3 = workspace.newBlock('field_variable_test_block', '3');
  var events = [
    new Blockly.Events.Ui(block1, 'commentOpen', 'false', 'true'),
    new Blockly.Events.Ui(block1, 'click', 'false', 'true'),
    new Blockly.Events.Ui(block2, 'mutatorOpen', 'false', 'true'),
    new Blockly.Events.Ui(block2, 'click', 'false', 'true'),
    new Blockly.Events.Ui(block3, 'warningOpen', 'false', 'true'),
    new Blockly.Events.Ui(block3, 'click', 'false', 'true')
  ];
  var filteredEvents = Blockly.Events.filter(events, true);
  assertEquals(3, filteredEvents.length);  // click event merged into corresponding *Open event
  assertEquals('commentOpen', filteredEvents[0].element);
  assertEquals('mutatorOpen', filteredEvents[1].element);
  assertEquals('warningOpen', filteredEvents[2].element);
  eventTest_tearDownWithMockBlocks();
}

/**
 * Helper function to simulate block move events.
 *
 * @param {!Array.<Blockly.Events.Abstract>} events a queue of events.
 * @param {!Blockly.Block} block the block to be moved
 * @param {number} newX new X coordinate of the block
 * @param {number} newY new Y coordinate of the block
 */
function helper_addMoveEvent(events, block, newX, newY) {
  events.push(new Blockly.Events.BlockMove(block));
  block.xy_ = new goog.math.Coordinate(newX, newY);
  events[events.length-1].recordNew();
}
