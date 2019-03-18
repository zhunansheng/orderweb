'''
 Create your models here.

'''
from django.db import models
from django.contrib.auth.models import AbstractUser
import ast


class JSONField(models.TextField):
    description = "Json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection, context):
        if not value:
            value = {}
        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_save(value)


class Account(AbstractUser):
    '''
    User table
    '''
    group = models.CharField(max_length=40)   #权限组 guest/admin
    department = models.CharField(max_length=40) #部门
    role = models.CharField(max_length=40, null=True)


class SqlDictionary(models.Model):   
    '''
    数据库字典表
    '''
    BaseName = models.CharField(max_length=100)  #库名
    TableName = models.CharField(max_length=100) #表名
    Field = models.CharField(max_length=100) #字段名
    Type = models.CharField(max_length=100) #类型
    Extra = models.TextField() #备注
    TableComment = models.CharField(max_length=100) #表备注
    Name = models.CharField(max_length=100, null=True) #连接名

    def __str__(self):
        return self.TableName


class SqlOrder(models.Model):
    '''
    工单提交表
    '''
    work_id = models.CharField(max_length=50, blank=True) #工单id
    username = models.CharField(max_length=50, blank=True) #账号
    status = models.IntegerField(blank=True) # 工单状态 0 disagree 1 agree 2 indeterminate 3 ongoing 4撤销
    type = models.SmallIntegerField(blank=True) #工单类型 0 DDL 1 DML
    backup = models.SmallIntegerField(blank=True)  # 工单是否备份 0 not backup 1 backup
    bundle_id = models.IntegerField(db_index=True, null=True) # Matching with Database_list id Field
    date = models.CharField(max_length=100, blank=True) # 提交日期
    basename = models.CharField(max_length=50, blank=True) #数据库名
    sql = models.TextField(blank=True) #sql语句
    text = models.CharField(max_length=100) # 工单备注
    assigned = models.CharField(max_length=50, blank=True)# 工单执行人

class CloudOrder(models.Model):
    '''
    工单提交表
    '''
    workid = models.CharField(max_length=50, blank=True) #工单id
    username = models.CharField(max_length=50, blank=True) #账号
    status = models.IntegerField(blank=True,null=True) # 工单状态 0 disagree 1 agree 2 indeterminate 3 ongoing 4撤销
    type = models.SmallIntegerField(blank=True) #工单类型 0 上线 1 扩容 2 新增服务器
    date = models.CharField(max_length=100, blank=True) # 提交日期
    remark = models.CharField(max_length=100) # 工单备注
    assigned = models.CharField(max_length=50, blank=True)# 工单执行人

class DatabaseList(models.Model):
    '''
    数据库连接信息表
    '''
    connection_name = models.CharField(max_length=50) #连接名
    computer_room = models.CharField(max_length=50) #机房
    ip = models.CharField(max_length=100) #ip地址
    username = models.CharField(max_length=150) #数据库用户名
    port = models.IntegerField() #端口
    password = models.CharField(max_length=50) #数据库密码
    before = models.TextField(null=True) #提交工单 钉钉webhook发送内容
    after = models.TextField(null=True)  #工单执行成功后 钉钉webhook发送内容
    url = models.TextField(blank=True)    #钉钉webhook url地址


class SqlRecord(models.Model):
    '''
    工单执行记录表
    '''
    date = models.CharField(max_length=50) #执行时间 下个版本可废弃
    state = models.CharField(max_length=100) #执行状态
    sql = models.TextField(blank=True) #
    area = models.CharField(max_length=50)#下个版本可废弃
    name = models.CharField(max_length=50)#下个版本可废弃
    base = models.CharField(max_length=50)#下个版本可废弃
    error = models.TextField(null=True)
    workid = models.CharField(max_length=50, null=True)
    person = models.CharField(max_length=50, null=True) #下个版本可废弃
    reviewer = models.CharField(max_length=50, null=True) #下个版本可废弃
    affectrow = models.CharField(max_length=100, null=True)
    sequence = models.CharField(max_length=50, null=True)
    backup_dbname = models.CharField(max_length=100, null=True) #下个版本可废弃
    execute_time = models.CharField(max_length=150, null=True)
    SQLSHA1 = models.TextField(null=True)


class Todolist(models.Model):
    '''
    todo info 
    '''
    username = models.CharField(max_length=50) #账户
    content = models.CharField(max_length=200) #内容


class Usermessage(models.Model):
    '''
    user  message
    '''
    to_user = models.CharField(max_length=50) #收信人
    from_user = models.CharField(max_length=50) #发件人
    content = models.TextField(max_length=500) #内容
    time = models.CharField(max_length=50) #发送时间
    state = models.CharField(max_length=10) #发送状态
    title = models.CharField(max_length=100) # 站内信标题



class gitinfo(models.Model):
    project = models.CharField(max_length=50, verbose_name="项目")
    project_item = models.CharField(max_length=50, verbose_name="子项目")
    progress_name = models.CharField(max_length=50, verbose_name="程序名")
    gitaddress = models.CharField(max_length=50, verbose_name="git地址")
    hostname = models.CharField(max_length=50, verbose_name="主机名")

class globalpermissions(models.Model):
    '''

    globalpermissions

    '''
    authorization = models.CharField(max_length=50, null=True, db_index=True)
    dingding = models.SmallIntegerField(default=0)
    email = models.SmallIntegerField(default=0)


class grained(models.Model):
    username = models.CharField(max_length=50,db_index=True)
    permissions = JSONField()


class onlineinfo_db(models.Model):
    workid = models.CharField(max_length=50, null=True)
    iteration_name = models.CharField(max_length=50, verbose_name="版本信息")
    env_name = models.CharField(max_length=50, verbose_name="环境")
    project_name = models.CharField(max_length=50, verbose_name="项目")
    upstart_time = models.CharField(max_length=50, verbose_name="上线时间")
    upbak_time = models.CharField(max_length=50, verbose_name="回退时间")
    versionvalue = models.CharField(max_length=50, verbose_name="升级版本")
    state_em = models.CharField(max_length=50, verbose_name="紧急程度")
    updesc = models.TextField(verbose_name="升级描述")
    sqlorder = models.TextField(verbose_name="sql审计工单")
    uporder = models.TextField(verbose_name="升级顺序")
    service = models.CharField(max_length=100, verbose_name="新增服务")
    staticversion = models.CharField(max_length=50, verbose_name="静态页面分支")
    config_properties = models.CharField(max_length=500, verbose_name="配置中心")
    addservice = models.CharField(max_length=500,null=True,blank=True, verbose_name="是否新增服务")
    assigned= models.CharField(max_length=100, verbose_name="指定审核人")
    progress_editor = models.CharField(max_length=200,verbose_name="开发人员")
    newserviceData = models.CharField(max_length=200,null=True, blank=True,verbose_name="开发人员")
    remark = models.CharField(max_length=500, verbose_name="其他事项")
    date = models.CharField(max_length=100, blank=True)
    owner = models.CharField(max_length=50, verbose_name="订单提交人")

class extendinfo_db(models.Model):
    workid = models.CharField(max_length=50, null=True)
    project_name = models.CharField(max_length=50, verbose_name="归属项目")
    env_name = models.CharField(max_length=50, verbose_name="环境")
    appname = models.CharField(max_length=50, verbose_name="应用名称")
    extend_type = models.CharField(max_length=50, verbose_name="类型")
    os_soft_need = models.CharField(max_length=50, verbose_name="系统软件要求")
    servernum = models.CharField(max_length=50, verbose_name="服务器数量")
    ghost_choice = models.CharField(max_length=50, verbose_name="是否克隆原配置")
    properties_change = models.CharField(max_length=50, verbose_name="新配置")
    assigned = models.CharField(max_length=50, verbose_name="指定审核人")
    remark = models.TextField(verbose_name="备注")
    opentime = models.CharField(max_length=100, verbose_name="开通时间")
    date = models.CharField(max_length=100, blank=True)
    owner = models.CharField(max_length=50, verbose_name="订单提交人")

class addnewpcinfo_db(models.Model):
    workid = models.CharField(max_length=50, null=True, verbose_name="工单号")
    date = models.CharField(max_length=100, blank=True, verbose_name="提交时间")
    project_name = models.CharField(max_length=50, verbose_name="归属项目")
    env_name = models.CharField(max_length=50, verbose_name="环境")
    appname = models.CharField(max_length=50, verbose_name="应用名称")
    newpc_type = models.CharField(max_length=50, verbose_name="类型")
    os_soft_need = models.CharField(max_length=50, verbose_name="系统软件要求")
    servernum = models.CharField(max_length=50, verbose_name="服务器数量")
    cpunum = models.CharField(max_length=50, verbose_name="cpu核数")
    mem = models.CharField(max_length=50, verbose_name="内存大小")
    OsDiskType = models.CharField(max_length=50, verbose_name="系统盘类型")
    OsDiskSize = models.CharField(max_length=50, verbose_name="系统盘大小")
    DataDiskSize = models.CharField(max_length=50, verbose_name="数据盘大小")
    jdk_version = models.CharField(max_length=50, verbose_name="jdk版本")
    https_choice = models.CharField(max_length=50, verbose_name="https是否需要")
    DataDiskType = models.CharField(max_length=50, verbose_name="数据盘类型")
    domain_choice = models.CharField(max_length=50, default='n', verbose_name="域名是否需要")
    domain = models.CharField(max_length=50, verbose_name="域名")
    jvm_properties = models.CharField(max_length=50, verbose_name="jvm配置参数")
    netbrand = models.CharField(max_length=50, verbose_name="网络带宽")
    assigned = models.CharField(max_length=50, verbose_name="指定审核人")
    remark = models.CharField(max_length=50, null=True, verbose_name="备注")
    owner = models.CharField(max_length=50, verbose_name="订单提交人")
    opentime = models.CharField(max_length=100, verbose_name="开通时间")

class modelist_db(models.Model):
    '''
    项目与git信息
    '''
    id = models.AutoField(primary_key=True)
    projectname = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"项目名")
    modename = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"子项目")
    servicename = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"应用名称")
    gitaddress = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"git地址")
    mavenpom = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"构建参数")
    java_version = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"java版本")
    jmx_port = models.IntegerField(blank=True,null=True, verbose_name=u"jmx端口")
    base_port = models.IntegerField(blank=True, null=True, verbose_name=u"网页端口")
    http_port = models.IntegerField(blank=True, null=True, verbose_name=u"网页端口")
    health_port = models.IntegerField(blank=True, null=True, verbose_name=u"健康检查端口")
    dubbo_port = models.IntegerField(blank=True, null=True, verbose_name=u"dubbo端口")
    remark = models.CharField(max_length=200, blank=True, null=True, verbose_name=u"备注")
    class Meta:
        db_table = 'modelist'

class attachmentinfo(models.Model):
    id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=200, blank=True, null=True, verbose_name="文件名")
    filepath = models.CharField(max_length=200, blank=True, null=True, verbose_name="文件路径")
    orderid = models.CharField(max_length=200, blank=True, null=True, verbose_name="订单id")
    oss_state = models.CharField(max_length=200, blank=True, null=True, verbose_name="oss上传状态，ready准备中，failed为上传异常，ok为完成")
    class Meta:
        db_table = 'attachmentinfo'