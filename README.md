# myblog
基于flask的个人博客系统<br>
前台见 [段少强的博客](http://www.duanshaoqiang.com)<br>
后台管理页面:<br>
首页:<br>![首页](http://ww1.sinaimg.cn/large/e9cd5756gy1g2w71wkjdmj21ha0pewfx.jpg)<br>
博客列表:<br>![博客列表](http://ww1.sinaimg.cn/large/e9cd5756gy1g2w72tig7tj21h90mxq63.jpg)<br>
如何使用:<br>
1.自行安装虚拟环境及所需第三方库<br>
2.激活虚拟环境后,在终端输入:set FLASK_APP=blog<br>
3.在settings.py文件中替换自己的数据库用户名密码以及数据库<br>
4.在终端输入:flask --help 可以看到<br>
![自定义flask命令生成虚拟数据](http://ww1.sinaimg.cn/large/e9cd5756gy1g2w78mpn6fj209705dq2u.jpg)<br>
5.输入:flask forge可以生成虚拟数据(同时生成了管理员（可以在faker.py中更改）：账号:admin;密码:helloblog)<br>
6.浏览器输入127.0.0.1:5000即可.<br><br>
