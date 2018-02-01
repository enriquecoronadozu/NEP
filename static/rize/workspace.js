  // ******************************** Main workspace definition ****************************************
  // DESCRIPTION: Here the settings of the main workspace are defined
  // ***************************************************************************************************
  
  var options = { 
    toolbox : toolbox, 
    collapse : true, 
    comments : true, 
    disable : true, 
    maxBlocks : Infinity, 
    trashcan : true, 
    horizontalLayout : false, 
    toolboxPosition : 'start', 
    css : true, 
    media : 'web_libraries/blockly/media/', 
    rtl : false, 
    scrollbars : true, 
    sounds : true, 
    oneBasedIndex : true, 
    grid : {
        spacing : 20, 
        length : 1, 
        colour : '#888', 
        snap : false
    }, 
    zoom : {
        controls : true, 
        wheel : true, 
        startScale : 1, 
        maxScale : 3, 
        minScale : 0.5, 
        scaleSpeed : 1.2
    }
};
