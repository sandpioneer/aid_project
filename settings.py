# settings.py
# 设置

PUBLIC_DIR = r'D:\test\\'

# PUBLIC_DIR = r'D:\CloudMusic\\'
DOWNLOAD = r'D:\w\d\\'

# 最大传送块
MAX_TRANSFER_BLOCK = 4096 * 300

# 命令分割符
CMD_SPLIT = '#*#'

# 服务器地址
HOST = '127.0.0.1'
PORT = 10086
SERVER_ADDR = (HOST, PORT)

# 测试连接使用的账号密码 
TEST_CONNECT_USR = 'admin'
TEST_CONNECT_USRPWD = 'admin'

# 自定义命令
# 登录命令，这里必须是大写，输入或者传递的时候不限制大小写
LOGIN = 'LOGIN'
# 退出命令
LOGOUT = 'LOGOUT'
# 注册命令
REG = 'REG'
# 下载文件
DOWN = 'DOWN'
#上传文件
UPLOAD = 'LOAD'
#显示服务器文件列表
LIST = 'LIST'
# 忽略
IGNORE = 'IGNORE'

# 服务器响应状态
SUCCESS = '1'
FAILED = '0'

# 文件发送结束标志
FILE_END_TAG = '###'

# 睡眠时间
SLEEP_TIME = 0.05

# 标准命令格式，区分客户端向服务器发送和服务器做出响应
# 客户端向服务器发送
# CMD_NAME [CMD_SPLIT PARAMETER]
# CMD[0] = CMD_NAME
# CMD[1-N] = PARAMETER

# 具体格式
# 说明：
#   USER: 指的是用户输入的格式
#   APPOINT: 指的是发送命令时约定的格式
#   
# 登录命令LOGIN
# USER: LOGIN USERNAME USERPWD
# APPOINT: LOGIN CMD_SPLIT USERNAME CMD_SPPLIT USERPWD
# CMD[0] = LOGIN ;  CMD[1] = USERNAME ; CMD[2] = USERPWD
# 
# 注册命令 REG
# REG
# USER: REG USERNAME USERPWD
# APPOINT: REG CMD_SPLIT USERNAME CMD_SPLIT USERPWD
# CMD[0] = REG ; CMD[1] = USERNAME ; CMD[2] = USERPWD
# 
# 获取文件列表命令 LIST
# 解释: LIST 不带参数表示，获取根目录下文件列表； 带有参数表示获取指定目录下文件列表
# USER: LIST [PARAMETER]
# APPOINT: LIST [CMD_SPLIT PARAMETER]
# 
# 下载文件命令 DOWN
# USER: DOWN FILENAME
# APPOINT: DOWN CMD_SPLIT FILENAME  
# CMD[0] = DOWN ; CMD[1] = FILENAME
# 服务器确认下载返回格式
# STATUS FILENAME FILESIZE
# 服务器返回文件数据时不再含有STATUS，直接是文件数据
# 
# 上传文件命令 UPLOAD
# USER: UPLOAD FILENAME
# APPOINT: UPLOAD CMD_SPLIT FILENAME
# CMD[0] = UPLOAD ; CMD[1] = FILENAME
# 服务器确认返回数据格式
# STATUS FILENAME
# 
# 服务器响应格式
# STATUS CMD_SPLIT RESPONSE_BODY
# 例如：
# 客户端发送登录请求，服务器回应
# 登录成功返回：SUCCESS CMD_SPLIT MSG
# 登录失败返回：FAILED CMD_SPLIT MSG
# MSG 表示提示消息