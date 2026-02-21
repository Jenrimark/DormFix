<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="font-heading text-2xl font-bold text-textDark">用户管理</h1>
      <button @click="openCreateDialog" class="bg-primary text-white px-4 py-2 rounded-lg hover:bg-primary/90 transition-colors cursor-pointer">
        添加用户
      </button>
    </div>

    <!-- 用户表单对话框 -->
    <UserFormDialog
      :is-open="dialogOpen"
      :user="editingUser"
      @close="closeDialog"
      @success="handleDialogSuccess"
    />

    <!-- 搜索和筛选 -->
    <div class="bg-white rounded-xl p-4 shadow-sm mb-4">
      <div class="flex flex-wrap gap-4">
        <input
          v-model="searchQuery"
          @input="handleSearch"
          type="text"
          placeholder="搜索用户名或姓名..."
          class="flex-1 min-w-[200px] px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
        />
        <select
          v-model="roleFilter"
          @change="handleSearch"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary cursor-pointer"
        >
          <option value="">全部角色</option>
          <option value="1">学生</option>
          <option value="2">维修人员</option>
          <option value="3">管理员</option>
        </select>
        <select
          v-model="statusFilter"
          @change="handleSearch"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary cursor-pointer"
        >
          <option value="">全部状态</option>
          <option value="true">启用</option>
          <option value="false">禁用</option>
        </select>
      </div>
    </div>

    <!-- 批量操作栏 -->
    <div v-if="selectedUsers.length > 0" class="bg-blue-50 rounded-xl p-4 mb-4 flex justify-between items-center">
      <span class="text-gray-700">已选择 {{ selectedUsers.length }} 个用户</span>
      <div class="flex gap-2">
        <button @click="handleBatchEnable" class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors cursor-pointer">
          批量启用
        </button>
        <button @click="handleBatchDisable" class="px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors cursor-pointer">
          批量禁用
        </button>
        <button @click="handleBatchDelete" class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors cursor-pointer">
          批量删除
        </button>
      </div>
    </div>

    <!-- 用户列表 -->
    <div class="bg-white rounded-xl shadow-sm overflow-hidden">
      <div v-if="loading" class="text-center py-12 text-gray-500">加载中...</div>
      <div v-else-if="users.length === 0" class="text-center py-12 text-gray-500">暂无用户数据</div>
      <table v-else class="w-full">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="px-4 py-3 text-left">
              <input
                type="checkbox"
                @change="toggleSelectAll"
                :checked="isAllSelected"
                class="w-4 h-4 cursor-pointer"
              />
            </th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">用户名</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">姓名</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">角色</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">状态</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">创建时间</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
            <td class="px-4 py-3">
              <input
                v-if="canManageUser(user)"
                type="checkbox"
                :checked="selectedUsers.includes(user.id)"
                @change="toggleSelectUser(user.id)"
                class="w-4 h-4 cursor-pointer"
              />
              <span v-else class="w-4 h-4 inline-block"></span>
            </td>
            <td class="px-4 py-3 text-sm text-gray-900">{{ user.username }}</td>
            <td class="px-4 py-3 text-sm text-gray-900">{{ user.real_name || '-' }}</td>
            <td class="px-4 py-3 text-sm">
              <span :class="getRoleBadgeClass(user.role)">
                {{ getRoleText(user.role) }}
              </span>
            </td>
            <td class="px-4 py-3 text-sm">
              <span :class="user.is_active ? 'text-green-600' : 'text-red-600'">
                {{ user.is_active ? '启用' : '禁用' }}
              </span>
            </td>
            <td class="px-4 py-3 text-sm text-gray-600">{{ formatDate(user.created_at) }}</td>
            <td class="px-4 py-3 text-sm">
              <div v-if="canManageUser(user)" class="flex gap-2">
                <button @click="openEditDialog(user)" class="text-primary hover:text-primary/80 cursor-pointer">
                  编辑
                </button>
                <button @click="handleToggleStatus(user)" class="text-yellow-600 hover:text-yellow-700 cursor-pointer">
                  {{ user.is_active ? '禁用' : '启用' }}
                </button>
                <button @click="handleResetPassword(user)" class="text-blue-600 hover:text-blue-700 cursor-pointer">
                  重置密码
                </button>
                <button @click="handleDelete(user)" class="text-red-600 hover:text-red-700 cursor-pointer">
                  删除
                </button>
              </div>
              <div v-else class="text-gray-400 text-sm">
                {{ user.id === userStore.user?.id ? '当前用户' : '无权限' }}
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页 -->
    <div v-if="totalPages > 1" class="flex justify-center gap-2 mt-6">
      <button
        @click="goToPage(currentPage - 1)"
        :disabled="currentPage === 1"
        class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
      >
        上一页
      </button>
      <span class="px-4 py-2">第 {{ currentPage }} / {{ totalPages }} 页</span>
      <button
        @click="goToPage(currentPage + 1)"
        :disabled="currentPage === totalPages"
        class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
      >
        下一页
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { listAllUsers, deleteUser, resetPassword, toggleUserStatus, batchOperation } from '@/api'
import UserFormDialog from '@/components/UserFormDialog.vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const users = ref([])
const loading = ref(false)
const searchQuery = ref('')
const roleFilter = ref('')
const statusFilter = ref('')
const selectedUsers = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const pageSize = 20
const dialogOpen = ref(false)
const editingUser = ref(null)

const isAllSelected = computed(() => {
  const manageableUsers = users.value.filter(u => canManageUser(u))
  return manageableUsers.length > 0 && selectedUsers.value.length === manageableUsers.length
})

// 判断当前用户是否是超级管理员（admin）
const isSuperAdmin = computed(() => {
  return userStore.user?.username === 'admin'
})

// 判断是否可以对某个用户进行操作
const canManageUser = (user) => {
  const currentUser = userStore.user
  
  // 不能操作自己
  if (user.id === currentUser?.id) {
    return false
  }
  
  // 如果目标用户是管理员
  if (user.role === 3) {
    // 只有超级管理员可以操作其他管理员
    return isSuperAdmin.value
  }
  
  // 可以操作学生和维修人员
  return true
}

onMounted(() => {
  loadUsers()
})

async function loadUsers() {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize
    }
    if (searchQuery.value) params.search = searchQuery.value
    if (roleFilter.value) params.role = roleFilter.value
    if (statusFilter.value) params.is_active = statusFilter.value

    const res = await listAllUsers(params)
    users.value = res.data.results || res.data
    if (res.data.count) {
      totalPages.value = Math.ceil(res.data.count / pageSize)
    }
  } catch (error) {
    console.error('加载用户列表失败:', error)
    alert('加载用户列表失败')
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  currentPage.value = 1
  selectedUsers.value = []
  loadUsers()
}

function goToPage(page) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    selectedUsers.value = []
    loadUsers()
  }
}

function toggleSelectAll(event) {
  if (event.target.checked) {
    // 只选择可以管理的用户
    selectedUsers.value = users.value
      .filter(u => canManageUser(u))
      .map(u => u.id)
  } else {
    selectedUsers.value = []
  }
}

function toggleSelectUser(userId) {
  const index = selectedUsers.value.indexOf(userId)
  if (index > -1) {
    selectedUsers.value.splice(index, 1)
  } else {
    selectedUsers.value.push(userId)
  }
}

function openCreateDialog() {
  editingUser.value = null
  dialogOpen.value = true
}

function openEditDialog(user) {
  editingUser.value = user
  dialogOpen.value = true
}

function closeDialog() {
  dialogOpen.value = false
  editingUser.value = null
}

function handleDialogSuccess() {
  loadUsers()
}

async function handleToggleStatus(user) {
  const action = user.is_active ? '禁用' : '启用'
  if (!confirm(`确定要${action}用户 ${user.username} 吗？`)) return

  try {
    await toggleUserStatus(user.id)
    alert(`${action}成功`)
    loadUsers()
  } catch (error) {
    console.error(`${action}用户失败:`, error)
    alert(`${action}失败`)
  }
}

async function handleResetPassword(user) {
  if (!confirm(`确定要重置用户 ${user.username} 的密码吗？`)) return

  try {
    const res = await resetPassword(user.id)
    alert(`密码重置成功！新密码：${res.data.new_password}`)
  } catch (error) {
    console.error('重置密码失败:', error)
    alert('重置密码失败')
  }
}

async function handleDelete(user) {
  if (!confirm(`确定要删除用户 ${user.username} 吗？此操作不可恢复！`)) return

  try {
    await deleteUser(user.id)
    alert('删除成功')
    loadUsers()
  } catch (error) {
    console.error('删除用户失败:', error)
    alert(error.response?.data?.error || '删除失败')
  }
}

async function handleBatchEnable() {
  if (!confirm(`确定要启用选中的 ${selectedUsers.value.length} 个用户吗？`)) return

  try {
    const res = await batchOperation({
      action: 'enable',
      user_ids: selectedUsers.value
    })
    alert(`批量启用完成：成功 ${res.data.success_count} 个，失败 ${res.data.failed_count} 个`)
    selectedUsers.value = []
    loadUsers()
  } catch (error) {
    console.error('批量启用失败:', error)
    alert('批量启用失败')
  }
}

async function handleBatchDisable() {
  if (!confirm(`确定要禁用选中的 ${selectedUsers.value.length} 个用户吗？`)) return

  try {
    const res = await batchOperation({
      action: 'disable',
      user_ids: selectedUsers.value
    })
    alert(`批量禁用完成：成功 ${res.data.success_count} 个，失败 ${res.data.failed_count} 个`)
    selectedUsers.value = []
    loadUsers()
  } catch (error) {
    console.error('批量禁用失败:', error)
    alert('批量禁用失败')
  }
}

async function handleBatchDelete() {
  if (!confirm(`确定要删除选中的 ${selectedUsers.value.length} 个用户吗？此操作不可恢复！`)) return

  try {
    const res = await batchOperation({
      action: 'delete',
      user_ids: selectedUsers.value
    })
    alert(`批量删除完成：成功 ${res.data.success_count} 个，失败 ${res.data.failed_count} 个`)
    selectedUsers.value = []
    loadUsers()
  } catch (error) {
    console.error('批量删除失败:', error)
    alert('批量删除失败')
  }
}

function getRoleText(role) {
  const roleMap = { 1: '学生', 2: '维修人员', 3: '管理员' }
  return roleMap[role] || '未知'
}

function getRoleBadgeClass(role) {
  const classMap = {
    1: 'px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs',
    2: 'px-2 py-1 bg-green-100 text-green-700 rounded text-xs',
    3: 'px-2 py-1 bg-purple-100 text-purple-700 rounded text-xs'
  }
  return classMap[role] || 'px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs'
}

function formatDate(dateString) {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>
