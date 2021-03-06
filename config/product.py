#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

from .default import Default


class Product( Default ):

    # 设置开发模式；
    DEBUG = False

    # 密钥
    SECRET_KEY = 'LOP09()*opKL675rftghKJIU9876!@hj'

    # 设置上传文件大小；
    # 如果设置为字节数， Flask 会拒绝内容长度大于此值的请求进入，并返回一个 413 状态码
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # 默认情况下 Flask 使用 ascii 编码来序列化对象。
    # 如果这个值被设置为 False ， Flask不会将其编码为 ASCII，并且按原样输出，返回它的 unicode 字符串。
    # 比如 jsonfiy 会自动地采用 utf-8 来编码它然后才进行传输。
    JSON_AS_ASCII = False

    ##SESSION
    # 会话 cookie 的域。如果不设置这个值，则 cookie 对 SERVER_NAME 的全部子域名有效
    SESSION_COOKIE_DOMAIN = ''
    # 会话 cookie 的路径。如果不设置这个值，且没有给 '/' 设置过，则 cookie 对 APPLICATION_ROOT 下的所有路径有效。
    SESSION_COOKIE_PATH = ''
    # 控制 cookie 是否应被设置 httponly 的标志， 默认为 True
    SESSION_COOKIE_HTTPONLY = ''
    # 控制 cookie 是否应被设置安全标志，默认为 False
    SESSION_COOKIE_SECURE = ''

    # 以datetime.timedelta对象控制长期会话的生存时间。从 Flask 0.8 开始，也可以用整数来表示秒。
    PERMANENT_SESSION_LIFETIME = ''

    # 这个标志控制永久会话如何刷新。如果被设置为 True （这是默认值），每一个请求 cookie 都会被刷新。如果设置为 False ，只有当 cookie 被修改后才会发送一个 set-cookie 的标头。非永久会话不会受到这个配置项的影响 。
    SESSION_REFRESH_EACH_REQUEST = ''

    # 启用/禁用 x-sendfile
    USE_X_SENDFILE = ''

    # 日志记录器的名称
    LOGGER_NAME = ''

    # 服务器名和端口。需要这个选项来支持子域名 （例如： 'myapp.dev:5000' ）。
    # 注意 localhost 不支持子域名，所以把这个选项设置为 “localhost” 没有意义。
    # 设置 SERVER_NAME 默认会允许在没有请求上下文而仅有应用上下文时生成 URL
    # SERVER_NAME = ''

    # 如果应用不占用完整的域名或子域名，这个选项可以被设置为应用所在的路径。
    # 这个路径也会用于会话 cookie 的路径值。如果直接使用域名，则留作 None
    APPLICATION_ROOT = ''

    # 默认缓存控制的最大期限，以秒计，在flask.Flask.send_static_file()(默认的静态文件处理器)中使用。
    # 对于单个文件分别在 Flask或Blueprint上使用get_send_file_max_age()来覆盖这个值。默认为 43200（12小时）。
    SEND_FILE_MAX_AGE_DEFAULT = ''

    # 如果这个值被设置为 True ，Flask不会执行 HTTP 异常的错误处理，而是像对待其它异常一样， 通过异常栈让它冒泡地抛出。这对于需要找出 HTTP 异常源头的可怕调试情形是有用的。
    TRAP_HTTP_EXCEPTIONS = ''

    # Werkzeug 处理请求中的特定数据的内部数据结构会抛出同样也是“错误的请求”异常的特殊的 key errors 。
    # 同样地，为了保持一致，许多操作可以显式地抛出 BadRequest 异常。
    # 因为在调试中，你希望准确地找出异常的原因，这个设置用于在这些情形下调试。如果这个值被设置为 True ，你只会得到常规的回溯。
    TRAP_BAD_REQUEST_ERRORS = ''

    # 生成URL的时候如果没有可用的 URL 模式话将使用这个值。默认为 http
    PREFERRED_URL_SCHEME = ''

    # 默认情况下 Flask 按照 JSON 对象的键的顺序来序来序列化它。
    # 这样做是为了确保键的顺序不会受到字典的哈希种子的影响，从而返回的值每次都是一致的，不会造成无用的额外 HTTP 缓存。
    # 你可以通过修改这个配置的值来覆盖默认的操作。
    # 但这是不被推荐的做法因为这个默认的行为可能会给你在性能的代价上带来改善。

    JSON_SORT_KEYS = ''

    # 如果这个配置项被 True （默认值）， 如果不是 XMLHttpRequest 请求的话（由 X-Requested-With 标头控制） json 字符串的返回值会被漂亮地打印出来。
    JSONIFY_PRETTYPRINT_REGULAR = ''

    # Flask-SQLAlchemy
    # 用于连接数据的数据库。例如：
    # sqlite:////tmp/test.dbmysql://username:password@server/db
    SQLALCHEMY_DATABASE_URI = ''

    # 一个映射绑定 (bind) 键到 SQLAlchemy 连接 URIs 的字典。 更多的信息请参阅 绑定多个数据库。
    SQLALCHEMY_BINDS = ''

    # 如果设置成 True，SQLAlchemy 将会记录所有 发到标准输出(stderr)的语句，这对调试很有帮助。
    SQLALCHEMY_ECHO = ''

    # 可以用于显式地禁用或者启用查询记录。查询记录在调试或者测试模式下自动启用。更多信息请参阅 get_debug_queries()。
    SQLALCHEMY_RECORD_QUERIES = ''

    # 可以用于显式地禁用支持原生的 unicode。这是 某些数据库适配器必须的（像在 Ubuntu 某些版本上的 PostgreSQL），当使用不合适的指定无编码的数据库默认值时。
    #SQLALCHEMY_NATIVE_UNICODE = ''

    # 数据库连接池的大小。默认是数据库引擎的默认值 （通常是 5）。
    SQLALCHEMY_POOL_SIZE = 20

    # 指定数据库连接池的超时时间。默认是 10。
    SQLALCHEMY_POOL_TIMEOUT = 10

    # 自动回收连接的秒数。这对 MySQL 是必须的，默认 情况下 MySQL 会自动移除闲置 8 小时或者以上的连接。
    # 需要注意地是如果使用 MySQL 的话， Flask-SQLAlchemy 会自动地设置这个值为 2 小时。
    SQLALCHEMY_POOL_RECYCLE = 60 * 60

    # 控制在连接池达到最大值后可以创建的连接数。当这些额外的连接回收到连接池后将会被断开和抛弃。
    SQLALCHEMY_MAX_OVERFLOW = 1000

    # 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    LOG_PATH = '/var/log/blog/app.log'

    LOG_LEVEL = "DEBUG"

    #redis
    REDIS_HOST = '127.0.0.1'

    REDIS_PORT = 6379

    REDIS_PWD = 'RMS9{Main!@'

    REDIS_EXPIRE = 60 * 60

    #mysql
    MYSQL_HOST = ''

    MYSQL_PORT = 3306

    MYSQL_USER = ''

    MYSQL_PWD = ''

    MYSQL_DBNAME = ''

    MYSQL_CHARSET = ''

    MYSQL_CURSOR = ''

    #mongodb
    MONGO_HOST = ''

    MONGO_PORT = 27017

    MONGO_USER = ''

    MONGO_PWD = ''

    MONGOD_DBNAME = ''

    PAGE_SIZE = 20

    PAGE_INDEX = 1

    pass


