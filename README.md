# carla-fastapi-bridge
carla fastapi bridge


2024.02.17 20:04

运行时先启动carla server，然后参考yu分支里面的代码，分别启动carlaBackend_lidar.py和carlaBackend_rgbcam.py，最后启动carlaFrontend_PYQT.py。我试着在一个代码里面同时启动lidar和rgbcam，没有成功，参考carlaBackend_lidar&rgbcam.py

1.carlaFrontend_PYQT.py，是用PYQT作的一个前端多窗口，来显示多个sensor的图像
2.carlaBackend_lidar.py，是后端用来生成lidar图像，用socket传给carlaFrontend_PYQT.py
3.carlaBackend_rgbcam.py，是后端用来生成rgb图像，用socket传给carlaFrontend_PYQT.py
4.Qt_UI.py，是用QT designer拖框生成的.ui文件转化而来的.py文件，用于被导入carlaFrontend_PYQT.py里面，作为界面被启动显示
5.carlaBackend_lidar&rgbcam.py，是后端用来同时生成lidar和rgb图像，用2个socket传给carlaFrontend_PYQT.py，但是这个没运行成功，估计是多进程的代码写的有问题
6.carlaBackend_lidar.py和carlaBackend_rgbcam.py同时运行时，carlaFrontend_PYQT.py可以同时显示，但是十几秒后就报错


