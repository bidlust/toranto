#!/bin/bash

#项目部署脚本；
#实现自动化拉去，初始化进程等。


log_path="/var/log/blog"

if [ ! -d "$log_path" ];then
    mkdir "$log_path"
fi