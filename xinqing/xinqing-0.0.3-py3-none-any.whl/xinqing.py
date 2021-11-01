import time
import sys
from random import uniform
import vlc


def typewriter_print(arr):
    for x in arr:
        print(x, end='')
        sys.stdout.flush()
        time.sleep(uniform(0, 0.3))
    print()


class Xinqing:
    def __init__(self):
        self.name = "Xinqing"
        self.age = 39
        self.occupation = "大学老师"
        self.hobby = "摸鱼"
        self.knowledge_quantity = "负无穷"
        self.sound = vlc.MediaPlayer("typing_long.mp3")

    def do_what(self):
        self.sound.play()
        typewriter_print("我想摸鱼、打牌、唱歌、再胡乱指使一个学生做点什么无意义的事情，我的一句话，他的一学期，想想就让人开心。")
        typewriter_print("你觉着呢？做哪个好呢？")
        self.sound.stop()

    def know_what(self):
        self.sound.play()
        typewriter_print("我博士没有发一篇SCI就毕业了，多亏了我左右逢源、深谙世事。")
        typewriter_print("在xx大学，我依旧发扬这种精神，从来不会发SCI。")
        typewriter_print("但是我还是有追求的，发SCI是我毕生的追求。")
        typewriter_print("但是，心里充满欲望，身体没有力量。")
        typewriter_print("好在，有很多优秀的学生被我光怪陆离的简历吸引，慕名前来。")
        typewriter_print("所以，自己能力不够，使劲压榨学生来凑。")
        typewriter_print("不过，因为自己实在是不懂什么技术，这该怎么指导学生呢？")
        typewriter_print("没事，就随便让他们做点什么，毕竟不是自己的时间。")
        self.sound.stop()
