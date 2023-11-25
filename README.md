# MyChatCat简介
使用pyqt5实现的chatGPT UI 客户端
全平台GUI客户端，只需在配置文件中填写自己Key即可

# 功能

- 自带远程免费的GPT接口，目前该接口不稳定
- 自动窗口保持，可以在多窗口情况下，一直在桌面最前显示，方便快捷对话
- 内置应用，免去输入文字烦恼
- 历史记录，可以查看过去的对话内容
- 任务栏图标唤起
- 非常简洁，虽然是demo级别的应用，但是功能稳定，没有杂乱的功能

Mac端已编译
如需在Windows或Linux中使用，克隆本项目，请使用pyinstaller打包成独立客户端
```
pyinstaller --windowed --name "MyChatCat" -i "assert/icon.icns" --add-data "assert/setting.png:." --onefile  mychatcat.py
```

# 工具截图
![截图](https://github.com/suais/MyChatCat/blob/main/images/Screen%20Shot%202023-11-25%20at%2012.34.16.png)
