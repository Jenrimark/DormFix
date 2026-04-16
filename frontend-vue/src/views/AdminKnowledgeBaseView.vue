<template>
  <div>
    <h1 class="font-heading text-2xl font-bold text-textDark mb-6">知识库管理</h1>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <div class="lg:col-span-1 bg-white rounded-xl shadow-sm p-4 space-y-3">
        <h2 class="font-medium text-textDark">新增/编辑条目</h2>

        <input
          v-model="form.title"
          type="text"
          placeholder="标题"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
        />

        <select
          v-model="form.category"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary cursor-pointer"
        >
          <option value="faq">FAQ</option>
          <option value="sop">维修SOP</option>
          <option value="rule">学校规则</option>
        </select>

        <select
          v-model="form.role_scope"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary cursor-pointer"
        >
          <option value="all">全部可见</option>
          <option value="student">仅学生</option>
          <option value="repairman">仅维修人员</option>
        </select>

        <textarea
          v-model="form.content"
          rows="8"
          placeholder="请输入知识内容"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
        />

        <label class="flex items-center gap-2 text-sm text-gray-700">
          <input v-model="form.is_active" type="checkbox" class="cursor-pointer" />
          启用该条目
        </label>

        <div class="flex gap-2">
          <button
            class="flex-1 px-4 py-2 rounded-lg bg-primary text-white hover:bg-primary/90 transition-colors cursor-pointer disabled:opacity-60"
            :disabled="saving"
            @click="save"
          >
            {{ saving ? '保存中...' : (form.id ? '更新' : '新增') }}
          </button>
          <button
            class="px-4 py-2 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-50 transition-colors cursor-pointer"
            :disabled="saving"
            @click="resetForm"
          >
            重置
          </button>
        </div>
      </div>

      <div class="lg:col-span-2 space-y-4">
        <div class="bg-white rounded-xl shadow-sm overflow-hidden">
          <div class="px-4 py-3 border-b border-gray-200 font-medium text-textDark">知识条目</div>
          <div class="px-4 py-3 border-b border-gray-100">
            <div class="flex flex-wrap gap-3 items-center">
              <input
                v-model="filters.search"
                @input="handleFilter"
                type="text"
                placeholder="搜索标题..."
                class="flex-1 min-w-[180px] px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              />
              <select
                v-model="filters.category"
                @change="handleFilter"
                class="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary cursor-pointer"
              >
                <option value="">全部分类</option>
                <option value="faq">FAQ</option>
                <option value="sop">维修SOP</option>
                <option value="rule">学校规则</option>
              </select>
              <select
                v-model="filters.role_scope"
                @change="handleFilter"
                class="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary cursor-pointer"
              >
                <option value="">全部角色</option>
                <option value="student">仅学生</option>
                <option value="repairman">仅维修人员</option>
              </select>
              <select
                v-model="filters.is_active"
                @change="handleFilter"
                class="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary cursor-pointer"
              >
                <option value="">全部状态</option>
                <option value="true">启用</option>
                <option value="false">停用</option>
              </select>
            </div>
          </div>
          <div v-if="loading" class="text-center py-10 text-gray-500">加载中...</div>
          <div v-else-if="items.length === 0" class="text-center py-10 text-gray-500">暂无条目</div>
          <table v-else class="w-full">
            <thead class="bg-gray-50 border-b border-gray-200">
              <tr>
                <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">标题</th>
                <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">分类</th>
                <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">可见角色</th>
                <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">状态</th>
                <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">操作</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="item in items" :key="item.id">
                <td class="px-4 py-3 text-sm text-gray-900">{{ item.title }}</td>
                <td class="px-4 py-3 text-sm text-gray-700">{{ item.category_display }}</td>
                <td class="px-4 py-3 text-sm text-gray-700">{{ item.role_scope_display }}</td>
                <td class="px-4 py-3 text-sm">
                  <span :class="item.is_active ? 'text-green-600' : 'text-gray-500'">
                    {{ item.is_active ? '启用' : '停用' }}
                  </span>
                </td>
                <td class="px-4 py-3 text-sm">
                  <div class="flex gap-2">
                    <button class="text-primary hover:underline cursor-pointer" @click="edit(item)">编辑</button>
                    <button class="text-red-600 hover:underline cursor-pointer" @click="remove(item.id)">删除</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-if="totalPages > 1" class="flex justify-center gap-2 mt-6 pb-6">
            <button
              @click="goToPage(currentPage - 1)"
              :disabled="currentPage === 1"
              class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
            >
              上一页
            </button>
            <span class="px-4 py-2">
              第 {{ currentPage }} / {{ totalPages }} 页
            </span>
            <button
              @click="goToPage(currentPage + 1)"
              :disabled="currentPage === totalPages"
              class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
            >
              下一页
            </button>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-sm overflow-hidden">
          <div class="px-4 py-3 border-b border-gray-200 font-medium text-textDark">问答日志</div>
          <div v-if="logLoading" class="text-center py-10 text-gray-500">加载中...</div>
          <div v-else-if="logs.length === 0" class="text-center py-10 text-gray-500">暂无日志</div>
          <div v-else class="divide-y divide-gray-100">
            <div v-for="log in logs" :key="log.id" class="px-4 py-3">
              <p class="text-sm text-gray-900"><span class="font-medium">问：</span>{{ log.question }}</p>
              <p class="text-sm text-gray-700 mt-1"><span class="font-medium">答：</span>{{ log.answer }}</p>
              <p class="text-xs text-gray-500 mt-2">{{ log.role }} · {{ log.created_at }} · {{ log.success ? '成功' : '失败' }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import {
  createKnowledgeItem,
  deleteKnowledgeItem,
  getKnowledgeItems,
  getKnowledgeQaLogs,
  updateKnowledgeItem,
} from '@/api'
import { useNotification } from '@/composables/useNotification'

const { notify, confirm } = useNotification()
const loading = ref(false)
const logLoading = ref(false)
const saving = ref(false)
const items = ref([])
const logs = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const pageSize = 10

const filters = ref({
  search: '',
  category: '',
  role_scope: '',
  is_active: '',
})

const form = ref({
  id: null,
  title: '',
  category: 'faq',
  role_scope: 'all',
  content: '',
  is_active: true,
})

onMounted(async () => {
  await Promise.all([loadItems(), loadLogs()])
})

function resetForm() {
  form.value = {
    id: null,
    title: '',
    category: 'faq',
    role_scope: 'all',
    content: '',
    is_active: true,
  }
}

function edit(item) {
  form.value = {
    id: item.id,
    title: item.title,
    category: item.category,
    role_scope: item.role_scope,
    content: item.content,
    is_active: item.is_active,
  }
}

async function loadItems() {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize,
    }
    if (filters.value.search) params.search = filters.value.search
    if (filters.value.category) params.category = filters.value.category
    if (filters.value.role_scope) params.role_scope = filters.value.role_scope
    if (filters.value.is_active !== '') params.is_active = filters.value.is_active

    const { data } = await getKnowledgeItems(params)
    items.value = data?.results || data || []
    if (data?.count) totalPages.value = Math.ceil(data.count / pageSize)
    else totalPages.value = 1
  } catch {
    items.value = []
    totalPages.value = 1
    notify({ message: '加载知识条目失败', type: 'error' })
  } finally {
    loading.value = false
  }
}

function handleFilter() {
  currentPage.value = 1
  loadItems()
}

function goToPage(p) {
  if (p < 1 || p > totalPages.value) return
  currentPage.value = p
  loadItems()
}

async function loadLogs() {
  logLoading.value = true
  try {
    const { data } = await getKnowledgeQaLogs({ page_size: 20 })
    logs.value = data?.results || data || []
  } catch {
    logs.value = []
  } finally {
    logLoading.value = false
  }
}


async function save() {
  if (!form.value.title.trim() || !form.value.content.trim()) {
    notify({ message: '标题和内容不能为空', type: 'warning' })
    return
  }

  saving.value = true
  try {
    const payload = {
      title: form.value.title.trim(),
      category: form.value.category,
      role_scope: form.value.role_scope,
      content: form.value.content.trim(),
      is_active: form.value.is_active,
    }

    if (form.value.id) {
      await updateKnowledgeItem(form.value.id, payload)
      notify({ message: '更新成功', type: 'success' })
    } else {
      await createKnowledgeItem(payload)
      notify({ message: '新增成功', type: 'success' })
    }

    resetForm()
    await loadItems()
  } catch (e) {
    notify({ message: e?.response?.data?.error || '保存失败', type: 'error' })
  } finally {
    saving.value = false
  }
}

async function remove(id) {
  const ok = await confirm({
    title: '确认删除',
    message: '删除后将无法恢复，是否继续？',
    confirmText: '删除',
    cancelText: '取消',
    type: 'warning',
  })
  if (!ok) return

  try {
    await deleteKnowledgeItem(id)
    notify({ message: '删除成功', type: 'success' })
    await loadItems()
  } catch {
    notify({ message: '删除失败', type: 'error' })
  }
}
</script>

