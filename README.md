# GIMS智能摄像头通用程式

[TOC]

## 1-模块架构

```
General-Industrial-Smart-Monitoring-V2.0
├─.idea
│  └─inspectionProfiles
├─appconfig    # 配置文件
├─db           # 数据库文件
├─font         # 字体文件
├─icon         # 图标文件
├─log          # 日志文件
├─log_unit     # 日志模块
│  └─__pycache__
├─plugins      # Yolo插件模块
├─qss          # QT样式表
├─shell        # shell脚本
├─ui           # 界面文件
│  └─__pycache__
└─utils        # 辅助模块
    └─__pycache__
```

### 1-1 appconfig文件夹

此文件夹存储一些配置文件，包括程式参数的配置文件和日志模块的配置文件。

`appconfig.xml`: 程式参数配置文件

`logging.yaml`: 日志模块配置文件

### 1-2 db文件夹

此文件夹存储程式需要离线存储的一些数据库文件。

你可以存储SQL、SQLite、MySQL格式等等的数据库文件。

### 1-3 font文件夹

此文件夹存储一些字库文件。

因为在Docker部署时可能会遇到缺少字体的情况，这个时候可以动态加载本地字库，解决中文字体不显示的情况。

### 1-4 icon文件夹

此文件夹存储程式需要的一些图标文件。

### 1-5 log文件夹

此文件夹存储程式运行期间记录的一些日志信息。

`errors.log`: 错误日志

`info.log`: 信息日志

### 1-6 log_unit文件夹

`app_logger.py`: 加载日志系统的配置文件，配置日志系统

`subModule.py`: 演示如何在自定义的程式中，使用已配置的程式

### 1-7 plugins文件夹

此文件夹同`tensorrt_demos`项目的`plugins`文件夹。

程式迁移设备后需要重新编译：

```bash
make clean
make
```

### 1-8 qss文件夹

此文件夹存储程式需要用到的样式表文件。

`mainWindow.qss`: 程式主窗口的样式表文件

`splashScreen.qss`: 程式启动窗口的样式表文件

### 1-9 shell文件夹

此文件夹存储一些自动化脚本。

`build_gism.sh`: 自动化构建GISM的容器

`development.sh`: 开发测试使用的构建容器的脚本

`docker_permission.sh`: Linux下的docker权限脚本

`install_gism.sh`: 自动化部署基于容器的程式；创建桌面启动图标

`make_tensorrt.sh`: 用于在每次启动容器时，自动编译基于TensorRT的Yolo插件，为了解决容器迁移时，驱动变化的问题；

`run_gism.sh`: 启动GISM容器的脚本，桌面图标的实际启动shell脚本

### 1-10 ui文件夹

`ActionHeaderWidget.py`: 动作编辑模块头部

`ActionSettingsWidget.py`: 动作顺序编辑页面

`ActionWidget.py`: 动作编辑模块

`ApplicationSettingsWidget.py`: 程式参数设置页面

`CameraSettingsWidget.py`: 相机参数设置界面

`CountWidget.py`: 合格数、不合格数、总数、良率模块

`DataGrid.py`: 数据库查询模块

`HeaderWidget.py`: 主页面头部模块

`HistoryItemWidget.py`: 历史图片窗口模块

`HistoryListView.py`: 历史图片ListView

`LogItemWidget.py`: 历史数据项模块

`LogWidget.py`: 历史数据参数模块

`MainWindow.py`: 程式主窗口界面

`ModelSettingsWidget.py`: 模型参数设置界面

`MonitorWidget.py`: 未使用到

`OutputSettingsWidget.py`: 输出参数设置界面

`RemoteCVSettingsWidget.py`: 远程视频推送设置窗口

`SequenceActionItemWidget.py`: 序列动作显示Item

`SequenceActionWidget.py`：序列动作显示Widget

`SortFilterProxyModel.py`：排序模型

`SplashScreen.py`: 程式启动窗口

`SwitchButton.py`: 模仿iOS的开关按钮

`SystemSettingsTabWidget.py`: 系统参数设置TabWidget

`TempWidget.py`：未使用到

`TimeDelayWidget.py`: 时间延迟模块窗口

`VideoSaveSettingsWidget.py`: 视频保存参数设置

`VideoWidget.py`: Video窗口，显示video

### 1-11 utils文件夹

`ActionItem.py`: 动作模块
`ArgsHelper.py`: 参数模块
`camera.py`: 相机模块
`CircleQueue.py`: 循环链表
`CommonHelper.py`: QSS文件读取模块
`custom_classes.py`: 自定义Yolo类别模块
`DataUploadThread.py`: 数据上报线程（前公司IT工程师姿态极高）
`DeleteFileThread.py`: 定时删除文件模块
`DetectTensorRT.py`: 检测类
`display.py`: display模块
`edgeAgent.py`: 没啥用的模块
`Empty.py`: Empty-Error-Class
`GPIOThread.py`: GPIO输出模块
`gpio_test.py`: GPIO测试模块
`Item.py`: Item基类
`ModelOutputItem.py`: 模型输出参数格式化模块
`Rectangle.py`: 矩形计算模块
`remote_cv.py`: 远程视频推送模块
`Result.py`: 输出结果模块
`ResultNode.py`: 流程节点模块
`rtsp_test_client.py`: RTSP测试客户端
`SaveVideoThread.py`: 保存视频模块
`TimeItem.py`: 超时模块
`visualization.py`: 可视化模块
`yolo_with_plugins.py`: Yolo插件模块

### Dockerfile

此文件的文件名，固定为`Dockerfile`。

用于构建Docker容器。

### main.py

程式入口文件。

### README.md

自述文件

### requirements.txt

程式运行环境需求。