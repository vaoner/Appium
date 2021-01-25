# coding:utf-8
from appium import webdriver
import time
caps={
    'platformName':'Android',#被测app所处平台-操作系统
    'platformVersion':'8.1.0',#操作系统(安卓)版本
    'deviceName':'5789f4be7cf5',#被测设备名称，可以在cmd中进入AndroidSDK\platform-tools目录执行adb devices -l查询到
    #被测app的信息-首先在设备上打开被测app（网易云音乐），然后在cmd中进入AndroidSDK\platform-tools目录执行adb shell dumpsys activity recents | findstr intent获取设备（手机）上最近活动日志，找到网易云音乐应用的日志，再找出包名和入口(cmp后面那一串字符)：
    #intent={act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] flg=0x10200000 cmp=com.netease.cloudmusic/.activity.LoadingActivity}
    'appPackage':'com.netease.cloudmusic',#包名-代表被测app在设备上的地址
    'appActivity':'.activity.LoadingActivity',#入口信息-被测app的入口
    'noReset':'True',#禁止app在自动化后重置
    'newCommandTimeout':3600,#设置命令超时时间，单位秒
    'automationName':'UiAutomator2'#指定驱动为UI2，安卓默认使用的是UiAutomator自动化框架，效率较低
}

#启动被测app：
driver=webdriver.Remote('http://127.0.0.1:4723/wd/hub',caps)#网址为Appium Server的地址，端口为Appium Server的端口，/wd/hub是固定的Appium Server端接口名称

#隐士等待：如果当前界面没有出现目标元素就会等待一下直到超出设定的时间（秒），如果出现了目标元素直接跳过等待
driver.implicitly_wait(10)
'''
##打印“每日推荐”的前三首歌曲
#进入“发现”页面
a=driver.find_element_by_id("com.netease.cloudmusic:id/desc").click()
#点击“每日推荐”
b=driver.find_element_by_id("com.netease.cloudmusic:id/portalTitle").click()
#获取前三首歌曲
c=driver.find_elements_by_id("com.netease.cloudmusic:id/songName")[:3]#elements方法获取的是列表
for i in c:
    print(i.text)
'''
##新建歌单“每日精选”，并将“每日推荐”内的前三首歌添加进去
#1.进入“我的”
driver.find_element_by_xpath("//*[@text='我的']").click()
#2.滑动屏幕，使用swipe方法，从start_x,start_y坐标滑动到end_x,end_y坐标。这样手机当前页面上才能看到新建歌单按钮
start_x=300
start_y=1000
end_x=300
end_y=500
time.sleep(2)#休眠2秒，防止超时报错
driver.swipe(start_x,start_y,end_x,end_y)
#3.点击新建"+"按钮
driver.find_element_by_id("com.netease.cloudmusic:id/create").click()
#4.输入歌单名称
driver.find_element_by_id("com.netease.cloudmusic:id/etPlaylistName").send_keys("每日精选")
time.sleep(1)#等待字符输入完之后，"完成"按钮才可以点击
#5.点击完成按钮
driver.find_element_by_id("com.netease.cloudmusic:id/tvCreatePlayListComplete").click()
time.sleep(1)
#6.返回主页面
driver.keyevent(4)#4表示android自带的返回键。android的系统按键参考：https://blog.csdn.net/weixin_43743725/article/details/85039615
#7.进入"发现"
driver.find_element_by_xpath("//*[@text='发现']").click()
#8.进入"每日推荐"
driver.find_element_by_xpath("//*[@text='每日推荐']").click()
#9.将前三首歌添加到每日精选歌单，获取前三首歌曲的操作菜单按钮，然后重复添加歌单过程
options=driver.find_elements_by_id('com.netease.cloudmusic:id/actionBtn')[:3]
for option in options:
    #点击操作按钮（三个小点）;
    option.click()
    #点击收藏到歌单
    driver.find_element_by_xpath('//*[@text="收藏到歌单"]').click()
    #选择每日精选这个歌单
    driver.find_element_by_xpath('//*[@text="每日精选"]').click()
    time.sleep(1)
##收尾操作，删除测试残留
# 1.返回主界面
driver.keyevent(4)
#2.选择"我的"
driver.find_element_by_xpath("//*[@text='我的']").click()
#3.查看歌单内容，然后返回
driver.find_element_by_xpath("//*[@text='每日精选']").click()
time.sleep(1)
driver.keyevent(4)
#4.选择"每日精选"歌单后面的三个点
driver.find_element_by_id("com.netease.cloudmusic:id/actionContainer").click()
#5.在弹出的选项中选择"删除",并在弹出的页面确认删除
driver.find_element_by_xpath("//*[@text='删除']").click()
driver.find_element_by_id("com.netease.cloudmusic:id/buttonDefaultPositive").click()

