<style lang="less">
@import '../../styles/common.less';
@import 'components/table.less';
</style>

<template>
<div>
  <Row>
    <Col span="24">
    <Card>
      <p slot="title">
        <Icon type="ios-redo"></Icon>
        配置信息
      </p>
      <div class="edittable-test-con">
        <div id="showImage" class="margin-bottom-10">

          <Form ref="formItem" :model="formItem" :rules="ruleValidate" :label-width="150">
            <Row>
              <Col span="6">
                <FormItem label="归属项目:" prop="project_name">
                  <Select v-model="formItem.project_name">
                    <Option v-for="c in project_list" :key=c.label :value=c.value >{{ c.label }}</Option>
                  </Select>
                </FormItem>
              </Col>
              <Col span="6">
                <FormItem label="环境:" prop="env_name">
                <Select v-model="formItem.env_name">
                  <Option v-for="i in env_name_list" :value="i.value" :key="i.value">{{ i.label }}</Option>
                </Select>
              </FormItem>
              </Col>
              <Col span="6">
                <FormItem label="应用名称:" prop="appname">
                  <Input v-model="formItem.appname" placeholder="" ></Input>
                </FormItem>
              </Col>
              <Col span="6">
                <FormItem label="类型:" prop="newpc_type">
                  <Select v-model="formItem.newpc_type">
                    <Option v-for="i in type_list" :value="i.value" :key="i.value">{{ i.label }}</Option>
                  </Select>
                </FormItem>
              </Col>

            </Row>
            <Row>
              <Col span="6">
                <FormItem label="系统/软件要求:" prop="os_soft_need">
                  <Select v-model="formItem.os_soft_need" multiple filterable>
                    <Option v-for="i in os_soft_need_list" :key="i.value" :value="i.value" >{{ i.label }}</Option>
                  </Select>
                </FormItem>
              </Col>
              <Col span="6">
                <FormItem label="服务器数量:" prop="servernum">
                  <Input v-model="formItem.servernum" placeholder="" ></Input>
                </FormItem>
              </Col>
              <Col span="6">
                <FormItem label="cpu核数:" prop="cpunum">
                  <Input v-model="formItem.cpunum" placeholder="" ></Input>
                </FormItem>
              </Col>
              <Col span="6">
                <FormItem label="内存大小/G:" prop="mem">
                  <Input v-model="formItem.mem" placeholder="" ></Input>
                </FormItem>
              </Col>
            </Row>
            <Row>
              <Col span="6">
                <FormItem label="系统盘大小/G:">
                  <Input v-model="formItem.OsDiskSize" placeholder="" ></Input>
                </FormItem>
              </Col>
              <Col span="6">
                <FormItem label="系统盘磁盘类型:">
                  <Select v-model="formItem.OsDiskType">
                    <Option v-for="i in disk_type_list" :value="i.value" :key="i.value">{{ i.label }}</Option>
                  </Select>
                </FormItem>
              </Col>
              <Col span="6">
                <FormItem label="数据盘大小/G:">
                  <Input v-model="formItem.DataDiskSize" placeholder="." ></Input>
                </FormItem>
              </Col>
            </Row>
            <Row>
              <Col span="6">
                <FormItem label="数据盘类型:">
                  <Select v-model="formItem.DataDiskType">
                    <Option v-for="i in disk_type_list" :key="i.value" :value="i.value" >{{ i.label }}</Option>
                  </Select>
                </FormItem>
              </Col>
              <Col span="6">
                <FormItem label="网络峰值/M:">
                  <Input v-model="formItem.netbrand" placeholder="" ></Input>
                </FormItem>
              </Col>
              <Col span="6">
                <FormItem label="JDK版本:">
                  <Select v-model="formItem.jdk_version">
                    <Option v-for="i in jdk_version_list" :value="i.value" :key="i.value">{{ i.label }}</Option>
                  </Select>
                </FormItem>
              </Col>
              <Col span="6">
                <FormItem label="JVM参数:">
                  <Input v-model="formItem.jvm_properties" placeholder="" ></Input>
                </FormItem>
              </Col>
            </Row>
            <Row>
              <Col span="6">
                <FormItem label="是否需要域名:">
                  <Select v-model="formItem.domain_choice">
                    <Option v-for="i in https_choice_list" :key="i.value" :value="i.value" >{{ i.label }}</Option>
                  </Select>
                </FormItem>
              </Col>

              <Col span="6">
                <FormItem label="是否需要配置https:">
                  <Select v-model="formItem.https_choice">
                    <Option v-for="i in https_choice_list" :value="i.value" :key="i.value">{{ i.label }}</Option>
                  </Select>
                </FormItem>
              </Col>
              <Col span="6">
                <FormItem label="域名规划:">
                  <Input v-model="formItem.domain" placeholder="" ></Input>
                </FormItem>
              </Col>
              <Col span="6">
                <FormItem label="开通时间:" prop="opentime">
                  <DatePicker type="datetime" v-model="formItem.opentime" format="yyyy-MM-dd HH:mm" placeholder="Select date and time(Excluding seconds)" style="width: 200px"></DatePicker>
                </FormItem>
              </Col>
            </Row>
            <Row>
              <Col span="12">
                <FormItem label="指定审核人:">
                  <Select v-model="formItem.assigned" filterable>
                    <Option v-for="i in this.assigned" :value="i.value" :key="i.label">{{i.label}}</Option>
                  </Select>
                </FormItem>
              </Col>
            </Row>
            <Row>
              <Col span="12">
                <FormItem label="备注:">
                  <Input v-model="formItem.remark" type="textarea" :autosize="true" placeholder=""></Input>
                </FormItem>
              </Col>
            </Row>


            <FormItem>
              <!--<Button type="warning" icon="android-search" @click.native="test_sql()">重置</Button>-->
              <Button type="success" icon="ios-redo" @click.native="commitorder()" style="margin-left: 1%">提交</Button>
            </FormItem>
          </Form>

        </div>
      </div>
    </Card>
    </Col>
  </Row>
</div>
</template>
<script>
import ICol from '../../../node_modules/iview/src/components/grid/col.vue'
import axios from 'axios'
import Cookies from 'js-cookie'
import util from '../../libs/util'
export default {
  components: {
    ICol,
    editor: require('../../libs/editor')
  },
  name: 'SQLsyntax',
  data () {
    return {
      validate_gen: true,
      assigned: [{
          value: 'admin',
          label: 'admin'
        }],
      formItem: {
        project_name: '',
        env_name: '',
        domain_choice: '',
        OsDiskType: '',
        os_soft_need: '',
        assigned: '',
        servernum: '',
        OsDiskSize: '',
        cpunum: '',
        DataDiskSize: '',
        mem: '',
        jdk_version: '',
        https_choice: '',
        DataDiskType: '',
        jvm_properties: '',
        mewpc_type: '',
        remark: '',
        netbrand: '',
        domain: ''
      },
      columnsName: [
        {
          title: 'ID',
          key: 'ID',
          width: '50'
        },
        {
          title: '阶段',
          key: 'stage',
          width: '100'
        },
        {
          title: '错误等级',
          key: 'errlevel',
          width: '100'
        },
        {
          title: '阶段状态',
          key: 'stagestatus',
          width: '150'
        },
        {
          title: '错误信息',
          key: 'errormessage'
        },
        {
          title: '当前检查的sql',
          key: 'sql'
        },
        {
          title: '预计影响的SQL',
          key: 'affected_rows',
          width: '130'
        }
      ],
      Testresults: [],
      item: {},
      project_list: [
          {
            value: '长安',
            label: '长安'
          },
          {
            value: '车机中心',
            label: '车机中心'
          }
        ],
      jdk_version_list: [
        {
          value: 'JDK1.8',
          label: 'JDK1.8'
        },
        {
          value: 'JDK1.7',
          label: 'JDK1.7'
        },
        {
          value: 'JDK1.6',
          label: 'JDK1.6'
        }
      ],
      https_choice_list: [
        {
          value: 'yes',
          label: '是'
        },
        {
          value: 'no',
          label: '否'
        }
      ],
      env_name_list: [
        {
          value: 'test',
          label: '测试环境'
        },
        {
          value: 'pre',
          label: '预发布'
        },
        {
          value: 'pro',
          label: '生产'
        }
      ],
      disk_type_list: [
        {
          value: 'HighEfficientCloudDisk',
          label: '高效云盘'
        },
        {
          value: 'SSD',
          label: 'SSD'
        }
      ],
      type_list: [
        {
          value: 'ECS',
          label: 'ECS'
        },
        {
          value: 'RDS-MYSQL',
          label: 'RDS-MYSQL'
        },
        {
          value: 'REDIS',
          label: 'REDIS'
        },
        {
          value: 'MongoDB',
          label: 'MongoDB'
        }
      ],
      os_soft_need_list: [
        {
          value: 'Centos6.8',
          label: 'Centos6.8'
        },
        {
          value: 'Centos7.4',
          label: 'Centos7.4'
        },
        {
          value: 'MySQL5.6',
          label: 'MySQL5.6'
        },
        {
          value: 'MySQL5.7',
          label: 'MySQL5.7'
        },
        {
          value: 'Redis3.2',
          label: 'Redis3.2'
        },
        {
          value: 'Redis3.4',
          label: 'Redis3.4'
        },
        {
          value: 'MongDB3.2',
          label: 'MongDB3.2'
        },
        {
          value: 'MongDB3.4',
          label: 'MongDB3.4'
        }
      ],
      datalist: {
        connection_name_list: [],
        basenamelist: [],
        sqllist: [],
        projectlist: util.projectlist
      },
      ruleValidate: {
        project_name: [{
          required: true,
          message: '机房地址不得为空',
          trigger: 'change'
        }],
        env_name: [{
          required: true,
          message: '环境不能为空',
          trigger: 'change'
        }],
        appname: [{
          required: true,
          message: '应用名称不能',
          trigger: 'change'
        }],
        newpc_type: [{
          required: true,
          message: '类型不能为空',
          trigger: 'change'
        }],
        os_soft_need: [{
          type: 'array',
          required: true,
          message: '软件和应用不能为空',
          trigger: 'change'
        }],
        servernum: [{
          required: true,
          message: '服务器数量不能为空',
          trigger: 'change'
        }],
        cpunum: [{
          required: true,
          message: 'cpu核数不能为空',
          trigger: 'change'
        }],
        mem: [{
          required: true,
          message: '内存大小不能为空',
          trigger: 'change'
        }],
        opentime: [{
          type: 'date',
          required: true,
          mesaage: '开通时间不能为空',
          trigger: 'change'
        }],
        text: [{
            required: true,
            message: '说明不得为空',
            trigger: 'blur'
          },
          {
            type: 'string',
            max: 20,
            message: '最多20个字',
            trigger: 'blur'
          }
        ],
        assigned: [{
          required: true,
          message: '说明不得为空',
          trigger: 'blur'
        }]
      }
    }
  },
  methods: {
    editorInit: function () {
      require('brace/mode/mysql')
      require('brace/theme/xcode')
    },
    beautify () {
      axios.put(`${util.url}/sqlsyntax/beautify`, {
          'data': this.formItem.textarea
        })
        .then(res => {
          this.formItem.textarea = res.data
        })
        .catch(error => {
          this.$Notice.error({
            title: '警告',
            desc: error
          })
        })
    },
    Connection_Name (val) {
      this.datalist.connection_name_list = []
      this.datalist.basenamelist = []
      this.formItem.connection_name = ''
      this.formItem.basename = ''
      if (val) {
        this.ScreenConnection(val)
      }
    },
    ScreenConnection (val) {
      this.datalist.connection_name_list = this.item.filter(item => {
        if (item.computer_room === val) {
          return item
        }
      })
    },
    DataBaseName (index) {
      if (index) {
        this.id = this.item.filter(item => {
          if (item.connection_name === index) {
            return item
          }
        })
        axios.put(`${util.url}/workorder/basename`, {
            'id': this.id[0].id
          })
          .then(res => {
            this.datalist.basenamelist = res.data
          })
          .catch(() => {
            this.$Notice.error({
              title: '警告',
              desc: '无法连接数据库!请检查网络'
            })
          })
      }
    },
    test_sql () {
      let ddl = ['select', 'alter', 'drop', 'create']
      let createtable = this.formItem.textarea.replace(/(;|；)$/gi, '').replace(/\s/g, ' ').replace(/；/g, ';').split(';')
      for (let i of createtable) {
        for (let c of ddl) {
          if (i.toLowerCase().indexOf(c) === 0) {
            this.$Message.error('不可提交非DML语句!');
            return false
          }
        }
      }
      this.$refs['formItem'].validate((valid) => {
        if (valid) {
          if (this.formItem.textarea) {
            let tmp = this.formItem.textarea.replace(/(;|；)$/gi, '').replace(/；/g, ';')
            axios.put(`${util.url}/sqlsyntax/test`, {
                'id': this.id[0].id,
                'base': this.formItem.basename,
                'sql': tmp
              })
              .then(res => {
               if (res.data.status === 200) {
                 this.Testresults = res.data.result
                 let gen = 0
                 this.Testresults.forEach(vl => {
                   if (vl.errlevel !== 0) {
                     gen += 1
                   }
                 })
                 if (gen === 0) {
                   this.validate_gen = false
                 } else {
                   this.validate_gen = true
                 }
               } else {
                 this.$Notice.error({
                   title: '警告',
                   desc: '无法连接到Inception!'
                 })
               }
              })
              .catch(error => {
               util.ajanxerrorcode(this, error)
              })
          } else {
            this.$Message.error('请填写sql语句后再测试!');
          }
        }
      })
    },
    commitorder () {
      Cookies.get('user');
      console.info(JSON.stringify(this.formItem));
      this.$refs['formItem'].validate((valid) => {
        if (valid) {
          console.info('true')
        axios.post(`${util.url}/addnewpcorder/`, {
          'data': JSON.stringify(this.formItem),
          'user': Cookies.get('user')
        })
          .then(res => {
            this.$Notice.success({
              title: '通知',
              desc: res.data
            })
            this.$router.push({
              name: 'myorder'
            })
          }).catch(error => {
          util.ajanxerrorcode(this, error)
        })
      }
      });
    },
    SubmitSQL () {
      this.$refs['formItem'].validate((valid) => {
        if (valid) {
          if (this.formItem.textarea) {
            this.datalist.sqllist = this.formItem.textarea.replace(/(;|；)$/gi, '').replace(/\s/g, ' ').replace(/；/g, ';').split(';')
            axios.post(`${util.url}/sqlsyntax/`, {
                'data': JSON.stringify(this.formItem),
                'sql': JSON.stringify(this.datalist.sqllist),
                'user': Cookies.get('user'),
                'type': 1,
                'id': this.id[0].id
              })
              .then(res => {
                this.$Notice.success({
                  title: '成功',
                  desc: res.data
                })
                this.ClearForm()
              })
              .catch(error => {
                util.ajanxerrorcode(this, error)
              })
          } else {
            this.$Message.error('请填写sql语句后再提交!');
          }
          this.validate_gen = true
        } else {
          this.$Message.error('表单验证失败!');
        }
      })
    },
    ClearForm () {
      this.formItem.textarea = ''
    }
  },
  mounted () {
    axios.put(`${util.url}/workorder/connection`, {'permissions_type': 'user'})
      .then(res => {
        this.con = res.data['connection']
        this.dicadd = res.data['dic']
        this.assigned = [{
          value: 'admin',
          label: 'admin'
        }]
      })
      .catch(error => {
        util.ajanxerrorcode(this, error)
      })
  }
}
</script>
