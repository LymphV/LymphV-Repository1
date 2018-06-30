本程序为以MPI并行优化的快速排序程序


本程序在windows操作系统下，使用microsoft mpi接口开发

库函数依赖为"mpi.h",<ctime>,<iostream>,<stack>,<cstring>,<cmath>,<algorithm>,<Windows.h>

运行命令为“mpiexec -n 100 sort”，其中100可以替换为所需要的进程数量，sort程序将从data.in文件中，
获取所需要排序的若干整数，并将调用<algorithm>库的std::sort函数串行排序得到的结果保存在std.out文件中，
使用本程序的并行排序得到的结果保存在data.out文件中，并同时分别输出两种算法排序所用的时间

produce.exe为data.in文件的随机生成器，双击打开produce.exe后输入一个整数，如10000000，则生成包含
10000000个整数的data.in文件

compare.cmd双击打开，可比较data.out和std.out文件的内容

data.in文件为sort程序的输入文件，当前的data.in文件等同于data6.in文件

data5.in，data6.in，data7.in分别为使用produce.exe生成的数据量为100000，1000000,10000000的输入文件

data.in，data.out，std.out文件格式：
第一行为一个整数n，表示需要排序的数的个数
后面n行每行一个整数，表示需要排序的每个数

如果有其他问题，请联系作者： LymphV QQ：470481777 邮箱：470481777@qq.com