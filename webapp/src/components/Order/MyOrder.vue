<style lang="less">
  @import '../../styles/common.less';
  @import '../Order/components/table.less';
  @import './article-publish.less';
  .demo-upload-list{
    display: inline-block;
    width: 60px;
    height: 60px;
    text-align: center;
    line-height: 60px;
    border: 1px solid transparent;
    border-radius: 4px;
    overflow: hidden;
    background: #fff;
    position: relative;
    box-shadow: 0 1px 1px rgba(0,0,0,.2);
    margin-right: 4px;
  }
  .demo-upload-list img{
    width: 100%;
    height: 100%;
  }
  .demo-upload-list-cover{
    display: none;
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(0,0,0,.6);
  }
  .demo-upload-list:hover .demo-upload-list-cover{
    display: block;
  }
  .demo-upload-list-cover i{
    color: #fff;
    font-size: 20px;
    cursor: pointer;
    margin: 0 2px;
  }
</style>
<template>
  <div>
    <Row>
      <Card>
        <p slot="title">
          <Icon type="person"></Icon>
          我的工单
        </p>
        <Row>
          <Col span="24">
            <Table border :columns="columns6" :data="applytable" stripe size="small"></Table>
          </Col>
        </Row>
        <br>
        <Page :total="pagenumber" show-elevator @on-change="currentpage" :page-size="20"></Page>
      </Card>
    </Row>
    <Modal v-model="moda9"  width="1100" :closable="false">
      <Form ref="formItem" :model="formitem0" :rules="ruleValidate" :label-width="150">
        <Row>

          <FormItem label="升级类型:">
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
              <Select v-model="formitem0.project_name" @on-change="projectChange(formitem0.project_name)">
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
              <Select v-model="formitem0.state_em">
                    <Option v-for="b in emergency_state_list" :key=b.label :value=b.value >{{ b.label }}</Option>
              </Select>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="20">
            <FormItem label="升级描述:">
              <textarea id="articleEditor"></textarea>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="6">
            <FormItem label="SQL审计工单号:">
              <Select v-model="formitem0.sqlorder" multiple style="width:260px">
                      <Option v-for="item in sqlorderList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                      </Select>
            </FormItem>
          </Col>
        </Row>
        <Row>
                  <Col span="12">
                    <FormItem label="是否新增模块:">
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
          <FormItem label="附件">
            <div id="upload">
              <Upload
                multiple
                ref="upload"
                :headers="Authorization"
                :with-credentials= true
                :default-file-list="defaultList"
                :before-upload="handleUpload"
                :show-upload-list="false"
                :accept="Accept"
                :format="Format"
                :on-success="uploadSuccess"
                type="drag"
                action="//120.27.192.237:9090/fileupload/">
                <div style="padding: 20px 0">
                  <Icon type="ios-cloud-upload" size="52" style="color: #3399ff"></Icon>
                  <p>Click or drag files here to upload</p>
                </div>
              </Upload>
              <div v-for="(item, index) in uploadList">已上传文件:  {{ item.name }}
                <a style="margin-left: 40px;" href="javascript:;"  @click="delectFile(item.keyID)">删除</a>
              </div>
            </div>
          </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="20">
            <FormItem label="升级顺序">
              <Table border :columns="columns7" :data="data6"></Table>
              <Icon type="plus" v-on:click="addline"></Icon>
            </FormItem>

          </Col>
        </Row>
        <Row>
          <Col span="18">
            <FormItem label="配置中心">
              <can-edit-table refs="table2" v-model="dataId1" :columns-list="editInlineColumns1"></can-edit-table>
              <Icon type="plus" v-on:click="addlinep"></Icon>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="12">
            <FormItem label="审核人:">
              <Select v-model="formitem0.assigned" filterable>
                <Option v-for="i in this.assigned" :value="i.value" :key="i.label">{{ i.label }}</Option>
              </Select>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="12">
            <FormItem label="开发成员:">
              <Input v-model="formitem0.progress_editor" type="textarea" :autosize="true" placeholder="Enter something..."></Input>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="12">
            <FormItem label="其它说明:">
              <Input v-model="formitem0.remark" type="textarea" :autosize="true" ></Input>
            </FormItem>
          </Col>
        </Row>
      </Form>


      <div slot="footer">
        <!--<Button type="warning" @click.native="test_button()">检测sql</Button>-->
        <Button type="error" v-if="seen" @click="out_button()" :disabled="summit">撤销</Button>
        <Button type="success" @click="put_online_button()" :disabled="summit" v-if="seen">保存</Button>
      </div>
    </Modal>
    <Modal v-model="moda8"  width="1200" :closable="false">
      <Form ref="formItem" :model="formitem2" :rules="ruleValidate" :label-width="150">
        <Row>
          <Col span="5">
            <FormItem label="归属项目:">
              <Select v-model="formitem2.project_name">
                <Option v-for="c in project_list" :key=c.label :value=c.value >{{ c.label }}</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="5">
            <FormItem label="环境:">
              <Select v-model="formitem2.env_name">
                <Option v-for="i in env_name_list" :value="i.value" :key="i.value">{{ i.label }}</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="5">
            <FormItem label="应用名称:">
              <Input v-model="formitem2.appname" placeholder="" ></Input>
            </FormItem>
          </Col>
          <Col span="5">
            <FormItem label="类型:">
              <Select v-model="formitem2.newpc_type">
                <Option v-for="i in type_list" :value="i.label" :key="i.value">{{ i.label }}</Option>
              </Select>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="12">
            <FormItem label="系统/软件要求:">
              <Select v-model="formitem2.os_soft_need" width="100" multiple filterable>
                <Option v-for="i in os_soft_need_list" :key="i.value" :value="i.value" >{{ i.label }}</Option>
              </Select>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="5">
            <FormItem label="服务器数量:">
              <Input v-model="formitem2.servernum" placeholder="" ></Input>
            </FormItem>
          </Col>
          <Col span="5">
            <FormItem label="cpu核数:">
              <Input v-model="formitem2.cpunum" placeholder="" ></Input>
            </FormItem>
          </Col>
          <Col span="5">
            <FormItem label="内存大小/G:">
              <Input v-model="formitem2.mem" placeholder="" ></Input>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="5">
            <FormItem label="系统盘大小/G:">
              <Input v-model="formitem2.OsDiskSize" placeholder="" ></Input>
            </FormItem>
          </Col>
          <Col span="5">
            <FormItem label="系统盘磁盘类型:">
              <Select v-model="formitem2.OsDiskType">
                <Option v-for="i in disk_type_list" :value="i.value" :key="i.value">{{ i.label }}</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="5">
            <FormItem label="数据盘大小/G:">
              <Input v-model="formitem2.DataDiskSize" placeholder="." ></Input>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="5">
            <FormItem label="数据盘类型:">
              <Select v-model="formitem2.DataDiskType">
                <Option v-for="i in disk_type_list" :key="i.value" :value="i.value" >{{ i.label }}</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="5">
            <FormItem label="网络峰值/M:">
              <Input v-model="formitem2.netbrand" placeholder="" ></Input>
            </FormItem>
          </Col>
          <Col span="5">
            <FormItem label="JDK版本:">
              <Select v-model="formitem2.jdk_version">
                <Option v-for="i in jdk_version_list" :value="i.value" :key="i.value">{{ i.label }}</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="5">
            <FormItem label="JVM参数:">
              <Input v-model="formitem2.jvm_properties" placeholder="" ></Input>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="5">
            <FormItem label="是否需要域名:">
              <Select v-model="formitem2.domain_choice">
                <Option v-for="i in domain_choice_list" :key="i.value" :value="i.value" >{{ i.label }}</Option>
              </Select>
            </FormItem>
          </Col>

          <Col span="5">
            <FormItem label="是否需要配置https:">
              <Select v-model="formitem2.https_choice">
                <Option v-for="i in https_choice_list" :value="i.value" :key="i.value">{{ i.label }}</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="5">
            <FormItem label="域名规划:">
              <Input v-model="formitem2.domain" placeholder="" ></Input>
            </FormItem>
          </Col>
          <Col span="5">
            <FormItem label="开通时间:">
              <DatePicker type="datetime" v-model="formitem2.opentime" format="yyyy-MM-dd HH:mm" placeholder="Select date and time(Excluding seconds)" style="width: 200px"></DatePicker>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="12">
            <FormItem label="指定审核人:">
              <Select v-model="formitem2.assigned" filterable>
                <Option v-for="i in this.assigned" :value="i.value" :key="i.label">{{i.value}}</Option>
              </Select>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="12">
            <FormItem label="备注:">
              <Input v-model="formitem2.remark" type="textarea" :autosize="true" placeholder="Enter something..."></Input>
            </FormItem>
          </Col>
        </Row>
      </Form>


      <div slot="footer">
        <!--<Button type="warning" @click.native="test_button()">检测sql</Button>-->
        <Button type="error" @click="out_button()" :disabled="summit" v-if="seen">撤销</Button>
        <Button type="success" @click="put_newpc_button()" :disabled="summit" v-if="seen">保存</Button>
      </div>
    </Modal>
    <Modal v-model="moda6" width="1000" title="扩容工单编辑">
      <Form ref="formItem" :model="formitem1" :rules="ruleValidate" :label-width="150">
        <Row>
          <Col span="6">
            <FormItem label="归属项目:" prop="prject_name" required>
              <Select v-model="formitem1.project_name">
                <Option v-for="c in project_list" :key=c.value :value=c.value >{{ c.label }}</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="6">
            <FormItem label="环境:">
              <Select v-model="formitem1.env_name">
                <Option v-for="i in env_name_list" :value="i.value" :key="i.value">{{ i.label }}</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="6">
            <FormItem label="应用名称:">
              <Input v-model="formitem1.appname" placeholder="Enter something..." ></Input>
            </FormItem>
          </Col>

        </Row>
        <Row>
          <Col span="16">
            <FormItem label="系统/软件要求:">
              <Select v-model="formitem1.os_soft_need" multiple filterable>
                <Option v-for="i in os_soft_need_list" :key="i.value" :value="i.value" >{{ i.label }}</Option>
              </Select>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="6">
            <FormItem label="类型:">
              <Select v-model="formitem1.extend_type">
                <Option v-for="i in type_list" :value="i.value" :key="i.label">{{ i.label }}</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="6">
            <FormItem label="服务器数量:">
              <Input v-model="formitem1.servernum" placeholder="Enter something..." ></Input>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="6">
            <FormItem label="克隆原配置:">
              <Select v-model="formitem1.ghost_choice">
                <Option v-for="i in ghost_choicelist" :key="i.value" :value="i.value" >{{ i.label }}</Option>
              </Select>
            </FormItem>
          </Col>
        </Row>

        <Row>
          <Col span="12">
            <FormItem label="新配置为:">
              <Input v-model="formitem1.properties_change" placeholder="实例: 2核4G/系统盘60G/数据盘100G/峰值带宽10M" ></Input>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="12">
            <FormItem label="开通时间:">
              <DatePicker  v-model="formitem1.opentime" type="datetime" format="yyyy-MM-dd HH:mm" placeholder="Select date and time(Excluding seconds)" style="width: 200px"></DatePicker>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="12">
            <FormItem label="指定审核人:">
              <Select v-model="formitem1.assigned" filterable>
                <Option v-for="i in this.assigned" :value="i.value" :key="i.label">{{i.value}}</Option>
              </Select>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="12">
            <FormItem label="备注:">
              <Input v-model="formitem1.remark" type="textarea" :autosize="true" placeholder="Enter something..."></Input>
            </FormItem>
          </Col>
        </Row>
      </Form>
      <div slot="footer">
        <!--<Button type="warning" @click.native="test_button()">检测sql</Button>-->
        <Button type="error" v-if="seen" @click="out_button()" :disabled="summit">撤销</Button>
        <Button type="success" @click="put_extend_button()" :disabled="summit" v-if="seen">保存</Button>
      </div>
    </Modal>
    <Modal v-model="reject.reje" @on-ok="rejecttext">
      <p slot="header" style="color:#f60;font-size: 16px">
        <Icon type="information-circled"></Icon>
        <span>工单系统撤销说明</span>
      </p>
      <Input v-model="reject.textarea" type="textarea" :autosize="{minRows: 15,maxRows: 15}" placeholder="请填写撤销说明"></Input>
    </Modal>
    <Modal v-model="moda15"  width="1000" :closable="false" title="配置新增服务基础信息">
      <Form ref="formItem" :model="formitem" :rules="ruleValidate" :label-width="150">
                <Row>
                        <can-edit-table refs="table2" v-model="newserviceData" @selectObj="selectObj" :columns-list="jenkinsColumns"></can-edit-table>
                        <Icon type="plus" v-on:click="addline2"></Icon>
                </Row>
      </Form>
    </Modal>
  </div>
</template>
<script>
  import ICol from '../../../node_modules/iview/src/components/grid/col.vue'
  import axios from 'axios'
  import Cookies from 'js-cookie'
  import util from '../../libs/util'
  import tinymce from 'tinymce'
  import canEditTable from './components/canEditTable.vue'
  import tableData from './components/table_data.js'
  export default {
    components: {
      ICol,
      editor: require('../../libs/editor'),
      canEditTable
    },
    name: 'put',
    data () {
      return {
        file: [],
        uploadList: [],
        showCurrentTableData: false,
        tableData: [],
        Authorization: {Authorization: Cookies.get('jwt')},
        ghost_choicelist: [
          {
            value: 'yes',
            label: '是'
          },
          {
            value: 'no',
            label: '否'
          }
        ],
        columns6: [
          {
            title: '工单编号:',
            key: 'workid',
            sortable: true
          },
          {
            title: '工单说明',
            key: 'remark'
          },
          {
            title: '工单类型',
            key: 'type'
          },
          {
            title: '提交时间:',
            key: 'date',
            sortable: true
          },
          {
            title: '提交人',
            key: 'username',
            sortable: true
          },
          {
            title: '状态',
            key: 'status',
            render: (h, params) => {
              const row = params.row
              let color = ''
              let text = ''
              if (row.status === 2) {
                color = 'blue'
                text = '同意'
              } else if (row.status === 1) {
                color = 'red'
                text = '拒绝'
              } else if (row.status === 4) {
                color = 'red'
                text = '已撤销'
              } else if (row.status === 3) {
                color = 'yellow'
                text = '审核中'
              } else {
                color = 'green'
                text = '完成'
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
              value: 2
            },
              {
                label: '驳回',
                value: 1
              },
              {
                label: '审核中',
                value: 3
              },
              {
                label: '完成',
                value: 6
              }
            ],
            //            filterMultiple: false 禁止多选,
            filterMethod (value, row) {
              if (value === 1) {
                return row.status === 1
              } else if (value === 0) {
                return row.status === 0
              } else if (value === 2) {
                return row.status === 2
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
                    type: 'text',
                    icon: 'edit'
                  },
                  on: {
                    click: () => {
                      this.edit_tab(params.row.workid, params.row.type, params.row.status)
                    }
                  }
                })
              ])
            }
          }
        ],
        assigned: [{
          value: 'admin',
          label: 'admin'
        }],
        upstart_time: '',
        projectselect: '',
        newserviceData: [],
        addservice: '',
        sqlorderlist: [],
        moda15: false,
        value1: [],
        temp_mode_name_select: [],
        service: '',
        validate_gen: true,
        columnsList: [],
        editInlineColumns: [],
        editInlineData: [],
        editInlineData1: [],
        editIncellColumns: [],
        editIncellData: [],
        editInlineColumns1: [],
        editInlineAndCellColumn: [],
        editInlineAndCellData: [],
        showCurrentColumns: [],
        project_name: '',
        seen: false,
        id: null,
        reject: {
          reje: false,
          textarea: ''
        },
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
                                console.info(this.data6[params.index])
                                console.info(this.mode_name)
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
                                          console.info(this.data6)
                                            this.data6.splice(params.index, 1)
                                        }
                                    }
                                }, '删除')
                            ]);
                        }
                    }
                 ],
                 data6: [],
        formitem0: {
          workid: '',
          assigned: '',
          iteration_name: '',
          env_name: '',
          project_name: '',
          owner: '',
          remark: '',
          progress_name: '',
          sqlorder: '',
          updesc: '',
          versionvalue: '',
          state_em: '',
          upbak_time: '',
          progress_editor: '',
          addservice: '',
          date: ''
        },
        formitem2: {
          workid: '',
          project_name: '',
          env_name: '',
          domain_choice: '',
          OsDiskType: '',
          os_soft_need: [],
          owner: '',
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
          newpc_type: '',
          appname: ''
        },
        formitem1: {
          workid: '',
          project_name: '',
          env_name: '',
          opentime: '',
          owner: '',
          remark: '',
          os_soft_need: [],
          ghost_choice: '',
          properties_change: '',
          servernum: '',
          appname: '',
          extend_type: '',
          type: ''
        },
        item: {},
        iteration_list: [
          {
            value: 'upversion',
            label: '版本上线'
          },
          {
            value: 'upemergency',
            label: '紧急上线'
          },
          {
            value: 'upiteration',
            label: '迭代版本'
          }
        ],
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
        domain_choice_list: [
          {
            value: 'y',
            label: '是'
          },
          {
            value: 'n',
            label: '否'
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
        emergency_state_list: [
        {
          value: 'a',
          label: '一般'
        },
        {
          value: 'b',
          label: '紧急'
        },
        {
          value: 'c',
          label: '非常紧急'
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
        env_list: [
          {
            value: 'pro',
            label: '生产'
          },
          {
            value: 'pre',
            label: '预发布'
          }
        ],
        datalist: {
          connection_name_list: [],
          basenamelist: [],
          sqllist: [],
          projectlist: util.projectlist
        },
        moda0: false,
        moda1: false,
        moda2: false,
        moda5: false,
        moda8: false,
        moda6: false,
        moda9: false,
        moda7: false,
        columnsName: [
          {
            title: '编号',
            type: 'index',
            width: 60,
            align: 'center'
          },
          {
            title: '服务名称',
            key: 'servicename'
          },
          {
            title: '升级分支名称',
            key: 'branch'
          },
          {
            title: '回滚分支名称',
            key: 'backbranch'
          }
        ],
        ruleValidate: {
          basename: [{
            required: true,
            message: '数据库名不得为空',
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
        },
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
        sql: [],
        mode_name: [],
        dataId: [],
        dataId1: [],
        pagenumber: 1,
        computer_room: util.computer_room,
        applytable: [],
        openswitch: false,
        modaltext: {},
        editsql: ''
      }
    },
    watch: {
        'formitem0.updesc' (val) {
            // 当传入值变化时跟新富文本内容
            tinymce.get('articleEditor').setContent(val);
        }
    },
    methods: {
      projectChange (projectname) {
        console.info(projectname)
        this.projectselect = projectname
        let arrlist = []
        for (let [key, value] of this.mode_name[projectname].entries()) {
          console.info(key, Object.keys(value)[0])
          arrlist.push(Object.keys(value)[0])
          console.info(arrlist)
        }
        this.temp_mode_name_select = arrlist
        console.info(this.temp_mode_name_select)
      },
      getsqlorderlist () {
        axios.get(`${util.url}/sqllistinfo/`)
          .then(res => {
            if (res.data.data !== 'error') {
              this.sqlorderList = res.data.data
            } else {
              this.$Notice.error({
              title: '通知',
              desc: '读取sql审计平台工单号失败'
            })
            }
          })
          .catch(error => {
            util.ajanxerrorcode(this, error)
          })
      },
      newaddservice () {
        if (this.formitem0.project_name !== '') {
          if (this.formitem0.addservice === 'yes') {
          this.moda15 = true
        }
        } else {
          this.$Notice.error({
              title: '通知',
              desc: '请先选择项目'
            })
        }
      },
      addline () {
        console.info('888888888888888888888')
        console.info(this.temp_mode_name_select)
        console.info('888888888888888888888')
        this.data6.push({
          ordernum: '',
          modename: [],
          servicename: [],
          volumeTypes: [],
          servicenamelist: [],
          volumeType: []
        });
      },
      delectFile (keyID) { // 删除文件
        console.log(keyID)
        this.file = this.file.filter(item => {
          return item.keyID !== keyID
        })
        this.uploadList = this.uploadList.filter(item => {
          return item.keyID !== keyID
        })
      },
      put_newpc_button () {
        Cookies.get('user');
        console.info(JSON.stringify(this.formitem2));
        axios.put(`${util.url}/addnewpcorder/`, {
          'data': JSON.stringify(this.formitem2),
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
        this.moda8 = false;
        this.onload();
      },
      put_extend_button () {
        Cookies.get('user');
        console.info(JSON.stringify(this.formitem1));
        axios.put(`${util.url}/extendorder/`, {
          'data': JSON.stringify(this.formitem1),
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
        this.moda6 = false;
        this.onload();
      },
      put_online_button () {
        Cookies.get('user');
        this.formitem0.updesc = tinymce.activeEditor.getContent()
        console.info(JSON.stringify(this.formitem0));
        console.info(JSON.stringify(this.dataId));
        console.info(JSON.stringify(this.editInlineData1));
        console.info(this.newserviceData)
        axios.put(`${util.url}/onlineorder/`, {
          'data': JSON.stringify(this.formitem0),
          'uporder': JSON.stringify(this.data6),
          'config_properties': JSON.stringify(this.dataId1),
          'newserviceData': JSON.stringify(this.newserviceData),
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
        this.moda9 = false;
        this.onload();
      },
      addline2 () {
        if (Object.prototype.toString.call(this.newserviceData) === '[object String]') {
          this.newserviceData = []
        }
        this.newserviceData.push({
          projectname: this.formitem0.project_name,
          modename: '',
          servicename: '',
          volumeTypes: '',
          servicenamelist: '',
          volumeType: '',
          java_version: '',
          remark: ''
        });
      },
      addlinep () {
        // this.columnsList = tableData.table1Columns;
        // this.tableData = tableData.table1Data;
        // this.editInlineColumns = tableData.editInlineColumns;

        // this.editIncellColumns = tableData.editIncellColumns;
        this.dataId1.push({
          servicename: '',
          branch: '',
          backbranch: ''
        });
        // this.editInlineAndCellColumn = tableData.editInlineAndCellColumn;
        // this.editInlineAndCellData = tableData.editInlineAndCellData;
        // this.showCurrentColumns = tableData.showCurrentColumns;
      },
      getData () {
        this.columnsList = tableData.table1Columns;
        this.tableData = tableData.table1Data;
        this.editInlineColumns = tableData.editInlineColumns;
        this.editInlineColumns1 = tableData.editInlineColumns1;
        this.editInlineData = tableData.editInlineData;
        this.jenkinsColumns = tableData.jenkinsColumns;
        this.newserviceData = tableData.newserviceData;
        this.editInlineData1 = tableData.editInlineData1;
        this.editIncellColumns = tableData.editIncellColumns;
        this.editIncellData = tableData.editIncellData;
        this.editInlineAndCellColumn = tableData.editInlineAndCellColumn;
        this.editInlineAndCellData = tableData.editInlineAndCellData;
        this.showCurrentColumns = tableData.showCurrentColumns;
      },
      handleNetConnect (state) {
        this.breakConnect = state;
      },
      handleLowSpeed (state) {
        this.lowNetSpeed = state;
      },
      getCurrentData () {
        this.showCurrentTableData = true;
      },
      handleDel (val, index) {
        this.$Message.success('删除了第' + (index + 1) + '行数据');
      },
      handleCellChange (val, index, key) {
        this.$Message.success('修改了第 ' + (index + 1) + ' 行列名为 ' + key + ' 的数据');
      },
      handleChange (val, index) {
        this.$Message.success('修改了第' + (index + 1) + '行数据');
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
      ClearForm () {
        this.formItem.textarea = ''
      },
      out_button () {
        this.moda0 = false
        this.moda1 = false
        this.moda2 = false
        this.reject.reje = true
      },
      selectObj () {
        console.info('hhahahha')
        axios.get(`${util.url}/modelistinfoview/`)
          .then(res => {
            console.info(res.data.data)
            this.mode_name = res.data.data
            let arrlist = []
        for (let [key, value] of this.mode_name[this.project_name].entries()) {
          console.info(key, Object.keys(value)[0])
          arrlist.push(Object.keys(value)[0])
          console.info(arrlist)
        }
        this.temp_mode_name_select = arrlist
          })
          .catch(error => {
            util.ajanxerrorcode(this, error)
          })
      },
      rejecttext () {
        axios.put(`${util.url}/cancelorder/`, {
          'type': 4,
          'from_user': Cookies.get('user'),
          'text': this.reject.textarea,
          'to_user': 'admin',
          'workid': this.tmp_workid
        })
          .then(res => {
            this.$Notice.warning({
              title: res.data
            })
            this.getsqlorderlist()
            this.onload()
            this.moda8 = this.moda9 = this.moda6 = false
            this.$refs.page.currentPage = 1
          })
          .catch(error => {
            util.ajanxerrorcode(this, error)
          })
          this.onload();
      },
      currentpage (vl) {
        axios.get(`${util.url}/myorder/?user=${Cookies.get('user')}&page=${vl}`)
          .then(res => {
            this.applytable = res.data.data
            this.pagenumber = parseInt(res.data.page.alter_number)
          })
          .catch(error => {
            util.ajanxerrorcode(this, error)
          })
      },
      get_uploadfile (orderid) {
        axios.get(`${util.url}/fileupload?orderid=${orderid}`)
          .then(res => {
            console.info(res.data.data)
            this.mode_name = res.data.data
            this.uploadList = res.data.data
          })
          .catch(error => {
            util.ajanxerrorcode(this, error)
          })
      },
      onload () {
      axios.get(`${util.url}/myorder/?user=${Cookies.get('user')}&page=1`)
        .then(res => {
          this.applytable = res.data.data
          this.applytable.forEach((item) => {
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
      edit_button: function () {
        this.moda5 = true
      },
      edit_tab: function (workid, type, status) {
        if (status === 4) {
          this.seen = false
        } else if (status === 1) {
          this.seen = false
        } else if (status === 2) {
          this.seen = false
        } else {
          this.seen = true
        }

        axios.get(`${util.url}/myorder?workid=${workid}&username=${Cookies.get('user')}`)
          .then(res => {
            this.tmp_detail = res.data.data
            this.tmp_detail.forEach((item) => {
              if (type === '上线') {
                this.moda9 = true
                this.uploadList = this.$refs.upload.fileList;
                this.get_uploadfile(workid)
                this.formitem0.workid = item.workid
                this.tmp_workid = item.workid
                this.formitem0.iteration_name = item.iteration_name
                this.formitem0.env_name = item.env_name
                this.formitem0.project_name = item.project_name
                this.projectselect = item.project_name
                this.project_name = item.project_name
                // tinymce.activeEditor.setContent('')
                // tinymce.get('articleEditor').destroy();
                this.formitem0.updesc = item.updesc
                console.info(this.formitem0.updesc)
                this.$nextTick(() => {
                            this.$nextTick(() => {
                              tinymce.get('#articleEditor').destroy();
                            })
                            // tinymce.get('articleEditor').destroy();
                            tinymce.init({
                                selector: '#articleEditor',
                                setup: (editor) => {
                                  editor.on('init', () => {
                                    editor.setContent(this.formitem0.updesc);
                                  })
                                },
                                branding: false,
                                elementpath: false,
                                height: 300,
                                // language: 'zh_CN.GB2312',
                                menubar: 'edit insert view format table tools',
                                theme: 'modern',
                                plugins: [
                                    'advlist autolink lists link image charmap print preview hr anchor pagebreak imagetools',
                                    'searchreplace visualblocks visualchars code fullscreen fullpage',
                                    'insertdatetime media nonbreaking save table contextmenu directionality',
                                    'emoticons paste textcolor colorpicker textpattern imagetools codesample'
                                ],
                                toolbar1: ' newnote print fullscreen preview | undo redo | insert | styleselect | forecolor backcolor bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image emoticons media codesample',
                                autosave_interval: '20s',
                                image_advtab: true,
                                table_default_styles: {
                                    width: '100%',
                                    borderCollapse: 'collapse'
                                }
                            });
                        })
                console.info('hhhahhahah')
                console.info(tinymce.activeEditor.getContent())
                this.formitem0.service = item.service
                this.formitem0.versionvalue = item.versionvalue
                this.formitem0.state_em = item.state_em
                this.formitem0.upbak_time = item.upbak_time
                this.formitem0.upstart_time = item.upstart_time
                this.formitem0.owner = item.owner
                this.formitem0.type = '上线'
                this.formitem0.date = item.date
                this.formitem0.progress_editor = item.progress_editor
                this.formitem0.assigned = item.assigned
                this.formitem0.remark = item.remark
                this.formitem0.addservice = item.addservice
                this.addservice = item.addservice
                console.info('11111111111111111')
                console.info(item.config_properties)
                this.dataId1 = JSON.parse(item.config_properties)
                console.info(item.newserviceData)
                this.newserviceData = JSON.parse(item.newserviceData)
                if (item.sqlorder === '') {
                  this.formitem0.sqlorder = []
                } else {
                  this.formitem0.sqlorder = JSON.parse(item.sqlorder)
                }
                console.info(this.data6)
                console.info(this.newserviceData)
                console.info(item.uporder)
                // this.data6 = item.uporder
                console.info(item.uporder === '[]')
                this.data6 = JSON.parse(item.uporder)
                this.project_name = item.project_name
                let arrlist = []
        for (let [key, value] of this.mode_name[this.formitem0.project_name].entries()) {
          console.info(key, Object.keys(value)[0])
          arrlist.push(Object.keys(value)[0])
          console.info(arrlist)
        }
        console.info(typeof arrlist)
        this.temp_mode_name_select = arrlist
              } else if (type === '扩容') {
                this.moda6 = true
                this.tmp_workid = item.workid
                this.formitem1.workid = item.workid
                this.formitem1.project_name = item.project_name
                this.formitem1.env_name = item.env_name
                this.formitem1.opentime = item.opentime
                this.formitem1.os_soft_need = JSON.parse(item.os_soft_need)
                console.log(this.formitem1.os_soft_need);
                console.log(typeof this.formitem1.os_soft_need);
                console.log(this.os_soft_need_list);
                this.formitem1.ghost_choice = item.ghost_choice
                this.formitem1.properties_change = item.properties_change
                this.formitem1.appname = item.appname
                this.formitem1.servernum = item.servernum
                this.formitem1.owner = item.owner
                this.formitem1.date = item.date
                this.formitem1.assigned = item.assigned
                this.formitem1.extend_type = item.extend_type
                this.formitem1.remark = item.remark
                console.info(this.formitem1)
              } else {
                this.moda8 = true
                this.formitem2.workid = item.workid
                this.tmp_workid = item.workid
                this.formitem2.project_name = item.project_name
                this.formitem2.assigned = item.assigned
                this.formitem2.env_name = item.env_name
                this.formitem2.domain_choice = item.domain_choice
                this.formitem2.OsDiskType = item.OsDiskType
                this.formitem2.os_soft_need = JSON.parse(item.os_soft_need)
                console.info(typeof item.os_soft_need)
                this.formitem2.servernum = item.servernum
                this.formitem2.OsDiskSize = item.OsDiskSize
                this.formitem2.cpunum = item.cpunum
                this.formitem2.DataDiskSize = item.DataDiskSize
                this.formitem2.mem = item.mem
                this.formitem2.newpc_type = item.newpc_type
                this.formitem2.jdk_version = item.jdk_version
                this.formitem2.https_choice = item.https_choice
                this.formitem2.DataDiskType = item.DataDiskType
                this.formitem2.jvm_properties = item.jvm_properties
                this.formitem2.remark = item.remark
                this.formitem2.netbrand = item.netbrand
                this.formitem2.domain = item.domain
                this.formitem2.opentime = item.opentime
                this.formitem2.date = item.date
                this.formitem2.owner = item.owner
                this.formitem2.appname = item.appname
                item.type = '新增服务器'
              }
            })
          })
          .catch(error => {
            util.ajanxerrorcode(this, error)
          })
      }
    },
    created () {
      this.getData();
    },
    mounted () {
      this.getsqlorderlist()
      this.onload()
      axios.get(`${util.url}/modelistinfoview/`)
          .then(res => {
            console.info(res.data.data)
            this.mode_name = res.data.data
          })
          .catch(error => {
            util.ajanxerrorcode(this, error)
          })
      this.$nextTick(() => {
                            this.$nextTick(() => {
                              tinymce.get('#articleEditor').destroy();
                            })
                            // tinymce.get('articleEditor').destroy();
                            tinymce.init({
                                selector: '#articleEditor',
                                setup: (editor) => {
                                  editor.on('init', () => {
                                    editor.setContent(this.formitem0.updesc);
                                  })
                                },
                                branding: false,
                                elementpath: false,
                                height: 300,
                                // language: 'zh_CN.GB2312',
                                menubar: 'edit insert view format table tools',
                                theme: 'modern',
                                plugins: [
                                    'advlist autolink lists link image charmap print preview hr anchor pagebreak imagetools',
                                    'searchreplace visualblocks visualchars code fullscreen fullpage',
                                    'insertdatetime media nonbreaking save table contextmenu directionality',
                                    'emoticons paste textcolor colorpicker textpattern imagetools codesample'
                                ],
                                toolbar1: ' newnote print fullscreen preview | undo redo | insert | styleselect | forecolor backcolor bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image emoticons media codesample',
                                autosave_interval: '20s',
                                image_advtab: true,
                                table_default_styles: {
                                    width: '100%',
                                    borderCollapse: 'collapse'
                                }
                            });
                        })
    },
    destroyed () {
        tinymce.get('articleEditor').destroy();
    }
  }
</script>
<!-- remove delete request -->
