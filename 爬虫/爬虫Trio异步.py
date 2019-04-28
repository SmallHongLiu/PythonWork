# 一个标准方法
def regular_double(x):
    return 2 * x


# 一个异步方法
async def async_double(x):
    return 2 * x


import trio

trio.run(async_double, 3)  # 使用trio.run调用第一个异步函数


# 异步中的等待
async def double_sleep(x):
    await trio.sleep(2 * x)

trio.run(double_sleep, 3)


# 异步函数调用的典型结构   trio.run -> [async function] -> ... -> [async function] -> trio.whatever


# 多个异步函数
async def child1():
    print(' child1: started! sleeping now...')
    await trio.sleep(1)
    print(' child1: exiting!')

async def child2():
    print(' child2: started! sleeping now...')
    await trio.sleep(1)
    print(' child2: exiting!')

async def partent():
    print('parent: started!')
    async with trio.open_nursery() as nursery:
        print('parent: spawning child1...')
        nursery.start_soon(child1)

        print('parent: spawning child2...')
        nursery.start_soon(child2)

        print('parent: waiting for children to finish...')

    print('parent: all done!')

trio.run(partent)