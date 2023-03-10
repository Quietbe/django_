from django.shortcuts import render, HttpResponse

from book.models import BookInfo


# Create your views here.


def index(request):
    books = BookInfo.objects.all()

    context = {
        'books': books
    }

    return render(request, 'index.html', context)
    # return HttpResponse('index首页')

# ORM数据库操作
def mysql_s(request):
    #############################################新增数据#################################################

    BookInfo.objects.create(
        name='java',
        pub_data='2010-1-1'
    )

    #############################################修改（更新）数据#################################################

    # # 1.现查询数据
    # book = BookInfo.objects.get(id=1)
    # # 2. 直接修改示例的属性
    # book.readcount = 20
    # book.save()

    # 方法2  直接更新
    # filter 过滤
    BookInfo.objects.filter(id=1).update(
        readcount=100,
        commentcount=200
    )

    #############################################删除数据#################################################

    # ## 方法1
    # # 1.先查询出数据
    # book = BookInfo.objects.get(id=5)
    # # 2.调用删除方法
    # book.delete()

    ## 方法2
    BookInfo.objects.filter(id=6).delete()

    #############################################基本查询#################################################
    # get 得到某一个数据
    # all 获得所有的
    # count 个数

    # 返回一个对象
    book = BookInfo.objects.get(id=1)

    # 查询id 不存在的数据会抛出异常
    book = BookInfo.objects.get(id=100)
    """
    book.models.BookInfo.DoesNotExist: BookInfo matching query does not exist.
    """
    try:
        book = BookInfo.objects.get(id=100)
    # except Exception as e:
    #     pass
    except BookInfo.DoesNotExist:
        pass

    # count
    BookInfo.objects.all().count()
    # or
    BookInfo.objects.count()

    #############################################filter,get,exclude#################################################
    """
    filter        :筛选/过滤  返回n个结果  0/1/n
    get           :          返回一个接轨
    exclude       :  排除掉符合条件剩下的结果  相当与   not
    
    
    语法形式：
              以filter(字段名__运算符=值) 为例
    """

    # 查询编号为1的图书
    # exact 精准的 就是等于
    BookInfo.objects.get(id__exact=1)
    BookInfo.objects.get(id=1)

    BookInfo.objects.filter(id=1)
    BookInfo.objects.filter(id__exact=1)

    # 查询书名包含 ’湖‘ 的图书
    # contains  包含
    BookInfo.objects.filter(name__contains='湖')
    # 查询书名以 '部' 结尾的图书
    BookInfo.objects.filter(name__endswith='部')
    # 查询书名为空的图书
    BookInfo.objects.filter(name__isnull=True)
    # 查询编号为1或者3或者5的 图书
    BookInfo.objects.filter(id__in=[1, 3, 5])
    # 查询编号大于3的图书
    # gt 大于            great
    # gte  大于等于       equal
    # lt 小于            less than
    # lte 小于等于
    BookInfo.objects.filter(id__gt=3)

    # 查询书籍id不为3的图书
    BookInfo.objects.exclude(id=3)
    BookInfo.objects.exclude(id__exact=3)

    # 查询1980 年发布的图书
    BookInfo.objects.filter(pub_data__year='1980')

    # 查询1990年1月1日后发布的图书
    BookInfo.objects.filter(pub_data__gt='1990-1-1')

    ############################################# F #################################################

    # 两个属性怎么比较 F对象
    """
    F 对象的语法形式
    
    filter(字段名__运算符=F('字段名'))
    
    查询阅读量大于评论量的图书
    """
    from django.db.models import F
    # 查询阅读量大于评论量的图书
    BookInfo.objects.filter(readcount__gt=F('commentcount'))

    # 查询阅读量大于评论量2倍的图书
    BookInfo.objects.filter(readcount__gt=F('commentcount') * 2)

    ############################################# Q对象(了解) #################################################

    # 需要查询id大于2 并且 阅读量大于20的书籍
    # 方式1 filter().filter()
    BookInfo.objects.filter(id__gt=2).filter(readcount__gt=20)
    # 方式2
    # filter(条件，条件)
    BookInfo.objects.filter(id__gt=2, readcount__gt=20)

    # 需要查询id大于2 或者 阅读量大于20的书籍
    from django.db.models import Q
    """
    Q(字段名__运算符=值)
    或者  Q()|Q()
    并且  Q() & Q()
    not  ~Q()
    """
    ## 需要查询id大于2 或者 阅读量大于20的书籍
    BookInfo.objects.filter(Q(id__gt=2) | Q(readcount__gt=20))

    ## 查询书籍id不为3的
    BookInfo.objects.exclude(id=3)
    BookInfo.objects.filter(~Q(id=3))

    ############################################# 聚合函数（了解） #################################################

    """
    Sum,Max,Min,Avg,Count(个数)
    
    聚合函数需要使用 aggregate
    语法形式是： aggragte(Xxx('字段'))
    """
    # 当前数据的阅读总量
    from django.db.models import Sum, Max, Min, Avg, Count
    BookInfo.objects.aggregate(Sum('readcount'))

    ############################################# 排序 #################################################
    # 默认升序
    BookInfo.objects.all().order_by('readcount')
    # 降序
    BookInfo.objects.all().order_by('-readcount')

    ############################################# 关联查询 #################################################

    """
    书籍和人物的关系是   1 : n
    书籍 中没有任何关于人物的字段
    
    人物 中又关于书籍的字段 book 外键
    
    语法形式:
        通过书籍查询人物信息（  已知 主表数据，关联查询从表书籍）
        主表模型(实例对象).关联模型类名小写_set.all()
    
        通过人物查询书籍信息（ 已知 从表书籍，关联查询主表数据）
        从表模型(实例对象).外键
        
    
    查询书籍为1的所有人信息
    查询人物为1的书籍信息
    """

    # 查询书籍为1的所有人信息

    # 通过书籍 查询人物

    # # 1.查询书籍
    # book = BookInfo.objects.get(id=1)
    # # 2.根据实际关联人物信息
    # book.peopleinfo_set.all()
    BookInfo.objects.get(id=1).peopleinfo_set.all()

    # 查询人物为1的书籍信息
    from book.models import PeopleInfo
    # # 1.查询人物
    # person = PeopleInfo.objects.get(id=1)
    # # 2.根据人物关联查询书籍
    # person.book.name
    PeopleInfo.objects.get(id=1).book.name

    ############################################# 关联查询的筛选 #################################################

    """
    书籍和人物的关系是   1 : n
    书籍 中没有任何关于人物的字段

    人物 中又关于书籍的字段 book 外键

    语法形式:
        1--
        我们需要的是 书籍信息，已知的是 人物信息
        我们需要的是 主表数据，已知的是 从表信息
        
        filter(关联模型类小写__字段名__运算符=值)
        
        2--
        我们需要的是 人物信息，已知条件是 书籍信息
        我们需要的是 从表书籍，已知条件是 主表信息
        filter(外键__字段__运算符=值)
    “”“
    
    ”“”
    查询图书。要求图书人物为 ’郭靖‘
    查询图书，要求图书中的人物的描述包含”八“
    """
    # 查询图书。要求图书人物为 ’郭靖‘
    # 需要的是图书，条件是人物
    BookInfo.objects.filter(peopleinfo__name__exact='郭靖')
    # PeopleInfo.objects.get(name='郭靖').book

    # 查询图书，要求图书中的人物的描述包含”八“
    BookInfo.objects.filter(peopleinfo__description__contains='八')
    # PeopleInfo.objects.filter(description__contains='八')[0].book

    """
    查询书名为“天龙八部”的所有人物
    查询图书阅读量大于30的所有人物
    """
    # 查询书名为“天龙八部”的所有人物
    PeopleInfo.objects.filter(book__name='天龙八部')
    # 查询图书阅读量大于30的所有人物
    PeopleInfo.objects.filter(book__readcount__gt=50)


    ############################################# 查询集 #################################################
    ##   惰性、缓存
    # 每次都执行一次sql语句
    [book.id for book in BookInfo.objects.all()]

    # 优化 使用变量接收结果，保存在变量中
    books = BookInfo.objects.all()
    [book.id for book in books]

    ############################################# 分页 #################################################
    from django.core.paginator import Paginator

    # object_list   结果集/列表
    #  per_page     每页多少条记录
    #  p = Paginator(object_list,per_page)
    books = BookInfo.objects.all()
    p = Paginator(books, 2)
    # 获取第几页的数据   books_page 是一个列表 []
    books_page = p.page(1)
    books_page.object_list  #输出列表


