# 1.模块
- 一个模块就是一个包含python代码的文件，后缀名是.py就可以，其实模块就是python文件

- 为什么用模块
    - 程序太大，编写维护非常不方便，需要拆分
    - 模块可以增加代码重复利用的方式
    - 当作命名空间使用，避免命名冲突，即可以在不同模块下使用相同的命名
    
- 如何定义模块
    - 模块就是一个普通文件，所以任何代码可以直接书写
    - 不过根据模块的规范，最好在本模块中编写一下内容
        - 函数（单一功能）
        - 类（相似功能的组合，或者类似业务模块）
        - 测试代码
        
- 如何使用模块
    - 模块直接导入
    - 语法
        import module_name
        module_name.function_name
        module_name.class_name
    - 借助importlib包可以实现导入以数字开头的模块名称
    - import 模块 as 别名
        - 导入的同时给模块起一个别名
        - 其余用法和第一种相同
    - from module_name import func_name, class_name, 用哪个就导入哪个
    - from module_name import *  等价于  import module_name
- 'if __name__ == "__main__'的使用
    - 可以有效避免模块代码被导入的时候被动执行的问题
    - 建议所有程序的入口都以此代码为入口
    
- 模块的搜索路径和存储
    - 模块的搜索路径：加载模块的时候，系统会根据哪些地方寻找模块
    - 系统默认的模块搜索路径
        import sys
        sys.path 属性可以获取所有的被搜索的路径列表
    - 添加搜索路径： sys.path.append(dir)
    - 模块的加载顺序
        - 1. 搜索内存中已经加载好额模块
        - 2. 搜索python的内置模块
        - 3. 搜索sys.path路径，其中这个里面的顺序是按照list的顺序进行搜索
        
- 包是一种组织管理代码的方式，包里面存放的是模块，即用于将模块包含在一起的文件夹就是包
- 自定义包的结构
    - 包
    - __init__.py  包的标志文件
    - 模块1
    - 模块2
    - 模块N
    - 子包（子文件夹）
    
    
- 包的导入操作
    - import package_name
        - 直接导入一个包，可以使用__init__.py中的内容
        - 使用方式：
                package_name.func_name
                package_name.class_name.func_name()
    - import package.module
        - 导入包中某一个具体的模块
        
    - from package import module1, module2,...
        - 这种导入方法不执行 "__init__"的内容
    - from package import *
        - 导入当前包 "__init__.py" 文件中所有的函数和类
    - from package_module import *
        - 导入包中指定的模块的所有内容
        
    - 在开发环境中经常会使用其它模块，可以在当前包中直接导入其它模块中的内容
        - import 完整的包或者模块的路径
        
    - "__all__" 的用法
        - 在使用from package import *  的时候，* 可以导入的内容
        - "__init__.py" 中如果文件为空，或者没有"__all__"，那么只可以把"__init__"中的内容导入  
        - "__init__" 如果设置了 "__all__" 的值，那么则按照 "__all__" 指定的子包或者模块进行导入，如此则不会载入 "__init__" 中的内容
        - "__all__=['module1', 'module2', 'pakage1', ....]"
        
- 命名空间：用于区分不同位置不同功能但相同名称的函数或者变量的一个特定前缀