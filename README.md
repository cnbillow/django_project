# django_project

A new django application.（Pycharm创建）

## Getting Started

项目代码在`templates\myAPP`文件中;  
`project_soft`中有项目配置`settings.py`;

项目运行图片：

![](https://note.youdao.com/yws/public/resource/ecd343f8a42de9e26c3391b2e8652ef7/xmlnote/E9B20E35E5DB44B1AA9E6C9354177F23/939)

![](https://note.youdao.com/yws/public/resource/ecd343f8a42de9e26c3391b2e8652ef7/xmlnote/854B2A2EE7C4411BB5D53687B6B36809/942)

## 最后成功使用Docker部署在Ubuntu服务器上，这里提几个比较坑的地方：
  1. 这里我用Google搜到的教程都不适合自己，反而Baidu到的第一条目可以使用
  2. 安装docker后，创建虚拟环境安装需要的包，为了避免requirements.txt安装出错，单独拿出来自己安装比较好
  3. 修改`mysqld.cnf`的`bind address = 0.0.0.0`
  4. 数据库在转过去后，大小写混淆了，不知道是不是服务器的原因，我在本地使用Apache是可以完美运行的，所以服务器中myapp开头的表全部需要新建myAPP开头的表，并把数据复制过去
  5. `mysql`的`host`需要修改为`%`，能够实现外部访问，将`settings.py`的`host`修改为自己的服务器地址
  6. 阿里云服务器的安全组要提前设置好，允许端口访问
  7. 这里走了很多弯路，最后文件结构也并不满意，但是已经可以正常工作，暂时不进行修改了，之后有了新的项目再进行钻研。
## 效果图：
<img src="https://github.com/XiXiangkun/images/blob/master/run1.png?raw=true" width="700" hegiht="250" align=center />
<img src="https://github.com/XiXiangkun/images/blob/master/run2.png?raw=true" width="700" hegiht="250" align=center />

## 要了我的老命啊
