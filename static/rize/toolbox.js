var toolbox = '<xml id="toolbox" style="display: none">';toolbox += '<category name="Actions" colour="#3373CC">'
toolbox +='<block type="do_action"></block>';
toolbox +='<block type="do_action_with_robot"></block>';
toolbox +='<block type="at_the_same_time"></block>';
toolbox += '</category>';
toolbox += '<sep></sep>';

toolbox += '<category name="Repeat actions" colour="#8E44AD">'
toolbox += '<block type="repeat_until_times"></block>';
toolbox +='<block type="repeat_until_action"></block>';
toolbox +='<block type="repeat_until_trigger"></block>';
toolbox += '</category>';
toolbox += '<sep></sep>';

toolbox += '<category name="Robots" colour="#CF63CF">'
toolbox +='<block type="add_robot"></block>';
toolbox += '<block type="lists_create_with"></block>';
toolbox += '</category>';
toolbox += '<sep></sep>';

toolbox += '<category name="Sequences"  colour="#2ABB9B">'
toolbox +='<block type="define_sequence"></block>';
toolbox +='<block type="do_sequence"></block>';
toolbox += '</category>';
toolbox += '<sep></sep>';

toolbox += '<category name="Reactive behaviors" colour="#06a18b">'
toolbox += '<block type="nep_robot_reactive"></block>';
toolbox +='<block type="nep_rule"></block>';
toolbox += '<block type="rule_exit"></block>';
toolbox += '</category>';
toolbox += '<sep></sep>';

toolbox += '<category name="Time control" colour="#BA4A00">'
toolbox += '<block type="wait"></block>';
toolbox += '</category>';
toolbox += '<sep></sep>';








toolbox += '<category name="robot action" colour="#F62459">'
toolbox +='    <block type="animation"></block>';
toolbox +='    <block type="say"></block>';
toolbox += '  </category>';
toolbox += '<category name="robot mode" colour="#F62459">'
toolbox +='    <block type="rest"></block>';
toolbox +='    <block type="wake_up"></block>';
toolbox += '  </category>';
toolbox += '<category name="human state" colour="#F62459">'
toolbox +='    <block type="human_emotion"></block>';
toolbox +='    <block type="human_gesture"></block>';
toolbox += '  </category>';
toolbox += '</xml>';