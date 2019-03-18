import logging
import json
from libs import baseview, util, call_inception
from rest_framework.response import Response
from django.db.models import Count
from django.http import HttpResponse
from core.models import (
    SqlOrder,
    Usermessage,
    DatabaseList,
    SqlRecord,
    CloudOrder,
    onlineinfo_db,
    extendinfo_db,
    addnewpcinfo_db
)

from core.task import order_push_message,rejected_push_messages,cancel_push_messages, order_result_message

conf = util.conf_path()
addr_ip = conf.ipaddress
CUSTOM_ERROR = logging.getLogger('Yearning.core.views')


class audit(baseview.SuperUserpermissions):

    '''

    :argument 审核页面相关操作api接口

    '''

    def get(self, request, args: str=None):

        '''

        :argument 审核页面数据展示请求接口

        :param None

        :return 数据条数, 数据

        '''

        try:
            workid = request.GET.get('workid',None)
            page = request.GET.get('page')
            username = request.GET.get('username')
        except KeyError as e:
            print(e)
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
        else:
            try:
                if workid:
                    info = CloudOrder.objects.get(workid=workid)
                    if info.type == 0:
                        info = onlineinfo_db.objects.filter(workid=workid)
                        data = util.ser(info)
                    elif info.type == 2:
                        info = addnewpcinfo_db.objects.filter(workid=workid)
                        data = util.ser(info)
                    else:
                        info = extendinfo_db.objects.filter(workid=workid)
                        data = util.ser(info)
                    return Response({'data': data})
                else:
                    page_number = CloudOrder.objects.all().exclude(status=4).aggregate(alter_number=Count('id'))
                    start = (int(page) - 1) * 20
                    end = int(page) * 20
                    info = CloudOrder.objects.all().exclude(status=4).order_by('-date')[start:end]
                    data = util.ser(info)
                    return Response({'page': page_number, 'data': data})
            except Exception as e:
                print(e)
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)

    def put(self, request, args: str=None):

        '''

        :argument 工单确认执行,驳回,二次检测接口。

        :param category 根据获得的category值执行具体的操作逻辑

        :return 提交结果信息

        '''

        try:
            category = request.data['type']
        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
        else:
            if category == 0:
                try:
                    from_user = request.data['from_user']
                    to_user = request.data['to_user']
                    text = request.data['text']
                    workid = request.data['workid']
                    print(request.data)
                except KeyError as e:
                    print(e)
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return HttpResponse(status=500)
                else:
                    try:
                        CloudOrder.objects.filter(workid=workid).update(status=1)
                        _tmpData = CloudOrder.objects.filter(workid=workid).values(
                            'workid','username','assigned'
                        ).first()
                        title = '工单:' + _tmpData['workid'] + '驳回通知'
                        Usermessage.objects.get_or_create(
                            from_user=from_user,
                            time=util.date(),
                            title=title,
                            content=text,
                            to_user=to_user,
                            state='unread'
                        )
                        print('e')
                        rejected_push_messages(_tmpData, to_user,from_user, addr_ip, text).start()
                        return Response('操作成功，该请求已驳回！')
                    except Exception as e:
                        print(e)
                        CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                        return HttpResponse(status=500)
            elif category == 1:
                try:
                    from_user = request.data['from_user']
                    workid = request.data['workid']
                    to_user = 'admin'
                except KeyError as e:
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return HttpResponse(status=500)
                else:
                    try:
                        CloudOrder.objects.filter(workid=workid).update(status=2)
                        order_push_message(addr_ip, workid, from_user, to_user).run()
                        return Response('管理员已同意执行工单，请联系管理员查看具体进度')
                    except Exception as e:
                        print(e)
                        CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                        return HttpResponse(status=500)
            elif category == 6:
                try:
                    from_user = request.data['from_user']
                    workid = request.data['workid']
                    to_user = 'admin'
                except KeyError as e:
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return HttpResponse(status=500)
                else:
                    try:
                        CloudOrder.objects.filter(workid=workid).update(status=6)
                        order_result_message(addr_ip, workid, from_user, to_user).run()
                        return Response('管理员已执行完成工单')
                    except Exception as e:
                        print(e)
                        CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                        return HttpResponse(status=500)




class del_order(baseview.BaseView):

    '''

    :argument 审核页面工单删除操作请求api

    :param data_id 根据data_id['status'] 值执行相应的删除逻辑

    :return 删除结果信息

    '''

    def post(self, request, args: str = None):
        try:
            data_id = json.loads(request.data['id'])
        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
        else:
            try:
                for i in data_id:
                    if i['status'] == 1:
                        work_id = SqlOrder.objects.filter(id=i['id']).first()
                        SqlRecord.objects.filter(workid=work_id.work_id).delete()
                        SqlOrder.objects.filter(id=i['id']).delete()
                    else:
                        SqlOrder.objects.filter(id=i['id']).delete()
                return Response({'status': 'success', 'log':'工单数据删除成功!'})
            except Exception as e:
                return Response({'status': 'failed', 'log': '工单数据删除失败!'})