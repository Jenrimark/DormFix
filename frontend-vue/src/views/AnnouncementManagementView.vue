<template>
  <div class="max-w-6xl mx-auto">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-800">系统公告管理</h1>
      <button 
        @click="showCreateDialog = true" 
        class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors"
      >
        发布公告
      </button>
    </div>

    <!-- 公告列表 -->
    <div class="bg-white rounded-lg shadow-md overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">标题</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">内容</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">发布者</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">发布时间</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="announcement in announcements" :key="announcement.id">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ announcement.title }}</td>
            <td class="px-6 py-4 text-sm text-gray-500 max-w-xs truncate">{{ announcement.content }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ announcement.author_real_name || announcement.author_name }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDateTime(announcement.created_at) }}</td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span 
                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                :class="announcement.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
              >
                {{ announcement.is_active ? '显示' : '隐藏' }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
              <button @click="editAnnouncement(announcement)" class="text-indigo-600 hover:text-indigo-900">编辑</button>
              <button @click="deleteAnnouncementConfirm(announcement.id)" class="text-red-600 hover:text-red-900">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="announcements.length === 0" class="text-center py-12 text-gray-400">
        暂无公告
      </div>
    </div>

    <!-- 创建/编辑公告对话框 -->
    <div v-if="showCreateDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-2xl">
        <h2 class="text-2xl font-bold mb-4">{{ editingAnnouncement ? '编辑公告' : '发布公告' }}</h2>
        
        <form @submit.prevent="submitAnnouncement">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">公告标题</label>
            <input 
              v-model="form.title" 
              type="text" 
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="请输入公告标题"
            />
          </div>
          
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">公告内容</label>
            <textarea 
              v-model="form.content" 
              required
              rows="6"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="请输入公告内容"
            ></textarea>
          </div>
          
          <div class="mb-6">
            <label class="flex items-center">
              <input 
                v-model="form.is_active" 
                type="checkbox" 
                class="rounded border-gray-300 text-primary focus:ring-primary"
              />
              <span class="ml-2 text-sm text-gray-700">立即显示</span>
            </label>
          </div>
          
          <div class="flex justify-end space-x-3">
            <button 
              type="button" 
              @click="closeDialog" 
              class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
            >
              取消
            </button>
            <button 
              type="submit" 
              class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90"
            >
              {{ editingAnnouncement ? '保存' : '发布' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAnnouncements, createAnnouncement, updateAnnouncement, deleteAnnouncement } from '@/api'
import { useNotification } from '@/composables/useNotification'

const { notify, confirm } = useNotification()
const announcements = ref([])
const showCreateDialog = ref(false)
const editingAnnouncement = ref(null)
const form = ref({
  title: '',
  content: '',
  is_active: true
})

const fetchAnnouncements = async () => {
  try {
    const { data } = await getAnnouncements()
    announcements.value = data.results || data
  } catch (error) {
    console.error('获取公告失败:', error)
    notify({
      message: '获取公告失败',
      type: 'error'
    })
  }
}

const submitAnnouncement = async () => {
  try {
    if (editingAnnouncement.value) {
      await updateAnnouncement(editingAnnouncement.value.id, form.value)
      notify({
        message: '公告更新成功',
        type: 'success'
      })
    } else {
      await createAnnouncement(form.value)
      notify({
        message: '公告发布成功',
        type: 'success'
      })
    }
    closeDialog()
    fetchAnnouncements()
  } catch (error) {
    console.error('操作失败:', error)
    notify({
      message: '操作失败',
      type: 'error'
    })
  }
}

const editAnnouncement = (announcement) => {
  editingAnnouncement.value = announcement
  form.value = {
    title: announcement.title,
    content: announcement.content,
    is_active: announcement.is_active
  }
  showCreateDialog.value = true
}

const deleteAnnouncementConfirm = async (id) => {
  const confirmed = await confirm({
    title: '确认删除',
    message: '确定要删除这条公告吗？',
    confirmText: '确定删除',
    cancelText: '取消',
    type: 'danger'
  })
  
  if (!confirmed) return
  
  try {
    await deleteAnnouncement(id)
    notify({
      message: '删除成功',
      type: 'success'
    })
    fetchAnnouncements()
  } catch (error) {
    console.error('删除失败:', error)
    notify({
      message: '删除失败',
      type: 'error'
    })
  }
}

const closeDialog = () => {
  showCreateDialog.value = false
  editingAnnouncement.value = null
  form.value = {
    title: '',
    content: '',
    is_active: true
  }
}

const formatDateTime = (dateString) => {
  return new Date(dateString).toLocaleString('zh-CN')
}

onMounted(() => {
  fetchAnnouncements()
})
</script>
