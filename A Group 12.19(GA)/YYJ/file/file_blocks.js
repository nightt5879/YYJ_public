'use strict';

Blockly.Blocks.open_file={
init: function () {
    this.setColour('#6cabde');
    this.appendDummyInput()
      .appendField('赋值');
    this.appendValueInput('f')
      .setCheck('var');
    this.appendValueInput('filename',String)
      .appendField('为文件')
      .setCheck("String");
      this.appendDummyInput()
      .appendField('打开方式为');
     var mode1 = [['只读', "'r'"], ['只写', "'w'"], ['追加', "'a'"]];
     this.appendDummyInput("")
            .appendField(new Blockly.FieldDropdown(mode1), 'DIR');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
  }
};

Blockly.Blocks.close_file={
init: function(){
    this.setColour('#6cabde');
    this.appendDummyInput()
      .appendField('关闭文件');
     this.appendValueInput('f')
     .setCheck('var');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
}
};

Blockly.Blocks.file_read={
init:function(){
    this.setColour('#6cabde');
    this.appendDummyInput()
      .appendField('文件');
      this.appendValueInput('f')
     .setCheck('var');
     this.appendDummyInput()
      .appendField('中的所有内容');
     this.setInputsInline(true);
    this.setOutput(true);
}
};

Blockly.Blocks.file_readline={
init:function(){
    this.setColour('#6cabde');
    this.appendDummyInput()
      .appendField('文件');
      this.appendValueInput('f')
     .setCheck('var');
     this.appendDummyInput()
      .appendField('中的当前行的内容');
     this.setInputsInline(true);
    this.setOutput(true);
}
};

Blockly.Blocks.file_readlines={
init: function() {
    this.appendValueInput("f")
        .setCheck("var")
        .appendField("文件");
        this.appendDummyInput()
        .appendField("中的第");
            this.appendValueInput("num")
        .setCheck("Number")
        this.appendDummyInput()
        .appendField("行的内容");
    this.setColour('#6cabde');
     this.setTooltip("");
 this.setHelpUrl("");
     this.setInputsInline(true);
    this.setOutput(true);
  }
};

Blockly.Blocks.file_GiveValue={
init:function(){
    this.setColour('#6cabde');
    this.appendDummyInput()
      .appendField('文件');
    this.appendValueInput('f')
     .setCheck('var');
     this.appendDummyInput()
      .appendField('中当前的读取位置');
     this.setInputsInline(true);
    this.setOutput(true);

}
};

Blockly.Blocks.BackToFirst={
init:function(){
    this.setColour('#6cabde');
    this.appendValueInput('f')
     .setCheck('var');
     this.appendDummyInput()
      .appendField('回到初始位置');
           this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
}
};

Blockly.Blocks.file_write={
init:function(){
    this.setColour('#6cabde');
    this.appendDummyInput()
      .appendField('向');
    this.appendValueInput('f')
     .setCheck('var');
     this.appendDummyInput()
      .appendField('中写入内容');
     this.appendValueInput('message')
     .setCheck('var');
          this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
}
};

Blockly.Blocks.file_write2={
init:function(){
    this.setColour('#6cabde');
    this.appendDummyInput()
      .appendField('向');
    this.appendValueInput('f')
     .setCheck('var');
     this.appendDummyInput()
      .appendField('中写入一串序列');
     this.appendValueInput('lines')
     .setCheck('var');
          this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
}
};

Blockly.Blocks.open_json={
init: function () {
    this.setColour('#6cabde');
    this.appendDummyInput()
      .appendField('赋值');
    this.appendValueInput('f')
      .setCheck('var');
    this.appendValueInput('filename',String)
      .appendField('为json文件')
      .setCheck("String");
      this.appendDummyInput()
      .appendField('打开方式为');
     var mode1 = [['只读', "'r'"], ['只写', "'w'"], ['追加', "'a'"]];
     this.appendDummyInput("")
            .appendField(new Blockly.FieldDropdown(mode1), 'DIR');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
  }
};

Blockly.Blocks.json_read={
init:function(){
    this.setColour('#6cabde');
    this.appendDummyInput()
      .appendField('json文件');
      this.appendValueInput('f')
     .setCheck('var');
     this.appendDummyInput()
      .appendField('中的所有内容');
     this.setInputsInline(true);
    this.setOutput(true);
}
};

Blockly.Blocks.json_write={
init:function(){
    this.setColour('#6cabde');
    this.appendDummyInput()
      .appendField('向json文件');
    this.appendValueInput('f')
     .setCheck('var');
     this.appendDummyInput()
      .appendField('中写入内容');
     this.appendValueInput('massage')
     .setCheck('var');
          this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
}
};



Blockly.Blocks.open_csv={
init: function () {
    this.setColour('#6cabde');
    this.appendDummyInput()
      .appendField('赋值');
    this.appendValueInput('f')
      .setCheck('var');
    this.appendValueInput('filename',String)
      .appendField('为csv文件')
      .setCheck("String");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
  }
};


Blockly.Blocks.print_head = {
  init: function() {
    this.appendValueInput("f")
        .setCheck("var")
        .appendField("打印CSV文件");
        this.appendDummyInput()
        .appendField("中的前");
    this.appendValueInput("num")
        .setCheck("Number")
    this.appendDummyInput()
        .appendField("行");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour('#6cabde');
 this.setTooltip("");
 this.setHelpUrl("");
  }
};

Blockly.Blocks.print_tail = {
  init: function() {
    this.appendValueInput("f")
        .setCheck("var")
        .appendField("打印CSV文件");
        this.appendDummyInput()
        .appendField("中的后");
    this.appendValueInput("num")
        .setCheck("Number")
    this.appendDummyInput()
        .appendField("行");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour('#6cabde');
 this.setTooltip("");
 this.setHelpUrl("");
  }
};

Blockly.Blocks.print_describe = {
  init: function() {
    this.appendValueInput("f")
        .setCheck("var")
        .appendField("打印CSV文件");
        this.appendDummyInput()
        .appendField("中的汇总统计");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour('#6cabde');
  }
};

Blockly.Blocks.get_a_row = {
  init: function() {
    this.appendValueInput("f")
        .setCheck("var")
        .appendField("CSV文件");
        this.appendDummyInput()
        .appendField("中的第");
            this.appendValueInput("num")
        .setCheck("Number")
        this.appendDummyInput()
        .appendField("行");
    this.setColour('#6cabde');
     this.setTooltip("");
 this.setHelpUrl("");
     this.setInputsInline(true);
    this.setOutput(true);
  }
};

Blockly.Blocks.get_a_column = {
  init: function() {
    this.appendValueInput("f")
        .setCheck("var")
        .appendField("CSV文件");
        this.appendDummyInput()
        .appendField("中的第");
            this.appendValueInput("num")
        .setCheck("Number")
        this.appendDummyInput()
        .appendField("列");
    this.setColour('#6cabde');
     this.setTooltip("");
 this.setHelpUrl("");
     this.setInputsInline(true);
    this.setOutput(true);
  }
};

Blockly.Blocks.dropna = {
  init: function() {
    this.appendValueInput("f")
        .setCheck("var")
        .appendField("删除CSV文件");
        this.appendDummyInput()
        .appendField("中的空白值");
    this.setColour('#6cabde');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
  }
};



Blockly.Blocks.fillna= {
  init: function () {
    this.setColour('#6cabde');
    this.appendValueInput("x")
        .setCheck("var")
        .appendField("用");
      this.appendValueInput('f')
      .appendField('替换csv文件')
      .setCheck("var");
              this.appendDummyInput()
        .appendField("中的所有空白值");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
  }
};

Blockly.Blocks.get_directory={
   init: function () {
    this.setColour('#6cabde');
    this.appendDummyInput()
      .appendField('csv文件');
    this.appendValueInput('f')
      .setCheck('var');
    this.appendDummyInput()
      .appendField('中的第');
    this.appendValueInput('row')
      .setCheck('Number');
    this.appendDummyInput()
      .appendField('行第');
    this.appendValueInput('column')
      .setCheck('Number');
    this.appendDummyInput()
      .appendField('列的元素');
   this.setInputsInline(true);
    this.setOutput(true);
  }
};



