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

    <!-- Login Form -->
    <div class="space-y-4 text-left">
      <!-- Email/Phone -->
      <div>
        <label class="block text-white text-base font-medium mb-2">
          电子邮箱地址或电话号码 <span class="text-red-400">*</span>
        </label>
        <input 
          v-model="formData.email"
          type="text" 
          class="w-full bg-gray-700 text-white px-4 py-3 rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none"
          :class="{ 'border-red-500': errors.email }"
          @blur="validateEmail"
        >
        <p v-if="errors.email" class="text-red-400 text-sm mt-1">{{ errors.email }}</p>
      </div>

      <!-- Password -->
      <div>
        <label class="block text-white text-base font-medium mb-2">
          密码 <span class="text-red-400">*</span>
        </label>
        <input 
          v-model="formData.password"
          type="password" 
          class="w-full bg-gray-700 text-white px-4 py-3 rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none"
          :class="{ 'border-red-500': errors.password }"
          @blur="validatePassword"
        >
        <p v-if="errors.password" class="text-red-400 text-sm mt-1">{{ errors.password }}</p>
      </div>

      <!-- Forgot Password -->
      <div class="text-left">
        <a href="#" class="text-blue-400 hover:underline text-sm">
          忘记密码？
        </a>
      </div>

      <!-- Error Message -->
      <div v-if="loginError" class="bg-red-900/30 border border-red-500 rounded-lg p-3">
        <p class="text-red-400 text-sm">{{ loginError }}</p>
      </div>

      <!-- Submit Button -->
      <button 
        @click="handleLogin"
        :disabled="!isFormValid || isLoggingIn"
        class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 disabled:cursor-not-allowed text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200"
      >
        {{ isLoggingIn ? '登录中...' : '登录' }}
      </button>

      <!-- Register Link -->
      <div class="text-center">
        <span class="text-gray-400 text-sm">需要新的账号？</span>
        <button 
          @click="$emit('register')"
          class="text-blue-400 hover:underline text-sm ml-1"
        >
          注册
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { getCookie } from '@/util/session'

const props = defineProps({
  serverInfo: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['back', 'register', 'login-success'])

const isLoggingIn = ref(false)
const loginError = ref('')

const formData = reactive({
  email: '',
  password: ''
})

const errors = reactive({
  email: '',
  password: ''
})

// Form validation
const isFormValid = computed(() => {
  return formData.email.trim().length > 0 &&
         formData.password.length > 0 &&
         !errors.email &&
         !errors.password
})

const validateEmail = () => {
  if (!formData.email.trim()) {
    errors.email = '请输入邮箱地址或电话号码'
  } else {
    errors.email = ''
  }
}

const validatePassword = () => {
  if (!formData.password) {
    errors.password = '请输入密码'
  } else {
    errors.password = ''
  }
}

const onImageError = (event) => {
  event.target.src = '/media/default/server/logo/logo.svg'
}

const handleLogin = async () => {
  if (!isFormValid.value) return
  
  // Clear previous errors
  loginError.value = ''
  isLoggingIn.value = true
  
  try {
    const formData_post = new FormData()
    formData_post.append('username', formData.email.trim())
    formData_post.append('password', formData.password)
    
    const response = await fetch('/api/account/login/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: formData_post,
      credentials: 'include'
    })
    
    if (response.ok) {
      const data = await response.json()
      if (data.r === 1 || data.success) {
        // Login successful
        emit('login-success')
      } else {
        loginError.value = data.msg || data.error || '登录失败'
      }
    } else {
      loginError.value = '登录请求失败，请稍后重试'
    }
  } catch (error) {
    console.error('Login error:', error)
    loginError.value = '登录时发生错误，请稍后重试'
  } finally {
    isLoggingIn.value = false
  }
}
</script>