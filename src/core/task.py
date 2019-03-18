from __future__ import absolute_import, unicode_literals
import logging
import functools
import threading
from django.http import HttpResponse
from libs import util
from libs import send_email
from libs import call_inception
from .models import (
    Usermessage,
    DatabaseList,
    Account,
    globalpermissions,
    SqlOrder,
    SqlRecord,
    grained,
    CloudOrder
)
CUSTOM_ERROR = logging.getLogger('Yearning.core.views')

dingding_url = ''
def grained_permissions(func):
    '''

    :argument 装饰器函数,校验细化权限。非法请求直接返回401交由前端判断状态码

    '''
    @functools.wraps(func)
    def wrapper(self, request, args=None):
        if request.method == "PUT" and args != 'connection':
            return func(self, request, args)
        else:
            if request.method == "GET":
                permissions_type = request.GET.get('permissions_type')
            else:
                permissions_type = request.data['permissions_type']
            user = grained.objects.filter(username=request.user).first()
            # if user is not None and user.permissions[permissions_type] == '1':
            if user is not None:
                return func(self, request, args)
            else:
                return HttpResponse(status=401)
    return wrapper


class order_push_message(object):

    '''

    :argument 同意执行工单调用该方法异步处理数据

    '''

    def __init__(self, addr_ip, workid, from_user, to_user):
        super().__init__()
        self.addr_ip = addr_ip
        self.order = CloudOrder.objects.filter(workid=workid).first()
        self.from_user = from_user
        self.to_user = to_user
        self.title = f'工单:{self.order.workid}审核通过通知'
        self.statue = 'normal'

    def run(self):
        self.agreed()

    def agreed(self):

        '''

        :argument 将执行的结果通过站内信,email,dingding 发送

        :param   self.from_user
                 self.to_user
                 self.title
                 self.order
                 self.addr_ip

        :return: none

        '''

        Usermessage.objects.get_or_create(
            from_user=self.from_user, time=util.date(),
            title=self.title, content='该工单已审核通过!', to_user=self.to_user,
            state='unread'
        )

        # content = DatabaseList.objects.filter(id=self.order.bundle_id).first()
        # mail = Account.objects.filter(username=self.to_user).first()
        # tag = globalpermissions.objects.filter(authorization='global').first()
        try:
            util.dingding(
                '# 【<font face=\"微软雅黑\">工单执行通知</font>】 \n #  \n <br>  \n  **工单编号:**  %s \n  \n  **发起人员:**  <font color=\"#000080\">%s</font><br /> \n \n  **审核人员:**  <font color=\"#000080\">%s</font><br /> \n \n **平台地址:**  http://%s \n  \n **工单备注:**  %s \n \n **执行状态:**  <font color=\"#38C759\">已同意</font><br />'
                % (self.order.workid, self.order.username, self.order.assigned, self.addr_ip, self.order.remark),
                url=dingding_url)
        except Exception as e:
            print(e)
            CUSTOM_ERROR.error(f'{e.__class__.__name__}--钉钉推送失败: {e}')

class order_result_message(object):

    '''

    :argument 同意执行工单调用该方法异步处理数据

    '''

    def __init__(self, addr_ip, workid, from_user, to_user):
        super().__init__()
        self.addr_ip = addr_ip
        self.order = CloudOrder.objects.filter(workid=workid).first()
        self.from_user = from_user
        self.to_user = to_user
        self.title = f'工单:{self.order.workid}执行完成通知'
        self.statue = 'normal'

    def run(self):
        self.agreed()

    def agreed(self):

        '''

        :argument 将执行的结果通过站内信,email,dingding 发送

        :param   self.from_user
                 self.to_user
                 self.title
                 self.order
                 self.addr_ip

        :return: none

        '''

        Usermessage.objects.get_or_create(
            from_user=self.from_user, time=util.date(),
            title=self.title, content='该工单已审核通过!', to_user=self.to_user,
            state='unread'
        )

        # content = DatabaseList.objects.filter(id=self.order.bundle_id).first()
        # mail = Account.objects.filter(username=self.to_user).first()
        # tag = globalpermissions.objects.filter(authorization='global').first()
        try:
            util.dingding(
                '# 【<font face=\"微软雅黑\">工单执行完成通知</font>】 \n #  \n <br>  \n  **工单编号:**  %s \n  \n  **发起人员:**  <font color=\"#000080\">%s</font><br /> \n \n  **审核人员:**  <font color=\"#000080\">%s</font><br /> \n \n **平台地址:**  http://%s \n  \n **工单备注:**  %s \n \n **执行状态:**  <font color=\"#38C759\">已执行</font><br /> \n \n **执行结果:**  <font color=\"#38C759\">正常</font><br /> '
                % (self.order.workid, self.order.username, self.order.assigned, self.addr_ip, self.order.remark),
                url=dingding_url)
        except Exception as e:
            print(e)
            CUSTOM_ERROR.error(f'{e.__class__.__name__}--钉钉推送失败: {e}')


class cancel_push_messages(threading.Thread):

    '''

    :argument 驳回工单调用该方法异步处理数据

    '''

    def __init__(self, _tmpData, to_user,from_user, addr_ip, text):
        super().__init__()
        self.to_user = to_user
        self.from_user = from_user
        self._tmpData = _tmpData
        self.addr_ip = addr_ip
        self.text = text

    def run(self):
        self.execute()

    def execute(self):

        '''

        :argument 更改该工单SqlOrder表中的status

        :param
                self._tmpData
                self.addr_ip
                self.text
                self.to_user

        :return: none

        '''
        # content = DatabaseList.objects.filter(id=self._tmpData['bundle_id']).first()
        # mail = Account.objects.filter(username=self.to_user).first()
        # tag = globalpermissions.objects.filter(authorization='global').first()
        # if tag is None or tag.dingding == 0:
        #     pass
        # else:
        try:
            # if content.url:
            util.dingding('# 【<font face=\"微软雅黑\">工单撤销通知</font>】 \n #  \n <br>  \n  **工单编号:**  %s \n  \n  **发起人员:**  <font color=\"#000080\">%s</font><br /> \n \n **审核人员:**  <font color=\"#000080\">%s</font><br /> \n \n **平台地址:**  http://%s \n  \n **撤销说明:**  %s \n \n **状态:**  <font color=\"#FF0000\">撤销</font>\n '
                                % (self._tmpData['workid'], self._tmpData['username'],self._tmpData['assigned'], self.addr_ip, self.text), url='https://oapi.dingtalk.com/robot/send?access_token=3c5909159e71b1472390a95b5100469aa5d88386962c100d63d0583401e7d90b')
        except Exception as e:
            print(e)
            CUSTOM_ERROR.error(f'{e.__class__.__name__}--钉钉推送失败: {e}')

class rejected_push_messages(threading.Thread):

    '''

    :argument 驳回工单调用该方法异步处理数据

    '''

    def __init__(self, _tmpData, to_user,from_user, addr_ip, text):
        super().__init__()
        self.to_user = to_user
        self.from_user = from_user
        self._tmpData = _tmpData
        self.addr_ip = addr_ip
        self.text = text

    def run(self):
        self.execute()

    def execute(self):

        '''

        :argument 更改该工单SqlOrder表中的status

        :param
                self._tmpData
                self.addr_ip
                self.text
                self.to_user

        :return: none

        '''
        # content = DatabaseList.objects.filter(id=self._tmpData['bundle_id']).first()
        # mail = Account.objects.filter(username=self.to_user).first()
        # tag = globalpermissions.objects.filter(authorization='global').first()
        # if tag is None or tag.dingding == 0:
        #     pass
        # else:
        try:
            # if content.url:
            util.dingding('# 【<font face=\"微软雅黑\">工单驳回通知</font>】 \n #  \n <br>  \n  **工单编号:**  %s \n  \n  **发起人员:**  <font color=\"#000080\">%s</font><br /> \n \n **审核人员:**  <font color=\"#000080\">%s</font><br /> \n \n **平台地址:**  http://%s \n  \n **驳回说明:**  %s \n \n **状态:**  <font color=\"#FF0000\">驳回</font>\n '
                                % (self._tmpData['workid'], self._tmpData['username'],self._tmpData['assigned'], self.addr_ip, self.text), url='https://oapi.dingtalk.com/robot/send?access_token=3c5909159e71b1472390a95b5100469aa5d88386962c100d63d0583401e7d90b')
        except Exception as e:
            print(e)
            CUSTOM_ERROR.error(f'{e.__class__.__name__}--钉钉推送失败: {e}')
        # if tag is None or tag.email == 0:
        #     pass
        # else:
        #     try:
        #         if mail.email:
        #             mess_info = {
        #                 'workid': self._tmpData['work_id'],
        #                 'to_user': self.to_user,
        #                 'addr': self.addr_ip,
        #                 'rejected': self.text}
        #             put_mess = send_email.send_email(to_addr=mail.email)
        #             put_mess.send_mail(mail_data=mess_info, type=1)
        #     except Exception as e:
        #         CUSTOM_ERROR.error(f'{e.__class__.__name__}--邮箱推送失败: {e}')

class edit_push_messages(object):

    '''

    :argument 提交工单调用该方法异步处理数据

    '''

    def __init__(self, workId, user,to_user, addr_ip, text, assigned, id):
        super().__init__()
        self.workId = workId
        self.user = user
        self.to_user = to_user
        self.addr_ip = addr_ip
        self.text = text
        self.assigned = assigned
        self.id = id

    def run(self):
        self.submit()

    def submit(self):
        '''

        :argument 更改该工单SqlOrder表中的status

        :param
                self.workId
                self.user
                self.addr_ip
                self.text
                self.assigned
                self.id
        :return: none

        '''
        content = DatabaseList.objects.filter(id=self.id).first()
        mail = Account.objects.filter(username=self.assigned).first()
        tag = globalpermissions.objects.filter(authorization='global').first()
        try:
            util.dingding(
                '# 【<font face=\"微软雅黑\">工单更新通知</font>】 \n #  \n <br>  \n  **工单编号:**  %s \n  \n  **提交人员:**  <font color=\"#000080\">%s</font><br /> \n \n **审核人员:**  <font color=\"#000080\">%s</font><br /> \n \n**平台地址:**  http://%s \n  \n **工单备注:**  %s \n \n **执行状态:**  <font color=\"#FF9900\">已提交</font><br /> \n \n **业务备注:** 测试'
                % (self.workId, self.user, self.to_user, self.addr_ip, self.text), url='https://oapi.dingtalk.com/robot/send?access_token=3c5909159e71b1472390a95b5100469aa5d88386962c100d63d0583401e7d90b')
        except Exception as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}--钉钉推送失败: {e}')
        # if tag is None or tag.dingding == 0:
        #     pass
        # else:
        #     if content.url:
        #         try:
        #             util.dingding('# 【<font face=\"微软雅黑\">工单提交通知</font>】 \n #  \n <br>  \n  **工单编号:**  %s \n  \n  **提交人员:**  <font color=\"#000080\">%s</font><br /> \n \n **审核人员:**  <font color=\"#000080\">%s</font><br /> \n \n**平台地址:**  http://%s \n  \n **工单备注:**  %s \n \n **执行状态:**  <font color=\"#FF9900\">已提交</font><br /> \n \n **业务备注:**  %s \n '
        #                         % (self.workId, self.user, self.to_user,self.addr_ip, self.text, content.before), url=content.url)
        #         except Exception as e:
        #             CUSTOM_ERROR.error(f'{e.__class__.__name__}--钉钉推送失败: {e}')
        if tag is None or tag.email == 0:
            pass
        else:
            if mail.email:
                mess_info = {
                    'workid': self.workId,
                    'to_user': self.user,
                    'addr': self.addr_ip,
                    'text': self.text,
                    'note': content.before}
                try:
                    put_mess = send_email.send_email(to_addr=mail.email)
                    put_mess.send_mail(mail_data=mess_info, type=2)
                except Exception as e:
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}--邮箱推送失败: {e}')

class submit_push_messages(object):

    '''

    :argument 提交工单调用该方法异步处理数据

    '''

    def __init__(self, workId, user,to_user, addr_ip, text, assigned, id):
        super().__init__()
        self.workId = workId
        self.user = user
        self.to_user = to_user
        self.addr_ip = addr_ip
        self.text = text
        self.assigned = assigned
        self.id = id

    def run(self):
        self.submit()

    def submit(self):
        '''

        :argument 更改该工单SqlOrder表中的status

        :param
                self.workId
                self.user
                self.addr_ip
                self.text
                self.assigned
                self.id
        :return: none

        '''
        content = DatabaseList.objects.filter(id=self.id).first()
        mail = Account.objects.filter(username=self.assigned).first()
        tag = globalpermissions.objects.filter(authorization='global').first()
        try:
            util.dingding(
                '# 【<font face=\"微软雅黑\">工单提交通知</font>】 \n #  \n <br>  \n  **工单编号:**  %s \n  \n  **提交人员:**  <font color=\"#000080\">%s</font><br /> \n \n **审核人员:**  <font color=\"#000080\">%s</font><br /> \n \n**平台地址:**  http://%s \n  \n **工单备注:**  %s \n \n **执行状态:**  <font color=\"#FF9900\">已提交</font><br /> \n \n **业务备注:** 测试'
                % (self.workId, self.user, self.to_user, self.addr_ip, self.text), url='https://oapi.dingtalk.com/robot/send?access_token=3c5909159e71b1472390a95b5100469aa5d88386962c100d63d0583401e7d90b')
        except Exception as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}--钉钉推送失败: {e}')
        # if tag is None or tag.dingding == 0:
        #     pass
        # else:
        #     if content.url:
        #         try:
        #             util.dingding('# 【<font face=\"微软雅黑\">工单提交通知</font>】 \n #  \n <br>  \n  **工单编号:**  %s \n  \n  **提交人员:**  <font color=\"#000080\">%s</font><br /> \n \n **审核人员:**  <font color=\"#000080\">%s</font><br /> \n \n**平台地址:**  http://%s \n  \n **工单备注:**  %s \n \n **执行状态:**  <font color=\"#FF9900\">已提交</font><br /> \n \n **业务备注:**  %s \n '
        #                         % (self.workId, self.user, self.to_user,self.addr_ip, self.text, content.before), url=content.url)
        #         except Exception as e:
        #             CUSTOM_ERROR.error(f'{e.__class__.__name__}--钉钉推送失败: {e}')
        if tag is None or tag.email == 0:
            pass
        else:
            if mail.email:
                mess_info = {
                    'workid': self.workId,
                    'to_user': self.user,
                    'addr': self.addr_ip,
                    'text': self.text,
                    'note': content.before}
                try:
                    put_mess = send_email.send_email(to_addr=mail.email)
                    put_mess.send_mail(mail_data=mess_info, type=2)
                except Exception as e:
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}--邮箱推送失败: {e}')
