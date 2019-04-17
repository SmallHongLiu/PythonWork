import itchat
import PIL.Image as Image
import math
import os

itchat.auto_login(True)  # 登录微信
friends = itchat.get_friends(update=True)[0:]

def save_avatar(avatar_file_path):
    num = 0
    for friend in friends:
        img = itchat.get_head_img(userName=friend['UserName'])
        save_path = avatar_file_path + '/' + str(num) + '.png'
        try:
            with open(save_path, 'wb') as f:
                f.write(img)
                print("正在保存第" + str(num) + "张头像")
        except Exception as e:
            print(e)

        num += 1

def make_path():
    avatar_file_path = r'test_avatar'
    if not os.path.exists(avatar_file_path):
        os.makedirs(avatar_file_path)
    return avatar_file_path

'''合成图片'''
def merge_avatar(path):
    length = len(os.listdir(path))
    each_size = int(math.sqrt(float(810 * 810) / length))
    lines = int(810 / each_size)
    image = Image.new("RGBA", (810, 810), 'white')
    x = 0
    y = 0
    for i in range(0, length):
        try:
            img = Image.open(path + '\\' + str(i) + '.png')
        except IOError:
            print("Error")
        else:
            img = img.resize((each_size, each_size), Image.ANTIALIAS)
            image.paste(img, (x * each_size, y * each_size))
            x += 1
            if x == lines:
                x = 0
                y += 1
    image.save(path + '/' + 'all.png')
    image.show()


if __name__ == "__main__":
    itchat.auto_login(True)
    friends = itchat.get_friends(update=True)[0:]
    avatar_file_path = make_path()
    save_avatar(avatar_file_path)
    merge_avatar(avatar_file_path)




