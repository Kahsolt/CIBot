#!/bin/bash

function download() {
  echo "假装在下载 $1 ..."
  # 这个函数封装一下curl或者wget
  # 下载到库目录lib下
  # 一定并且按照规则建立文件夹分类

  # 比较大的数据集放个链接在这里
  # 可以组成个一键下载脚本2333
  # 然后最好把这个脚本移动到bin目录下
}

download "http://lab.iriscraft.tk/2333.data"

cat $0
