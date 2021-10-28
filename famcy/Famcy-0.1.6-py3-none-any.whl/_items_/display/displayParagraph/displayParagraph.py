import markdown
import Famcy
import json

class displayParagraph(Famcy.FamcyBlock):
    """
    Represents the block to display
    paragraph. 
    """
    def __init__(self):
        self.value = displayParagraph.generate_template_content()
        super(displayParagraph, self).__init__()

    @classmethod
    def generate_template_content(cls):
        return {
                "title": "displayParagraph",
                "content": '''
**Nexuni 会社ウェブサイトの案内** 

    1. 希望能讓來到Nexuni的新朋友都能夠快速地學習並瞭解我們工作時會使用到的軟體、程式語言、工具等等。
    2. 作為能力考核的依據
    3. 整合所有公司內部的管理工具，如發票上傳、PO申請、報帳工具、打卡記錄等

快速入門:

    * 點擊總覽 -> 訓練網介紹（可以看到本網頁的所有的內容簡介
    * 點擊相關訓練內容 -> 開始練習
    * 點擊總覽 -> 學習進度裡面的進度報告（可以看到練習的成果）

（網頁內容的版權皆為Nexuni Co. 擁有）
'''
        }

    def render_inner(self):
        inner_html = '<div id="' + self.id + '" class="displayParagraph"><h3>' + self.value["title"] + '</h3><h4>' + markdown.markdown(self.value["content"]) + '</h4></div>'
        return inner_html
