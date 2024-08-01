# ProjectRename

工具-提取版本号作为exe的文件名

### Overview

> [!NOTE]
> 工程使用PyCharm开发，Python 3.12+，主要用于提取版本号重命名exe的文件名。

### 运行条件

#### 依赖库

使用pywin32库，它提供了一些用于访问Windows API的函数。

首先安装pywin32：

```shell
pip install pywin32
```

### 打包

使用**pyinstaller**打包成exe文件，打开**PyCharm**的`Terminal`输入：

```shell
pyinstaller --onefile --name Magic --icon app.ico main.py
```

![](https://raw.githubusercontent.com/zhongwcool/ProjectRename/main/Assets/app-logo.png)