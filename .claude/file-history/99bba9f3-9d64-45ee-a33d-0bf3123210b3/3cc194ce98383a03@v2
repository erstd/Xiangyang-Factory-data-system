<template>
  <div class="wage-calculation">
    <!-- 操作按钮 -->
    <el-card class="action-card" shadow="never">
      <el-button type="primary" @click="loadData">刷新</el-button>
      <el-button
        v-if="userStore.isFinance"
        type="success"
        @click="handleAdd"
      >
        添加记录
      </el-button>
    </el-card>

    <!-- 数据表格 -->
    <el-card class="table-card" shadow="never">
      <el-table
        :data="tableData"
        stripe
        border
        height="calc(100vh - 320px)"
      >
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="workshop_name" label="加工车间" width="150" />
        <el-table-column prop="knitting_qty" label="织片数量" width="100" align="right" />
        <el-table-column prop="knitting_wage" label="织片工资" width="100" align="right">
          <template #default="{ row }">
            ¥{{ row.knitting_wage }}
          </template>
        </el-table-column>
        <el-table-column prop="overlock_goods_type" label="套口货物" width="100" />
        <el-table-column prop="overlock_wage" label="套口工资" width="100" align="right">
          <template #default="{ row }">
            ¥{{ row.overlock_wage }}
          </template>
        </el-table-column>
        <el-table-column prop="hand_sewing_goods_type" label="手缝货物" width="100" />
        <el-table-column prop="hand_sewing_wage" label="手缝工资" width="100" align="right">
          <template #default="{ row }">
            ¥{{ row.hand_sewing_wage }}
          </template>
        </el-table-column>
        <el-table-column prop="created_by" label="创建人" width="100" />
        <el-table-column prop="created_date" label="创建时间" width="160" />
      </el-table>
    </el-card>

    <!-- 新增对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="工资核算记录"
      width="750px"
      @close="handleDialogClose"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
      >
        <!-- 车间信息 -->
        <el-divider content-position="left">车间信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="加工车间" prop="workshop_name">
              <el-input v-model="form.workshop_name" placeholder="请输入车间名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="加工日期" prop="processing_date">
              <el-date-picker
                v-model="form.processing_date"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="织片数量" prop="knitting_qty">
              <el-input-number
                v-model="form.knitting_qty"
                :min="0"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="织片工资" prop="knitting_wage">
              <el-input-number
                v-model="form.knitting_wage"
                :min="0"
                :precision="2"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 套口信息 -->
        <el-divider content-position="left">套口信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="套口员工" prop="overlock_employee">
              <el-input v-model="form.overlock_employee" placeholder="请输入员工姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="货物种类" prop="overlock_goods_type">
              <el-select v-model="form.overlock_goods_type" placeholder="请选择">
                <el-option label="织纱" value="织纱" />
                <el-option label="织片" value="织片" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="套口数量" prop="overlock_qty">
              <el-input-number
                v-model="form.overlock_qty"
                :min="0"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="套口工资" prop="overlock_wage">
              <el-input-number
                v-model="form.overlock_wage"
                :min="0"
                :precision="2"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 手缝信息 -->
        <el-divider content-position="left">手缝信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="手缝员工" prop="hand_sewing_employee">
              <el-input v-model="form.hand_sewing_employee" placeholder="请输入员工姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="货物种类" prop="hand_sewing_goods_type">
              <el-select v-model="form.hand_sewing_goods_type" placeholder="请选择">
                <el-option label="织纱" value="织纱" />
                <el-option label="织片" value="织片" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="手缝数量" prop="hand_sewing_qty">
              <el-input-number
                v-model="form.hand_sewing_qty"
                :min="0"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="手缝工资" prop="hand_sewing_wage">
              <el-input-number
                v-model="form.hand_sewing_wage"
                :min="0"
                :precision="2"
                style="width: 100%"
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
import { ref, reactive, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { getWageList, addWage } from '@/api';
import { useUserStore } from '@/store/user';

const userStore = useUserStore();
const formRef = ref(null);
const dialogVisible = ref(false);
const tableData = ref([]);

const form = reactive({
  workshop_name: '',
  processing_date: '',
  knitting_qty: 0,
  knitting_wage: 0,
  overlock_employee: '',
  overlock_goods_type: '织纱',
  overlock_qty: 0,
  overlock_wage: 0,
  hand_sewing_employee: '',
  hand_sewing_goods_type: '织纱',
  hand_sewing_qty: 0,
  hand_sewing_wage: 0
});

const rules = {
  workshop_name: [
    { required: true, message: '请输入车间名称', trigger: 'blur' }
  ]
};

const loadData = async () => {
  try {
    const data = await getWageList();
    tableData.value = data;
  } catch (error) {
    console.error('加载数据失败:', error);
  }
};

const handleAdd = () => {
  resetForm();
  dialogVisible.value = true;
};

const handleSubmit = async () => {
  if (!formRef.value) return;

  await formRef.value.validate(async (valid) => {
    if (!valid) return;

    try {
      await addWage(form);
      ElMessage.success('添加成功');
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
    workshop_name: '',
    processing_date: '',
    knitting_qty: 0,
    knitting_wage: 0,
    overlock_employee: '',
    overlock_goods_type: '织纱',
    overlock_qty: 0,
    overlock_wage: 0,
    hand_sewing_employee: '',
    hand_sewing_goods_type: '织纱',
    hand_sewing_qty: 0,
    hand_sewing_wage: 0
  });
};

onMounted(() => {
  loadData();
});
</script>

<style scoped>
.wage-calculation {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.action-card,
.table-card {
  margin-bottom: 0;
}

.el-divider {
  margin: 16px 0;
}
</style>
