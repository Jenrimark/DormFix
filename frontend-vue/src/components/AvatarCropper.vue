<template>
  <div v-if="show" @click="close" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
    <div @click.stop class="bg-white rounded-xl max-w-2xl w-full p-6">
      <h3 class="font-heading text-xl font-bold text-gray-900 mb-4">裁剪头像</h3>
      
      <div class="space-y-4">
        <!-- 裁剪区域 -->
        <div class="relative bg-gray-100 rounded-lg overflow-hidden" style="height: 400px;">
          <canvas ref="canvas" 
            @mousedown="startDrag" 
            @mousemove="drag" 
            @mouseup="endDrag"
            @mouseleave="endDrag"
            @wheel.prevent="zoom"
            class="cursor-move">
          </canvas>
        </div>

        <!-- 控制按钮 -->
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <button @click="rotate(-90)" 
              class="px-3 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors cursor-pointer">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6"></path>
              </svg>
            </button>
            <button @click="rotate(90)" 
              class="px-3 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors cursor-pointer">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 10H11a8 8 0 00-8 8v2m18-10l-6 6m6-6l-6-6"></path>
              </svg>
            </button>
            <span class="text-sm text-gray-500">滚轮缩放 | 拖动调整位置</span>
          </div>
          
          <div class="flex gap-3">
            <button @click="close" 
              class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors cursor-pointer">
              取消
            </button>
            <button @click="cropAndSave" 
              class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors cursor-pointer">
              确认裁剪
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, nextTick } from 'vue'

const props = defineProps({
  show: Boolean,
  imageFile: File
})

const emit = defineEmits(['close', 'cropped'])

const canvas = ref(null)
const ctx = ref(null)
const image = ref(null)

// 图片状态
const imageState = ref({
  x: 0,
  y: 0,
  scale: 1,
  rotation: 0
})

// 拖拽状态
const dragState = ref({
  isDragging: false,
  startX: 0,
  startY: 0,
  startImageX: 0,
  startImageY: 0
})

watch(() => props.show, async (newVal) => {
  if (newVal && props.imageFile) {
    await nextTick()
    await loadImage()
  }
})

async function loadImage() {
  if (!canvas.value) return

  const img = new Image()
  const reader = new FileReader()

  reader.onload = (e) => {
    img.onload = () => {
      image.value = img
      initCanvas()
      drawImage()
    }
    img.src = e.target.result
  }

  reader.readAsDataURL(props.imageFile)
}

function initCanvas() {
  if (!canvas.value || !image.value) return

  const container = canvas.value.parentElement
  const size = Math.min(container.clientWidth, 400)
  
  canvas.value.width = size
  canvas.value.height = size
  ctx.value = canvas.value.getContext('2d')

  // 计算初始缩放和位置，使图片居中
  const imgAspect = image.value.width / image.value.height
  const canvasAspect = size / size

  if (imgAspect > canvasAspect) {
    imageState.value.scale = size / image.value.height
  } else {
    imageState.value.scale = size / image.value.width
  }

  imageState.value.x = (size - image.value.width * imageState.value.scale) / 2
  imageState.value.y = (size - image.value.height * imageState.value.scale) / 2
}

function drawImage() {
  if (!ctx.value || !image.value || !canvas.value) return

  const { x, y, scale, rotation } = imageState.value
  const centerX = canvas.value.width / 2
  const centerY = canvas.value.height / 2

  // 清空画布
  ctx.value.clearRect(0, 0, canvas.value.width, canvas.value.height)
  
  // 绘制图片
  ctx.value.save()
  ctx.value.translate(centerX, centerY)
  ctx.value.rotate((rotation * Math.PI) / 180)
  ctx.value.translate(-centerX, -centerY)
  
  ctx.value.drawImage(
    image.value,
    x,
    y,
    image.value.width * scale,
    image.value.height * scale
  )
  
  ctx.value.restore()

  // 绘制裁剪框遮罩
  drawCropBox()
}

function drawCropBox() {
  if (!ctx.value || !canvas.value) return

  const size = canvas.value.width
  const cropSize = size * 0.8
  const cropX = (size - cropSize) / 2
  const cropY = (size - cropSize) / 2

  // 绘制半透明遮罩（四个矩形，不覆盖裁剪区域）
  ctx.value.fillStyle = 'rgba(0, 0, 0, 0.5)'
  
  // 上方遮罩
  ctx.value.fillRect(0, 0, size, cropY)
  // 下方遮罩
  ctx.value.fillRect(0, cropY + cropSize, size, size - cropY - cropSize)
  // 左侧遮罩
  ctx.value.fillRect(0, cropY, cropX, cropSize)
  // 右侧遮罩
  ctx.value.fillRect(cropX + cropSize, cropY, size - cropX - cropSize, cropSize)

  // 绘制裁剪框边框
  ctx.value.strokeStyle = '#fff'
  ctx.value.lineWidth = 2
  ctx.value.strokeRect(cropX, cropY, cropSize, cropSize)

  // 绘制网格线
  ctx.value.strokeStyle = 'rgba(255, 255, 255, 0.5)'
  ctx.value.lineWidth = 1
  
  // 垂直线
  ctx.value.beginPath()
  ctx.value.moveTo(cropX + cropSize / 3, cropY)
  ctx.value.lineTo(cropX + cropSize / 3, cropY + cropSize)
  ctx.value.moveTo(cropX + (cropSize * 2) / 3, cropY)
  ctx.value.lineTo(cropX + (cropSize * 2) / 3, cropY + cropSize)
  ctx.value.stroke()

  // 水平线
  ctx.value.beginPath()
  ctx.value.moveTo(cropX, cropY + cropSize / 3)
  ctx.value.lineTo(cropX + cropSize, cropY + cropSize / 3)
  ctx.value.moveTo(cropX, cropY + (cropSize * 2) / 3)
  ctx.value.lineTo(cropX + cropSize, cropY + (cropSize * 2) / 3)
  ctx.value.stroke()
}

function startDrag(e) {
  dragState.value.isDragging = true
  dragState.value.startX = e.clientX
  dragState.value.startY = e.clientY
  dragState.value.startImageX = imageState.value.x
  dragState.value.startImageY = imageState.value.y
}

function drag(e) {
  if (!dragState.value.isDragging) return

  const dx = e.clientX - dragState.value.startX
  const dy = e.clientY - dragState.value.startY

  imageState.value.x = dragState.value.startImageX + dx
  imageState.value.y = dragState.value.startImageY + dy

  drawImage()
}

function endDrag() {
  dragState.value.isDragging = false
}

function zoom(e) {
  const delta = e.deltaY > 0 ? -0.1 : 0.1
  imageState.value.scale = Math.max(0.1, Math.min(5, imageState.value.scale + delta))
  drawImage()
}

function rotate(angle) {
  imageState.value.rotation = (imageState.value.rotation + angle) % 360
  drawImage()
}

function cropAndSave() {
  if (!canvas.value || !image.value) return

  const size = canvas.value.width
  const cropSize = size * 0.8
  const cropX = (size - cropSize) / 2
  const cropY = (size - cropSize) / 2

  // 创建临时 canvas 用于裁剪
  const tempCanvas = document.createElement('canvas')
  const outputSize = 200 // 输出头像大小
  tempCanvas.width = outputSize
  tempCanvas.height = outputSize
  const tempCtx = tempCanvas.getContext('2d')

  // 绘制裁剪后的图片
  tempCtx.drawImage(
    canvas.value,
    cropX,
    cropY,
    cropSize,
    cropSize,
    0,
    0,
    outputSize,
    outputSize
  )

  // 转换为 Blob
  tempCanvas.toBlob((blob) => {
    emit('cropped', blob)
  }, 'image/jpeg', 0.9)
}

function close() {
  emit('close')
}
</script>
