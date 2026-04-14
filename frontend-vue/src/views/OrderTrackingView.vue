<template>
  <div>
    <h1 class="font-heading text-2xl font-bold text-textDark mb-6">我的工单</h1>
    <div class="flex gap-2 mb-4 flex-wrap">
      <button v-for="s in statusFilters" :key="s.value"
        :class="['px-4 py-2 rounded-lg transition-colors cursor-pointer', filterStatus === s.value ? 'bg-primary text-white' : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50']"
        @click="filterStatus = s.value">
        {{ s.label }}
      </button>
    </div>
    <div v-if="loading" class="text-center py-12 text-gray-500">加载中...</div>
    <div v-else-if="!filteredList.length" class="bg-white rounded-xl p-8 text-center text-gray-500">暂无工单</div>
    <div v-else class="space-y-4">
      <div v-for="order in filteredList" :key="order.id" 
        @click="selectedOrder = order"
        class="bg-white rounded-xl shadow-sm p-4 border border-gray-100 hover:shadow-md transition-shadow cursor-pointer">
        <div class="flex gap-4">
          <!-- 图片缩略图 -->
          <div v-if="order.img_proof" class="flex-shrink-0">
            <img :src="order.img_proof" :alt="order.repair_type_info?.name" 
              class="w-20 h-20 object-cover rounded-lg border border-gray-200">
          </div>
          
          <!-- 工单信息 -->
          <div class="flex-1 min-w-0">
            <div class="flex justify-between items-start gap-2">
              <span class="font-heading font-medium text-textDark">{{ order.order_sn }}</span>
              <span :class="statusClass(order.status)" class="flex-shrink-0">{{ order.status_display }}</span>
            </div>
            <p class="text-gray-600 mt-2 text-sm">{{ order.repair_type_info?.name }} · {{ order.priority_display }}</p>
            <p class="text-gray-700 mt-1 line-clamp-2">{{ order.content }}</p>
            <p class="text-gray-400 text-xs mt-2">{{ order.create_time }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 工单详情弹窗 -->
    <div v-if="selectedOrder" @click="selectedOrder = null" 
      class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div @click.stop class="bg-white rounded-xl w-full max-w-5xl h-[85vh] overflow-hidden">
        <div class="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
          <h2 class="font-heading text-xl font-bold text-textDark">工单详情</h2>
          <button @click="selectedOrder = null" class="text-gray-400 hover:text-gray-600 transition-colors cursor-pointer">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <div class="p-6 h-[calc(85vh-73px)] overflow-y-auto">
          <!-- 工单编号和状态 -->
          <div class="flex justify-between items-center mb-4">
            <span class="font-medium text-gray-900">{{ selectedOrder.order_sn }}</span>
            <span :class="statusClass(selectedOrder.status)" class="px-3 py-1 rounded-full text-sm">
              {{ selectedOrder.status_display }}
            </span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6">
            <!-- 左列：图片 + 基本信息 -->
            <div class="space-y-4">
              <!-- 图片 -->
              <div v-if="selectedOrder.img_proof" class="rounded-lg overflow-hidden border border-gray-200 bg-gray-50">
                <button
                  type="button"
                  class="block w-full cursor-zoom-in"
                  @click="openImagePreview(selectedOrder.img_proof)"
                  aria-label="点击放大查看图片"
                >
                  <img
                    :src="selectedOrder.img_proof"
                    :alt="selectedOrder.repair_type_info?.name"
                    class="w-full max-h-64 object-cover"
                  >
                </button>
                <div class="px-3 py-2 text-xs text-gray-500 border-t border-gray-200 bg-white">
                  点击图片可放大查看
                </div>
              </div>

              <!-- 基本信息 -->
              <div class="space-y-2">
                <div class="flex items-center gap-2 text-sm">
                  <span class="text-gray-500">故障类型：</span>
                  <span class="text-gray-900">{{ selectedOrder.repair_type_info?.name }}</span>
                </div>
                <div class="flex items-center gap-2 text-sm">
                  <span class="text-gray-500">紧急程度：</span>
                  <span class="text-gray-900">{{ selectedOrder.priority_display }}</span>
                </div>
                <div class="flex items-center gap-2 text-sm">
                  <span class="text-gray-500">提交时间：</span>
                  <span class="text-gray-900">{{ selectedOrder.create_time }}</span>
                </div>
                <div v-if="selectedOrder.repairman_info" class="flex items-center gap-2 text-sm">
                  <span class="text-gray-500">维修员：</span>
                  <span class="text-gray-900">{{ selectedOrder.repairman_info.username }}</span>
                </div>
                <div v-if="selectedOrder.finish_time" class="flex items-center gap-2 text-sm">
                  <span class="text-gray-500">完成时间：</span>
                  <span class="text-gray-900">{{ selectedOrder.finish_time }}</span>
                </div>
              </div>
            </div>

            <!-- 右列：描述/备注/评价 -->
            <div class="space-y-4">
              <!-- 维修凭证 -->
              <div v-if="selectedOrder.status === 3 && (selectedOrder.repair_proof_img || selectedOrder.repair_description)">
                <h3 class="text-sm font-medium text-gray-500 mb-2">维修凭证</h3>
                <div class="bg-green-50 rounded-lg p-4 space-y-3">
                  <div v-if="selectedOrder.repair_proof_img" class="rounded-lg overflow-hidden border border-green-200 bg-white">
                    <button
                      type="button"
                      class="block w-full cursor-zoom-in"
                      @click="openImagePreview(selectedOrder.repair_proof_img)"
                      aria-label="点击放大查看维修凭证图片"
                    >
                      <img
                        :src="selectedOrder.repair_proof_img"
                        alt="维修凭证"
                        class="w-full max-h-64 object-cover"
                      >
                    </button>
                    <div class="px-3 py-2 text-xs text-gray-500 border-t border-green-200 bg-white">
                      点击图片可放大查看
                    </div>
                  </div>
                  <p v-if="selectedOrder.repair_description" class="text-gray-900 whitespace-pre-wrap">
                    {{ selectedOrder.repair_description }}
                  </p>
                </div>
              </div>
              <div v-else-if="selectedOrder.status === 3" class="bg-gray-50 rounded-lg p-4 border border-gray-200">
                <h3 class="text-sm font-medium text-gray-700 mb-1">维修凭证</h3>
                <p class="text-sm text-gray-500">该工单暂未上传维修凭证。</p>
              </div>

              <!-- 问题描述 -->
              <div>
                <h3 class="text-sm font-medium text-gray-500 mb-2">问题描述</h3>
                <p class="text-gray-900 whitespace-pre-wrap">{{ selectedOrder.content }}</p>
              </div>

              <!-- 备注 -->
              <div v-if="selectedOrder.remark">
                <h3 class="text-sm font-medium text-gray-500 mb-2">备注</h3>
                <p class="text-gray-900 whitespace-pre-wrap">{{ selectedOrder.remark }}</p>
              </div>

              <!-- 评价 -->
              <div v-if="selectedOrder.comment" class="bg-amber-50 rounded-lg p-4">
                <h3 class="text-sm font-medium text-gray-700 mb-2">我的评价</h3>
                <div class="flex items-center gap-1 mb-2">
                  <svg v-for="i in 5" :key="i" class="w-5 h-5" 
                    :class="i <= selectedOrder.comment.score ? 'text-amber-400' : 'text-gray-300'"
                    fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                  </svg>
                </div>
                <p v-if="selectedOrder.comment.feedback" class="text-gray-700 text-sm">
                  {{ selectedOrder.comment.feedback }}
                </p>
              </div>

              <!-- 去评价 -->
              <div v-else-if="selectedOrder.status === 3" class="bg-white border border-amber-200 rounded-lg p-4">
                <div class="flex items-center justify-between gap-3">
                  <div>
                    <h3 class="text-sm font-medium text-gray-900">评价本次维修</h3>
                    <p class="text-xs text-gray-500 mt-1">提交后将无法修改或重复提交</p>
                  </div>
                  <button
                    class="px-4 py-2 rounded-lg bg-amber-500 text-white text-sm font-medium hover:bg-amber-600 transition-colors cursor-pointer disabled:opacity-60 disabled:cursor-not-allowed"
                    :disabled="submittingComment"
                    @click="openCommentDialog"
                  >
                    去评价
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 图片放大预览 -->
    <div
      v-if="imagePreviewUrl"
      class="fixed inset-0 bg-black/80 flex items-center justify-center p-4 z-[60]"
      @click="closeImagePreview"
    >
      <div class="max-w-5xl w-full max-h-[90vh]" @click.stop>
        <img
          :src="imagePreviewUrl"
          alt="图片预览"
          class="w-full h-full object-contain rounded-lg"
        >
      </div>
    </div>

    <!-- 评价弹窗 -->
    <div v-if="commentDialogOpen" @click="closeCommentDialog"
      class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div @click.stop class="bg-white rounded-xl w-full max-w-md">
        <div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
          <h3 class="font-heading text-lg font-bold text-textDark">提交评价</h3>
          <button @click="closeCommentDialog" class="text-gray-400 hover:text-gray-600 transition-colors cursor-pointer">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <div class="p-6 space-y-4">
          <div>
            <div class="flex items-center gap-1">
              <button
                v-for="i in 5"
                :key="i"
                class="cursor-pointer"
                @click="commentScore = i"
                :aria-label="`评分 ${i} 星`"
              >
                <svg class="w-7 h-7" :class="i <= commentScore ? 'text-amber-400' : 'text-gray-300'"
                  fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                </svg>
              </button>
            </div>
            <p class="text-xs text-gray-500 mt-2">请选择 1-5 星</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">文字反馈（可选）</label>
            <textarea
              v-model="commentFeedback"
              rows="4"
              class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-amber-200 focus:border-amber-300"
              placeholder="说说你的体验，比如维修是否及时、是否解决问题等"
            />
          </div>

          <div v-if="commentError" class="text-sm text-red-600">
            {{ commentError }}
          </div>

          <div class="flex items-center justify-end gap-2">
            <button
              class="px-4 py-2 rounded-lg border border-gray-300 text-gray-700 text-sm hover:bg-gray-50 transition-colors cursor-pointer"
              :disabled="submittingComment"
              @click="closeCommentDialog"
            >
              取消
            </button>
            <button
              class="px-4 py-2 rounded-lg bg-amber-500 text-white text-sm font-medium hover:bg-amber-600 transition-colors cursor-pointer disabled:opacity-60 disabled:cursor-not-allowed"
              :disabled="submittingComment || commentScore < 1 || commentScore > 5"
              @click="submitComment"
            >
              {{ submittingComment ? '提交中...' : '提交' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getMyOrders, createComment } from '@/api'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const loading = ref(true)
const list = ref([])
const filterStatus = ref('')
const selectedOrder = ref(null)

const commentDialogOpen = ref(false)
const commentScore = ref(5)
const commentFeedback = ref('')
const submittingComment = ref(false)
const commentError = ref('')
const imagePreviewUrl = ref('')

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

function openCommentDialog() {
  commentError.value = ''
  commentScore.value = 5
  commentFeedback.value = ''
  commentDialogOpen.value = true
}

function closeCommentDialog() {
  if (submittingComment.value) return
  commentDialogOpen.value = false
}

function openImagePreview(url) {
  imagePreviewUrl.value = url || ''
}

function closeImagePreview() {
  imagePreviewUrl.value = ''
}

async function submitComment() {
  if (!selectedOrder.value) return
  commentError.value = ''
  submittingComment.value = true
  try {
    await createComment({
      work_order: selectedOrder.value.id,
      score: commentScore.value,
      feedback: commentFeedback.value || null,
    })
    commentDialogOpen.value = false
    await load()
    // 重新定位当前选中的工单对象（load() 会换引用）
    selectedOrder.value = list.value.find((o) => o.id === selectedOrder.value.id) || selectedOrder.value
  } catch (e) {
    const msg = e?.response?.data?.error || e?.response?.data?.detail
    // DRF serializer 错误一般是对象
    const data = e?.response?.data
    if (typeof data === 'object' && data) {
      const firstKey = Object.keys(data)[0]
      const firstVal = Array.isArray(data[firstKey]) ? data[firstKey][0] : data[firstKey]
      commentError.value = firstVal || msg || '提交失败'
    } else {
      commentError.value = msg || '提交失败'
    }
  } finally {
    submittingComment.value = false
  }
}

onMounted(load)
</script>
