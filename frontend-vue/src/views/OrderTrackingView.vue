<template>
  <div>
    <h1 class="font-heading text-2xl font-bold text-textDark mb-6">我的工单</h1>
    <div class="flex gap-2 mb-4 flex-wrap">
      <button v-for="s in statusFilters" :key="s.value"
        :class="['px-4 py-2 rounded-lg transition-colors', filterStatus === s.value ? 'bg-primary text-white' : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50']"
        @click="filterStatus = s.value">
        {{ s.label }}
      </button>
    </div>
    <div v-if="loading" class="text-center py-12 text-gray-500">加载中...</div>
    <div v-else-if="!filteredList.length" class="bg-white rounded-xl p-8 text-center text-gray-500">暂无工单</div>
    <div v-else class="space-y-4">
      <div v-for="order in filteredList" :key="order.id" class="bg-white rounded-xl shadow-sm p-4 border border-gray-100">
        <div class="flex justify-between items-start">
          <span class="font-heading font-medium text-textDark">{{ order.order_sn }}</span>
          <span :class="statusClass(order.status)">{{ order.status_display }}</span>
        </div>
        <p class="text-gray-600 mt-2 text-sm">{{ order.repair_type_info?.name }} · {{ order.priority_display }}</p>
        <p class="text-gray-700 mt-1">{{ order.content }}</p>
        <p class="text-gray-400 text-xs mt-2">{{ order.create_time }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getMyOrders } from '@/api'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const loading = ref(true)
const list = ref([])
const filterStatus = ref('')

const statusFilters = [
  { value: '', label: '全部' },
  { value: '0', label: '待审核' },
  { value: '1', label: '已派单' },
  { value: '2', label: '维修中' },
  { value: '3', label: '已完成' },
  { value: '4', label: '已取消' },
]

const statusClass = (status) => {
  const m = { 0: 'text-amber-600', 1: 'text-blue-600', 2: 'text-primary', 3: 'text-green-600', 4: 'text-gray-500' }
  return m[status] || 'text-gray-600'
}

const filteredList = computed(() => {
  if (filterStatus.value === '') return list.value
  return list.value.filter((o) => String(o.status) === filterStatus.value)
})

async function load() {
  if (!userStore.user) return
  loading.value = true
  try {
    const { data } = await getMyOrders()
    list.value = Array.isArray(data) ? data : data?.results ?? []
  } catch {
    list.value = []
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
