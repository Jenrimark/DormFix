import { ref } from 'vue'

// 全局通知状态
const notifications = ref([])
let notificationId = 0

// 全局确认对话框状态
const confirmDialog = ref({
  visible: false,
  title: '',
  message: '',
  confirmText: '确定',
  cancelText: '取消',
  type: 'warning',
  onConfirm: null,
  onCancel: null
})

export function useNotification() {
  /**
   * 显示通知
   * @param {Object} options - 通知选项
   * @param {string} options.message - 通知消息
   * @param {string} options.type - 通知类型: success, error, warning, info
   * @param {number} options.duration - 显示时长（毫秒），0 表示不自动关闭
   */
  const notify = ({ message, type = 'info', duration = 3000 }) => {
    const id = notificationId++
    const notification = {
      id,
      message,
      type,
      visible: true
    }

    notifications.value.push(notification)

    if (duration > 0) {
      setTimeout(() => {
        removeNotification(id)
      }, duration)
    }

    return id
  }

  const removeNotification = (id) => {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index > -1) {
      notifications.value[index].visible = false
      setTimeout(() => {
        notifications.value.splice(index, 1)
      }, 300) // 等待动画完成
    }
  }

  /**
   * 显示确认对话框
   * @param {Object} options - 对话框选项
   * @param {string} options.title - 标题
   * @param {string} options.message - 消息内容
   * @param {string} options.confirmText - 确认按钮文本
   * @param {string} options.cancelText - 取消按钮文本
   * @param {string} options.type - 类型: warning, danger, info
   * @returns {Promise<boolean>} - 用户选择结果
   */
  const confirm = ({
    title = '确认操作',
    message,
    confirmText = '确定',
    cancelText = '取消',
    type = 'warning'
  }) => {
    return new Promise((resolve) => {
      confirmDialog.value = {
        visible: true,
        title,
        message,
        confirmText,
        cancelText,
        type,
        onConfirm: () => {
          confirmDialog.value.visible = false
          resolve(true)
        },
        onCancel: () => {
          confirmDialog.value.visible = false
          resolve(false)
        }
      }
    })
  }

  return {
    notifications,
    notify,
    removeNotification,
    confirmDialog,
    confirm
  }
}
