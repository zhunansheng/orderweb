<style lang="less">
@import '../../styles/common.less';
@import '../Order/components/table.less';
</style>
<template>
<div>
  <Row>
    <Card>
      <p slot="title">
        <Icon type="person"></Icon>
        审核工单
      </p>
      <Row>
        <Col span="24">
        <Poptip
          confirm
          title="您确认删除这些工单信息吗?"
          @on-ok="delrecordData"
          >
        </Poptip>
        <Button type="info" style="margin-left: -1%" @click.native="mou_data()">刷新</Button>
        <Table border :columns="columns6" :data="tmp" stripe ref="selection" @on-selection-change="delrecordList"></Table>
        <br>
        <Page :total="pagenumber" show-elevator @on-change="splicpage" :page-size="20" ref="page"></Page>
        </Col>
      </Row>
    </Card>
  </Row>
  <Modal v-model="moda00"  width="1200" :closable="false">
      <Form ref="formItem" :model="formitem0" :rules="ruleValidate" :label-width="150">
        <Row>

          <FormItem label="版本信息:">
            <Col span="3">
              <Select v-model="formitem0.iteration_name">
                <Option v-for="a in iteration_list" :key=a.label :value=a.value >{{ a.label }}</Option>
              </Select>
            </Col>
            <Col span="3" style="margin-left: 1%">
              <Select v-model="formitem0.env_name">
                <Option v-for="b in env_list" :key=b.label :value=b.value >{{ b.label }}</Option>
              </Select>
            </Col>
            <Col span="3" style="margin-left: 1%">
              <Select v-model="formitem0.project_name">
                <Option v-for="c in project_list" :key=c.label :value=c.value >{{ c.label }}</Option>
              </Select>
            </Col>

          </FormItem>

        </Row>
        <Row>
          <Col span="5">
            <FormItem label="升级时间:">
              <DatePicker type="datetime" v-model="formitem0.upstart_time" format="yyyy-MM-dd HH:mm" placeholder="Select date and time(Excluding seconds)" style="width: 200px"></DatePicker>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="5">
            <FormItem label="回退时间:">
              <DatePicker type="datetime" v-model="formitem0.upbak_time" format="yyyy-MM-dd HH:mm" placeholder="Select date and time(Excluding seconds)" style="width: 200px"></DatePicker>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="6">
            <FormItem label="升级版本:">
              <Input  v-model="formitem0.versionvalue" placeholder="Enter something..." ></Input>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="6">
            <FormItem label="紧急程度:">
              <span>{{ formitem0.state_em }}</span>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="6">
            <FormItem label="升级描述:">
              <span>{{ formitem0.updesc }}</span>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="6">
            <FormItem label="sql审计工单号:">
              <Select v-model="formitem0.sqlorder" multiple style="width:260px">
                      <Option v-for="item in sqlorderList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                      </Select>
            </FormItem>
          </Col>
        </Row>
        <Row>
                  <Col span="12">
                    <FormItem label="本次新增服务:">
                      <RadioGroup v-model="formitem0.addservice"  @on-change="newaddservice">
        <Radio label="yes">
            <span>是</span>
        </Radio>
        <Radio label="no">
            <span>否</span>
        </Radio>
        <Icon type="ios-compose-outline" size="16" color="#19be6b" @click.native="newaddservice"></Icon>
    </RadioGroup>
                    </FormItem>
                  </Col>
                </Row>
        <Row>
          <Col span="20">
            <FormItem label="升级顺序">
              <p class="pa">升级顺序:</p>
      <Table border :columns="columnsName" :data="dataId"></Table>
            </FormItem>

          </Col>
        </Row>
        <Row>
          <Col span="18">
            <FormItem label="配置中心">
              <Table border :columns="columnsName1" :data="dataId1"></Table>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="12">
            <FormItem label="指定审核人:">
              <Select v-model="formitem0.assigned" filterable>
                <Option v-for="i in this.assigned" :value="i.value" :key="i.label">{{ i.label }}</Option>
              </Select>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="12">
            <FormItem label="开发人员:">
              <Input v-model="formitem0.progress_editor" type="textarea" :autosize="true" placeholder="Enter something..."></Input>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="12">
            <FormItem label="工单说明:">
              <Input v-model="formitem0.remark" type="textarea" :autosize="true" ></Input>
            </FormItem>
          </Col>
        </Row>
      </Form>


      <div slot="footer">
        <!--<Button type="warning" @click.native="test_button()">检测sql</Button>-->
        <Button type="error" @click="out_button()" :disabled="summit">驳回</Button>
      <Button type="success" @click="put_button()" :disabled="summit">同意</Button>
      </div>
    </Modal>
  <Modal v-model="moda0" width="800">
    <p slot="header" style="color:#f60;font-size: 16px">
      <Icon type="information-circled"></Icon>
      <span>上线工单详细信息</span>
    </p>
    <Form label-position="right">
      <FormItem label="工单编号:">
        <span>{{ formitem0.workid }}</span>
      </FormItem>
      <FormItem label="提交时间:">
        <span>{{ formitem0.date }}</span>
      </FormItem>
      <FormItem label="提交人:">
        <span>{{ formitem0.assigned }}</span>
      </FormItem>
      <FormItem label="升级类型:">
        <span>{{ formitem0.iteration_name}}</span>
      </FormItem>
      <FormItem label="项目:">
        <span>{{ formitem0.project_name}}</span>
      </FormItem>
      <FormItem label="环境:">
        <span v-if="formitem0.env_name === 'pro'">生产</span>
        <span v-if="formitem0.env_name === 'pre'">预发布</span>
      </FormItem>
      <FormItem label="升级时间:">
        <span>{{ formitem0.upstart_time }}</span>
      </FormItem>
      <FormItem label="回退时间:">
        <span>{{ formitem0.upbak_time }}</span>
      </FormItem>
      <FormItem label="升级版本:">
      <span>{{ formitem0.versionvalue}}</span>
    </FormItem>
      <FormItem label="紧急程度:">
        <span v-if="formitem0.state_em === 'a'">一般</span>
        <span v-if="formitem0.state_em === 'b'">紧急</span>
        <span v-if="formitem0.state_em === 'c'">非常紧急</span>
      </FormItem>
      <FormItem label="升级描述:">
        <span>{{ formitem0.updesc }}</span>
      </FormItem>
      <FormItem label="sql审计工单号:">
        <span>{{ formitem0.sqlorder }}</span>
      </FormItem>
      <FormItem label="本次新增服务:">
                      <RadioGroup v-model="formitem0.addservice"  @on-change="newaddservice">
        <Radio label="yes">
            <span>是</span>
        </Radio>
        <Radio label="no">
            <span>否</span>
        </Radio>
    </RadioGroup>
                    </FormItem>
      <p class="pa" v-if="formitem0.addservice === 'yes'">新增服务模块:</p>
      <Table v-if="formitem0.addservice === 'yes'" border :columns="modecolumnsName" :data="newserviceData"></Table>
      <br>
      <p class="pa">升级顺序:</p>
      <Table border :columns="columnsName" :data="dataId"></Table>
      <p class="pa">配置中心:</p>
      <Table border :columns="columnsName1" :data="dataId1"></Table>
      <FormItem label="开发人员:">
        <span>{{ formitem0.progress_editor }}</span>
      </FormItem>
      <FormItem label="其它说明:">
        <span>{{ formitem0.remark }}</span>
      </FormItem>
    </Form>


    <div slot="footer">
      <!--<Button type="warning" @click.native="test_button()">检测sql</Button>-->
      <Button type="error" @click="out_button()" :disabled="summit">驳回</Button>
      <Button type="success" @click="put_button()" :disabled="summit">同意</Button>
    </div>
  </Modal>
  <Modal v-model="moda1" width="800">
    <p slot="header" style="color:#f60;font-size: 16px">
      <Icon type="information-circled"></Icon>
      <span>扩容工单详细信息</span>
    </p>
    <Form label-position="right">
      <FormItem label="工单编号:">
        <span>{{ formitem1.workid }}</span>
      </FormItem>
      <FormItem label="提交时间:">
        <span>{{ formitem1.date }}</span>
      </FormItem>
      <FormItem label="提交人:">
        <span>{{ formitem1.owner }}</span>
      </FormItem>
      <FormItem label="归属项目:">
        <span>{{ formitem1.project_name }}</span>
      </FormItem>
      <FormItem label="环境:">
        <span>{{ formitem1.env_name }}</span>
      </FormItem>
      <FormItem label="应用名称:">
        <span>{{ formitem1.appname }}</span>
      </FormItem>
      <FormItem label="类型:">
      <span>{{ formitem1.type }}</span>
    </FormItem>
      <FormItem label="工单说明:">
        <span>{{ formitem1.remark }}</span>
      </FormItem>
    </Form>
    <div slot="footer">
      <!--<Button type="warning" @click.native="test_button()">检测sql</Button>-->
      <Button type="error" @click="out_button()" :disabled="summit" v-if="seen">驳回</Button>
      <Button type="success" @click="put_button()" :disabled="summit" v-if="seen">同意</Button>
    </div>
  </Modal>
  <Modal v-model="moda2" width="800">
    <p slot="header" style="color:#f60;font-size: 16px">
      <Icon type="information-circled"></Icon>
      <span>新增服务器工单详细信息</span>
    </p>
    <Form label-position="right">
      <FormItem label="工单编号:">
        <span>{{ formitem2.workid }}</span>
      </FormItem>
      <FormItem label="提交时间:">
        <span>{{ formitem2.date }}</span>
      </FormItem>
      <FormItem label="提交人:">
        <span>{{ formitem2.assigned }}</span>
      </FormItem>
      <FormItem label="归属项目:">
        <span>{{ formitem2.project_name }}</span>
      </FormItem>
      <FormItem label="环境:">
        <span>{{ formitem2.env_name }}</span>
      </FormItem>
      <FormItem label="应用名称:">
        <span>{{ formitem2.appname }}</span>
      </FormItem>
      <FormItem label="类型:">
        <span>{{ formitem2.appname }}</span>
      </FormItem>
      <FormItem label="系统/软件要求:">
        <span>{{ formitem2.os_soft_need }}</span>
      </FormItem>
      <FormItem label="服务器数量:">
        <span>{{ formitem2.servernum }}</span>
      </FormItem>
      <FormItem label="cpu核数:">
        <span>{{ formitem2.cpunum }}</span>
      </FormItem>
      <FormItem label="内存大小:">
        <span>{{ formitem2.mem }}</span>
      </FormItem>
      <FormItem label="系统盘大小:">
        <span>{{ formitem2.OsDiskSize }}</span>
      </FormItem>
      <FormItem label="系统盘磁盘类型:">
        <span>{{ formitem2.OsDiskType }}</span>
      </FormItem>
      <FormItem label="数据盘大小/G:">
      <span>{{ formitem2.DataDiskSize }}</span>
    </FormItem>
      <FormItem label="数据盘大小/G:">
        <span>{{ formitem2.DataDiskSize }}</span>
      </FormItem>
      <FormItem label="数据盘类型/G:">
        <span>{{ formitem2.DataDiskType }}</span>
      </FormItem>
      <FormItem label="网络峰值/G:">
        <span>{{ formitem2.netbrand }}</span>
      </FormItem>
      <FormItem label="jdk版本:">
        <span>{{ formitem2.jdk_version }}</span>
      </FormItem>
      <FormItem label="jvm参数:">
        <span>{{ formitem2.jdk_version }}</span>
      </FormItem>
      <FormItem label="是否需要域名:">
      <span>{{ formitem2.domain_choice }}</span>
    </FormItem>
      <FormItem label="是否需要配置https:">
        <span>{{ formitem2.https_choice }}</span>
      </FormItem>
      <FormItem label="域名规划:">
        <span>{{ formitem2.https_choice }}</span>
      </FormItem>
      <FormItem label="工单说明:">
        <span>{{ formitem2.remark }}</span>
      </FormItem>
    </Form>
    <div slot="footer">
      <!--<Button type="warning" @click.native="test_button()">检测sql</Button>-->
      <Button type="error" @click="out_button()" :disabled="summit" v-if="seen">驳回</Button>
      <Button type="success" @click="put_button()" :disabled="summit" v-if="seen">同意</Button>
    </div>
  </Modal>
  <Modal v-model="modal2" width="800">
    <p slot="header" style="color:#f60;font-size: 16px">
      <Icon type="information-circled"></Icon>
      <span>SQL工单详细信息</span>
    </p>
    <Form label-position="right">
      <FormItem label="id:">
        <span>{{ formitem.id }}</span>
      </FormItem>
      <FormItem label="工单编号:">
        <span>{{ formitem.workid }}</span>
      </FormItem>
      <FormItem label="提交时间:">
        <span>{{ formitem.date }}</span>
      </FormItem>
      <FormItem label="提交人:">
        <span>{{ formitem.username }}</span>
      </FormItem>
      <FormItem label="机房:">
        <span>{{ formitem.computer_room }}</span>
      </FormItem>
      <FormItem label="连接名称:">
        <span>{{ formitem.connection_name }}</span>
      </FormItem>
      <FormItem label="数据库库名:">
        <span>{{ formitem.basename }}</span>
      </FormItem>
      <FormItem label="工单说明:">
        <span>{{ formitem.remark }}</span>
      </FormItem>
      <FormItem label="SQL语句:">
        <p v-for="i in sql">{{ i }}</p>
      </FormItem>
    </Form>
    <p class="pa">SQL检查结果:</p>
    <Table border :columns="columnsName" :data="dataId"></Table>
    <div slot="footer">
      <!--<Button type="warning" @click.native="test_button()">检测sql</Button>-->
      <Button type="error" @click="out_button()" :disabled="summit" v-if="seen">驳回</Button>
      <Button type="success" @click="put_button()" :disabled="summit" v-if="seen">同意</Button>
    </div>
  </Modal>

  <Modal v-model="reject.reje" @on-ok="rejecttext">
    <p slot="header" style="color:#f60;font-size: 16px">
      <Icon type="information-circled"></Icon>
      <span>SQL工单驳回理由说明</span>
    </p>
    <Input v-model="reject.textarea" type="textarea" :autosize="{minRows: 15,maxRows: 15}" placeholder="请填写驳回说明"></Input>
  </Modal>
</div>
</template>
<script>
import axios from 'axios'
import Cookies from 'js-cookie'
import util from '../../libs/util'
export default {
  name: 'Sqltable',
  data () {
    return {
      columns7: [
          {
            title: '编号',
            key: 'ordernum',
            width: 100,
            align: 'center',
            render: (h, params) => {
                            return h('Input', {
                                props: {
                                  type: 'text',
                                  value: this.data6[params.index].ordernum
                                },
                                on: {
                                    'on-change': (event) => {
                                      this.data6[params.index].ordernum = event.data
                                    }
                                }
                            })
                        }
            },
                    {
                        title: '模块',
                        key: 'modename',
                        render: (h, params) => {
                        return h('Select', {
                          props: {
                            value: this.data6[params.index].modename
                            },
                            on: {
                              'on-change': (event) => {
                                this.data6[params.index].modename = event;
                                for (let [key, value] of this.mode_name[this.projectselect].entries()) {
                                  console.info(event, Object.keys(value)[0], key)
                                  if (Object.keys(value)[0] === event) {
                                    this.data6[params.index].servicenamelist = value[event]
                                  }
                                 }
                                console.info(this.data6[params.index])
                                }
                              }
                            },
                          this.temp_mode_name_select.map(function (type) {
                            return h('Option', {
                              props: {value: type}
                              }, type);
                            })
                        );
                    }
                    },
                    {
                        title: '服务名称',
                        key: 'servicename',
                        render: (h, params) => {
                        return h('Select', {
                          props: {
                            value: this.data6[params.index].servicename
                            },
                            on: {
                              'on-change': (event) => {
                                this.data6[params.index].servicename = event;
                                this.data6[params.index].volumeTypes = ['加载分支中......']
                                console.info(this.data6[params.index])
                                   axios.get(`${util.url}/gitlabinfo?modename=${this.data6[params.index]['modename']}&servicename=${this.data6[params.index]['servicename']}&env_name=${this.formitem0.env_name}`)
                                    .then(res => {
                                    console.info(res.data)
                                    if (res.data.data !== 'error') {
                                      this.data6[params.index].volumeTypes = res.data.data
                                    } else {
                                      this.$Notice.error({
                                         title: '发生错误',
                                        desc: res.data.log
                                       });
                                       this.data6[params.index].volumeTypes = []
                                    }
                                  })
                              .catch(error => {
                              util.ajanxerrorcode(this, error)
                               })
                                }
                              }
                            },
                          this.data6[params.index].servicenamelist.map(function (type) {
                            return h('Option', {
                              props: {value: type}
                              }, type);
                            })
                        );
                    }
                    },
                    {
                        title: '升级分支名称',
                        key: 'address',
                        render: (h, params) => {
                        return h('Select', {
                          props: {
                            value: this.data6[params.index].volumeType
                            },
                            on: {
                              'on-change': (event) => {
                                this.data6[params.index].volumeType = event;
                                console.info(this.data6)
                                }
                              }
                            },
                          this.data6[params.index].volumeTypes.map(function (type) {
                            return h('Option', {
                              props: {value: type}
                              }, type);
                            })
                        );
                    }
                    },
                    {
                      title: '回滚分支名称',
                      key: 'values',
                      render: (h, params) => {
                        return h('Select', {
                          props: {
                            value: this.data6[params.index].bakvolumeType
                            },
                            on: {
                              'on-change': (event) => {
                                this.data6[params.index].bakvolumeType = event;
                                console.info(this.data6)
                                }
                              }
                            },
                          this.data6[params.index].volumeTypes.map(function (type) {
                            return h('Option', {
                              props: {value: type}
                              }, type);
                            })
                        );
                    }
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
                                        type: 'error',
                                        size: 'small'
                                    },
                                    on: {
                                        click: () => {
                                            this.remove(params.index)
                                        }
                                    }
                                }, '删除')
                            ]);
                        }
                    }
                 ],
      columns6: [
        {
          type: 'selection',
          width: 60,
          align: 'center'
        },
        {
          title: '工单编号:',
          key: 'workid',
          sortable: true,
          sortType: 'desc',
          width: 250
        },
        {
          title: '工单说明:',
          key: 'remark'
        },
        {
          title: '工单类型',
          key: 'type'
        },
        {
          title: '提交时间:',
          key: 'date',
          sortable: true,
          width: 150
        },
        {
          title: '提交人',
          key: 'username',
          sortable: true,
          width: 150
        },
        {
          title: '状态',
          key: 'status',
          width: 150,
          render: (h, params) => {
            const row = params.row
            let color = ''
            let text = ''
            if (row.status === 0) {
              color = 'red'
              text = '拒绝'
            } else if (row.status === 3) {
              color = 'green'
              text = '同意'
            } else if (row.status === 4) {
              color = 'red'
              text = '已撤销'
            } else {
              color = 'yellow'
              text = '审核中'
            }
            return h('Tag', {
              props: {
                type: 'dot',
                color: color
              }
            }, text)
          },
          sortable: true,
          filters: [{
              label: '同意',
              value: '同意'
            },
            {
              label: '拒绝',
              value: '拒绝'
            },
            {
              label: '审核中',
              value: '审核中'
            },
            {
              label: '进行中',
              value: '进行中'
            }
          ],
          //            filterMultiple: false 禁止多选,
          filterMethod (value, row) {
            if (value === 1) {
              return row.status === 1
            } else if (value === 2) {
              return row.status === 2
            } else if (value === 0) {
              return row.status === 0
            } else if (value === 3) {
              return row.status === 3
            }
          }
        },
        {
          title: '操作',
          key: 'action',
          width: 100,
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('Button', {
                props: {
                  size: 'small',
                  type: 'text'
                },
                on: {
                  click: () => {
                    this.edit_tab(params.row.workid, params.row.type, params.row.status)
                  }
                }
              }, '查看')
            ])
          }
        }
      ],
      tmp_workid: '',
      newserviceData: '',
      modal2: false,
      moda0: false,
      moda1: false,
      moda2: false,
      sql: null,
      seen: true,
      formitem: {
        workid: '',
        date: '',
        username: '',
        dataadd: '',
        database: '',
        att: '',
        id: null,
        remark: '',
        upstart_time: ''
      },
      formitem0: {
        workid: '',
        iteration_name: '',
        env_name: '',
        project_name: '',
        assigned: '',
        remark: '',
        progress_name: '',
        versionvalue: '',
        sqlorder: '',
        updesc: '',
        up_version: '',
        state_em: '',
        upbak_time: '',
        staticversion: '',
        progress_editor: '',
        date: ''
      },
      formitem2: {
        workid: '',
        project_name: '',
        env_name: '',
        domain_choice: '',
        OsDiskType: '',
        os_soft_need: [],
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
        remark: '',
        netbrand: '',
        domain: '',
        date: '',
        appname: ''
      },
      formitem1: {
        workid: '',
        project_name: '',
        env_name: '',
        opentime: '',
        assigned: '',
        remark: '',
        os_soft_need: [],
        ghost_choice: '',
        properties_change: '',
        servernum: '',
        appname: '',
        type: ''
      },
      summit: false,
      columnsName: [
        {
          title: '编号',
          width: 60,
          key: 'ordernum',
          align: 'center'
        },
        {
          title: '模块',
          key: 'modename',
          align: 'center'
        },
        {
          title: '服务名称',
          key: 'servicename'
        },
        {
          title: '升级分支名称',
          key: 'volumeType'
        },
        {
          title: '回滚分支名称',
          key: 'bakvolumeType'
        }
      ],
      modecolumnsName: [
        {
        title: '编号',
        type: 'index',
        width: 100,
        align: 'center'
    },
        {
          title: '项目',
          key: 'projectname',
          align: 'center'
        },
        {
          title: '模块名称',
          key: 'modename'
        },
        {
          title: '服务名',
          key: 'servicename'
        },
        {
          title: 'git-ssh地址',
          key: 'gitaddress'
        },
        {
          title: 'maven打包命令',
          key: 'mavenpom'
        },
        {
          title: 'java版本',
          key: 'java_version'
        },
        {
          title: '备注',
          key: 'remark'
        }
      ],
      columnsName1: [
        {
          title: '配置文件',
          key: 'config_properties'
        },
        {
          title: '程序文件',
          key: 'programname'
        },
        {
          title: '键',
          key: 'keyname'
        },
        {
          title: '值',
          key: 'valuename'
        },
        {
          title: '状态',
          key: 'statevalue'
        }
      ],
      dataId: [],
      dataId1: [],
      reject: {
        reje: false,
        textarea: ''
      },
      tmp: [],
      tmp_detail: [],
      pagenumber: 1,
      delrecord: [],
      togoing: null
    }
  },
  methods: {
    edit_tab: function (workid, type, status) {
      console.info(workid)
      this.togoing = workid
      this.dataId = []
      console.info(status)
      if (status === 4) {
        this.seen = false
      }
      axios.get(`${util.url}/audit_sql?workid=${workid}&username=${Cookies.get('user')}`)
        .then(res => {
          console.info(res.data.data)
          this.tmp_detail = res.data.data
          this.tmp_detail.forEach((item) => {
            if (type === '上线') {
              this.moda0 = true
              this.formitem0.workid = item.workid
              this.tmp_workid = item.workid
              this.formitem0.iteration_name = item.iteration_name
              this.formitem0.env_name = item.env_name
              this.formitem0.project_name = item.project_name
              this.formitem0.versionvalue = item.versionvalue
              if (item.sqlorder === '[]') {
                this.formitem0.sqlorder = '无'
              } else {
                this.formitem0.sqlorder = item.sqlorder
              }
              this.formitem0.updesc = item.updesc
              this.formitem0.versionvalue = item.versionvalue
              this.formitem0.state_em = item.state_em
              this.formitem0.upbak_time = item.upbak_time
              this.formitem0.upstart_time = item.upstart_time
              this.formitem0.staticversion = item.staticversion
              this.formitem0.assigned = item.assigned
              this.formitem0.type = '上线'
              this.formitem0.date = item.date
              this.formitem0.progress_editor = item.progress_editor
              this.formitem0.assigned = item.assigned
              this.formitem0.addservice = item.addservice
              this.dataId1 = JSON.parse(item.config_properties)
              this.dataId = JSON.parse(item.uporder)
              this.newserviceData = JSON.parse(item.newserviceData)
              this.formitem0.remark = item.remark
              console.info(this.dataId)
            } else if (type === '扩容') {
              this.moda1 = true
              this.tmp_workid = item.workid
              this.formitem1.workid = item.workid
              this.formitem1.project_name = item.project_name
              this.formitem1.env_name = item.env_name
              this.formitem1.opentime = item.opentime
              this.formitem1.os_soft_need = item.os_soft_need
              this.formitem1.ghost_choice = item.ghost_choice
              this.formitem1.properties_change = item.properties_change
              this.formitem1.appname = item.appname
              this.formitem1.date = item.date
              this.formitem1.owner = item.owner
              this.formitem1.type = '扩容'
              this.formitem1.remark = item.remark
              console.info(this.formitem1)
            } else {
              this.moda2 = true
              this.formitem2.workid = item.workid
              this.tmp_workid = item.workid
              this.formitem2.project_name = item.project_name
              this.formitem2.assigned = item.assigned
              this.formitem2.env_name = item.env_name
              this.formitem2.domain_choice = item.domain_choice
              this.formitem2.OsDiskType = item.OsDiskType
              this.formitem2.os_soft_need = item.os_soft_need
              this.formitem2.servernum = item.servernum
              this.formitem2.OsDiskSize = item.OsDiskSize
              this.formitem2.cpunum = item.cpunum
              this.formitem2.DataDiskSize = item.DataDiskSize
              this.formitem2.mem = item.mem
              this.formitem2.jdk_version = item.jdk_version
              this.formitem2.https_choice = item.https_choice
              this.formitem2.DataDiskType = item.DataDiskType
              this.formitem2.jvm_properties = item.jvm_properties
              this.formitem2.remark = item.remark
              this.formitem2.netbrand = item.netbrand
              this.formitem2.domain = item.domain
              this.formitem2.date = item.date
              this.formitem2.appname = item.appname
              item.type = '新增服务器'
            }
          })
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    },
    cancel_button (num) {
      if (num === 0) {
        this.moda0 = false
      } else if (num === 1) {
        this.moda1 = false
      } else if (num === 2) {
        this.moda2 = false
      }
    },
    disput_button () {
      this.modal2 = false
      this.moda0 = false
      this.moda1 = false
      this.moda2 = false
      console.info('hello')
      // this.tmp[this.togoing].status = 3
      axios.put(`${util.url}/audit_sql`, {
        'type': 0,
        'to_user': 'admin',
        'text': this.reject.textarea,
        'from_user': Cookies.get('user'),
        'workid': this.tmp_workid
      })
        .then(res => {
          this.$Notice.success({
            title: '驳回成功',
            desc: res.data
          })
          this.mou_data()
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    },
    put_button () {
      this.modal2 = false
      this.moda0 = false
      this.moda1 = false
      this.moda2 = false
      console.info('hello')
      // this.tmp[this.togoing].status = 3
      axios.put(`${util.url}/audit_sql`, {
          'type': 1,
          'from_user': Cookies.get('user'),
          'workid': this.tmp_workid
        })
        .then(res => {
          this.$Notice.success({
            title: '执行成功',
            desc: res.data
          })
          this.mou_data()
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    },
    out_button () {
      this.moda0 = false
      this.moda1 = false
      this.moda2 = false
      this.reject.reje = true
    },
    rejecttext () {
      axios.put(`${util.url}/audit_sql`, {
          'type': 0,
          'from_user': Cookies.get('user'),
          'text': this.reject.textarea,
          'to_user': 'admin',
          'workid': this.tmp_workid
        })
        .then(res => {
          this.$Notice.warning({
            title: res.data
          })
          this.mou_data()
          this.$refs.page.currentPage = 1
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    },
    test_button () {
      axios.put(`${util.url}/audit_sql`, {
          'type': 'test',
          'base': this.formitem.basename,
          'id': this.formitem.id
        })
        .then(res => {
          if (res.data.status === 200) {
            this.dataId = res.data.result
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
    },
    splicpage (page) {
      this.mou_data(page)
    },
    mou_data (vl = 1) {
      axios.get(`${util.url}/audit_sql?page=${vl}&username=${Cookies.get('user')}`)
        .then(res => {
          this.tmp = res.data.data
          this.tmp.forEach((item) => {
            if (item.type === 0) {
              item.type = '上线'
            } else if (item.type === 1) {
              item.type = '扩容'
            } else {
              item.type = '新增服务器'
            }
          })
          this.pagenumber = res.data.page.alter_number
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    },
    delrecordList (vl) {
      this.delrecord = vl
    },
    delrecordData () {
      axios.post(`${util.url}/undoOrder`, {
        'id': JSON.stringify(this.delrecord)
      })
        .then(res => {
          this.$Notice.info({
            title: '信息',
            desc: res.data
          })
          this.mou_data()
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    }
  },
  mounted () {
    this.mou_data()
  }
}
</script>
<!-- remove delete request -->
