'''
url table
'''
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from core.api.sqldic import (
    adminpremisson,
    exportdoc,
    dictionary,
    downloadFile,
    downloaderrorLog
)
from core.api.user import (
    userinfo,
    generaluser,
    authgroup,
    ldapauth,
    login_auth,
    gitinfoview
)
from core.api.dashboard import (
    dashboard,
    messages
)
from core.api.managerdb import (
    management_db,
    push_permissions,
    dingding
)
from core.api.auditorder import (
    audit,
    del_order
)
from core.api.record import (
    record_order,
    order_detail
)
from core.api.sqlorder import sqlorder
from core.api.sqlorder import onlineorderview
from core.api.sqlorder import extendorderview
from core.api.sqlorder import addnewpcorderview
from core.api.sqlorder import gitlabinfoview
from core.api.sqlorder import sqllistinfoview
from core.api.sqlorder import cancelview
from core.api.sqlorder import modelistinfoview
from core.api.sqlorder import fileuploadview
from core.api.serachsql import search
from core.api.osc import osc_step
from core.api.myorder import order
from core.api.gensql import gen_sql
from core.api.general import addressing

urlpatterns = [
    url(r'^api/v1/userinfo/(.*)', userinfo.as_view()),
    url(r'^api/v1/gitinfo/(.*)', gitinfoview.as_view()),
    url(r'^api/v1/sqllistinfo/(.*)', sqllistinfoview.as_view()),
    url(r'^api/v1/modelistinfoview/(.*)', modelistinfoview.as_view()),
    url(r'^api/v1/gitlabinfo/(.*)', gitlabinfoview.as_view()),
    url(r'^api/v1/onlineorder/(.*)', onlineorderview.as_view()),
    url(r'^api/v1/cancelorder/(.*)', cancelview.as_view()),
    url(r'^api/v1/extendorder/(.*)', extendorderview.as_view()),
    url(r'^api/v1/addnewpcorder/(.*)', addnewpcorderview.as_view()),
    url(r'^api/v1/workorder/(.*)', addressing.as_view()),
    url(r'^api/v1/myorder', order.as_view()),
    url(r'^api/v1/gensql/(.*)', gen_sql.as_view()),
    url(r'^api/v1/management_sql', management_db.as_view()),
    url(r'^api/v1/audit_sql', audit.as_view()),
    url(r'^api/v1/sqldic/(.*)', dictionary.as_view()),
    url(r'^api/v1/auth_twice', authgroup.as_view()),
    url(r'^api/v1/sqlsyntax/(.*)', sqlorder.as_view()),
    url(r'^api/v1/adminsql/(.*)', adminpremisson.as_view()),
    url(r'^api/v1/record/(.*)', record_order.as_view()),
    url(r'^api/v1/homedata/(.*)', dashboard.as_view()),
    url(r'^api/v1/messages/(.*)', messages.as_view()),
    url(r'^api/v1/otheruser/(.*)', generaluser.as_view()),
    url(r'^api/v1/exportdocx/', exportdoc.as_view()),
    url(r'^api/v1/dingding', dingding.as_view()),
    url(r'^api/v1/detail', order_detail.as_view()),
    url(r'^api/v1/search', search.as_view()),
    url(r'^api/v1/ldapauth', ldapauth.as_view()),
    url(r'^api/v1/global_switch', push_permissions.as_view()),
    url(r'^api/v1/undoOrder', del_order.as_view()),
    url(r'^api/v1/osc/(.*)', osc_step.as_view()),
    url(r'^api/v1/download', downloadFile),
    url(r'^api/v1/fileupload/(.*)', fileuploadview.as_view()),
    url(r'^api-token-auth', login_auth.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
