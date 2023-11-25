import sys
import requests
import json
import logging
import platform
import configparser
import os
import csv
import pathlib
from datetime import datetime
from enum import Enum
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QApplication, 
    QMenu, 
    QSystemTrayIcon, 
    QAction, 
    QVBoxLayout, 
    QTextEdit,
    QWidget,
    QPushButton,
    QMessageBox,
    QPlainTextEdit,
    QLabel,
    QHBoxLayout,
    QComboBox,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem
    )

os_name = platform.system()

APP_NAME = 'MyChatCat'
VRESION = "beta 1.0"
CONFIG_local = "local"
CONFIG_remote = "remote"

if os_name == 'Darwin':
    csv_file_name = "/usr/local/share/mychatcat/historay.csv"
    config_file = "/usr/local/share/mychatcat/config.ini"

# linux path
if os_name == 'Linux':
    csv_file_name = "/usr/local/share/mychatcat/historay.csv"
    config_file = "/usr/local/share/mychatcat/config.ini"

# windows path
if os_name == 'Windows':
    app_data = dir_path = '%s\\mychatcat\\' %  os.environ['APPDATA']
    config_file = '%sconfig.ini' % app_data
    csv_file_name = '%shistoray.csv' % app_data
    
def create_floder(path):
    floder = os.path.dirname(path) 
    if not os.path.exists(floder):
        os.makedirs(floder)

def create_ini(path):
    config = configparser.ConfigParser()
    config.add_section('network')
    config.set('network', 'type', 'remote')
    config.add_section('openai')
    config.set('openai', 'url', 'https://api.openai.com/v1/chat/completions')
    config.set('openai', 'key', 'this is your api key')
    
    if not os.path.exists(path):
        create_floder(config_file)
        with open(path, 'w') as file:
            config.write(file)
            
def create_csv(path):
    if not os.path.isfile(path):
        # 如果文件不存在，则创建它
        with open(path, 'w', newline='') as csvfile:
            # 可以选择写入一些初始数据
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['input', 'output', 'time'])  # 写入表头示例
        print(f"已创建文件 '{path}'")
    else:
        print(f"文件 '{path}' 已存在")
        
def write_to_csv(filename, data):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

create_csv(csv_file_name)
create_ini(config_file)

config = configparser.ConfigParser()
config.read(config_file)
NETWORK_CON = config.get('network', 'type')
remote_url = "https://api.freegpt.hgostand.com/"
authorization = "Bearer 1234567890"
headers = {"Authorization": authorization}

# openai api
openai_key = config.get('openai', 'key')
openai_url = config.get('openai', 'url')

class OpAi(object):
    def __init__(self) -> None:
        self.KEY = openai_key
        self.url = openai_url

    def chat(self, prompt):
        payload = json.dumps({
            "model": "gpt-3.5-turbo",
            "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
            ]
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.KEY}'
        }

        response = requests.request("POST", self.url, headers=headers, data=payload, verify=False)
        response.encoding = 'utf-8'
        logging.debug(response.text)
        if response.status_code == 200:
            item = json.loads(response.text)
            result = item['choices'][0]['message']['content']
            logging.info(result)
            return result
        else:
            logging.error(response.text)
            return "network error"
        
def remote_chat(prompt):
    
    data = {'prompt':prompt}
    response = requests.post(remote_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.text
    else:
        return "network error"
    
    
def gpt_chat(type_config, prompt):

    if type_config == CONFIG_remote:
        respone = remote_chat(prompt)
        return respone
    
    if type_config == CONFIG_local:
        my_gpt = OpAi()
        respone = my_gpt.chat(prompt)
        return respone


class AssistantOptions(Enum):
    SMART_ASSISTANT = "智能助理"
    CODE_WRITING_ASSISTANCE = "编程助手"
    CODE_COMMENT = "注释描述"
    CODE_OPTIMIZER = "代码优化器"  # 更新了名称
    ENGLISH_TO_CHINESE_TRANSLATION = "英语翻译成中文"
    CHINESE_TO_ENGLISH_TRANSLATION = "中文翻译成英语"
    SQL_GENERATOR = "SQL生成器"
    PYTHON_INTERPRETER = "Python解释器"
    LEETCODE = "LeetCode"  # 移除重复的选项
    WORD_DEFINITION = "名词解释"  # 更新了选项
    FASHION_ASSISTANT = "时尚助手"  # 更新了选项
    VIRTUAL_BOYFRIEND = "虚拟男友"  # 更新了选项
    VIRTUAL_GIRLFRIEND = "虚拟女友"  # 更新了选项
    VIRTUAL_MALE_FRIEND = "虚拟男性友人"  # 更新了选项
    VIRTUAL_FEMALE_FRIEND = "虚拟女性友人"  # 更新了选项
    AUTO_COMPLETE = "提示词完善"  # 更新了选项
    
def get_text(value):
    if AssistantOptions.SMART_ASSISTANT.value == value: return "你是一个智能助理，帮我回答以下问题："
    if AssistantOptions.CODE_WRITING_ASSISTANCE.value == value: return "你是一个编程助手，代码调试、语法纠错、编程语言学习、算法解析、项目管理、软件开发实践、编程工具推荐、常见错误解决方案、技术资源推荐、开发环境搭建、API文档解读、帮我回答以下问题："
    if AssistantOptions.CODE_OPTIMIZER.value == value: return "你是一个代码优化器，帮我优化以下代码，使代码更精简，更容易阅读："
    if AssistantOptions.CODE_COMMENT.value == value: return "帮我根据以下代码，用英文写出最合适的注释："
    if AssistantOptions.ENGLISH_TO_CHINESE_TRANSLATION.value == value: return "你是一个英语翻译成中文的助手，帮我翻译，只显示结果："
    if AssistantOptions.CHINESE_TO_ENGLISH_TRANSLATION.value == value: return "你是一个中文翻译成英语的助手，帮我翻译，只显示结果："
    if AssistantOptions.SQL_GENERATOR.value == value: return "你是一个SQL生成器，只需给出相应的代码，帮我生成以下SQL语言："
    if AssistantOptions.PYTHON_INTERPRETER.value == value: return "你是一个Python解释器，帮我虚拟执行这段代码："
    if AssistantOptions.LEETCODE.value == value: return "你是一个LeetCode助手，随机给出一道测试题,问题难度随机，编程语言随机："
    if AssistantOptions.WORD_DEFINITION.value == value: return "你是一个名词解释助手，帮我回答以下问题："
    if AssistantOptions.FASHION_ASSISTANT.value == value: return "你是一个时尚助手，帮我回答以下问题："
    if AssistantOptions.VIRTUAL_BOYFRIEND.value == value: return "你是一个虚拟男友助手，帮我回答以下问题："
    if AssistantOptions.VIRTUAL_GIRLFRIEND.value == value: return "你是一个虚拟女友助手，帮我回答以下问题："
    if AssistantOptions.VIRTUAL_MALE_FRIEND.value == value: return "你是一个虚拟男性友人助手，帮我回答以下问题："
    if AssistantOptions.VIRTUAL_FEMALE_FRIEND.value == value: return "你是一个虚拟女性友人助手，帮我回答以下问题："
    if AssistantOptions.AUTO_COMPLETE.value == value: return "你是一个提示词完善助手，帮我回答以下问题："


class CSVViewer(QWidget):
    def __init__(self, parent=None, csv_file=None):
        super().__init__(parent)
        
        layout = QVBoxLayout() # 创建窗口布局
        
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('历史记录')
        self.scv_file = csv_file
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)
        self.load_csv_to_table(self.scv_file)
        
        self.delete_history_button = QPushButton("清除")
        self.delete_history_button.clicked.connect(self.delete)
        layout.addWidget(self.delete_history_button)
        
        self.setLayout(layout) # 设置窗口布局
        
    def load_csv_to_table(self, file_name):
        with open(file_name, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)

            self.table_widget.setColumnCount(len(header))
            self.table_widget.setHorizontalHeaderLabels(header)

            for row_data in csv_reader:
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)

                for column, data in enumerate(row_data):
                    self.table_widget.setItem(row_position, column, QTableWidgetItem(data))

    def delete(self):
        print("删除历史记录")
        with open(csv_file_name, 'w', newline='') as csvfile:
            # 可以选择写入一些初始数据
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['input', 'output', 'time'])  # 写入表头示例
            
        message_box = QMessageBox(self)
        message_box.setText("已清除")
        message_box.show()
        
        # 设置定时器，在2秒后自动关闭消息提示框
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(message_box.close)
        timer.start(2000)
        
        self.table_widget.clear()
        self.load_csv_to_table(self.scv_file)

class ChatWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout() # 创建窗口布局
        hbox = QHBoxLayout()
        
        self.text_prompt = None
        self.history_window = None
        
        self.prompt_label = QLabel("请选择一个应用", self)
        self.prompt_label.move(50, 50)
        layout.addWidget(self.prompt_label)
        
        self.combo_box = QComboBox()
        
        for option in AssistantOptions:
            self.combo_box.addItem(option.value)
        
        self.combo_box.currentIndexChanged.connect(self.on_combobox_changed)
        self.on_combobox_changed()
        layout.addWidget(self.combo_box)
        
        self.input_field = QPlainTextEdit(self)  # 创建输入组件
        self.input_field.installEventFilter(self)
        self.input_field.setFixedHeight(100)
        self.input_field.setPlaceholderText("Enter some text...")
        layout.addWidget(self.input_field)
        
        self.chat_label = QLabel("应答窗口:")
        layout.addWidget(self.chat_label)

        self.output_label = QTextEdit(self) # 创建文字输出组件
        self.output_label.setReadOnly(True)
        self.output_label.setPlaceholderText("Result text in here")
        layout.addWidget(self.output_label)
        
        clear_button = QPushButton('清除', self) # 创建清除输入框内文字的按钮
        clear_button.clicked.connect(self.clear_input)
        clear_button.setFixedHeight(50)
        clear_button.setStyleSheet('background-color: #4BA5E6; color: white')
        hbox.addWidget(clear_button)
        
        self.confirm_button = QPushButton('确定', self) # 创建确定按钮
        self.confirm_button.setToolTip('Shift+Enter')
        self.confirm_button.clicked.connect(self.process_input)
        self.confirm_button.setFixedHeight(50)
        self.confirm_button.setStyleSheet('background-color: #4CAF50; color: white')
        hbox.addWidget(self.confirm_button)
        
        self.copy_text = QPushButton('复制结果', self) # 创建清除输入框内文字的按钮
        self.copy_text.clicked.connect(self.copy)
        self.copy_text.setFixedHeight(40)
        layout.addWidget(self.copy_text)
        
        self.history_button = QPushButton('历史记录', self) # 创建清除输入框内文字的按钮
        self.history_button.clicked.connect(self.history)
        self.history_button.setFixedHeight(40)
        layout.addWidget(self.history_button)
        
        layout.addLayout(hbox)
        
        self.setLayout(layout) # 设置窗口布局
        
    def on_combobox_changed(self):
        # selected_option = self.combo_box.currentText()
        selected_index = self.combo_box.currentIndex()
        selected_text = self.combo_box.itemText(selected_index)
        result = get_text(selected_text)
        print("您选择了：%s" % selected_text)
        print("prompt：%s" % result)
        self.text_prompt = result
    def clear_input(self): # 清除输入框内的文字
        
        self.input_field.clear()
        self.output_label.clear()
        
    def copy(self):
        text_to_copy = self.output_label.toPlainText()
        QApplication.clipboard().setText(text_to_copy)
        
    def history(self):
        print("打开历史记录窗口")
        self.history_window = CSVViewer(csv_file=csv_file_name)
        self.history_window.show()
    
    def process_input(self):
        global openai_key
        global openai_url
        global NETWORK_CON
        config.read(config_file)
        NETWORK_CON = config.get('network', 'type')
        openai_key = config.get('openai', 'key')
        openai_url = config.get('openai', 'url')
        input_text = self.input_field.toPlainText() # 处理输入框内的文字，并在输出组件中显示
        respone_text = gpt_chat(type_config=NETWORK_CON, prompt=self.text_prompt + input_text)
        self.output_label.setPlainText(respone_text)
        now = datetime.now()
        formatted = now.strftime("%Y-%m-%d %H:%M:%S")
        data = [[input_text, respone_text, formatted]]
        write_to_csv(csv_file_name, data)
        
    def eventFilter(self, obj, event):
        if obj is self.input_field and event.type() == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_Return and event.modifiers() & Qt.ShiftModifier or key == Qt.Key_Enter and event.modifiers() & Qt.ShiftModifier:
    
                self.confirm_button.click() # 按下Enter键时触发按钮点击事件
                return True  # 事件被处理

        return super().eventFilter(obj, event)
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon('setting.png'))

        # 创建 QWidget 实例
        widget = ChatWindow(self)

        self.setGeometry(700, 100, 500, 800)
        self.setCentralWidget(widget)
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '提示', '确定要退出吗？', 
                                     QMessageBox.Yes | QMessageBox.No, 
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
class TextEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout() # 创建窗口布局
        
        # 创建文本编辑区域
        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)
        self.open_file()
        self.save_config_button = QPushButton('保存', self) # 创建确定按钮
        self.save_config_button.clicked.connect(self.save_file)
        layout.addWidget(self.save_config_button)

        # 设置窗口属性
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('配置编辑器')
        
        self.setLayout(layout) # 设置窗口布局

    def open_file(self):
        file_name = config_file
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
            self.text_edit.setPlainText(content)

    def save_file(self):
        file_name = config_file
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(self.text_edit.toPlainText())
            
        message_box = QMessageBox(self)
        message_box.setText("已保存")
        message_box.show()
        
        # 设置定时器，在2秒后自动关闭消息提示框
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(message_box.close)
        timer.start(2000)
        
    def closeEvent(self, event):
        # 阻止窗口关闭事件传播，只关闭当前窗口
        event.ignore()
        self.hide()  # 隐藏窗口，而不是销毁
        self.deleteLater()

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None, window=None):
        super(SystemTrayIcon, self).__init__(parent)
        
        self.window = MainWindow() # 传入window
        self.new_widget = None 
        self.show_window()
        
        folder = pathlib.Path(__file__).parent.resolve()
        print(folder)
        self.setIcon(QIcon(f"{folder}/assert/setting.png")) # 创建托盘图标
        self.menu = QMenu() # 创建任务栏菜单
        
        # 添加菜单项
        self.show_action = QAction("显示对话窗口", self, triggered=self.show_window)
        self.hide_action = QAction("隐藏对话窗口", self, triggered=self.hide_window)
        self.open_config_file_action = QAction("打开配置文件", self, triggered=self.open_file_dialog)
        self.exit_action = QAction(f"退出{APP_NAME}", self, triggered=self.exit_application)
        
        self.menu.addAction(self.show_action)
        self.menu.addAction(self.hide_action)
        self.menu.addAction(self.open_config_file_action)
        self.menu.addSeparator()
        self.menu.addAction(self.exit_action)
        
        # 将菜单附加到托盘图标上
        self.setContextMenu(self.menu)
        
    def show_window(self):
        print("显示主窗口")
        self.window.show()
    
    def hide_window(self):
        print("隐藏主窗口")
        self.window.hide()
    
    def open_file_dialog(self):
        print("打开配置编辑器")
        self.new_widget = TextEditor()
        self.new_widget.show()
        
    def exit_application(self):
        # 在这里添加退出应用程序的逻辑
        QApplication.quit()

def main():
    app = QApplication(sys.argv)
    tray_icon = SystemTrayIcon()# 创建系统托盘图标
    tray_icon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

# pyinstaller --windowed --name "MyChatCat" -i "assert/icon.icns" --add-data "assert/setting.png:." --onefile  mychatcat.py