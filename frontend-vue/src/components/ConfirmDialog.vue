<template>
  <Teleport to="body">
    <Transition name="dialog">
      <div
        v-if="confirmDialog.visible"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        @click.self="handleCancel"
      >
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm"></div>

        <!-- Dialog -->
        <div
          class="relative bg-white rounded-xl shadow-2xl max-w-md w-full transform transition-all duration-300"
          :class="confirmDialog.visible ? 'scale-100 opacity-100' : 'scale-95 opacity-0'"
        >
          <!-- Icon -->
          <div class="p-6 pb-4">
            <div :class="getIconContainerClass(confirmDialog.type)" class="mx-auto flex items-center justify-center w-12 h-12 rounded-full">
              <svg v-if="confirmDialog.type === 'danger'" class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
              <svg v-else-if="confirmDialog.type === 'warning'" class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
              <svg v-else class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
              </svg>
            </div>
          </div>

          <!-- Content -->
          <div class="px-6 pb-4 text-center">
            <h3 class="text-lg font-semibold text-gray-900 mb-2">
              {{ confirmDialog.title }}
            </h3>
            <p class="text-sm text-gray-600">
              {{ confirmDialog.message }}
            </p>
          </div>

          <!-- Actions -->
          <div class="px-6 pb-6 flex gap-3">
            <button
              @click="handleCancel"
              class="flex-1 px-4 py-2.5 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors duration-200 cursor-pointer"
            >
              {{ confirmDialog.cancelText }}
            </button>
            <button
              @click="handleConfirm"
              :class="getConfirmButtonClass(confirmDialog.type)"
              class="flex-1 px-4 py-2.5 text-sm font-medium text-white rounded-lg transition-colors duration-200 cursor-pointer"
            >
              {{ confirmDialog.confirmText }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { useNotification } from '@/composables/useNotification'

const { confirmDialog } = useNotification()

const handleConfirm = () => {
  if (confirmDialog.value.onConfirm) {
    confirmDialog.value.onConfirm()
  }
}

const handleCancel = () => {
  if (confirmDialog.value.onCancel) {
    confirmDialog.value.onCancel()
  }
}

const getIconContainerClass = (type) => {
  const classes = {
    danger: 'bg-red-100 text-red-600',
    warning: 'bg-yellow-100 text-yellow-600',
    info: 'bg-blue-100 text-blue-600'
  }
  return classes[type] || classes.info
}

const getConfirmButtonClass = (type) => {
  const classes = {
    danger: 'bg-red-600 hover:bg-red-700',
    warning: 'bg-yellow-600 hover:bg-yellow-700',
    info: 'bg-blue-600 hover:bg-blue-700'
  }
  return classes[type] || classes.info
}
</script>

<style scoped>
.dialog-enter-active,
.dialog-leave-active {
  transition: opacity 0.3s ease;
}

.dialog-enter-from,
.dialog-leave-to {
  opacity: 0;
}

.dialog-enter-active .relative,
.dialog-leave-active .relative {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.dialog-enter-from .relative,
.dialog-leave-to .relative {
  transform: scale(0.95);
  opacity: 0;
}
</style>
