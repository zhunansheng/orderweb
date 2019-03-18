export const table1Columns = [
    {
        title: '升级顺序',
        type: 'index',
        width: 80,
        align: 'center'
    },
    {
        title: '服务名称',
        align: 'center',
        key: 'servicename',
        editable: true
    },
    {
        title: '升级分支名称',
        align: 'center',
        key: 'branch',
        editable: true
    },
    {
        title: '回滚分支名称',
        align: 'center',
        key: 'backbranch',
        editable: true
    },
    {
        title: '操作',
        align: 'center',
        width: 120,
        key: 'handle',
        handle: ['delete']
    }
];

export const table1Data = [
    {
        servicename: 'lisa',
        branch: 'hello',
        backbranch: '程序员鼓励师'
    }
];

export const editInlineColumns1 = [
  {
    title: '配置文件',
    align: 'center',
    key: 'config_properties',
    editable: true
  },
  {
    title: '程序文件',
    align: 'center',
    key: 'programname',
    editable: true
  },
  {
    title: '键',
    align: 'center',
    key: 'keyname',
    editable: true
  },
  {
    title: '值',
    align: 'center',
    key: 'valuename',
    editable: true
  },
  {
    title: '状态',
    align: 'center',
    key: 'statevalue',
    editable: true
  },
  {
    title: '操作',
    align: 'center',
    width: 190,
    key: 'handle',
    handle: ['edit', 'delete']
  }
];

export const jenkinsColumns = [
    {
        title: '编号',
        type: 'index',
        width: 100,
        align: 'center'
    },
    {
        title: '项目',
        key: 'projectname',
        width: 80,
        align: 'center'
    },
    {
        title: '模块名称',
        align: 'center',
        width: 90,
        key: 'modename',
        editable: true
    },
    {
        title: '服务名',
        align: 'center',
        width: 90,
        key: 'servicename',
        editable: true
    },
    {
        title: 'git-ssh地址',
        align: 'center',
        width: 110,
        key: 'gitaddress',
        editable: true
    },
    {
        title: 'maven打包命令',
        align: 'center',
        width: 130,
        key: 'mavenpom',
        editable: true
    },
    {
        title: 'java版本',
        align: 'center',
        width: 90,
        key: 'java_version',
        editable: true
    },
    {
        title: '备注',
        align: 'center',
        key: 'remark',
        editable: true
    },
    {
        title: '操作',
        align: 'center',
        width: 190,
        key: 'handle',
        handle: ['edit', 'delete']
    }
];

export const editInlineColumns = [
    {
        title: '编号',
        type: 'index',
        width: 100,
        align: 'center'
    },
    {
        title: '模块',
        align: 'center',
        key: 'mode',
        editable: true
    },
    {
        title: '服务名称',
        align: 'center',
        key: 'servicename',
        editable: true
    },
    {
        title: '升级分支名称',
        align: 'center',
        key: 'action',
        render: (h, params) => {
            return h('Select', {
                props: {
                    value: this.data[params.index].volumeType
                },
                on: {
                    'on-change': (event) => {
                        this.data[params.index].volumeType = event;
                    }
                }
            },
            [
                h('Option', {
                    props: {
                        value: '1'
                    }
                }, 'option1'),
                h('Option', {
                    props: {
                        value: '2'
                    }
                }, 'option2')
            ]
            );
        }
    },
    {
        title: '回滚分支名称',
        align: 'center',
        key: 'backbranch',
        editable: true
    },
    {
        title: '操作',
        align: 'center',
        width: 190,
        key: 'handle',
        handle: ['edit', 'delete']
    }
];

export const editInlineData = [
  {
    servicename: '',
    branch: '',
    backbranch: ''
  }
];
export const editInlineData1 = [
  {
    config_properties: '',
    programname: '',
    keyname: '',
    valuename: '',
    statevalue: ''
  }
];
export const newserviceData = [];

export const editIncellColumns = [
    {
        title: '序号',
        type: 'index',
        width: 80,
        align: 'center'
    },
    {
        title: '姓名',
        align: 'center',
        key: 'name',
        width: 120,
        editable: true
    },
    {
        title: '性别',
        align: 'center',
        key: 'sex'
    },
    {
        title: '岗位',
        align: 'center',
        width: 160,
        key: 'work',
        editable: true
    },
    {
        title: '操作',
        align: 'center',
        width: 120,
        key: 'handle',
        handle: ['delete']
    }
];

export const editIncellData = [
  {
    servicename: 'lisa',
    branch: 'hello',
    backbranch: '程序员鼓励师'
  }
];

export const editInlineAndCellColumn = [
    {
        title: '序号',
        type: 'index',
        width: 80,
        align: 'center'
    },
    {
        title: '姓名',
        align: 'center',
        key: 'name',
        width: 300,
        editable: true
    },
    {
        title: '性别',
        align: 'center',
        key: 'sex'
    },
    {
        title: '岗位',
        align: 'center',
        width: 300,
        key: 'work',
        editable: true
    },
    {
        title: '操作',
        align: 'center',
        width: 200,
        key: 'handle',
        handle: ['edit', 'delete']
    }
];

export const editInlineAndCellData = [
    {
        name: 'Aresn',
        sex: '男',
        work: '前端开发'
    },
    {
        name: 'Lison',
        sex: '男',
        work: '前端开发'
    },
    {
        name: 'lisa',
        sex: '女',
        work: '程序员鼓励师'
    }
];

export const showCurrentColumns = [
    {
        title: '序号',
        type: 'index',
        width: 80,
        align: 'center'
    },
    {
        title: '姓名',
        align: 'center',
        key: 'name',
        width: 300,
        editable: true
    },
    {
        title: '性别',
        align: 'center',
        key: 'sex'
    },
    {
        title: '岗位',
        align: 'center',
        width: 300,
        key: 'work',
        editable: true
    }
];

const tableData = {
    table1Columns: table1Columns,
    table1Data: table1Data,
    jenkinsColumns: jenkinsColumns,
    editInlineColumns: editInlineColumns,
    editInlineColumns1: editInlineColumns1,
    editInlineData1: editInlineData1,
    editInlineData: editInlineData,
    newserviceData: newserviceData,
    editIncellColumns: editIncellColumns,
    editIncellData: editIncellData,
    editInlineAndCellColumn: editInlineAndCellColumn,
    editInlineAndCellData: editInlineAndCellData,
    showCurrentColumns: showCurrentColumns
};

export default tableData;
