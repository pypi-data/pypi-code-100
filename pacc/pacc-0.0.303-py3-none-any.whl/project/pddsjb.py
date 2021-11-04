from .project import Project


class Activity:
    MainFrameTabActivity = 'com.xunmeng.merchant/com.xunmeng.merchant.ui.MainFrameTabActivity'


class Class:
    EditText = 'android.widget.EditText'


class Bounds:
    InputBox = '[246,-1][903,-1]'  # 搜索框


class PDDSJB(Project):
    def __init__(self, deviceSN):
        super(PDDSJB, self).__init__(deviceSN)

    def openApp(self):
        super(PDDSJB, self).openApp(Activity.MainFrameTabActivity)

    def enterShoppingInterface(self):
        try:
            self.reopenApp()
            self.uIAIns.click(text='我的')
            self.uIAIns.click(text='拼多多批发')
        except FileNotFoundError as e:
            print(e)
            self.enterShoppingInterface()

    def search(self):
        self.enterShoppingInterface()
        self.uIAIns.getCurrentUIHierarchy()
        self.uIAIns.click(Class=Class.EditText)
        self.uIAIns.click(Class=Class.EditText)
        self.adbIns.inputText('裤')
        self.adbIns.pressEnterKey()
        self.uIAIns.click(text='价格')

