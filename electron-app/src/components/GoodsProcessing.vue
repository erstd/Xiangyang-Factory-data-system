<template>
  <div class="goods-processing">
    <!-- 搜索区域 -->
    <el-card class="search-card" shadow="never">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="货物类型">
          <el-select
            v-model="searchForm.goodsType"
            placeholder="全部"
            style="width: 120px"
            @change="loadData"
          >
            <el-option label="全部" value="" />
            <el-option label="织纱" value="织纱" />
            <el-option label="织片" value="织片" />
          </el-select>
        </el-form-item>

        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.keyword"
            placeholder="搜索客户名称/款号..."
            style="width: 240px"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 操作按钮 -->
    <el-card class="action-card" shadow="never">
      <el-button type="success" @click="handleAdd">新增记录</el-button>
      <el-button type="warning" @click="handleEdit">修改记录</el-button>
      <el-button
        type="danger"
        :disabled="!canDelete"
        @click="handleDelete"
      >
        删除记录
      </el-button>
    </el-card>

    <!-- 数据表格 -->
    <el-card class="table-card" shadow="never">
      <el-table
        :data="tableData"
        stripe
        border
        height="calc(100vh - 420px)"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="goods_type" label="类型" width="80" />
        <el-table-column prop="customer_name" label="客户名称" width="150" />
        <el-table-column prop="customer_style_no" label="客户款号" width="130" />
        <el-table-column prop="customer_send_qty" label="客户发货量" width="110" align="right" />
        <el-table-column prop="factory_receive_qty" label="工厂收货量" width="110" align="right" />
        <el-table-column prop="diff_receive" label="收发差异" width="100" align="right">
          <template #default="{ row }">
            <span :style="{ color: getDiffColor(row.diff_receive) }">
              {{ row.diff_receive }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="factory_send_qty" label="工厂出货量" width="110" align="right" />
        <el-table-column prop="customer_receive_qty" label="客户收货量" width="110" align="right" />
        <el-table-column prop="diff_factory_customer" label="厂客差异" width="100" align="right">
          <template #default="{ row }">
            <span :style="{ color: getDiffColor(row.diff_factory_customer) }">
              {{ row.diff_factory_customer }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="modified_date" label="最后更新" width="160" />
        <el-table-column prop="modified_by" label="操作人" width="100" />
      </el-table>

      <!-- 统计信息 -->
      <div class="statistics">
        <el-tag type="info">总客户发货: {{ statistics.totalCustomerSend }}</el-tag>
        <el-tag type="info">总工厂收货: {{ statistics.totalFactoryReceive }}</el-tag>
        <el-tag :type="statistics.totalDiffReceive !== 0 ? 'warning' : 'success'">
          总收发差异: {{ statistics.totalDiffReceive }}
        </el-tag>
        <el-tag type="info">总工厂出货: {{ statistics.totalFactorySend }}</el-tag>
        <el-tag type="info">总客户收货: {{ statistics.totalCustomerReceive }}</el-tag>
        <el-tag :type="statistics.totalDiffFactoryCustomer !== 0 ? 'warning' : 'success'">
          总厂客差异: {{ statistics.totalDiffFactoryCustomer }}
        </el-tag>
      </div>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="900px"
      @close="handleDialogClose"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
      >
        <!-- 货物类型 -->
        <el-form-item v-if="dialogMode === 'add'" label="货物类型" prop="goods_type">
          <el-select v-model="form.goods_type" placeholder="请选择">
            <el-option label="织纱" value="织纱" />
            <el-option label="织片" value="织片" />
          </el-select>
        </el-form-item>

        <!-- 客户发货信息 -->
        <el-divider content-position="left">📦 客户发货信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="客户名称" prop="customer_name">
              <el-input v-model="form.customer_name" placeholder="请输入客户名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="客户款号" prop="customer_style_no">
              <el-input v-model="form.customer_style_no" placeholder="请输入客户款号" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="发货时间" prop="customer_send_date">
              <el-date-picker
                v-model="form.customer_send_date"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="运输方式" prop="customer_send_method">
              <el-select v-model="form.customer_send_method" placeholder="请选择">
                <el-option label="快递" value="快递" />
                <el-option label="物流" value="物流" />
                <el-option label="自提" value="自提" />
                <el-option label="其他" value="其他" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="发货数量" prop="customer_send_qty">
              <el-input-number
                v-model="form.customer_send_qty"
                :min="0"
                style="width: 100%"
                @change="calculateDiff"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 工厂收货信息 -->
        <el-divider content-position="left">🏭 工厂收货信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="收货数量" prop="factory_receive_qty">
              <el-input-number
                v-model="form.factory_receive_qty"
                :min="0"
                style="width: 100%"
                @change="calculateDiff"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="收发差异">
              <el-input
                :model-value="diffReceive"
                readonly
                :style="{ color: getDiffColor(diffReceive) }"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 工厂出货信息 -->
        <el-divider content-position="left">🚚 工厂出货信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="出货时间" prop="factory_send_date">
              <el-date-picker
                v-model="form.factory_send_date"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="运输方式" prop="factory_send_method">
              <el-select v-model="form.factory_send_method" placeholder="请选择">
                <el-option label="快递" value="快递" />
                <el-option label="物流" value="物流" />
                <el-option label="自提" value="自提" />
                <el-option label="其他" value="其他" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="出货数量" prop="factory_send_qty">
              <el-input-number
                v-model="form.factory_send_qty"
                :min="0"
                style="width: 100%"
                @change="calculateDiff"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 客户收货信息 -->
        <el-divider content-position="left">✅ 客户收货信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="收货数量" prop="customer_receive_qty">
              <el-input-number
                v-model="form.customer_receive_qty"
                :min="0"
                style="width: 100%"
                @change="calculateDiff"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="厂客差异">
              <el-input
                :model-value="diffFactoryCustomer"
                readonly
                :style="{ color: getDiffColor(diffFactoryCustomer) }"
              />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { getGoodsList, addGoods, updateGoods, deleteGoods } from '@/api';
import { useUserStore } from '@/store/user';

const userStore = useUserStore();
const formRef = ref(null);
const dialogVisible = ref(false);
const dialogMode = ref('add');
const selectedRows = ref([]);
const tableData = ref([]);

const searchForm = reactive({
  goodsType: '',
  keyword: ''
});

const form = reactive({
  goods_type: '织纱',
  customer_name: '',
  customer_style_no: '',
  customer_send_date: '',
  customer_send_method: '快递',
  customer_send_qty: 0,
  factory_receive_qty: 0,
  factory_send_date: '',
  factory_send_method: '快递',
  factory_send_qty: 0,
  customer_receive_qty: 0
});

const rules = {
  customer_name: [
    { required: true, message: '请输入客户名称', trigger: 'blur' }
  ],
  customer_send_qty: [
    { required: true, message: '请输入发货数量', trigger: 'blur' }
  ]
};

const dialogTitle = computed(() => {
  return dialogMode.value === 'add' ? '新增货品记录' : '修改货品记录';
});

const canDelete = computed(() => {
  return userStore.isFinance && selectedRows.value.length > 0;
});

const diffReceive = computed(() => {
  return form.customer_send_qty - form.factory_receive_qty;
});

const diffFactoryCustomer = computed(() => {
  return form.factory_send_qty - form.customer_receive_qty;
});

const statistics = computed(() => {
  const stats = {
    totalCustomerSend: 0,
    totalFactoryReceive: 0,
    totalDiffReceive: 0,
    totalFactorySend: 0,
    totalCustomerReceive: 0,
    totalDiffFactoryCustomer: 0
  };

  tableData.value.forEach(row => {
    stats.totalCustomerSend += row.customer_send_qty || 0;
    stats.totalFactoryReceive += row.factory_receive_qty || 0;
    stats.totalFactorySend += row.factory_send_qty || 0;
    stats.totalCustomerReceive += row.customer_receive_qty || 0;
  });

  stats.totalDiffReceive = stats.totalCustomerSend - stats.totalFactoryReceive;
  stats.totalDiffFactoryCustomer = stats.totalFactorySend - stats.totalCustomerReceive;

  return stats;
});

const getDiffColor = (value) => {
  if (value < 0) return '#F44336';
  if (value > 0) return '#4CAF50';
  return '#616161';
};

const loadData = async () => {
  try {
    const params = {};
    if (searchForm.goodsType) {
      params.goods_type = searchForm.goodsType;
    }
    if (searchForm.keyword) {
      params.keyword = searchForm.keyword;
    }

    const data = await getGoodsList(params);
    tableData.value = data;
  } catch (error) {
    console.error('加载数据失败:', error);
  }
};

const handleSearch = () => {
  loadData();
};

const handleReset = () => {
  searchForm.goodsType = '';
  searchForm.keyword = '';
  loadData();
};

const handleSelectionChange = (selection) => {
  selectedRows.value = selection;
};

const handleAdd = () => {
  dialogMode.value = 'add';
  resetForm();
  dialogVisible.value = true;
};

const handleEdit = () => {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请先选择一条记录');
    return;
  }
  if (selectedRows.value.length > 1) {
    ElMessage.warning('只能选择一条记录进行编辑');
    return;
  }

  dialogMode.value = 'edit';
  const row = selectedRows.value[0];
  Object.keys(form).forEach(key => {
    if (row[key] !== undefined) {
      form[key] = row[key];
    }
  });
  form.id = row.id;
  dialogVisible.value = true;
};

const handleDelete = () => {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请先选择要删除的记录');
    return;
  }

  ElMessageBox.confirm('确定要删除选中的记录吗？', '确认删除', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      for (const row of selectedRows.value) {
        await deleteGoods(row.id);
      }
      ElMessage.success('删除成功');
      loadData();
    } catch (error) {
      console.error('删除失败:', error);
    }
  }).catch(() => {});
};

const handleSubmit = async () => {
  if (!formRef.value) return;

  await formRef.value.validate(async (valid) => {
    if (!valid) return;

    try {
      const data = {
        ...form,
        diff_receive: diffReceive.value,
        diff_factory_customer: diffFactoryCustomer.value
      };

      if (dialogMode.value === 'add') {
        await addGoods(data);
        ElMessage.success('添加成功');
      } else {
        await updateGoods(form.id, data);
        ElMessage.success('修改成功');
      }

      dialogVisible.value = false;
      loadData();
    } catch (error) {
      console.error('保存失败:', error);
    }
  });
};

const handleDialogClose = () => {
  resetForm();
};

const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields();
  }
  Object.assign(form, {
    goods_type: '织纱',
    customer_name: '',
    customer_style_no: '',
    customer_send_date: '',
    customer_send_method: '快递',
    customer_send_qty: 0,
    factory_receive_qty: 0,
    factory_send_date: '',
    factory_send_method: '快递',
    factory_send_qty: 0,
    customer_receive_qty: 0
  });
};

const calculateDiff = () => {
  // 触发计算属性更新
};

onMounted(() => {
  loadData();
});
</script>

<style scoped>
.goods-processing {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.search-card,
.action-card,
.table-card {
  margin-bottom: 0;
}

.search-form {
  margin-bottom: 0;
}

.statistics {
  margin-top: 16px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.el-divider {
  margin: 16px 0;
}
</style>
</script>


