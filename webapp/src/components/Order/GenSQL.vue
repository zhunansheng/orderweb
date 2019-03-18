<style lang="less">
    @import './common.less';
    @import './article-publish.less';
    @import 'upload.less';
</style>
<template>
  <div>
    <Row>
      <Col span="24">
        <Card style="min-height: 1000px;">
          <div class="step-header-con">
          <h3>上线</h3>
          <h5>欢迎你</h5>
        </div>
        <p class="step-content"></p>
        <br>
        <Row v-if="current === 3">
          <i-col span="24">
            <Alert type="success" show-icon>
              提交成功:
              <span slot="desc">
              已完成提交，请在我的工单里面查看
            </span>
            </Alert>
          </i-col>
        </Row>
        <Row v-if="current !== 3">
          <i-col span="18" v-if="current !== 3">
            <Form ref="formItem" :model="formItem" :rules="ruleValidate" :label-width="150">
                <Row v-if="current === 0">

                    <FormItem label="升级类型:" prop="iteration_name">
                      <Col span="6">
                        <Select v-model="formItem.iteration_name">
                          <Option v-for="a in iteration_list" :key=a.label :value=a.value >{{ a.label }}</Option>
                        </Select>
                      </Col>
                    </FormItem>
                    <FormItem label="环境说明" prop="env_name">
                      <Col span="6">
                        <Select v-model="formItem.env_name">
                          <Option v-for="b in env_list" :key=b.label :value=b.value >{{ b.label }}</Option>
                        </Select>
                      </Col>
                      </FormItem>
                       <FormItem label="归属项目" prop="project_name">
                      <Col span="6">
                        <Select v-model="formItem.project_name" @on-change="projectChange(formItem.project_name)">
                          <Option v-for="c in project_list" :key=c.label :value=c.value >{{ c.label }}</Option>
                        </Select>
                      </Col>
                      </FormItem>


                </Row>
                <Row v-if="current === 0">
                  <Col span="6">
                    <FormItem label="升级时间:" prop="upstart_time">
                      <DatePicker type="datetime" v-model="formItem.upstart_time" format="yyyy-MM-dd HH:mm" placeholder="" style="width: 200px"></DatePicker>
                    </FormItem>
                  </Col>
                </Row>
                <Row v-if="current === 0">
                  <Col span="6">
                    <FormItem label="回退时间:" prop="upbak_time">
                      <DatePicker type="datetime" v-model="formItem.upbak_time" format="yyyy-MM-dd HH:mm" placeholder="" style="width: 200px"></DatePicker>
                    </FormItem>
                  </Col>
                </Row>
                <Row v-if="current === 0">
                  <Col span="6">
                    <FormItem label="升级版本:" prop="versionvalue">
                      <Input  v-model="formItem.versionvalue" placeholder="" ></Input>
                    </FormItem>
                  </Col>
                </Row>
                <Row v-if="current === 0">
                  <Col span="6">
                    <FormItem label="紧急程度:" prop="state_em">
                      <Select v-model="formItem.state_em">
                          <Option v-for="b in emergency_state_list" :key=b.label :value=b.value >{{ b.label }}</Option>
                        </Select>
                    </FormItem>
                  </Col>
                </Row>
                <Row v-if="current === 0">
                  <Col span="8">
                    <FormItem label="本次新增服务:">
                      <RadioGroup v-model="formItem.addservice"  @on-change="newaddservice">
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
                <Row v-if="current === 1">
                  <Col span="24">
                    <FormItem label="sql审计工单号:">
                      <Select v-model="formItem.sqlorder" multiple>
                      <Option v-for="item in sqlorderList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                      </Select>
                    </FormItem>
                  </Col>
                </Row>
                <Row v-if="current === 1">
                  <Col span="24">
                    <FormItem label="升级顺序">
                      <Button type="success" icon="plus" style="margin-bottom: 5px;" size="small" v-on:click="addline">增加一行</Button>
                      <Table border :columns="columns7" :data="data6"></Table>
                    </FormItem>
                  </Col>
                </Row>
                <Row v-if="current === 1">
                  <Col span="24">
                    <FormItem label="配置中心">
                      <Button type="success" icon="plus" style="margin-bottom: 5px;" size="small" v-on:click="addline1">增加一行</Button>
                      <can-edit-table refs="table2" v-model="editInlineData1" :columns-list="editInlineColumns1" style="padding-bottom: 20px;"></can-edit-table>
                    </FormItem>
                  </Col>
                </Row>
                <Row v-if="current === 0">
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
                      <div v-for="(item, index) in uploadList">待上传文件:  {{ item.name }}
                        <a style="margin-left: 40px;" href="javascript:;"  @click="delectFile(item.keyID)">删除</a>
                      </div>
                    </div>
                  </FormItem>
                </Row>
                <Row v-if="current === 2">
                  <Col span="12">
                    <FormItem label="指定审核人:">
              <Select v-model="formItem.assigned" filterable>
                <Option v-for="i in this.audit_list" :value="i.value" :key="i.label">{{i.value}}</Option>
              </Select>
            </FormItem>
                  </Col>
                </Row>
                <Row v-if="current === 2">
                  <Col span="12">
                    <FormItem label="开发人员:">
                      <Input v-model="formItem.progress_editor" type="textarea" :autosize="true" placeholder=""></Input>
                    </FormItem>
                  </Col>
                </Row>
                <Row v-if="current === 2">
                  <Col span="20">
                    <FormItem label="升级描述:">
                      <textarea id="articleEditor" v-html="formItem.updesc"></textarea>
                    </FormItem>
                  </Col>
                </Row> 
                <Row v-if="current === 2">
                  <Col span="12">
                    <FormItem label="其它说明:">
                      <Input v-model="formItem.remark" type="textarea" :autosize="true" placeholder=""></Input>
                    </FormItem>
                  </Col>
                </Row>
              </Form>
          </i-col>
          <i-col span="5" offset="1">
            <Alert type="warning" show-icon>
              注意事项:
              <span slot="desc">
              1.必须选择项目后，才能使用新增服务，以及配置升级顺序 
              <br>
              2.必须选择升级和回退时间 
              <br>
              3.配置中心记得点击保存按钮
              <br>
              4.支持管理未同意或驳回情况下修改，撤销
              <br>
              5.目前只支持admin审核
            </span>
            </Alert>
          </i-col>
        </Row>
        <br>
            
        </Card>
      </Col>
    </Row>
    <Row>
      <i-col span="24">
      <div style="background: rgba(255, 255, 255, 1);position:fixed; bottom: 0px;;height:100px;z-index: 99999999;width: 100%">
    <Button type="primary" @click="up"  style="position:fixed; bottom: 60px; margin-left: 35%" v-if="current === 1">上一步</Button>
        <Button type="primary" @click="up"  style="position:fixed; bottom: 60px; margin-left: 35%" v-else-if="current === 2">上一步</Button>
        <Button type="primary" style="position:fixed; bottom: 60px; margin-left: 35%" disabled v-if="current === 0">上一步</Button>
        <Button type="primary" @click="next"  style="position:fixed; bottom: 60px; margin-left: 40%" v-if="current === 0">下一步</Button>
        <Button type="primary" @click="next"  style="position:fixed; bottom: 60px; margin-left: 40%" v-if="current === 1">下一步</Button>
        <Button type="success" icon="ios-redo" @click.native="commitorder" style="position:fixed; bottom: 60px; margin-left: 40%" v-if="current === 2">提交</Button>
        <Button type="success" icon="ios-redo" @click.native="next" style="position:fixed; bottom: 65px; margin-left: 45%" v-if="current === 3">再提一单</Button>
    <Steps :current="current" style="position:fixed; bottom: 10px;">
        <Step title="基础信息配置" content="配置项目的基础信息"></Step>
        <Step title="流程配置" content="流程信息"></Step>
        <Step title="人员配置" content="配置人员信息"></Step>
        <Step title="完成" content="点击提交即可完成"></Step>
    </Steps>
    </div>
      </i-col>
    </Row>
    <Modal v-model="moda9"  width="1000" :closable="false" title="配置新增服务基础信息">
      <Form ref="formItem" :model="formItem" :rules="ruleValidate" :label-width="150">
                <Row>
                  <Button type="success" icon="plus" style="margin-bottom: 5px;" size="small" v-on:click="addline2">增加一行</Button>
                        <can-edit-table refs="table2" @selectObj="selectObj" v-model="newserviceData" :columns-list="jenkinsColumns"></can-edit-table>
                </Row>
      </Form>
    </Modal>
  </div>
</template>

<script>
  import ICol from '../../../node_modules/iview/src/components/grid/col.vue'
  import axios from 'axios'
  import tinymce from 'tinymce'
  import Cookies from 'js-cookie'
  import util from '../../libs/util'
  import canEditTable from './components/canEditTable.vue'
  import tableData from './components/table_data.js'
  export default {
    components: {
      ICol,
      editor: require('../../libs/editor'),
      canEditTable
    },
    name: 'artical-publish',
    data () {
      return {
        file: [],
        orderid: '',
        Authorization: {Authorization: Cookies.get('jwt')},
        defaultList: [
            ],
            imgName: '',
            visible: false,
            uploadList: [],
        articleTitle: '',
            articleError: '',
            showLink: false,
            fixedLink: '',
            articlecontent: '<p>haha</p>',
            articlePath: '',
            articlePathHasEdited: false,
            editLink: false,
            editPathButtonType: 'ghost',
            editPathButtonText: '编辑',
            articleStateList: [{value: '草稿'}, {value: '等待复审'}],
            editOpenness: false,
            Openness: '公开',
            currentOpenness: '公开',
            topArticle: false,
            publishTime: '',
            publishTimeType: 'immediately',
            editPublishTime: false, // 是否正在编辑发布时间
            articleTagSelected: [], // 文章选中的标签
            articleTagList: [], // 所有标签列表
            classificationList: [],
            classificationSelected: [], // 在所有分类目录中选中的目录数组
            offenUsedClass: [],
            offenUsedClassSelected: [], // 常用目录选中的目录
            classificationFinalSelected: [], // 最后实际选择的目录
            publishLoading: false,
            addingNewTag: false, // 添加新标签
            newTagName: '', // 新建标签名
        value1: [],
        assigned: [{
          value: 'admin',
          label: 'admin'
        }],
        service: '',
        validate_gen: true,
        columnsList: [],
        tableData: [],
        editInlineColumns: [],
        editInlineData: [],
        newserviceData: [],
        editInlineData1: [],
        editIncellColumns: [],
        editIncellData: [],
        editInlineColumns1: [],
        editInlineAndCellColumn: [],
        editInlineAndCellData: [],
        showCurrentColumns: [],
        sqlorderList: [
                    {
                        value: 'New York',
                        label: 'New York'
                    },
                    {
                        value: 'London',
                        label: 'London'
                    },
                    {
                        value: 'Sydney',
                        label: 'Sydney'
                    },
                    {
                        value: 'Ottawa',
                        label: 'Ottawa'
                    },
                    {
                        value: 'Paris',
                        label: 'Paris'
                    },
                    {
                        value: 'Canberra',
                        label: 'Canberra'
                    }
                ],
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
                                      console.info(this.data6)
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
                                   axios.get(`${util.url}/gitlabinfo?modename=${this.data6[params.index]['modename']}&servicename=${this.data6[params.index]['servicename']}&env_name=${this.formItem.env_name}`)
                                    .then(res => {
                                    console.info(res.data)
                                    if (res.data.data !== 'error') {
                                      this.data6[params.index].volumeTypes = res.data.data
                                    } else {
                                      this.data6[params.index].volumeTypes = ['无']
                                      this.$Notice.error({
                                         title: '未找到分支号，请在gitlab上面尝试将该服务授权给clzaiops账号',
                                        desc: res.data.log
                                       });
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
                        title: 'Action',
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
                data6: [
                ],
                volumeTypes: ['1', '2'],
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
        adEdTableData: [
    {
        sort: '1',
        name: '纱线用途',
        values: [
            {
                value: '1',
                label: '1'
            },
            {
                value: '2',
                label: '2'
            }
        ]
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
        audit_list: [
          {
            value: 'admin',
            label: 'admin'
          }
        ],
        mode_name: [],
        current: 0,
        showCurrentTableData: false,
        temp_mode_name_select: [],
        projectselect: '',
        addservice: 'no',
        formItem: {
          emergency_state: '',
          iteration_name: '',
          env_name: 'pro',
          project_name: '',
          assigned: '',
          upstart_time: '',
          remark: '',
          progress_name: '',
          sqlorder: '',
          updesc: '',
          versionvalue: '',
          state_em: '',
          upbak_time: '',
          progress_editor: '',
          addservice: 'no'
        },
        Testresults: [],
        item: {},
        ruleValidate: {
          iteration_name: [{
            required: true,
            message: '数据库名不得为空',
            trigger: 'change'
          }],
          env_name: [{
            required: true,
            message: '说明不得为空',
            trigger: 'blur'
          }
          ],
          project_name: [{
            required: true,
            message: '说明不得为空',
            trigger: 'blur'
          }],
          progress_editor: [{
            required: true,
            message: '开发人员不得为空',
            trigger: 'blur'
          }
          ],
          upstart_time: [{
            type: 'date',
            required: true,
            message: '开始时间不能为空',
            trigger: 'change'
          }],
          upbak_time: [{
            type: 'date',
            required: true,
            message: '回退时间不能为空',
            trigger: 'change'
          }],
          versionvalue: [{
            required: true,
            message: '升级版本不能为空',
            trigger: 'blur'
          }],
          state_em: [{
            required: true,
            message: '说明不得为空',
            trigger: 'blur'
          }],
          updesc: [{
            required: true,
            message: '升级描述不能为空',
            trigger: 'blur'
          }]
        },
        id: null,
        moda9: false,
        value7: null,
        remark: null
      }
    },
    methods: {
        handleArticletitleBlur () {
            if (this.articleTitle.length !== 0) {
                // this.articleError = '';
                localStorage.articleTitle = this.articleTitle; // 本地存储文章标题
                if (!this.articlePathHasEdited) {
                    let date = new Date();
                    let year = date.getFullYear();
                    let month = date.getMonth() + 1;
                    let day = date.getDate();
                    this.fixedLink = window.location.host + '/' + year + '/' + month + '/' + day + '/';
                    this.articlePath = this.articleTitle;
                    this.articlePathHasEdited = true;
                    this.showLink = true;
                }
            } else {
                // this.articleError = '文章标题不可为空哦';
                this.$Message.error('文章标题不可为空哦');
            }
        },
        editArticlePath () {
            this.editLink = !this.editLink;
            this.editPathButtonType = this.editPathButtonType === 'ghost' ? 'success' : 'ghost';
            this.editPathButtonText = this.editPathButtonText === '编辑' ? '完成' : '编辑';
        },
        handleEditOpenness () {
            this.editOpenness = !this.editOpenness;
        },
        handleSaveOpenness () {
            this.Openness = this.currentOpenness;
            this.editOpenness = false;
        },
        cancelEditOpenness () {
            this.currentOpenness = this.Openness;
            this.editOpenness = false;
        },
        handleEditPublishTime () {
            this.editPublishTime = !this.editPublishTime;
        },
        handleSavePublishTime () {
            this.publishTimeType = 'timing';
            this.editPublishTime = false;
        },
        cancelEditPublishTime () {
            this.publishTimeType = 'immediately';
            this.editPublishTime = false;
        },
        setPublishTime (datetime) {
            this.publishTime = datetime;
        },
        setClassificationInAll (selectedArray) {
            this.classificationFinalSelected = selectedArray.map(item => {
                return item.title;
            });
            localStorage.classificationSelected = JSON.stringify(this.classificationFinalSelected); // 本地存储所选目录列表
        },
        setClassificationInOffen (selectedArray) {
            this.classificationFinalSelected = selectedArray;
        },
        handleAddNewTag () {
            this.addingNewTag = !this.addingNewTag;
        },
        createNewTag () {
            if (this.newTagName.length !== 0) {
                this.articleTagList.push({value: this.newTagName});
                this.addingNewTag = false;
                setTimeout(() => {
                    this.newTagName = '';
                }, 200);
            } else {
                this.$Message.error('请输入标签名');
            }
        },
        cancelCreateNewTag () {
            this.newTagName = '';
            this.addingNewTag = false;
        },
        canPublish () {
            if (this.articleTitle.length === 0) {
                this.$Message.error('请输入文章标题');
                return false;
            } else {
                return true;
            }
        },
        handlePreview () {
            if (this.canPublish()) {
                if (this.publishTimeType === 'immediately') {
                    let date = new Date();
                    let year = date.getFullYear();
                    let month = date.getMonth() + 1;
                    let day = date.getDate();
                    let hour = date.getHours();
                    let minute = date.getMinutes();
                    let second = date.getSeconds();
                    localStorage.publishTime = year + ' 年 ' + month + ' 月 ' + day + ' 日 -- ' + hour + ' : ' + minute + ' : ' + second;
                } else {
                    localStorage.publishTime = this.publishTime; // 本地存储发布时间
                }
                localStorage.content = tinymce.activeEditor.getContent();
                console.log(tinymce.activeEditor.getContent())
                this.$router.push({
                    name: 'preview'
                });
            }
        },
        handleSaveDraft () {
            if (!this.canPublish()) {
                //
            }
        },
        handlePublish () {
            if (this.canPublish()) {
                this.publishLoading = true;
                console.info(tinymce.activeEditor.getContent())
                setTimeout(() => {
                    this.publishLoading = false;
                    this.$Notice.success({
                        title: '保存成功',
                        desc: '文章《' + this.articleTitle + '》保存成功'
                    });
                }, 1000);
            }
        },
        handleSelectTag () {
            localStorage.tagsList = JSON.stringify(this.articleTagSelected); // 本地存储文章标签列表
        },
      projectChange (projectname) {
        console.info(projectname)
        if (this.projectselect !== '') {
          this.$Notice.error({
              title: '警告！！！！',
              desc: '修改了项目，请确认升级顺序里面的模块和服务是否属于该项目'
            })
        }
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
      handleUpload (file) { // 保存需要上传的文件
        let keyID = Math.random().toString().substr(2);
        file['keyID'] = keyID;
        this.file.push(file);
        this.uploadList.push(file)
        console.info(this.uploadList)
        return false;
      },
      delectFile (keyID) { // 删除文件
          console.log(keyID);
        this.file = this.file.filter(item => {
          return item.keyID !== keyID
        })
        this.uploadList = this.uploadList.filter(item => {
          return item.keyID !== keyID
        })
      },
      // handleUpload (file) {
      //   for (let index of file.name.split('\n')) {
      //     var dic = {};
      //     dic['name'] = index
      //     this.defaultList.push(dic)
      //   }
      //   return false;
      // },

      show (index) {
                this.$Modal.info({
                    title: 'User Info',
                    content: `Name：${this.data6[index].name}<br>Age：${this.data6[index].age}<br>Address：${this.data6[index].address}`
                })
            },
            remove (index) {
                this.data6.splice(index, 1);
            },
      newaddservice () {
        console.info(this.addservice)
        if (this.formItem.project_name !== '') {
          if (this.formItem.addservice === 'yes') {
          this.moda9 = true
        }
        } else {
          this.$Notice.error({
              title: '通知',
              desc: '请先选择项目'
            })
        }
      },
      commitorder () {
        if (this.formItem.progress_editor === '' | this.formItem.projectname === '' | this.formItem.upstart_time === '' | this.formItem.upbak_time === '' | this.formItem.iteration_name === '' | this.formItem.progress_editor === '' | this.formItem.assigned === '') {
          this.$Notice.error({
              title: '通知',
              desc: '请填写完必填项目才能提交！！！'
            })
        } else {
          Cookies.get('user');
          this.formItem.updesc = tinymce.activeEditor.getContent()
        console.info(JSON.stringify(this.formItem));
        console.info(JSON.stringify(this.editInlineData));
        console.info(JSON.stringify(this.editInlineData1));
        axios.post(`${util.url}/onlineorder/`, {
          'data': JSON.stringify(this.formItem),
          'uporder': JSON.stringify(this.data6),
          'newserviceData': JSON.stringify(this.newserviceData),
          'config_properties': JSON.stringify(this.editInlineData1),
          'user': Cookies.get('user')
        })
          .then(res => {
            this.$Notice.success({
              title: '通知',
              desc: '正在上传附件....'
            })
            this.orderid = res.data.orderid
            this.upload()
            // this.$router.push({
            //   name: 'myorder'
            // })
          }).catch(error => {
          util.ajanxerrorcode(this, error)
        })
        }
      },
      addline () {
        this.data6.push({
          ordernum: '',
          modename: '',
          servicename: '',
          volumeTypes: [],
          servicenamelist: [],
          volumeType: []
        });
      },
      up () {
              this.current -= 1;
              if (this.current !== 2) {
                  this.$nextTick(() => {
                        tinymce.get('articleEditor').destroy();
                        })
              }
            },
      next () {
                if (this.current === 3) {
                    this.current = 0;
                } else {
                    this.current += 1;
                    if (this.current === 2) {
                        this.$nextTick(() => {
                            tinymce.init({
                                selector: '#articleEditor',
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
                    } else {
                        this.$nextTick(() => {
                        tinymce.get('articleEditor').destroy();
                        })
                    }
                }
        },
      addline1 () {
        this.editInlineData1.push({
          servicename: '',
          branch: '',
          backbranch: ''
        });
      },
      selectObj () {
        console.info('hhahahha')
        axios.get(`${util.url}/modelistinfoview/`)
          .then(res => {
            console.info(res.data.data)
            this.mode_name = res.data.data
            let arrlist = []
            console.info(this.project_name)
        for (let [key, value] of this.mode_name[this.formItem.project_name].entries()) {
          console.info(key, Object.keys(value)[0])
          arrlist.push(Object.keys(value)[0])
          console.info(arrlist)
        }
        this.temp_mode_name_select = arrlist
        console.info(this.temp_mode_name_select)
          })
          .catch(error => {
            util.ajanxerrorcode(this, error)
          })
      },
      addline2 () {
        this.newserviceData.push({
          projectname: this.formItem.project_name,
          modename: '',
          servicename: '',
          volumeTypes: '',
          servicenamelist: '',
          volumeType: '',
          java_version: '',
          remark: ''
        });
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
      getData () {
        this.columnsList = tableData.table1Columns;
        this.tableData = tableData.table1Data;
        this.editInlineColumns = tableData.editInlineColumns;
        this.jenkinsColumns = tableData.jenkinsColumns;
        this.editInlineColumns1 = tableData.editInlineColumns1;
        this.newserviceData = tableData.newserviceData;
        this.editInlineData = tableData.editInlineData;
        this.editInlineData1 = tableData.editInlineData1;
        this.editIncellColumns = tableData.editIncellColumns;
        this.editIncellData = tableData.editIncellData;
        this.editInlineAndCellColumn = tableData.editInlineAndCellColumn;
        this.editInlineAndCellData = tableData.editInlineAndCellData;
        this.showCurrentColumns = tableData.showCurrentColumns;
      },
      handleRemove (file) {
        const fileList = this.$refs.upload.fileList;
        this.$refs.upload.fileList.splice(fileList.indexOf(file), 1);
        console.info(fileList)
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
      upload () { // 上传文件
        if (this.uploadList.length === 0) {
          this.$Message.error('未选择上传文件')
          return false
        }
        for (let i = 0; i < this.uploadList.length; i++) {
          let data = new FormData();
          data.append('file', this.uploadList[i])
          data.append('orderid', this.orderid)
          axios.post('http://120.27.192.237:9090/fileupload/', data).then(
            res => {
              if (res.data.status === 'success') {
                this.$Notice.success({
                  title: '上传成功',
                  desc: this.uploadList[i].name
                })
              } else {
                this.$Notice.error({
                  title: '上传失败',
                  desc: this.uploadList[i].name + 'errorlog' + res.data.log
                })
              }
            }
          )
          // let item = this.file[i]
          // this.$refs.upload.post(item);
        }
        this.$router.push({
          name: 'myorder'
        })
      },
      uploadSuccess (response, file, fileList) { // 文件上传回调 上传成功后删除待上传文件
        console.log(response) // 后端返回数据
        console.log(file)   // 当前上传文件
        console.log(fileList) // 整个input file 里的文件数组
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
      }
    },
    created () {
      this.getData();
    },
    mounted () {
      this.uploadList = this.$refs.upload.fileList;
      console.info(this.uploadList)
      this.articleTagList = [
            {value: 'vue'},
            {value: 'iview'},
            {value: 'ES6'},
            {value: 'webpack'},
            {value: 'babel'},
            {value: 'eslint'}
        ];
        this.classificationList = [
            {
                title: 'Vue实例',
                expand: true,
                children: [
                    {
                        title: '数据与方法',
                        expand: true
                    },
                    {
                        title: '生命周期',
                        expand: true
                    }
                ]
            },
            {
                title: 'Class与Style绑定',
                expand: true,
                children: [
                    {
                        title: '绑定HTML class',
                        expand: true,
                        children: [
                            {
                                title: '对象语法',
                                expand: true
                            },
                            {
                                title: '数组语法',
                                expand: true
                            },
                            {
                                title: '用在组件上',
                                expand: true
                            }
                        ]
                    },
                    {
                        title: '生命周期',
                        expand: true
                    }
                ]
            },
            {
                title: '模板语法',
                expand: true,
                children: [
                    {
                        title: '插值',
                        expand: true
                    },
                    {
                        title: '指令',
                        expand: true
                    },
                    {
                        title: '缩写',
                        expand: true
                    }
                ]
            }
        ];
        this.offenUsedClass = [
            {
                title: 'vue实例'
            },
            {
                title: '生命周期'
            },
            {
                title: '模板语法'
            },
            {
                title: '插值'
            },
            {
                title: '缩写'
            }
        ];
      this.assigned = 'admin'
      this.addline()
      this.getsqlorderlist()
      axios.get(`${util.url}/modelistinfoview/`)
          .then(res => {
            console.info(res.data.data)
            this.mode_name = res.data.data
          })
          .catch(error => {
            util.ajanxerrorcode(this, error)
          })
    }
  }
</script>
<style lang="less">
  .step {
    &-header-con {
      text-align: center;
      h3 {
        margin: 10px 0;
      }
      h5 {
        margin: 0 0 5px;
      }
    }
    &-content {
      padding: 5px 20px 26px;
      margin-bottom: 20px;
      border-bottom: 1px solid #dbdddf;
    }
    &-form {
      padding-bottom: 10px;
      border-bottom: 1px solid #dbdddf;
      margin-bottom: 20px;
    }
  }
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
