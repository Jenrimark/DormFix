<template>
  <div class="max-w-2xl mx-auto">
    <h1 class="font-heading text-2xl font-bold text-textDark mb-6">提交报修工单</h1>
    <div class="bg-white rounded-xl shadow-md p-6">
      <form @submit.prevent="onSubmit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">故障类型</label>
          <select v-model="form.repair_type" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary">
            <option value="">请选择</option>
            <option v-for="t in repairTypes" :key="t.id" :value="t.id">{{ t.name }}</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">紧急程度</label>
          <select v-model="form.priority" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary">
            <option value="low">不急</option>
            <option value="medium">一般</option>
            <option value="high">紧急</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">问题描述</label>
          <textarea v-model="form.content" required rows="4" maxlength="500" placeholder="请详细描述故障情况"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary"></textarea>
          <p class="text-sm text-gray-500 mt-1">{{ form.content.length }}/500</p>
        </div>
        <button type="submit" :disabled="loading" class="w-full py-3 bg-cta text-white rounded-lg font-medium hover:bg-cta/90 disabled:opacity-50 cursor-pointer">
          {{ loading ? '提交中...' : '提交工单' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getRepairTypes, createWorkOrder } from '@/api'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const repairTypes = ref([])
const loading = ref(false)
const form = reactive({
  repair_type: '',
  priority: 'medium',
  content: '',
})

onMounted(async () => {
  if (!userStore.user) {
    router.push({ name: 'Login', query: { redirect: '/submit' } })
    return
  }
  try {
    const { data } = await getRepairTypes()
    repairTypes.value = data
  } catch {
    if (typeof window.__toast === 'function') window.__toast('获取故障类型失败', 'error')
  }
})

async function onSubmit() {
  loading.value = true
  try {
    await createWorkOrder({
      repair_type: Number(form.repair_type),
      priority: form.priority,
      content: form.content.trim(),
    })
    if (typeof window.__toast === 'function') window.__toast('提交成功', 'success')
    router.push('/orders')
  } catch (e) {
    const msg = e.response?.data?.detail || '提交失败'
    if (typeof window.__toast === 'function') window.__toast(msg, 'error')
  } finally {
    loading.value = false
  }
}
</script>
