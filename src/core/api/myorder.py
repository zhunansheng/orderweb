import logging
from libs import baseview, util
from django.db.models import Count
from core.models import SqlOrder, CloudOrder
from django.http import HttpResponse
from rest_framework.response import Response
from raven.contrib.django.raven_compat.models import client

from django.db.models import Q
CUSTOM_ERROR = logging.getLogger('Yearning.core.views')
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



class order(baseview.BaseView):

    '''

    :argument 我的工单展示接口api

    '''

    def get(self, request, args: str=None):
        try:
            username = request.GET.get('user')
            page = request.GET.get('page')
            workid = request.GET.get('workid', None)
        except KeyError as e:
            client.captureException()
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
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
                    # if username == 'admin':
                    #     page_number = CloudOrder.objects.all().order_by('-date').aggregate(alter_number=Count('id'))
                    # else:
                    page_number = CloudOrder.objects.filter(username=username).aggregate(alter_number=Count('id'))
                    start = (int(page) - 1) * 20
                    end = int(page) * 20
                    # if username == 'admin':
                    #     info = CloudOrder.objects.all().order_by('-date')[start:end]
                    # else:
                    info = CloudOrder.objects.filter(username=username).order_by('-date')[start:end]
                    data = util.ser(info)
                    print(data)
                    return Response({'page': page_number, 'data': data})
            except Exception as e:
                client.captureException()
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)