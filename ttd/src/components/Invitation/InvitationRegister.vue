<template>
  <div class="text-center">
    <!-- Server Info -->
    <div class="flex justify-center mb-6">
      <div class="relative">
        <img 
          :src="serverInfo.logoSrc" 
          :alt="serverInfo.name"
          class="w-16 h-16 rounded-xl bg-gray-700"
          @error="onImageError"
        >
        <div class="absolute -bottom-1 -right-1 bg-gray-800 rounded-lg p-1">
          <div class="w-4 h-4 bg-green-600 rounded text-xs text-white flex items-center justify-center font-bold">
            SFF
          </div>
        </div>
      </div>
    </div>

    <h1 class="text-white text-xl font-semibold mb-1">您已被邀请加入</h1>
    <h2 class="text-white text-2xl font-bold mb-3">{{ serverInfo.name }}</h2>
    <div class="flex justify-center items-center space-x-4 text-sm mb-8">
      <div class="flex items-center">
        <div class="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
        <span class="text-gray-300">{{ serverInfo.onlineCount }} 人在线</span>
      </div>
      <div class="flex items-center">
        <div class="w-2 h-2 bg-gray-400 rounded-full mr-2"></div>
        <span class="text-gray-400">{{ serverInfo.memberCount }} 位成员</span>
      </div>
    </div>

    <!-- Registration Form -->
    <div class="space-y-4 text-left">
      <!-- Nickname -->
      <div>
        <label class="block text-white text-base font-medium mb-2">昵称</label>
        <input 
          v-model="formData.nickname"
          type="text" 
          placeholder="希望大家怎么称呼您？"
          class="w-full bg-gray-700 text-white px-4 py-3 rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none"
          maxlength="32"
        >
        <p class="text-gray-400 text-sm mt-1">
          这是其他人所看到的您的名称。可以使用特殊字符和表情符号。
        </p>
      </div>

      <!-- Birth Date -->
      <div>
        <label class="block text-white text-base font-medium mb-2">出生日期</label>
        <div class="grid grid-cols-3 gap-3">
          <div class="relative">
            <select 
              v-model="formData.birthYear"
              class="w-full bg-gray-700 text-white px-4 py-3 rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none appearance-none"
            >
              <option value="">年</option>
              <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
            </select>
            <div class="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none text-gray-400">
              <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
                <path d="M6 8.5L2 4.5h8L6 8.5z"/>
              </svg>
            </div>
          </div>
          <div class="relative">
            <select 
              v-model="formData.birthMonth"
              class="w-full bg-gray-700 text-white px-4 py-3 rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none appearance-none"
            >
              <option value="">月</option>
              <option v-for="month in months" :key="month.value" :value="month.value">{{ month.label }}</option>
            </select>
            <div class="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none text-gray-400">
              <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
                <path d="M6 8.5L2 4.5h8L6 8.5z"/>
              </svg>
            </div>
          </div>
          <div class="relative">
            <select 
              v-model="formData.birthDay"
              class="w-full bg-gray-700 text-white px-4 py-3 rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none appearance-none"
            >
              <option value="">日</option>
              <option v-for="day in days" :key="day" :value="day">{{ day }}</option>
            </select>
            <div class="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none text-gray-400">
              <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
                <path d="M6 8.5L2 4.5h8L6 8.5z"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Terms -->
      <div class="text-sm text-gray-400">
        点击"创建账号"即表示您同意 Tostada 的
        <a href="#" class="text-blue-400 hover:underline">服务条款</a>，
        并已阅读
        <a href="#" class="text-blue-400 hover:underline">隐私政策</a>
      </div>

      <!-- Submit Button -->
      <button 
        @click="handleSubmit"
        :disabled="!isFormValid || isSubmitting"
        class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 disabled:cursor-not-allowed text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200"
      >
        {{ isSubmitting ? '创建中...' : '创建账号' }}
      </button>

      <!-- Login Link -->
      <div class="text-center">
        <button 
          @click="$emit('login')"
          class="text-blue-400 hover:underline text-sm"
        >
          已经拥有账号？请登录
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'

const props = defineProps({
  serverInfo: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['back', 'login', 'continue-registration'])

const isSubmitting = ref(false)

const formData = reactive({
  nickname: '',
  birthYear: '',
  birthMonth: '',
  birthDay: ''
})

// Generate years (current year down to 1900)
const currentYear = new Date().getFullYear()
const years = computed(() => {
  const yearList = []
  for (let year = currentYear; year >= 1900; year--) {
    yearList.push(year)
  }
  return yearList
})

// Months
const months = [
  { value: '1', label: '1月' },
  { value: '2', label: '2月' },
  { value: '3', label: '3月' },
  { value: '4', label: '4月' },
  { value: '5', label: '5月' },
  { value: '6', label: '6月' },
  { value: '7', label: '7月' },
  { value: '8', label: '8月' },
  { value: '9', label: '9月' },
  { value: '10', label: '10月' },
  { value: '11', label: '11月' },
  { value: '12', label: '12月' }
]

// Days
const days = computed(() => {
  const dayList = []
  for (let day = 1; day <= 31; day++) {
    dayList.push(day)
  }
  return dayList
})

// Form validation
const isFormValid = computed(() => {
  return formData.nickname.trim().length >= 2 &&
         formData.birthYear && 
         formData.birthMonth && 
         formData.birthDay
})

const onImageError = (event) => {
  event.target.src = '/media/default/server/logo/logo.svg'
}

const handleSubmit = async () => {
  if (!isFormValid.value) return
  
  isSubmitting.value = true
  
  try {
    // Format birth date
    const birthDate = `${formData.birthYear}-${formData.birthMonth.padStart(2, '0')}-${formData.birthDay.toString().padStart(2, '0')}`
    
    const userData = {
      nickname: formData.nickname.trim(),
      birth_date: birthDate
    }
    
    // Pass data to parent for email verification step
    emit('continue-registration', userData)
  } catch (error) {
    console.error('Registration error:', error)
  } finally {
    isSubmitting.value = false
  }
}
</script>