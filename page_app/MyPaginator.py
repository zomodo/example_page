# author:zomodo
# date:2020-03-24
# desc:自定义分页组件

class Pagination(object):
    def __init__(self,total_count,current_page,per_page=10,max_page_num=7,search_word=''):
        self.total_count=int(total_count)        # 数据总条数

        try:
            if int(current_page) < 1:            # 当前页
                self.current_page=1
            else:
                self.current_page=int(current_page)
        except Exception as e:
            self.current_page=1

        self.per_page=int(per_page)              # 每页的数据条数
        self.max_page_num=int(max_page_num)      # 显示的页面数

        if search_word.strip():                  # 搜索框内容
            self.search_word='search=%s&' %search_word
        else:
            self.search_word=''

    @property
    def start(self):
        return (self.current_page-1) * self.per_page

    @property
    def end(self):
        return self.current_page * self.per_page

    @property
    def num_pages(self):
        # 计算总页数
        val,mod=divmod(self.total_count,self.per_page)
        if mod==0:
            return val
        else:
            return val+1


    def page_num_range(self):
        # 页数特别少
        if self.num_pages <= self.max_page_num:
            return range(1,self.num_pages+1)
        # 页数特别多
        part=int(self.max_page_num/2)

        if self.current_page <= part:
            # 判断头部
            return range(1,self.max_page_num+1)
        elif self.current_page > (self.num_pages-part):
            # 判断尾部
            return range(self.num_pages-self.max_page_num+1,self.num_pages+1)
        else:
            # 剩余中间
            return range(self.current_page-part,self.current_page+part+1)

    def show_page(self):
        page_list=[]

        # 添加首页标签
        first="<li><a href='?%spage=1'>首页</a></li>" %(self.search_word)
        page_list.append(first)
        # 添加上一页标签
        if self.current_page == 1:
            pre=""
        else:
            pre="<li><a href='?%spage=%s'>上一页</a></li>" %(self.search_word,self.current_page-1)
        page_list.append(pre)
        # 添加中间页标签
        for page in self.page_num_range():
            if page == self.current_page:
                temp="<li class='active'><a href='?%spage=%s'>%s</a></li>" %(self.search_word,page,page)
            else:
                temp="<li><a href='?%spage=%s'>%s</a></li>" %(self.search_word,page,page)
            page_list.append(temp)
        # 添加下一页标签
        if self.current_page == self.num_pages:
            ne = ""
        else:
            ne = "<li><a href='?%spage=%s'>下一页</a></li>" %(self.search_word,self.current_page+1)
        page_list.append(ne)
        # 添加尾页标签
        end = "<li><a href='?%spage=%s'>尾页</a></li>" %(self.search_word,self.num_pages)
        page_list.append(end)

        return ''.join(page_list)   # 返回字符串