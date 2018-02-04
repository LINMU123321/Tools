# 未来改进方向：
# 	1. 增加自定义字符集功能；
#   2. 增加自定义宽度增幅值功能；
#   3. 分离字符画展示与图片缩略图展示, 缩略图不形变。
from tkinter import *
from tkinter import filedialog
import tkinter.scrolledtext as tkst
from PIL import ImageTk, Image


class ImgToCode:

    def __init__(self, img_url, heigth):
        self.heigh = heigth
        # self.codeLib = 'MNHQ$OC?7>!:-;.'#生成字符画所需的字符集
        self.codeLib = 'MNHQ$OC?7>!:-  '#生成字符画所需的字符集
        # self.codeLib = '''@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1}[]?-_+~>i!lI;:,"^`'. '''#生成字符画所需的字符集
        self.count = len(self.codeLib)
        print(img_url)
        self.image = Image.open(img_url)
        self.width, self.height = self.image.size

    def get_pic_w(self, h):
        w = float((self.width/self.height+1.35)) * float(h)
        return int(w)

    '''
    没事干了解装饰器才做这个，不然真是傻逼，费这么大功夫做些吃力的事，后面很容易解决，除了不好看。
    '''
    # def to_html(func):
    #     html_head = """
    #             <!DOCTYPE html>
    #             <html lang="en">
    #             <head>
    #                 <meta charset="UTF-8">
    #                 <title>字符画</title>
    #             </head>
    #             <body>
    #             <p style=text-align:center>"""
    #     html_nail = '</body></html>'
    #     @functools.wraps(func)
    #     def wrapper(piccode):
    #         code = func(piccode)
    #         code = ''.join(line + '<br/>' for line in code.splitlines())
    #         return html_head + code + html_nail
    #     return wrapper

    # @to_html
    @property
    def transform(self):
        img = self.image.resize((self.get_pic_w(self.heigh), self.heigh), Image.ANTIALIAS)  # 调整图片大小
        # Image._show(img)
        monochrome_img = img.convert('L')
        width, height = monochrome_img.size
        codePic = ''

        for h in range(0, height):  # size属性表示图片的分辨率，'0'为横向大小，'1'为纵向
            for w in range(0, width):
                gray = monochrome_img.getpixel((w, h))#返回指定位置的像素，如果所打开的图像是多层次的图片，那这个方法就返回一个元组
                codePic += self.codeLib[int(((self.count-1)*gray)/256)]#建立灰度与字符集的映射
                # print(codePic)
            codePic += '\n<br/>'
        return codePic

    @staticmethod
    def save_file(picstr, filename):
        html_trmplet = """<!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <title>字符画</title>
                        </head>
                        <body>
                        <p style=text-align:center>{}</p>
                        </body></html>"""

        with open(r'{}.html'.format(filename), 'w') as file:
            file.write(html_trmplet.format(picstr))
        with open(r'{}.txt'.format(filename), 'w') as file:
            file.write(picstr.replace('<br/>', ''))
        print('html file have been saved, plz check it.')


class GUI(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        # window = Tk()
        master.geometry("1024x720+500+500")
        master.title("字符画工具")
        master.resizable(True, True)
        self.pack()
        self.file_path = ''
        self.picstr = ''

        # 菜单栏
        menubar = Menu(master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.OpenFile)
        filemenu.add_command(label="Save", command=self.SaveFile)
        # filemenu.add_separator()#分割线
        filemenu.add_command(label="Exit", command=master.destroy)
        menubar.add_cascade(label="File", menu=filemenu)
        master.config(menu=menubar)

        # 做三个框架来容纳控件
        ## 在'master'上创建一个'frame'
        frm = Frame(master)
        frm.pack()
        frm_a = Frame(frm, height=480, width=360, bg='black')
        frm_b = Frame(frm, height=10, width=235)#, bg='blue'
        frm_c = Frame(frm, height=690, width=360)# , bg='red'
        # 这里是控制小的`frm`部件在大的`frm`的相对位置，此处`frm_l`就是在`frm`的左边，`frm_r`在`frm`的右边
        frm_a.pack(side=LEFT)
        frm_b.pack(anchor=SE)
        frm_c.pack(anchor=SE, fill='both', expand='yes')

        #初始化其他两个框架内的控件
        self.str = tkst.ScrolledText(frm_c, height=465, width=360)
        self.str.pack()
        master.update_idletasks()
        self.canvas = Canvas(frm_a, bg='white', width=355, height=475)
        self.canvas.pack(side=LEFT)

        # 控件属性名称：anchor；
        # 控件属性对应值：对齐方式，左对齐”w”，右对齐”e”，顶对齐”n”，底对齐”s”...
        # 控件属性值枚举：“n”, “s”, “w”, “e”, “nw”, “sw”, “se”, “ne”, “center” (默认为” center”)
        # 输入文本框
        # clear_str = Button(frm_b, text="清空文本", command=self.clearer)
        # clear_str["relief"] = 'ridge'
        # # clear_str.config(anchor=W,, padding=5)
        # clear_str.pack(side=RIGHT)
        self.input_height = Entry(frm_b, width=30)
        self.input_height.pack(side='left')
        self.contents = StringVar()
        self.contents.set("输入想要的字符画高度如：30")
        self.input_height["textvariable"] = self.contents
        # self.input_height.bind('<Key-Return>', self.insert_height)
        b1 = Button(frm_b, text="设置高度",  command=self.insert_height)
        b1["relief"] = 'ridge'
        b1.pack(side='right')

        mainloop()

    # 清除显示文本
    # def clearer(self):
    #     self.picstr = 'blank'
    #     print(self.picstr)
    #     self.str_show()

    def str_show(self):
        # 在右侧显示字符画结果
        # t = Text(frm_c, height=690, width=360)
        self.str.insert(INSERT, self.picstr.replace('<br/>', ''))
        # print(self.picstr)
        # self.str.update_idletasks()
        self.str.pack()
        # mainloop()

    def img_show(self, file_path):
        # 在左侧显示缩略图，变形的。
        image = Image.open(file_path) # self.OpenFile()
        img = image.resize((360, 480), Image.ANTIALIAS)
        # img = image.resize((self.get_pic_w(self.heigh), self.heigh), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=NW, image=photo)
        mainloop()

    #文件操作的对话框
    def OpenFile(self):
        self.file_path = filedialog.askopenfilename(title='打开文件', initialdir='.', filetypes=[('Images', '*.jpg *.bmp *.gif *.jfif'), ('All Files', '*')])
        self.img_show(self.file_path)

    def SaveFile(self):
        filename = filedialog.asksaveasfilename(title='保存字符画文件', initialdir='.', initialfile='字符画')
        ImgToCode.save_file(self.picstr, filename)
        #可调用OS模块保存

    def insert_height(self):
        var_height = self.contents.get()
        print(var_height)
        f = ImgToCode(self.file_path, int(var_height))
        self.picstr = f.transform
        self.str_show()
        # print(self.picstr.replace('<br/>', ''))


if __name__ == '__main__':
    window = Tk()
    my_app = GUI(master=window)


