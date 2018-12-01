# Django系统
- 环境
    - python3.6
    - django1.8
- 参考资料
    - 中文教程：http://python.usyiyi.cn/
    - django架站的16堂课
    
# 环境搭建
- anaconda + pycharm
- anaconda的使用
    - conda list: 显示当前环境安装的包
    - conda env list: 显示安装的虚拟环境列表
    - conda create -n env_name python=3.6
    - 激活conda的虚拟环境
        - (Linux) source activate env_name
        - (win) activate env_name
    -pip install django=1.8
    
# 后台需要的流程

# 创建第一个Django程序
- 命令行启动
        Django-admin startproject ******
        cd ******
        python manage.py runserver
        
# 路由系统-urls
- 创建app
    - app：负责一个具体业务或者一类具体业务的模块
    - python manage.py startapp teacher
    
- 路由
    - 按照具体的请求url，导入到相应的业务处理模块的一个功能模块
    - django的信息控制中枢
    - 本质上是接受的URL和相应的处理模块的一个映射
    - 在接受URL请求的匹配上使用了RE
    - URL的具体格式如urls.py中所示
- 需要关注两点：
    1. 接受的URL是什么，即如何使用RE对传入的URL进行匹配
    2. 已知URL匹配到哪个处理模块
    
- url匹配规则
    - 从上往下一个一个对比
    - url格式是分级格式，则按照级别一级一级往下对比，主要对应url包含子url的情况
    - 子url一旦被调用，则不会返回到主url
        - /one/two/three
    - 正则以r开头，表示不需要转移，注意尖号(^)和美元符号($)
        - '/one/two/three' 匹配r'^one/
        - '/oo/one/two/three' 不匹配r'^one/"
        - '/one/two/three/' 匹配r'three/$'
        - '/oo/one/two/three/oo' 不匹配r'three'$"
        - 开头不需要有反斜杠
    - 如果从上向下都没有找到合适的匹配内容，则报错
    
# 2. 正常映射
- 把某一个符合RE的URL映射到事物处理函数中去
    - 举例如下：
        from showeast import views as sv
        
        urlpatterns = [
            url(r'^admin/', admin.site.urls),
            url(r'^normalmap/', sv.normalmap),
        ]
        
        
# 3. URL中带参数映射
- 在事件处理代码中需要由URL传入参数，形如 /myurl/param中的param
- 参数都是字符串形式，如果需要整数等形式需要自行转换
- 通常的形式如下：
    '''
    /search/page/432中的432需要经常性变换，所以
    '''
    
# 4. URL在app中的处理
- 如果所有应用URL都集中django_school_demo/urls.py中，可能导致文件的臃肿
- 可以把urls具体功能逐渐分散到每个app中
    - 从django.conf.urls导入include
    - 注意此时RE部分的写法
    - 添加include导入
- 使用方法
    - 确保include被导入
    - 写主路由的开头url
    - 写子路由
    - 编写views函数
- 同样可以使用参数

# 5. URL中的嵌套参数
- 捕获某个参数的一部分
    - 例如URL /index/page-3, 需要捕获参数3作为参数
        url(r'index_1/(page-(\d+)/)?$', sv.myindex_1), # 不太好
        url(r'index_2/(?:page-(?P<page_number>\d+)/)?$', sv.myindex_2), # 好
- 上述例子会得到两个参数，但 ?: 表示忽略此参数

# 6. 传递额外参数
- 参数不仅仅来自URL，还可能是我们自己定义的内容
    url(r'extra/$', sv.extra_param, {'name': 'SmallHong'}),
- 附加参数同样适用于include语句，此时对include内所有都添加

# 7. URL的反向解析
- 防止硬编码
- 本质上是对每一个URL进行命名
- 以后再编码代码中使用URL的值，原则上都应该使用反向解析

# views视图
- 1. 视图概述
    - 视图即视图函数，接受web请求并返回web响应的事物处理函数
    - 响应指符合http协议要求的任何内容，包括json, string, html等
    - 本章忽略事务处理，重点在如何返回处理结果上
- 2. 其它简单视图
    - django.http给我们提供很多和HttpResponse类似的简单视图，通过查看django.http代码我们知道，此类视图使用方法基本类似，可以通过return语句直接反馈返回给浏览器
    - Http404为Exception子类，所以需要raise使用 

- 3. HttpResponse详解
- 方法
    - init：使用页内容实例话HttpResponse对象
    - write(content): 以文件的方式写
    - flush(): 以文件的方式输出缓存区
    - set_cookie(key, value='', max_age=None, expires=None): 设置cookie
        - key, value都是字符串类型
        - max_age是一个整数，表示在指定秒数后过期
        - expires是一个datetime或timedelta对象，会话将在这个指定的日期/时间过期
        - max_age与expires二选一
        -如果不指定过期时间，则两个星期后过期
    - delete_cookie(key)：删除指定的key的cookie，如果key不存在则表示什么也不会发生
    
- 4. HttpResponseRedirect
    - 重定向，服务器端跳转
    - 构造函数的第一个参数用来指定重定向的地址
    - 案例
        url(r'^v10_1/', views.v10_1),
        url(r'^v10_2/', views.v10_2),
        url(r'^v11/', views.v11, name='v11),
        
        def v10_1(request):
            return HttpResponseRedirect('/v11)
            
        def v10_2(request):
            return HttpResponseRedirect(reverse('v11'))
            
        def v11(request):
            return HttpResponse('哈哈，这是v11的访问返回')
            
- 5. Request对象
- Request介绍
    - 服务器接收到http协议的请求后，会根据报文创建HttpRequest对象
    - 视图函数的第一个参数是HttpRequest对象
    - 在django.http模块中定义了HttpRequest对象的API
- 属性
    - 下面除非特别说明，属性都是只读的
    - path: 一个字符串，表示请求的页面的完整路径，不包含域名
    - method: 一个字符串，表示请求使用的Http方法，常用值包括：get，post
    - encoding: 一个字符串，表示提交的数据的编码方式
        - 如果为None，则表示使用浏览器的默认设置，一般为utf-8
        - 这个属性是可写的，可以通过修改它来修改访问表单数据使用的编码
    - GET: 一个类似于字典的对象，包含get请求方式的所有参数
    - POST: 一个类似于字典的对象，包含post请求方式的所有参数
    - FILES：一个类似于字典的对象，包含所有的上传文件
    - COOKIE: 一个标准的python字典，包含所有的cookie，键和值
    - session: 一个既可读又可写的类似于字典的对象，表示当前的会话，只有当Django启动会话的支持时才可用，详细内容见'状态保持'
    - is_ajax(): 如果请求是通过XMLHttpRequest发起的，则返回True
- 方法
    - is_ajax(): 如果请求是通过XMLHttpRequest发起的，则返回True
- QueryDict对象
    - 定义在django.http.QueryDict
    - request对象的属性get，post都是QueryDict类型的对象
    - 与python字典不同，QueryDict类型的对象用来处理同一个键带有多个值的情况
    - 方法get(): 根据键获取值
        - 只能获取键的一个值
        - 如果一个键同时拥有多个值，获取最后一个值
    - 方法getlist(): 根据键获取值
        - 将键的值以列表返回，可以获取一个键的多个值
- GET属性
    - QueryDict类型的对象
    - 包含get请求方式的所有参数
    - 与url请求地址中的参数对应，位于？后面
    - 参数的格式是键值对，如key1=value1
    - 多个参数之间，使用&连接，如key1=value1&key2=value2
    - 键是开发人员定下来的，值是可变的
- POST属性
    - QueryDict类型的对象
    - 包含post请求方式的所有参数
    - 与form表单中的控件对应
    - 表单中控件必须有name属性，name为健，value为值
        - checkbox 存在一键多值的问题
    - 键是开发人员定下来的，值是可变的
    
- 6. 手动编写视图
    - 实验目的：
        - 利用Django快捷函数手动编写视图处理函数
        - 编写过程中理解视图运行原理
    - 分析
        - Django把所有请求信息封装入request
        - Django通过urls模块把相应请求跟事件处理函数链接起来，并把request作为参数传入
        - 在相应的处理函数中，我们需要完成两部分
            - 处理业务
            - 把结果封装并返回，我们可以使用简单HttpResponse，同样也可以自己处理此功能
    
    - render(request, template_name, context_instance......)
        - 使用模版和一个给定的上下文环境，返回一个渲染好的HttpResponse对象
        - request：Django的传入请求
        - template_name: 模版名称
        - content_instance: 上下文环境
        
    - render_to_response
        - 根据给定的上下文字典渲染给定模版，返回渲染后的HttpResponse

- 7. 系统内建视图
    - 系统内建视图，可以直接使用
    - 404
        - default.page_not_found(request, template_name='404.html')
        - 系统引发Http404时触发
        - 默认传递request_path变量给模版，即导致错误的url
        - DEBUG=True则不会调用404，取而代之是调试信息
        - 404视图会被传递一个RequestContext对象并且可以访问模版上下文处理器提供的变量
        
- 8. 基于类的视图
- 和基于函数的视图的优势和区别：
    - Http方法的method可以有各自的方法，不需要使用条件分支来解决
    - 可以使用OOP技术
- 概述
    - 核心是允许使用不同的实例方法来对应不同的http请求方法，而避开条件分支实现
    - as_view函数作为类的可调用入口，该方法创建一个实例并调用dispatch方法
- 类属性使用
    - 在类定义时直接覆盖
    - 在调用as_view的时候直接作为参数使用，例如：
        urlpatterns = [
            url(r'^about/', GreetingView.as_view(greeting="G'day")),
        ]
        
- 对基于类的视图的扩充大致有三种方法：Mixin，装饰as_view, 装饰dispatch
- 使用Mixin
    - 多继承的一种形式，来自父类的行为和属性组合在一起
    - 解决多继承问题
    - View的子类只能单继承，多继承会导致不可期问题
    - 多继承带来的问题：
        - 结构复杂

    
    

        
        