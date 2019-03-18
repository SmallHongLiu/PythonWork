# 结构化文件存储
- xml，json
- 为了解决不同设备之间信息交换

# xml文件
- 参考资料

- XML(EXtensible Markup Language): 可扩展的标记语言
    - 标记语言：语言中使用尖扣号括起来的文本字符串标记
    - 可扩展：用户可以自己定义需要的标记
    - 是w3c组织制定的一个标准
    - xml描述的是数据本身，即数据的结构和语义
    - HTML侧重于如何显示web页面中的数据
    
- XML文档的构成
    - 处理指令（可以认为一个文件内只有一个处理指令）
        - 最多只有一行
        - 且必须在第一行
        - 内容是与xml本身处理器相关的一些声明或者指令
        - 以xml关键字开头
        - 一般用于声明xml的版本和采用的编码
            - version表示版本
            - encoding表示编码方式，也就是用来指出xml解释器使用的编码，常用utf-8
    - 根元素（一个文件内只有一个根元素）
        - 在整个xml文件中，可以把它看作一个树形结构
        - 根元素有且只能有一个
    - 子元素
    - 属性
    - 内容
        - 表明标签所存储的信息
    - 注释
        - 起说明作用的信息
        - 注释不能嵌套在标签里
        - 只有在注释的开始和结尾使用双短横线
        - 三短横线只能出现在注释的开头
        
- 保留字符的处理
    - xml中使用的符号可能和实际符号相冲突，典型的就是左右尖括号
    - 使用实体引用（EntityReference）来表示保留字符
        - 如
        <score> score&gt;80</score> # 使用实体引用
    - 把含有保留字符的部分放在CDATA块内部，CDATA块把内容信息视为不需要转义
    - 常用的需要转移的保留字符和对应实体引用
        - &:&amp;
        - <:&lt;
        - >: &gt;
        - ': &apos;
        - ": &quot;
        - 一共五个，每个实体引用都以&开头并且以分号结尾
        
- XML标签的命名规则
    - Pascal命名法
    - 用单词表示，第一个单词大写
    - 大小写严格区分
    - 配对的标签必须一致
    
- 命名空间
    - 为了防止命名冲突
    - 如果想归并两个内容信息，则可能会产生冲突
    - 解决冲突的办法：给可能产生冲突元素添加命名空间
    - xmlns: xml name space
        - 如：<Schooler xmlns:stuent="http://my_student" xmlns:="http://my_room">
                <student:Name>SmallHong</student:Name>
                <Age>18</Age>
                <room:Name>房间1</room:Name>
                <Locaiton>银沙横街</Locaiton>
              </Schooler>
              
# 读取
- xml读取分两个主要技术: SAX, DOM
- SAX(Simple Api for XML)
    - 基于事情驱动
    - 利用SAX解析文档涉及到解析器和事件处理两部分
    - 特点：
        - 快
        - 流失读取
        
- DOM
    - 是w3c规定的xml编程接口
    - 一个xml文档在缓存中以树形结构保存，读取
    - 用途
        - 定位浏览xml中任何一个节点信息
        - 添加删除相应内容
    - minidom
    - etree
    
- xml文件写入
    - 更改
        - ele.set: 修改属性
        - ele.append: 添加子元素
        - ele.remove: 删除元素
    - 生成创建的方法
        - SubElement创建
        - minidom创建
        - etree创建
        