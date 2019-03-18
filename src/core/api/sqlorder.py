#coding: utf-8
import logging
import json
import urllib
from libs import send_email
from libs import baseview
from libs import call_inception
from libs import util
from django.db.models import Count
from core.task import submit_push_messages,edit_push_messages,cancel_push_messages
from rest_framework.response import Response
from django.http import HttpResponse
from sqlalchemy import create_engine
from raven.contrib.django.raven_compat.models import client
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select,update
from sqlalchemy.schema import *
import os


from core.models import (
    DatabaseList,
    SqlOrder,
    Usermessage,
    Account,
    globalpermissions,
    onlineinfo_db,
    CloudOrder,
    extendinfo_db,
    addnewpcinfo_db,
    modelist_db,
    attachmentinfo
)
from settingConf import settings

iteration_list = {
    'upversion': '版本上线',
    'upemergency': '紧急上线',
    'upiteration': '迭代版本'
}
env_name_list = {
    'test': '测试环境',
    'pre': '预发布',
    'pro': '生产'
}


CUSTOM_ERROR = logging.getLogger('Yearning.core.views')

conf = util.conf_path()
addr_ip = conf.ipaddress

class cancelview(baseview.BaseView):
    def put(self, request, args: str = None):
        try:
            from_user = request.data['from_user']
            to_user = request.data['to_user']
            text = request.data['text']
            workid = request.data['workid']
            print(request.data)
        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
        else:
            try:
                CloudOrder.objects.filter(workid=workid).update(status=4)
                _tmpData = CloudOrder.objects.filter(workid=workid).values(
                    'workid', 'username', 'assigned'
                ).first()
                title = '工单:' + _tmpData['workid'] + '撤销通知'
                Usermessage.objects.get_or_create(
                    from_user=from_user,
                    time=util.date(),
                    title=title,
                    content=text,
                    to_user=to_user,
                    state='unread'
                )
                cancel_push_messages(_tmpData, to_user, from_user, addr_ip, text).start()
                return Response('操作成功，该请求已撤销！')
            except Exception as e:
                return Response({'status': 'failed', 'log': '发生错误！！'})

class addnewpcorderview(baseview.BaseView):
    '''

    :argument 手动模式工单提交相关接口api

    put   更新数据

    post 提交工单

    '''

    def put(self, request, args=None):
        try:
            data = json.loads(request.data['data'])
            user = request.data['user']
        except KeyError as e:
            client.captureException()
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
        else:
            try:
                info = addnewpcinfo_db.objects.get(workid=data['workid'])
                info.date = util.date()
                info.env_name = data['env_name']
                info.project_name = data['project_name']
                info.remark = data['remark']
                info.owner = user
                info.os_soft_need = str(data['os_soft_need']).replace('\'', '\"')
                info.opentime = data['opentime']
                info.appname = data['appname']
                info.assigned = data['assigned']
                info.newpc_type = data['newpc_type']
                info.servernum = data['servernum']
                info.cpunum = data['cpunum']
                info.mem = data['mem']
                info.OsDiskType = data['OsDiskType']
                info.OsDiskSize = data['OsDiskSize']
                info.DataDiskSize = data['DataDiskSize']
                info.domain = data['domain']
                info.jdk_version = data['jdk_version']
                info.jvm_properties = data['jvm_properties']
                info.netbrand = data['netbrand']
                info.domain_choice = data['domain_choice']
                info.https_choice = data['https_choice']
                info.DataDiskType = data['DataDiskType']
                info.save()

                c_info = CloudOrder.objects.get(workid=data['workid'])
                c_info.date = util.date()
                c_info.remark=data['remark']
                c_info.status = 3
                c_info.assigned=data['assigned']
                c_info.username=user
                c_info.save()
                edit_push_messages(
                    workId=data['workid'],
                    user=user,
                    to_user=data['assigned'],
                    id=1,
                    addr_ip=addr_ip,
                    assigned=data['assigned'],
                    text='更新'
                ).run()
                return Response('已提交，请等待管理员审核!')
            except Exception as e:
                logging.info(e)
                print(e)
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return Response({'status': '500'})

    def post(self, request, args=None):
        try:
            print(request.data)
            data = json.loads(request.data['data'])
            user = request.data['user']
        except KeyError as e:
            client.captureException()
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
        else:
            workId = util.workId()
            addnewpcinfo_db.objects.get_or_create(
                date=util.date(),
                workid=workId,
                env_name=data['env_name'],
                project_name=data['project_name'],
                remark=data['remark'],
                owner=user,
                os_soft_need=str(data['os_soft_need']).replace('\'', '\"'),
                opentime=data['opentime'],
                appname=data['appname'],
                assigned=data['assigned'],
                newpc_type = data['newpc_type'],
                servernum = data['servernum'],
                cpunum = data['cpunum'],
                mem = data['mem'],
                OsDiskType = data['OsDiskType'],
                OsDiskSize = data['OsDiskSize'],
                DataDiskSize = data['DataDiskSize'],
                domain = data['domain'],
                jdk_version = data['jdk_version'],
                jvm_properties = data['jvm_properties'],
                netbrand = data['netbrand'],
                https_choice = data['https_choice'],
                DataDiskType = data['DataDiskType']
            )
            CloudOrder.objects.get_or_create(
                date=util.date(),
                remark=data['remark'],
                type=2,
                status=3,
                username=user,
                assigned=data['assigned'],
                workid = workId
            )
            submit_push_messages(
                workId=workId,
                user=user,
                to_user=data['assigned'],
                id=1,
                addr_ip=addr_ip,
                assigned=data['assigned'],
                text='text'
            ).run()
            return Response('已提交，请等待管理员审核!')
            # try:

            # except Exception as e:
            #     print(e)
            #     CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            #     return HttpResponse(status=500)

class extendorderview(baseview.BaseView):
    '''

    :argument 手动模式工单提交相关接口api

    put   更新数据

    post 提交工单

    '''

    def put(self, request, args=None):
        try:
            data = json.loads(request.data['data'])
            user = request.data['user']
        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
        else:
            try:
                info = extendinfo_db.objects.get(workid=data['workid'])
                info.date = util.date()
                info.env_name = data['env_name']
                info.project_name = data['project_name']
                info.remark = data['remark']
                info.owner = user,
                info.extend_type = data['extend_type']
                info.ghost_choice = data['ghost_choice']
                info.os_soft_need = str(data['os_soft_need']).replace('\'', '\"')
                info.opentime = data['opentime']
                info.servernum = data['servernum']
                info.properties_change = data['properties_change']
                info.appname = data['appname']
                info.assigned = data['assigned']
                info.save()

                c_info = CloudOrder.objects.get(workid=data['workid'])
                c_info.date = util.date()
                c_info.status = 3
                c_info.remark=data['remark']
                c_info.assigned=data['assigned']
                c_info.username=user
                c_info.save()
                edit_push_messages(
                    workId=data['workid'],
                    user=user,
                    to_user=data['assigned'],
                    id=1,
                    addr_ip=addr_ip,
                    assigned=data['assigned'],
                    text='更新'
                ).run()
                return Response('已提交，请等待管理员审核!')
            except Exception as e:
                client.captureException()
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return Response({'status': '500'})

    def post(self, request, args=None):
        try:
            data = json.loads(request.data['data'])
            user = request.data['user']
        except KeyError as e:
            client.captureException()
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
        else:
            workId = util.workId()
            extendinfo_db.objects.get_or_create(
                date=util.date(),
                workid=workId,
                env_name=data['env_name'],
                project_name=data['project_name'],
                remark=data['remark'],
                owner=user,
                extend_type=data['extend_type'],
                ghost_choice=data['ghost_choice'],
                os_soft_need=str(data['os_soft_need']).replace('\'', '\"'),
                opentime=data['opentime'],
                servernum=data['servernum'],
                properties_change=data['properties_change'],
                appname=data['appname'],
                assigned=data['assigned']
            )
            CloudOrder.objects.get_or_create(
                date=util.date(),
                remark=data['remark'],
                type=1,
                status=3,
                username=user,
                assigned=data['assigned'],
                workid = workId
            )
            submit_push_messages(
                workId=workId,
                user=user,
                to_user=data['assigned'],
                id=1,
                addr_ip=addr_ip,
                assigned=data['assigned'],
                text='text'
            ).run()
            return Response('已提交，请等待管理员审核!')
            # try:

            # except Exception as e:
            #     print(e)
            #     CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            #     return HttpResponse(status=500)
class modelistinfoview(baseview.BaseView):
    def get(self, request, args: str = None):
        try:
            choice = request.GET.get('choice', None)
            page = request.GET.get('page', None)
            if choice == 'all':
                page_number = modelist_db.objects.all().aggregate(alter_number=Count('id'))
                start = (int(page) - 1) * 10
                end = int(page) * 10
                info = modelist_db.objects.all()[start:end]
                data = util.ser(info)
                return Response({'page': page_number, 'data': data})
            info = modelist_db.objects.all().values('projectname', 'modename', 'servicename','base_port','jmx_port','http_port','dubbo_port')
            temp_info = {}
            for d in info:
                if d['projectname'] not in temp_info.keys():
                    temp = {}
                    temp_info[d['projectname']] = []
                    temp[d['modename']] = []
                    temp[d['modename']].append(d['servicename'])
                    temp_info[d['projectname']].append(temp)
                else:
                    temp = {}
                    temp_list = []
                    for data in temp_info[d['projectname']]:
                        print(type(data.keys()))
                        temp_list.append(list(data.keys())[0])
                        if d['modename'] in data.keys():
                            data[d['modename']].append(d['servicename'])
                    if d['modename'] not in temp_list:
                        temp = {}
                        temp[d['modename']] = []
                        temp[d['modename']].append(d['servicename'])
                        temp_info[d['projectname']].append(temp)
            print(temp_info)
            return Response({'data': temp_info})
        except Exception as e:
            client.captureException()
    def put(self, request, args=None):
        try:
            print(request.data)
            data = request.data['data']
        except KeyError as e:
            print(e)
            client.captureException()
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
        else:
            try:
                mode_tmp = modelist_db.objects.get(id=data['id'])
                mode_tmp.projectname = data['projectname']
                mode_tmp.modename = data['modename']
                mode_tmp.servicename = data['servicename']
                mode_tmp.gitaddress = data['gitaddress']
                mode_tmp.mavenpom = data['mavenpom']
                mode_tmp.java_version = data['java_version']
                mode_tmp.base_port = data['base_port']
                mode_tmp.http_port = data['http_port']
                mode_tmp.dubbo_port = data['dubbo_port']
                mode_tmp.jmx_port = data['jmx_port']
                mode_tmp.remark = data['remark']
                mode_tmp.health_port = data['health_port']
                mode_tmp.save()
                return HttpResponse({'data':'success'})
            except Exception as e:
                print(e)
                client.captureException()
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)

    def delete(self, request, args=None):
        try:
            print(request.data)
            data = request.data['data']
        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
        else:
            try:
                modelist_db.objects.get(id=data['id']).delete()
                return HttpResponse({'data':'success'})
            except Exception as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)

class gitlabinfoview(baseview.BaseView):
    def get(self, request, args: str = None):
        try:
            url = conf.giturl
            token = conf.gittoken
            mode_dict = {}
            print(request.GET)
            try:
                with urllib.request.urlopen('%s/api/v3/projects?per_page=1000&private_token=%s' % (url, token)) as response:
                    content = json.loads(response.read())
                    for data in content:
                        mode_dict[data['ssh_url_to_repo']] = str(data['id'])
            except Exception as e:
                client.captureException()
                return Response({'data': 'error', 'log': e})
            modename = request.GET['modename']
            servicename = request.GET['servicename']
            env_name = request.GET['env_name']
        except KeyError as e:
            print(e)
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
        else:
            try:
                gitaddress_temp = modelist_db.objects.get(modename=modename, servicename=servicename).gitaddress
                id_temp = mode_dict[gitaddress_temp]
                print(id_temp)
                try:
                    branch_list = []
                    with urllib.request.urlopen(
                            '%s/api/v3/projects/%s/repository/branches?private_token=%s' % (
                            url, id_temp, token)) as response:
                        content = json.loads(response.read())
                        for data in content:
                            if env_name == 'pro':
                                if data['name'].startswith('release'):
                                    branch_list.append(data['name'])
                            if env_name == 'pre':
                                if data['name'].startswith(env_name):
                                    branch_list.append(data['name'])
                    branch_list.reverse()
                    return Response({'data': branch_list})
                except Exception as e:
                    client.captureException()
                    return Response({'data': 'error', 'log': '与gitlab服务器通信失败'})
            except Exception as e:
                client.captureException()
                return Response({'data': '[]'})
    def post(self, request, args: str = None):
        try:
            print(request.data)
            data = request.data['data']
        except KeyError as e:
            print(e)
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
        else:
            try:
                try:
                    info = modelist_db.objects.get(projectname=data['projectname'], modename=data['modename'],
                                                   servicename=data['servicename'])
                    info.gitaddress = data['gitaddress']
                    info.mavenpom = data['mavenpom']
                    info.remark = data['remark']
                    info.java_version = data['java_version']
                    info.save()
                    return Response({'data': 'ok', 'log': '修改成功'})
                except modelist_db.DoesNotExist as e:
                    client.captureException()
                    info = modelist_db(projectname=data['projectname'], modename=data['modename'],
                                       servicename=data['servicename'], gitaddress=data['gitaddress'],
                                       mavenpom=data['mavenpom'], remark=data['remark'], java_version=data['java_version'])
                    info.save()
                    return Response({'data': 'success'})
            except Exception as e:
                client.captureException()
                return Response({'data': 'error', 'log': '发生错误，字段缺少或者其它错误'})

class sqllistinfoview(baseview.BaseView):
    def get(self, request, args: str = None):
        try:
            db_engine = create_engine('mysql+mysqldb://%s:%s@%s:%s/%s' %(conf.sqlusername, conf.sqlpassword, conf.sqlurl, conf.sqlport, conf.sqldbname), echo=True)
            DBSession = sessionmaker(bind=db_engine)
            session = DBSession()
            sqlorderlist_temp = []
            sqlorderlist = session.execute('select work_id from core_sqlorder').fetchall()
            for data in sqlorderlist:
                temp = {}
                temp['value'] = data[0]
                temp['label'] = data[0]
                sqlorderlist_temp.append(temp)
            session.close()
            sqlorderlist_temp.reverse()
            return Response({'data': sqlorderlist_temp})
        except Exception as e:
            client.captureException()
            return Response({'data': 'error', 'log': '与sql审计平台数据库连接发生错误'})


class fileuploadview(baseview.BaseView):
    '''
    :文件上传接口
    '''
    def post(self, request, args: str = None):
        try:
            up_file = request.data['file']
            orderid = request.data['orderid']
        except KeyError as e:
            return Response({'status':'failed', 'log':'缺少必要参数'})
        else:
            try:
                base_dir = settings.BASE_DIR
                storage = base_dir + '/' + 'storage/' + str(orderid) + '/'
                try:
                    if not os.path.isfile(base_dir + '/' + 'storage/' + str(orderid)):
                        os.makedirs(base_dir + '/' + 'storage/' + str(orderid))
                except Exception as e:
                    pass
                new_file = storage + up_file.name

                with open(new_file, 'wb+') as destination:
                    for chunk in up_file.chunks():
                        destination.write(chunk)

                    destination.close()
                m = attachmentinfo(filename=up_file.name, filepath=storage, orderid=orderid)
                m.save()
                return Response({'status': 'success'})
            except Exception as e:
                return Response({'status': 'failed', 'log': '保存失败'})
    def get(self, request, args: str = None):
        try:
            orderid = request.GET['orderid']
        except KeyError as e:
            return Response({'status': 'failed', 'log': '缺少必要参数'})
        else:
            try:
                file_info =  attachmentinfo.objects.filter(orderid=orderid).values('filename', 'id')
                if len(file_info) > 0:
                    temp_list = []
                    for line in file_info:
                        temp_dict = {}
                        temp_dict['name'] = line['filename']
                        temp_dict['keyID'] = line['id']
                        temp_list.append(temp_dict)
                    return Response({'status': 'success', 'data': temp_list})
                else:
                    return Response({'status': 'failed', 'log': 'empty'})
            except Exception as e:
                return Response({'status': 'failed', 'log': '查询发生异常'})



class onlineorderview(baseview.BaseView):
    '''

    :argument 手动模式工单提交相关接口api

    put   美化sql  测试sql

    post 提交工单

    '''

    def put(self, request, args=None):
        try:
            print(request.data)
            data = json.loads(request.data['data'])
            uporder = request.data['uporder']
            config_properties = request.data['config_properties']
            newserviceData = request.data['newserviceData']
            user = request.data['user']
        except KeyError as e:
            client.captureException()
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
        else:
            try:
                info = onlineinfo_db.objects.get(workid=data['workid'])
                info.iteration_name=data['iteration_name']
                info.date=util.date()
                info.env_name=data['env_name']
                info.project_name=data['project_name']
                info.upstart_time=data['upstart_time']
                info.upbak_time=data['upbak_time']
                info.versionvalue=data['versionvalue']
                info.state_em=data['state_em']
                info.updesc=data['updesc']
                info.sqlorder=str(data['sqlorder']).replace('\'', '\"')
                info.service=data['service']
                info.config_properties=config_properties
                info.progress_editor=data['progress_editor']
                info.owner = user
                info.uporder = uporder
                info.remark = data['remark']
                info.newserviceData = newserviceData
                info.addservice = data['addservice']
                info.assigned=data['assigned']
                info.save()

                c_info = CloudOrder.objects.get(workid=data['workid'])
                c_info.date = util.date()
                c_info.remark=data['project_name'] + '_' + env_name_list[data['env_name']] + '_' + iteration_list[data['iteration_name']]
                c_info.assigned=data['assigned']
                c_info.username=user
                c_info.status = 3
                c_info.save()
                edit_push_messages(
                    workId=data['workid'],
                    user=user,
                    to_user=data['assigned'],
                    id=1,
                    addr_ip=addr_ip,
                    assigned=data['assigned'],
                    text='更新'
                ).run()
                return Response('已提交，请等待管理员审核!')
            except Exception as e:
                client.captureException()
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return Response({'status': '500'})

    def post(self, request, args=None):
        try:
            print(request.data)
            newserviceData = request.data['newserviceData']
            data = json.loads(request.data['data'])
            uporder = request.data['uporder']
            config_properties = request.data['config_properties']
            user = request.data['user']
        except KeyError as e:
            client.captureException()
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
        else:
            try:
                workId = util.workId()
                onlineinfo_db.objects.get_or_create(
                    iteration_name=data['iteration_name'],
                    date=util.date(),
                    workid=workId,
                    env_name=data['env_name'],
                    project_name=data['project_name'],
                    upstart_time=data['upstart_time'],
                    upbak_time=data['upbak_time'],
                    versionvalue=data['versionvalue'],
                    newserviceData=newserviceData,
                    state_em=data['state_em'],
                    updesc=data['updesc'],
                    sqlorder=str(data['sqlorder']).replace('\'', '\"'),
                    uporder=uporder,
                    addservice=data['addservice'],
                    config_properties=config_properties,
                    progress_editor=data['progress_editor'],
                    remark=data['remark'],
                    owner=user,
                    assigned=data['assigned']
                )
                CloudOrder.objects.get_or_create(
                    date=util.date(),
                    remark=data['project_name'] + '_' + env_name_list[data['env_name']] + '_' + iteration_list[data['iteration_name']],
                    type=0,
                    status=3,
                    username=user,
                    assigned=data['assigned'],
                    workid=workId
                )
                submit_push_messages(
                    workId=workId,
                    user=user,
                    to_user=data['assigned'],
                    id=1,
                    addr_ip=addr_ip,
                    assigned=data['assigned'],
                    text='text'
                ).run()
                return Response({'status': 'success','orderid': workId})
            except Exception as e:
                client.captureException()
                return Response({'status': 'error', 'log': '后端保存失败'})
            # try:

            # except Exception as e:
            #     print(e)
            #     CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            #     return HttpResponse(status=500)

class sqlorder(baseview.BaseView):
    '''

    :argument 手动模式工单提交相关接口api

    put   美化sql  测试sql

    post 提交工单

    '''

    def put(self, request, args=None):
        if args == 'beautify':
            try:
                data = request.data['data']
            except KeyError as e:
                client.captureException()
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            else:
                try:
                    res = call_inception.Inception.BeautifySQL(sql=data)
                    return HttpResponse(res)
                except Exception as e:
                    client.captureException()
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return HttpResponse(status=500)

        elif args == 'test':
            try:
                id = request.data['id']
                base = request.data['base']
                sql = request.data['sql']
                sql = str(sql).strip('\n').strip().rstrip(';')
                data = DatabaseList.objects.filter(id=id).first()
                info = {
                    'host': data.ip,
                    'user': data.username,
                    'password': data.password,
                    'db': base,
                    'port': data.port
                    }
            except KeyError as e:
                client.captureException()
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            else:
                try:
                    with call_inception.Inception(LoginDic=info) as test:
                        res = test.Check(sql=sql)
                        return Response({'result': res, 'status': 200})
                except Exception as e:
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return Response({'status': '500'})

    def post(self, request, args=None):
        try:
            data = json.loads(request.data['data'])
            tmp = json.loads(request.data['sql'])
            user = request.data['user']
            type = request.data['type']
            id = request.data['id']
        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
        else:
            try:
                x = [x.rstrip(';') for x in tmp]
                sql = ';'.join(x)
                sql = sql.strip(' ').rstrip(';')
                workId = util.workId()
                SqlOrder.objects.get_or_create(
                    username=user,
                    date=util.date(),
                    work_id=workId,
                    status=2,
                    basename=data['basename'],
                    sql=sql,
                    type=type,
                    text=data['text'],
                    backup=data['backup'],
                    bundle_id=id,
                    assigned=data['assigned']
                    )
                submit_push_messages(
                    workId=workId,
                    user=user,
                    addr_ip=addr_ip,
                    text=data['text'],
                    assigned=data['assigned'],
                    id=id
                ).run()
                return Response('已提交，请等待管理员审核!')
            except Exception as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)