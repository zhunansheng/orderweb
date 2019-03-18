<style lang="less">
  @import '../../styles/common.less';
  @import '../Order/components/table.less';
</style>
<template>
  <div>
    <Col span="24" class="padding-left-10">
      <Card>
        <p slot="title">
          <Icon type="ios-crop-strong"></Icon>
          gitlab版本配置列表
        </p>
        <div class="edittable-con-1">
          <Table border :columns="columns6" :data="data5" stripe height="550"></Table>
        </div>
        <br>
        <Page :total="pagenumber" show-elevator @on-change="currentpage" :page-size="15"></Page>
      </Card>
    </Col>

    <Modal v-model="editPasswordModal" :closable='false' :mask-closable=false :width="500">
      <Card>
        <p slot="title">
          <Icon type="load-b"></Icon>
          添加gitlab版本信息
        </p>
        <div class="edittable-testauto-con">
          <Form :model="gitinfo" :label-width="80" ref="gitinfova" :rules="gitinfoValidate">
            <FormItem label="项目" prop="username">
              <Input v-model="gitinfo.project" placeholder="请输入"></Input>
            </FormItem>
            <FormItem label="子项目" prop="password">
              <Input v-model="gitinfo.project_item" placeholder="请输入"></Input>
            </FormItem>
            <FormItem label="程序名" prop="confirmpassword">
              <Input v-model="gitinfo.programe_name" placeholder="请输入"></Input>
            </FormItem>
            <FormItem label="仓库" prop="department">
              <Input v-model="gitinfo.gitaddress" placeholder="请输入"></Input>
            </FormItem>
            <FormItem label="hostname" prop="department">
              <Input v-model="gitinfo.hostname" placeholder="请输入"></Input>
            </FormItem>
            <Button type="primary" @click.native="Registered" style="margin-left: 35%">保存</Button>
          </Form>
        </div>
      </Card>
      <div slot="footer">
        <Button type="text" @click="cancelEditPass">取消</Button>
        <Button type="primary" @click="saveEditPass" :loading="savePassLoading">保存</Button>
      </div>
    </Modal>



    <Modal v-model="deluserModal" :closable='false' :mask-closable=false :width="500">
      <h3 slot="header" style="color:#2D8CF0">删除用户</h3>
      <Form :label-width="100" label-position="right">
        <FormItem label="用户名">
          <Input v-model="username" readonly="readonly"></Input>
        </FormItem>
        <FormItem label="请输入用户名">
          <Input v-model="confirmuser" placeholder="请确认用户名"></Input>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button type="text" @click="cancelDelInfo">取消</Button>
        <Button type="warning" @click="delUser">删除</Button>
      </div>
    </Modal>

    <Modal v-model="editemail" :closable='false' :mask-closable=false :width="500">
      <h3 slot="header" style="color:#2D8CF0">更改email邮箱</h3>
      <Form :label-width="100" label-position="right">
        <FormItem label="E-mail">
          <Input v-model="email"></Input>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button type="text" @click="editemail=false">取消</Button>
        <Button type="warning" @click="putemail">更改</Button>
      </div>
    </Modal>
  </div>
</template>
<script>
  import axios from 'axios'
  import '../../assets/tablesmargintop.css'
  import util from '../../libs/util'
  export default {
    data () {
      return {
        percent: 0,
        permission: {
          ddl: '0',
          ddlcon: [],
          dml: '0',
          dmlcon: [],
          dic: '0',
          diccon: [],
          dicedit: '0',
          dicexport: '0',
          index: '0',
          indexcon: [],
          query: '0',
          querycon: [],
          user: '0',
          base: '0'
        },
        con: [],
        columns6: [
          {
        title: '编号',
        type: 'index',
        width: 100,
        align: 'center'
    },
          {
            title: '项目',
            key: 'projectname'
          },
          {
            title: '模块名称',
            key: 'modename'
          },
          {
            title: '服务名',
            width: 300,
            key: 'servicename'
          },
          {
            title: 'git-ssh地址',
            width: 300,
            key: 'gitaddress'
          },
          {
            title: 'maven打包命令',
            width: 360,
            key: 'mavenpom'
          },
          {
            title: 'java版本',
            key: 'java_version'
          },
          {
            title: '备注',
            key: 'remark'
          },
          {
            title: '操作',
            key: 'action',
            width: 150,
            align: 'center',
            render: (h, params) => {
                return h('div', [
                  h('Button', {
                    props: {
                      type: 'primary',
                      size: 'small'
                    },
                    style: {
                      marginRight: '5px'
                    },
                    on: {
                      click: () => {
                        console.info(params.index)
                      }
                    }
                  }, '修改'),
                  h('Button', {
                    props: {
                      type: 'warning',
                      size: 'small'
                    },
                    on: {
                      click: () => {
                        console.info(params.index)
                      }
                    }
                  }, '删除')
                ])
              }
          }
        ],
        data5: [],
        pagenumber: 1,
        gitinfo: {
          project: '',
          project_item: '',
          programe_name: '',
          gitaddress: '',
          hostname: ''
        },
        gitinfoValidate: {
          project: [{
            required: true,
            message: '请输入用户名',
            trigger: 'blur'
          }],
          project_item: [{
            required: true,
            message: '子项目',
            trigger: 'blur'
          }
          ],
          progress_name: [{
            required: true,
            message: '程序名',
            trigger: 'blur'
          }],
          gitaddress: [{
            required: true,
            message: '请输入git仓库地址',
            trigger: 'blur'
          }],
          hostname: [{
            required: true,
            message: '请输入hostname',
            trigger: 'blur'
          }]
        },
        // 更改密码遮罩层状态
        editPasswordModal: false,
        // 更改密码
        editPasswordForm: {
          oldPass: '',
          newPass: '',
          rePass: ''
        },
        // 保存更改密码loding按钮状态
        savePassLoading: false,
        // 更改密码表单验证规则
        // 更改部门及权限
        editInfodForm: {
          group: '',
          department: ''
        },
        // 更改部门及权限遮罩层状态
        editInfodModal: false,
        editemail: false,
        email: '',
        // 用户名
        username: '',
        confirmuser: '',
        deluserModal: false,
        userid: null,
        dicadd: []
      }
    },
    methods: {
      edituser (index) {
        this.editPasswordModal = true
        this.username = this.data5[index].username
      },
      editgroup (index) {
        this.editInfodModal = true
        this.userid = this.data5[index].id
        this.username = this.data5[index].username
        this.editInfodForm.department = this.data5[index].department
        this.editInfodForm.group = this.data5[index].group
        axios.get(`${util.url}/userinfo/permissions?user=${this.username}`)
          .then(res => {
            this.permission = res.data
          })
      },
      currentpage (vl = 1) {
        axios.get(`${util.url}/modelistinfoview/?choice=all&page=${vl}`)
          .then(res => {
            this.data5 = res.data.data
            this.page_number = parseInt(res.data.page.alter_number)
          })
          .catch(error => {
            util.ajanxerrorcode(this, error)
          })
      },
      deleteUser (index) {
        this.deluserModal = true
        this.username = this.data5[index].username
      },
      editEmail (index) {
        this.editemail = true
        this.username = this.data5[index].username
        this.email = this.data5[index].email
      },
      putemail () {
        axios.put(`${util.url}/userinfo/changemail`, {
          'username': this.username,
          'mail': this.email
        })
          .then(res => {
            this.$Notice.success({
              title: res.data
            })
            this.editemail = false
            this.refreshuser()
          })
          .catch(error => {
            util.ajanxerrorcode(this, error)
          })
      },
      Registered () {
        this.$refs['gitinfova'].validate((valid) => {
          if (valid) {
            axios.post(util.url + '/gitinfo/', {
              'project': this.gitinfo.project,
              'project_item': this.gitinfo.project_item,
              'progress_name': this.gitinfo.programe_name,
              'gitaddress': this.gitinfo.gitaddress,
              'hostname': this.gitinfo.hostname
            })
              .then(res => {
                this.$Notice.success({
                  title: res.data
                })
                this.refreshuser()
                this.gitinfo = {
                  username: '',
                  password: '',
                  confirmpassword: '',
                  group: '',
                  checkbox: '',
                  department: '',
                  email: ''}
              })
              .catch(() => {
                this.$Notice.error({
                  title: '警告',
                  desc: '用户名已注册过,请更换其他用户名注册！'
                })
              })
          }
        })
      },
      refreshuser (vl = 1) {
        axios.get(`${util.url}/gitinfo/all?page=${vl}`)
          .then(res => {
            this.data5 = res.data.data
            this.pagenumber = parseInt(res.data.page.alter_number)
          })
          axios.get(`${util.url}/modelistinfoview/?choice=all&page=1`)
          .then(res => {
            console.info(res.data.data)
            this.data5 = res.data.data
            this.pagenumber = parseInt(res.data.page.alter_number)
          })
          .catch(error => {
            util.ajanxerrorcode(this, error)
          })
      },
      splicpage (page) {
        this.refreshuser(page)
      },
      cancelEditPass () {
        this.editPasswordForm = {}
        this.editPasswordModal = false
      },
      cancelEditInfo () {
        this.editInfodModal = false;
        this.editInfodForm = {}
      },
      cancelDelInfo () {
        this.deluserModal = false;
        this.confirmuser = ''
      },
      saveEditPass () {
        this.$refs['editPasswordForm'].validate((valid) => {
          if (valid) {
            this.savePassLoading = true;
            axios.put(util.url + '/userinfo/changepwd', {
              'username': this.username,
              'new': this.editPasswordForm.newPass,
              'old': this.editPasswordForm.oldPass
            })
              .then(res => {
                this.$Notice.success({
                  title: '通知',
                  desc: res.data
                })
                this.editPasswordModal = false;
              })
              .catch(error => {
                util.ajanxerrorcode(this, error)
              })
            this.savePassLoading = false
          }
        });
      },
      saveEditInfo () {
        axios.put(util.url + '/userinfo/changegroup', {
          'username': this.username,
          'group': this.editInfodForm.group,
          'department': this.editInfodForm.department,
          'permission': JSON.stringify(this.permission)
        })
          .then(res => {
            this.$Notice.success({
              title: '通知',
              desc: res.data
            })
            this.refreshuser()
          })
          .catch(error => {
            util.ajanxerrorcode(this, error)
          })
        this.editInfodModal = false
      },
      delUser () {
        if (this.username === this.confirmuser) {
          axios.delete(util.url + '/userinfo/' + this.username)
            .then(res => {
              this.$Notice.success({
                title: '通知',
                desc: res.data
              })
              this.deluserModal = false
              this.refreshuser()
            })
            .catch(error => {
              util.ajanxerrorcode(this, error)
            })
        } else {
          this.$Message.error('用户名不一致!请重新操作!')
        }
      }
    },
    mounted () {
      axios.put(`${util.url}/workorder/connection`, {'permissions_type': 'user'})
        .then(res => {
          this.con = res.data['connection']
          this.dicadd = res.data['dic']
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
      this.refreshuser()
    }
  }
</script>
<!-- reder put request  render_group put request  remove delete request-->
