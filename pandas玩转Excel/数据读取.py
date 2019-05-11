import pandas as pd

'''
df = pd.DataFrame({'ID': [1, 2, 3], 'Name': ['Tim', 'Victor', 'Nick']})

df.to_excel("output.xlsx")
print("Done!")
'''

'''读取文件到pd'''
'''
people = pd.read_excel("People.xlsx")
print(people.shape)
print(people.columns)
print(people.head())  # 默认为前5行的数据，可以通过传值设置读取多少行

people = pd.read_excel('People.xlsx', header=1)  # 设置起始行的位置

people = pd.read_excel('People.xlsx', header=None)  # 设置没有header
people.columns = ['ID', 'Type', 'Title', 'FirstName','MiddleName', 'LastName']  # 设置header
people.set_index('ID', inplace=True)
print(people.columns)
people.to_excel('output.xlsx')
print('Done!')
'''

'''
df = pd.read_excel('output.xlsx', index_col='ID')  # 指明index, 避免重复生成index
df.to_excel('output2.xlsx')
print(df.head())
'''
'''
d = {'x': 100, 'y': 200, 'z': 300}

print(d['x'], d['y'], d['z'])

s1 = pd.Series(d)
print(s1.data)

L1 = [100, 200, 300]
L2 = ['x', 'y', 'z']

s1 = pd.Series(L1, index=L2)
print(s1.index)

s1 = pd.Series([100, 200, 300], index=['x', 'y', 'z'])
'''

'''
s1 = pd.Series([1, 2, 3], index=[1, 2, 3], name='A')
s2 = pd.Series([10, 20, 30], index=[1, 2, 3], name='B')
s3 = pd.Series([100, 200, 300], index=[1, 2, 3], name='C')

df = pd.DataFrame({s1.name: s1, s2.name: s2, s3.name: s3})
print(df)

df = pd.DataFrame([s1, s2, s3])
print(df)
'''

'''
from datetime import date, timedelta

def add_month(d, md): # 参数d: date, md: ➕的月份
    yd = md // 12 # 年份
    m = d.month + md % 12
    if m != 12:
        yd += m // 12
        m = m % 12
    return date(d.year+yd, m, d.day)


books = pd.read_excel('Books.xlsx', skiprows=3, usecols='C:F', index_col=None, dtype={'ID': str, 'InStore': str, 'Date': str}) # skiprows: 跳过几行; usecols：使用哪些列, 注意：这里不能直接设置dtype为int类型
start = date(1993, 10, 20)
for i in books.index:
    books['ID'].at[i] = i + 1
    books['InStore'].at[i] = 'Yes' if i % 2 == 0 else 'No'
    # books['Date'].at[i] = start + timedelta(days=i) # 天数➕1, timedelta可以➕秒，分，时，天，不能➕月和年
    books['Date'].at[i] = add_month(start, i)
    # books.at[i, 'Date'] = add_month(start, i) 同上一行一样的效果，只不过这个是直接修改，而不用先拿到值
print(books)

books.set_index("ID", inplace=True)
books.to_excel('Output_Books.xlsx')
'''

'''
def add_2(x):
    return x + 2;

# 注意：在Excel中，我们操作的是单元格，但是在python中，我们操作的是一列数据
books = pd.read_excel('Books_Info.xlsx', index_col='ID')
books['Price'] = books['ListPrice'] * books['Discount']

for i in books.index: # 获取每一行的索引
    books['Price'].at[i] = books['ListPrice'].at[i] * books['Discount'].at[i] # 一般情况下不使用这种情况，当不希望从头到尾的运算，比如只希望从哪一行到哪一行运算的时候可以使用这种方法

books['ListPrice'] = books['ListPrice'].apply(add_2)
# books['ListPrice'] = books['ListPrice'].apply(lambda x: x + 2) 同上一行代码效果相同
print(books)
'''


''''
products = pd.read_excel('List.xlsx', index_col='ID')
products.sort_values(by='Price', inplace=True, ascending=False) # inplace=True: 表示在当前数据中排序，而不会生成一个新的
products.sort_values(by=['Worthy', 'Price'], inplace=True, ascending=[True, False]) # by：数组，多个数据排序
print(products)
'''

'''
def age_18_to_30(age):
    return 18 <= age < 30

def level_a(score):
    return 85 <= score <= 100

students = pd.read_excel('Students.xlsx', index_col='ID')
# students = students.loc[students['Age'].apply(age_18_to_30)].loc[students['Score'].apply(level_a)] # 将Age这一列数据依次塞入age_18_to_30这个函数中
students = students.loc[students.Age.apply(age_18_to_30)] \
    .loc[students.Score.apply(level_a)]

print(students)
'''

import matplotlib.pyplot as plt

'''
students = pd.read_excel('Students_Statistic.xlsx')
students.sort_values(by='Number', inplace=True, ascending=False)
print(students)

# students.plot.bar(x='Field', y='Number', color='orange', title='International Students by Field')

plt.bar(students.Field, students.Number, color='orange')
plt.xticks(students.Field, rotation='90') # rotation旋转
plt.xlabel('Field')
plt.ylabel('Number')
plt.title('International Students by Field', fontsize=16)
plt.tight_layout() # 表示紧凑型布局

plt.show()
'''

'''
students = pd.read_excel('Students_Compare.xlsx')
students.sort_values(by='2017', inplace=True, ascending=False)
print(students)
students.plot.bar(x='Field', y=['2016', '2017'], color=['orange', 'red'])
plt.title('International Student by Field', fontsize=16)
plt.xlabel('Field', fontweight='bold')
plt.ylabel('Number', fontweight='bold')
ax = plt.gca()  # gca: get color axis
ax.set_xticklabels(students['Field'], rotation=45, ha='right')  # ha：表示水平对齐方向
f = plt.gcf()
f.subplots_adjust(left=0.2, bottom=0.42)  # subplots_adjust：调整子图区域
plt.tight_layout()
plt.show()
'''

'''
users = pd.read_excel('Users.xlsx')
users['Total'] = users['Oct'] + users['Nov'] + users['Dec']
users.sort_values(by='Total', inplace=True, ascending=True)
print(users)

users.plot.barh(x='Name', y=['Oct', 'Nov', 'Dec'], stacked=True, title='User Behavior')
plt.tight_layout()
plt.show()
'''

'''
students = pd.read_excel('Students_Source.xlsx', index_col='From')  # 注意：如果读取时不指定index，则其将自动生成index，从0开始
print(students)

# 注意：画饼图需要的是Series数据，即只需要一列数据就行，不用拿这个DataFrame的数据
# students['2017'].sort_values(ascending=True).plot.pie(fontsize=8, startangle=-270)  # 注意，通常还可以使用students.**(其中，**表示某列的名称)，但是由于2017是个数字，比较特殊，则不能使用该方式
students['2017'].plot.pie(fontsize=8, counterclock=False, startangle=-270)  # counterclock: 逆时针
plt.title('Source of International Students', fontsize=10)
plt.ylabel('2017', fontsize=12, fontweight='bold')

plt.show()
'''

'''
weeks = pd.read_excel('Weeks.xlsx', index_col='Week')
print(weeks)
print(weeks.columns)

# 叠加区域图和叠加柱状图的区别：
# 叠加柱状图重在表达在某一个节点上的值叠加起来是个什么的样子的高度，
# 而叠加区域图主要是通过这些连连续续的点为我们指明一个趋势，走势
# weeks.plot.area(y=['Accessories', 'Bikes', 'Clothing', 'Components'])  # 叠加区域图
weeks.plot.bar(y=['Accessories', 'Bikes', 'Clothing', 'Components'], stacked=True) # 叠加柱状图
plt.title('Sales Weekly Trend', fontsize=16, fontweight='bold')
plt.ylabel('Total', fontsize=12, fontweight='bold')
plt.xticks(weeks.index, fontsize=8)
plt.show()
'''

'''
pd.options.display.max_columns = 888
homes = pd.read_excel('home_data.xlsx')
# print(homes.head())
'''

'''
# 散点图
homes.plot.scatter(x='sqft_living', y='price')
'''

'''
# 直方图

homes.price.plot.hist(bins=100)
plt.xticks(range(0, max(homes.price), 100000), fontsize=8, rotation=90)
'''

'''
# 密度图
homes.sqft_living.plot.kde()
plt.xticks(range(0, max(homes.sqft_living), 500), fontsize=8, rotation=90)
'''

'''
print(homes.corr())  # 各列之间的关系

plt.show()
'''

'''
students = pd.read_excel('Student_score.xlsx', sheet_name='Students', index_col='ID')
scores = pd.read_excel('Student_score.xlsx', sheet_name='Scores', index_col='ID')

# table = students.merge(scores, how='left', on='ID').fillna(0)  # 根据左边的数据进行合并，on:表示利用哪个共同的数据进行连接
table = students.join(scores, how='left').fillna(0)
table.Score = table.Score.astype(int)
print(table)
'''


# 注意：当读取Excel数据时，最好不要手动设置index_col，这样子有利于表格中所有的数据以普通数据格式进行展示

'''
def score_validation(row):
    # 方法1：try-except
    try:
        assert 0 <= row.Score <= 100
    except:
        print(f'{row.ID}\tstudent {row.Name} has an invalid score {row.Score}.')  # \t表格制表符

    # 方法2：if
    if not 0 <= row.Score <= 100:
        print(f'{row.ID}\tstudent {row.Name} has an invalid score {row.Score}.')

students = pd.read_excel('Students_Scores.xlsx')

# 校验分数
students.apply(score_validation, axis=1)  # axis：轴，1：从左向右，0：从上向下，这里也就是一行一行的校验
# print(students)
'''

'''
# 数据分割
employees = pd.read_excel('Employees.xlsx', index_col='ID')
df = employees['Full Name'].str.split(n=2, expand=True)  # n: 表示切割出来之后保留的子字符串的个数，如果不写，则表示有多少保留多少
employees['First Name'] = df[0]
employees['Last Name'] = df[1]
print(employees)
'''


'''
students = pd.read_excel('Students_All_Scores.xlsx', index_col='ID')

temp = students[['Test_1', 'Test_2', 'Test_3']]
row_sum = temp.sum(axis=1)
row_mean = temp.mean(axis=1)
students['Total'] = row_sum
students['Average'] = row_mean

col_mean = students[['Test_1', 'Test_2', 'Test_3', 'Total', 'Average']].mean()
col_mean['Name'] = 'Summary'
students = students.append(col_mean, ignore_index=True)  # append是以一行的形式进行追加
print(students)
'''


'''
students = pd.read_excel('Students_Duplicates.xlsx')
dupe = students.duplicated(subset='Name')  # 查看某列中哪些数据是重复的
dupe = dupe[dupe]
print(students.iloc[dupe.index])  # iloc：表示使用index来loc
students.drop_duplicates(subset='Name', inplace=True, keep='first')  # 去重, inplace:表示在当前进行操作, keep：表示当重复时保存开头的还是结尾的数据
# print(students)
'''


'''
# 旋转数据
pd.options.display.max_columns = 999
videos = pd.read_excel('Videos.xlsx')
table = videos.transpose()
print(table)
'''


'''
# 读取各种文件格式
student1 = pd.read_csv('Students_Format.csv', index_col='ID')
print(student1)

student2 = pd.read_csv('Students_Format.tsc', sep='\t', index_col='ID')  # sep:表示利用\t来分割数据
print(student2)

student3 = pd.read_csv('Students_Format.txt', sep='|', index_col='ID')
print(student3)
'''

import numpy as np

'''
# 数据透视
pd.options.display.max_columns = 999
orders = pd.read_excel('Orders_Group.xlsx')
orders['Year'] = pd.DatetimeIndex(orders['Date']).year

pt1 = orders.pivot_table(index='Category', columns='Year', values='Total', aggfunc=np.sum)

# 数据分组
groups = orders.groupby(['Category', 'Year'])
s = groups['Total'].sum()
c = groups['ID'].count()

pt2 = pd.DataFrame({'Sum': s, 'Count': c})
print(pt2)
'''

'''
# 线性回归方程，对数据进行预测
from scipy.stats import linregress
sales = pd.read_excel('Sales.xlsx', dtype={'Month': str})
print(sales)
'''


'''
plt.bar(sales.index, sales.Revenue)
plt.title('Sales')
'''


'''
# 计算线性回归方程
slope, intercept, r, p, std_err = linregress(sales.index, sales.Revenue)
exp = sales.index * slope + intercept

plt.scatter(sales.index, sales.Revenue)
plt.plot(sales.index, exp, color='orange')
plt.title(f'y={slope} * x + {intercept}')
plt.xticks(sales.index, sales.Month, rotation=90)

plt.tight_layout()
plt.show()
'''

# 综合使用
page_001 = pd.read_excel('Students_Composite.xlsx', sheet_name='Page_001')
page_002 = pd.read_excel('Students_Composite.xlsx', sheet_name='Page_002')

'''
students = page_001.append(page_002).reset_index(drop=True)  # drop：表示是否放弃原有的index

# 追加一行
stu = pd.Series({'ID': 41, 'Name': 'Abel', 'Score': 99})
students.append(stu, ignore_index=True)

# 修改值
students.at[39, 'Name'] = 'Bailey'
students.at[39, 'Score'] = '120'
# 等同于上面两行代码，但是两者的原理不同，在内存中，这个会直接替换到id为39的那行数据，上面的不会替换
stu = pd.Series({'ID': 40, 'Name': 'Bailey', 'Score': 120})
students.iloc[39] = stu

# 插入一行数据
stu = pd.Series({'ID': 101, 'Name': 'Danni', 'Score': 101})
part1 = students[:20]
part2 = students[20:]
students = part1.append(stu, ignore_index=True).append(part2).reset_index(drop=True)

# 删除数据行
students.drop(index=[0, 1, 2], inplace=True)
students.drop(index=range(0, 10), inplace=True)
# 利用切片删除数据行
students.drop(index=students[0:10], inplace=True)

# 按条件删除
for i in range(5, 15):
    students['Name'].at[i] = ''

missing = students.loc[students['Name'] == '']
students.drop(index=missing.index, inplace=True)

students = pd.concat([page_001, page_002], axis=1)  # 并列两个数据
students['Age'] = 25
# students['Age'] = np.repeat(25, len(students))
# students['Age'] = np.arange(0, len(students))

students.drop(columns=['Age', 'Score'], inplace=True)
students.insert(1,  column='Foo', value=np.repeat('foo', len(students)))
students.rename(columns={'Foo': 'FOO', 'Name': 'NAME'}, inplace=True)

# 去掉空值操作
students['ID'] = students['ID'].astype(float)
for i in range(5, 15):
    students['ID'].at[i] = np.nan
students.dropna(inplace=True)  # dropna：会扫描所有列的数据

print(students)
'''

'''
# 连接数据库
import pyodbc
import sqlalchemy
import pandas as pd

connection = pyodbc.connect('DRIVER={SQL Server}; SERVER=(local); DATABASE=AdventureWorks;USER=sa;PASSWORD=123456')
engine = sqlalchemy.create_engine('mssql+pyodbc://sa:123456@(local)/AdventureWorks?driver=SQL+Server')

query = 'SELECT FirstName, LastName FROM Person.Person'
df1 = pd.read_sql_query(query, connection)
df2 = pd.read_sql_query(query, engine)

pd.options.display.max_columns = 999
print(df1.head())
print(df2.head())
'''


# 复杂方程的编写

def get_circumcircle_area(l, h):
    r = np.sqrt(l ** 2, h ** 2) / 2
    return r ** 2 * np.pi

def wrapper(row):
    return get_circumcircle_area(row['Length'], row['Height'])

rects = pd.read_excel('Rectangles.xlsx')
# rects['CA'] = rects.apply(wrapper, axis=1)
rects['CA'] = rects.apply(lambda row: get_circumcircle_area(row['Length'], row['Height']), axis=1)  # 同上面效果相同

print(rects)





































