#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

from urllib.parse import quote_plus as urlquote
import pymysql
from .default import Default
from redis import StrictRedis

class Develop( Default ):

    #设置开发模式；
    DEBUG = True

    SERVER_DOMAMIN = 'http://127.0.0.1:5050/'

    #密钥
    SECRET_KEY = 'uHUk98@#$598ujkij987!@3ffuckgirl#$kjiu'

    #设置上传文件大小；
    #如果设置为字节数， Flask 会拒绝内容长度大于此值的请求进入，并返回一个 413 状态码
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    #默认情况下 Flask 使用 ascii 编码来序列化对象。
    # 如果这个值被设置为 False ， Flask不会将其编码为 ASCII，并且按原样输出，返回它的 unicode 字符串。
    # 比如 jsonfiy 会自动地采用 utf-8 来编码它然后才进行传输。
    JSON_AS_ASCII = False

    ##SESSION
    #会话 cookie 的域。如果不设置这个值，则 cookie 对 SERVER_NAME 的全部子域名有效
    SESSION_COOKIE_DOMAIN = ''
    #会话 cookie 的路径。如果不设置这个值，且没有给 '/' 设置过，则 cookie 对 APPLICATION_ROOT 下的所有路径有效。
    SESSION_COOKIE_PATH = ''
    #控制 cookie 是否应被设置 httponly 的标志， 默认为 True
    SESSION_COOKIE_HTTPONLY = ''
    #控制 cookie 是否应被设置安全标志，默认为 False
    SESSION_COOKIE_SECURE = ''

    #以datetime.timedelta对象控制长期会话的生存时间。从 Flask 0.8 开始，也可以用整数来表示秒。
    PERMANENT_SESSION_LIFETIME = ''

    #这个标志控制永久会话如何刷新。如果被设置为 True （这是默认值），每一个请求 cookie 都会被刷新。如果设置为 False ，只有当 cookie 被修改后才会发送一个 set-cookie 的标头。非永久会话不会受到这个配置项的影响 。
    SESSION_REFRESH_EACH_REQUEST = ''

    #启用/禁用 x-sendfile
    USE_X_SENDFILE = ''

    #日志记录器的名称
    LOGGER_NAME = ''

    #服务器名和端口。需要这个选项来支持子域名 （例如： 'myapp.dev:5000' ）。
    # 注意 localhost 不支持子域名，所以把这个选项设置为 “localhost” 没有意义。
    # 设置 SERVER_NAME 默认会允许在没有请求上下文而仅有应用上下文时生成 URL
    #开发状态下关闭，否则请求页面一直会报404错误！2020-07-25
    #SERVER_NAME = ''

    #如果应用不占用完整的域名或子域名，这个选项可以被设置为应用所在的路径。
    # 这个路径也会用于会话 cookie 的路径值。如果直接使用域名，则留作 None
    APPLICATION_ROOT = ''

    #默认缓存控制的最大期限，以秒计，在flask.Flask.send_static_file()(默认的静态文件处理器)中使用。
    # 对于单个文件分别在 Flask或Blueprint上使用get_send_file_max_age()来覆盖这个值。默认为 43200（12小时）。
    SEND_FILE_MAX_AGE_DEFAULT = ''

    #如果这个值被设置为 True ，Flask不会执行 HTTP 异常的错误处理，而是像对待其它异常一样， 通过异常栈让它冒泡地抛出。这对于需要找出 HTTP 异常源头的可怕调试情形是有用的。
    TRAP_HTTP_EXCEPTIONS = ''

    #Werkzeug 处理请求中的特定数据的内部数据结构会抛出同样也是“错误的请求”异常的特殊的 key errors 。
    # 同样地，为了保持一致，许多操作可以显式地抛出 BadRequest 异常。
    # 因为在调试中，你希望准确地找出异常的原因，这个设置用于在这些情形下调试。如果这个值被设置为 True ，你只会得到常规的回溯。
    TRAP_BAD_REQUEST_ERRORS = ''

    #生成URL的时候如果没有可用的 URL 模式话将使用这个值。默认为 http
    PREFERRED_URL_SCHEME = ''

    #默认情况下 Flask 按照 JSON 对象的键的顺序来序来序列化它。
    # 这样做是为了确保键的顺序不会受到字典的哈希种子的影响，从而返回的值每次都是一致的，不会造成无用的额外 HTTP 缓存。
    # 你可以通过修改这个配置的值来覆盖默认的操作。
    # 但这是不被推荐的做法因为这个默认的行为可能会给你在性能的代价上带来改善。

    JSON_SORT_KEYS = ''

    #如果这个配置项被 True （默认值）， 如果不是 XMLHttpRequest 请求的话（由 X-Requested-With 标头控制） json 字符串的返回值会被漂亮地打印出来。
    JSONIFY_PRETTYPRINT_REGULAR = ''

    #Flask-SQLAlchemy
    #用于连接数据的数据库。例如：
    #sqlite:////tmp/test.dbmysql://username:password@server/db
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://blog:Blog123!@@127.0.0.1:3306/blog?charset=utf8'

    #一个映射绑定 (bind) 键到 SQLAlchemy 连接 URIs 的字典。 更多的信息请参阅 绑定多个数据库。
    SQLALCHEMY_BINDS = ''

    #如果设置成 True，SQLAlchemy 将会记录所有 发到标准输出(stderr)的语句，这对调试很有帮助。
    SQLALCHEMY_ECHO = False

    #可以用于显式地禁用或者启用查询记录。查询记录在调试或者测试模式下自动启用。更多信息请参阅 get_debug_queries()。
    SQLALCHEMY_RECORD_QUERIES = ''

    #可以用于显式地禁用支持原生的 unicode。这是 某些数据库适配器必须的（像在 Ubuntu 某些版本上的 PostgreSQL），当使用不合适的指定无编码的数据库默认值时。
    #SQLALCHEMY_NATIVE_UNICODE = ''

    #数据库连接池的大小。默认是数据库引擎的默认值 （通常是 5）。
    SQLALCHEMY_POOL_SIZE = 20

    #指定数据库连接池的超时时间。默认是 10。
    SQLALCHEMY_POOL_TIMEOUT	= 10

    #自动回收连接的秒数。这对 MySQL 是必须的，默认 情况下 MySQL 会自动移除闲置 8 小时或者以上的连接。
    # 需要注意地是如果使用 MySQL 的话， Flask-SQLAlchemy 会自动地设置这个值为 2 小时。
    SQLALCHEMY_POOL_RECYCLE = 60 * 60

    #控制在连接池达到最大值后可以创建的连接数。当这些额外的连接回收到连接池后将会被断开和抛弃。
    SQLALCHEMY_MAX_OVERFLOW = 1000

    #如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    LOG_PATH = 'E:/toranto/log/app.log'

    LOG_LEVEL = "DEBUG"

    REDIS_HOST = '127.0.0.1'

    REDIS_PORT = 6379

    REDIS_PWD = '123456'

    REDIS_EXPIRE = 60 * 20

    MYSQL_HOST = '127.0.0.1'

    MYSQL_PORT = 3306

    MYSQL_USER = ''

    MYSQL_PWD = ''

    MYSQL_DBNAME = ''

    MYSQL_CHARSET = 'utf8'

    MYSQL_CURSOR = pymysql.cursors.Cursor

    ORACLE_HOST = ''

    ORACLE_PORT = ''

    ORACLE_USER = ''

    ORACLE_PWD = ''

    ORACLE_SID = ''

    MONGO_HOST = ''

    MONGO_PORT = 27017

    MONGO_USER = ''

    MONGO_PWD = ''

    MONGOD_DBNAME = ''

    #COOKIE - 秒;
    COOKIE_MAX_AGE = 60 * 60

    SESSION_COOKIE_NAME = 'SESSION_ID'

    SESSION_COOKIE_DOMAIN = ''

    SESSION_COOKIE_PATH = '/'

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SECURE = False

    PERMANENT_SESSION_LIFETIME = 60 * 60

    SESSION_TYPE = 'redis'

    SESSION_REDIS = StrictRedis(host="127.0.0.1", port=6379,  password='123456', db=2)

    SESSION_PERMANENT = False

    SESSION_USE_SIGNER = True

    SESSION_KEY_PREFIX = ''

    PAGE_SIZE = 20

    PAGE_INDEX = 1


    #后台返回；
    RESPONSE_SUCCESS_CODE = 0
    RESPONSE_SUCCESS_MESSAGE = '恭喜，操作成功！'

    RESPONSE_ERROR_CODE = 1
    RESPONSE_ERROR_MESSAGE = '操作失败,请与管理员联系！'

    RESPONSE_PARAM_ERROR_CODE = 2
    RESPONSE_PARAM_ERROR_MESSAGE = '参数传递错误！'

    RESPONSE_UNAUTH_CODE = 3
    RESPONSE_UNAUTH_MESSAGE = '您访问的资源需要授权！'

    RESPONSE_UPLOAD_ERROR_CODE = 4
    RESPONSE_UPLOAD_ERROR_MESSAGE = '服务端读取上传文件失败！'

    RESPONSE_UPLOAD_NOT_ALLOW_CODE = 5
    RESPONSE_UPLOAD_NOT_ALLOW_MESSAGE = '上传文件格式不符合要求！'

    RESPONSE_SAVE_ERROR_CODE = 6
    RESPONSE_SAVE_ERROR_MESSAGE = '服务端保存文件失败！'

    RESPONSE_SAVE_SUCCESS = 7
    RESPONSE_SAVE_SUCCESS_MESSAGE = '上传成功！'

    #Ueditor配置
    IMAGE_UPLOAD_ACTION = ''
    IMAGE_PATH = ''
    IMAGE_FIELD_NAME = ''
    IMAGE_MAX_SIZE = 2048

    IMAGE_ALLOWED = ['.jpg', '.png', '.jpge', '.gif', '.bmp']

    FILE_ALLOWED = ['.zip', '.tar', '.gz', '.pdf', 'tgz', '.jpg', '.png', '.jpge', '.gif', '.bmp', '.doc', 'docx', '.xls', '.xlsx', '.sql', '.rpm', '.txt', 'phar']

    UPLOAD_PATH = "E:/toranto/upload"


    #article setting
    ARTICLE_PICTURE = None

    ARTICLE_CLICK = 1

    ARTICLE_SQ = 1

    ARTICLE_IS_TOP = '0'

    ARTICLE_IS_COMMENT = '1'

    ARTICLE_IS_TOOLBAR = '1'

    ARTICLE_PRAISE = 1

    ARTICLE_STEP = 1

    ARTICLE_PRICE = 99

    ARTICLE_PASSWORD = None

    ARTICLE_DESC = None

    ARTICLE_TAG = None

    ARTICLE_IS_VISIBLE = '1'

    ARTICLE_CATEGORY = 'Default'

    ARTICLE_SEO = 'make-you-fit'

    ARTICLE_AUTHOR = 'admin'

    ARTICLE_EXPIRE_DATE = '2100-01-01 00:00:00'

    ARTICLE_CONTENT = None

    ARTICLE_TITLE = None

    ARTICLE_IS_PUBLISH = '1'

    ARTICLE_ADD_SUCCESS_CODE = 8

    ARTICLE_ADD_SUCCESS_MESSAGE = '文章内容已提交成功！'

    ARTICLE_ADD_ERROR_CODE = 9

    ARTICLE_ADD_ERROR_MESSAGE = '文章提交失败！'

    ARTICLE_EDIT_SUCCESS_CODE = 10

    ARTICLE_EDIT_SUCCESS_MESSAGE = '文章编辑成功！'

    ARTICLE_EDIT_ERROR_CODE = 11

    ARTICLE_EDIT_ERROR_MESSAGE = '文章编辑失败！'

    ARTICLE_DELETE_SUCCESS_CODE = 12

    ARTICLE_DELETE_SUCCESS_MESSAGE = '文章删除成功！'

    ARTICLE_DELETE_ERROR_CODE = 13

    ARTICLE_DELETE_ERROR_MESSAGE = '文章删除失败！'

    PAGE_SIZE = 10

    MAX_PAGE = 10


    pass
