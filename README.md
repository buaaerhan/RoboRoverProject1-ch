[//]: # (Image References)
[image_0]: ./misc/rover_image.jpg
# Search and Sample Return Project
![alt text][image_0] 

本项目是[NASA sample return challenge](https://www.nasa.gov/directorates/spacetech/centennial_challenges/sample_return_robot/index.html)项目的模型，且可以让你初步体验机器人相关的要点, 视角转换，决策和相应的动作。 你可以使用Unity游戏引擎来完成这个项目。  

## 模拟器
首先下载对应操作系统的模拟器，不同系统下的下载链接如下： [Linux](https://s3-us-west-1.amazonaws.com/udacity-robotics/Rover+Unity+Sims/Linux_Roversim.zip), [Mac](	https://s3-us-west-1.amazonaws.com/udacity-robotics/Rover+Unity+Sims/Mac_Roversim.zip), or [Windows](https://s3-us-west-1.amazonaws.com/udacity-robotics/Rover+Unity+Sims/Windows_Roversim.zip).  

你可以启动测试模拟器，选择“Training Mode”。  使用鼠标或者键盘查看到处查看环境。

## 依赖项
你需要安装Python 3以及Jupyter Notebooks。 最好的方法就是使用Anaconda，如下[RoboND-Python-Starterkit](https://github.com/ryan-keenan/RoboND-Python-Starterkit). 


下面是一个关于Anaconda和Jupyter Notebook的教程[Anaconda and Jupyter Notebooks](https://classroom.udacity.com/courses/ud1111)

## 记录数据
已经给出一些事先保存好的数据，放在`test_dataset`文件夹下。 在此文件夹下你可以找到一个csv文件，里面包含了一些记录数据和每次运行所记录的图片路径。 同样地，为做一些初始标定工作，`calibration_images`文件夹下也保存了一些图片。  

首先要做的是记录你自己的数据。 第一要创建一个新的文件夹用来保存图片。 然后启动模拟器，选择“Training Mode”， 按下"r"键，用键盘导航到你所想要记录数据的区域，然后在此区域运动并收集数据。再次按下“r”键，停止收集数据。

## 数据分析
`Rover_Project_Test_Notebook.ipynb`文档中包含了课程中出现过的函数，用来执行本项目中的各种操作。 文档中的函数不经修改就能正常执行， 要查看文档中的具体内容或者要执行里面的代码，用下面的命令启动jupyter notebook服务器：

```sh
jupyter notebook
```

这个命令将会打开浏览器窗口，并定位到当前目录下，你可以选择进入`Rover_Project_Test_Notebook.ipynb`文档所在的目录并选择打开文档。 从上到下依次运行里面的代码块，查看数据分析步骤。  

最后两个代码块是为了从一个文件夹中读取并处理所有的图片，创建模拟器环境并输出视频。 这些代码块可以直接运行并保存成一个名为`test_mapping.mp4`的视频到`output`文件夹。 这将会给你一些关于怎样修改`process_image()`能够更好地建图的主意。  

## 自主导航
`drive_rover.py`是你在自动导航模式下将会使用到的文件。 这个脚本文件调用`perception.py` 和 `decision.py`中的函数。 上面.pynb文件中的函数都包含在`perception.py`文件中，你所要做的就是合理填充`perception_step()`函数并更新小车状态。 `decision.py`文件包含了另外一个名为`decision_step()`的函数, 其包含了一些示例条件，用以处理自主导航过程中的情况。 这里你应当添加其它的条件，并基于`perception_step()`中输出的小车状态做出相应的决定和动作。

如果你已经安装好了相应的Python包，则`drive_rover.py`应当正常运行。 在命令行中运行： 

```sh
python drive_rover.py
```  

然后启动模拟器，选择"Autonomous Mode"。 小车应该会自己行驶! 当然，行驶过程中可能会遇到一些问题，你的工作就是让它行驶得更好!  

**注意: 运行模拟器时如果选择不同的分辨率和图像质量，产生的结果可能会不同！ 因此，在你提交项目时，请注明你的模拟器设置。**


