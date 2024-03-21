import { ref, watch, onUnmounted } from 'vue'

export function useWatchOnce(source, callback, options = {}) {
  const stopped = ref(false)
  let cleanupWatcher = null

  const stopWatcher = () => {
    if (stopped.value) return
    if (cleanupWatcher) {
      cleanupWatcher()
      cleanupWatcher = null
      stopped.value = true
    }
  }

  const watcher = watch(
    source,
    async (newValue, oldValue) => {
      if (!stopped.value) {
        const shouldstop = await callback(newValue, oldValue)
        if (shouldstop)
          stopWatcher()
      }
    },
    options
  )

  cleanupWatcher = watcher

  onUnmounted(stopWatcher)

  return {
    stopped,
    stopWatcher
  }
}