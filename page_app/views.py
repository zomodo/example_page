from django.shortcuts import render
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from page_app.models import Books

# Create your views here.

def index(request):
    return render(request,'page_app/index.html')

# Django内置分页
def pager1(request):
    book_list=Books.objects.all()
    current_page=request.GET.get('page','1')
    paginator = Paginator(book_list,10)

    """
    1.Paginator对象
    paginator.count   数据总数
    paginator.num_pages   总页数
    paginator.page_range   页码的列表
    
    2.books数据对象
    books.has_next()   是否有下一页
    books.next_page_number()   下一页的页码
    books.has_previous()   是否有上一页
    books.previous_page_number()   上一页的页码
    books.number      当前页
    books.object_list    当前页上所有对象的列表
    """

    try:
        books=paginator.page(current_page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数，返回第一页
        books=paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页
        books=paginator.page(paginator.num_pages)

    context={'books':books}
    return render(request, 'page_app/pager1.html', context)

# Django内置分页扩展
class CustomPaginator(Paginator):
    def __init__(self,current_page,per_page_num,*args,**kwargs):
        self.current_page=int(current_page)     # 当前页
        self.per_page_num=int(per_page_num)     # 显示的页数
        super(CustomPaginator, self).__init__(*args,**kwargs)

    def page_num_range(self):
        # self.num_pages  总页数
        # 页数特别少
        if self.num_pages <= self.per_page_num:
            return range(1,self.num_pages+1)
        # 页数特别多
        part=int(self.per_page_num/2)

        if self.current_page <= part:
            # 判断头部
            return range(1,self.per_page_num+1)
        elif self.current_page > (self.num_pages-part):
            # 判断尾部
            return range(self.num_pages-self.per_page_num+1,self.num_pages+1)
        else:
            # 剩余中间
            return range(self.current_page-part,self.current_page+part+1)

def pager2(request):
    book_list = Books.objects.all()
    current_page = request.GET.get('page','1')

    per_page_num = 7    # 显示的页数
    paginator = CustomPaginator(current_page,per_page_num,book_list,10)

    try:
        books = paginator.page(current_page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数，返回第一页
        books = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页
        books = paginator.page(paginator.num_pages)

    context = {'books': books}
    return render(request, 'page_app/pager2.html', context)

# 自定义分页组件
def pager3(request):
    from page_app.MyPaginator import Pagination

    book_list = Books.objects.all()
    book_count = book_list.count()
    current_page = request.GET.get('page','1')

    page_obj = Pagination(book_count,current_page)
    books = book_list[page_obj.start:page_obj.end]        # 切片

    context={'books':books,'page_obj':page_obj}
    return render(request, 'page_app/pager3.html',context)

# 自定义分页组件添加搜索结果分页功能
def search(request):
    from page_app.MyPaginator import Pagination

    if request.method=='POST':
        word=request.POST.get('word')
    else:
        word=request.GET.get('search')      # 翻页用GET取search字段

    book_list = Books.objects.filter(name__contains=word)
    if book_list:
        book_count = book_list.count()
        current_page = request.GET.get('page','1')

        page_obj = Pagination(book_count,current_page,search_word=word)
        books = book_list[page_obj.start:page_obj.end]        # 切片

        context={'books':books,'page_obj':page_obj}
        return render(request, 'page_app/pager3.html',context)
    else:
        return render(request,'page_app/pager3.html')
