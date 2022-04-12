# frame_extractor
A tool for handbook painters to create low FPS video from high FPS video
##English Manual:
###1	How to use this:
Drag and drop your video file on the .exe file or the .py file (if exists).

=========

###2	How to change desired video width, height, fps and format:
The name of the file is written in the format of 

			frame_extractor&desired_width&desired_height&desired_fps&output_format&$language$.exe.

To modify this, just change values of "desired_width" "desired_height" "desired_fps" "output_format" between ampersands. Notably, the former 3 values only accept integers. The desired_fps should not be greater than the original fps. To switch to Chinese, change the "language" to zh_CN .

=========

###3	How to use the extractor through the command options:
First, you need to make sure you have installed python3, numpy and opencv-python. Then, open cmd in the directory of the .py file and run 
	
	python ".py file" -h 

to see available options. ".py file" is the name of the .py file. It may change due to your modification. Notably, [-i] or [--input] option is REQUIRED for it is the name or path of the original video. When using extractor through command line options, setting width, height and fps through filename are not available.


====================================================


##中文说明：
###1	如何使用：
拖动要抽帧的视频到.exe文件或者.py文件上即可。

=========

###2	如何设置导出视频的长、宽、帧率、格式：
文件名是按照 

			frame_extractor&目标宽度&目标高度&目标帧率&输出格式&$语言$.exe 

的格式命名的，只要修改文件名中“目标宽度” “目标高度” “目标帧率” “输出格式”的数值即可。注意，前三项只接受整数。目标帧率不得超过原视频帧率。如需切换为英语，请将“语言”更改为 en_US .

=========

###3	如何通过命令行使用frame extractor:
首先确保你安装了python3, numpy和opencv-python. 然后在.py文件目录下打开cmd，运行

	python ".py文件" -h

查看可用options。 ".py 文件"是.py文件名，根据你的修改文件名会有些许不同。注意，[-i]或者[--input] option是必需的，因为它用于搜索原视频。在使用命令行操作时，通过文件名设置宽高和帧率的功能不可用。
