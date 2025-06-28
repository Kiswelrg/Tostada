<template>
  <div class="text-center">
    <!-- Header with close button -->
    <div class="flex justify-between items-start mb-6">
      <div></div>
      <button 
        @click="$emit('back')"
        class="text-gray-400 hover:text-white transition-colors"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
          <path d="M18.4 4L12 10.4L5.6 4L4 5.6L10.4 12L4 18.4L5.6 20L12 13.6L18.4 20L20 18.4L13.6 12L20 5.6L18.4 4Z"/>
        </svg>
      </button>
    </div>

    <!-- Icon and title -->
    <div class="mb-8">
      <div class="flex justify-center mb-4">
        <div class="relative">
          <div class="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="white">
              <path d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 1L9 7V9C9 10.1 9.9 11 11 11V22H13V11C14.1 11 15 10.1 15 9Z"/>
            </svg>
          </div>
          <div class="absolute -bottom-1 -right-1">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" fill="#ffd700"/>
              <path d="M8 12L11 15L16 9" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="absolute top-2 -right-2">
            <div class="w-3 h-3 bg-blue-400 rounded-full animate-pulse"></div>
          </div>
        </div>
      </div>
      
      <h1 class="text-white text-2xl font-bold mb-2">完成注册</h1>
      <p class="text-gray-300 text-base">
        请输入电子邮件地址和密码，以验证您的账号。
      </p>
    </div>

    <!-- Form -->
    <div class="space-y-4 text-left">
      <!-- Email -->
      <div>
        <label class="block text-white text-base font-medium mb-2">电子邮件</label>
        <input 
          v-model="formData.email"
          type="email" 
          class="w-full bg-gray-700 text-white px-4 py-3 rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none"
          :class="{ 'border-red-500': errors.email }"
          @blur="validateEmail"
        >
        <p v-if="errors.email" class="text-red-400 text-sm mt-1">{{ errors.email }}</p>
      </div>

      <!-- Password -->
      <div>
        <label class="block text-white text-base font-medium mb-2">密码</label>
        <input 
          v-model="formData.password"
          type="password" 
          class="w-full bg-gray-700 text-white px-4 py-3 rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none"
          :class="{ 'border-red-500': errors.password }"
          @blur="validatePassword"
        >
        <p v-if="errors.password" class="text-red-400 text-sm mt-1">{{ errors.password }}</p>
      </div>

      <!-- Email Verification Code -->
      <div>
        <label class="block text-white text-base font-medium mb-2">邮箱验证码</label>
        <div class="flex space-x-2">
          <input 
            v-model="formData.verificationCode"
            type="text" 
            placeholder="请输入验证码"
            class="flex-1 bg-gray-700 text-white px-4 py-3 rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none"
            :class="{ 'border-red-500': errors.verificationCode }"
            maxlength="6"
          >
          <button 
            @click="sendVerificationCode"
            :disabled="!canSendCode || isSendingCode"
            class="px-4 py-3 bg-gray-600 hover:bg-gray-500 disabled:bg-gray-700 disabled:cursor-not-allowed text-white text-sm rounded-lg transition-colors duration-200 whitespace-nowrap"
          >
            {{ isSendingCode ? '发送中...' : (countdown > 0 ? `${countdown}s` : '发送验证码') }}
          </button>
        </div>
        <p v-if="errors.verificationCode" class="text-red-400 text-sm mt-1">{{ errors.verificationCode }}</p>
        <p v-if="codeMessage" class="text-green-400 text-sm mt-1">{{ codeMessage }}</p>
      </div>

      <!-- Error Message -->
      <div v-if="submitError" class="bg-red-900/30 border border-red-500 rounded-lg p-3">
        <p class="text-red-400 text-sm">{{ submitError }}</p>
      </div>

      <!-- Submit Button -->
      <button 
        @click="handleVerification"
        :disabled="!isFormValid || isSubmitting"
        class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 disabled:cursor-not-allowed text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200"
      >
        {{ isSubmitting ? '验证中...' : '认证账号' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCookie } from '@/util/session'

const props = defineProps({
  serverInfo: {
    type: Object,
    required: true
  },
  userData: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['back', 'verification-success'])
const router = useRouter()

const isSubmitting = ref(false)
const isSendingCode = ref(false)
const submitError = ref('')
const codeMessage = ref('')
const countdown = ref(0)
let countdownTimer = null

const formData = reactive({
  email: '',
  password: '',
  verificationCode: ''
})

const errors = reactive({
  email: '',
  password: '',
  verificationCode: ''
})

// Form validation
const isFormValid = computed(() => {
  return formData.email.trim().length > 0 &&
         formData.password.length >= 6 &&
         formData.verificationCode.length >= 4 &&
         !errors.email &&
         !errors.password &&
         !errors.verificationCode
})

const canSendCode = computed(() => {
  return formData.email.trim().length > 0 && 
         !errors.email && 
         countdown.value === 0
})

const validateEmail = () => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!formData.email.trim()) {
    errors.email = '请输入邮箱地址'
  } else if (!emailRegex.test(formData.email.trim())) {
    errors.email = '请输入有效的邮箱地址'
  } else {
    errors.email = ''
  }
}

const validatePassword = () => {
  if (!formData.password) {
    errors.password = '请输入密码'
  } else if (formData.password.length < 6) {
    errors.password = '密码至少需要6个字符'
  } else {
    errors.password = ''
  }
}

const startCountdown = () => {
  countdown.value = 60
  countdownTimer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(countdownTimer)
      countdownTimer = null
    }
  }, 1000)
}

const sendVerificationCode = async () => {
  if (!canSendCode.value) return
  
  validateEmail()
  if (errors.email) return
  
  isSendingCode.value = true
  codeMessage.value = ''
  
  try {
    // Get CSRF token first if not available
    let csrfToken = getCookie('csrftoken')
    if (!csrfToken) {
      const tokenResponse = await fetch('/api/account/get-csrf-token/')
      if (tokenResponse.ok) {
        const tokenData = await tokenResponse.json()
        csrfToken = tokenData.csrfToken
      }
    }
    
    const response = await fetch('/api/account/send-verification-code/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({
        email: formData.email.trim()
      })
    })
    
    const data = await response.json()
    
    if (response.ok && data.success) {
      codeMessage.value = '验证码已发送到您的邮箱'
      startCountdown()
    } else {
      errors.email = data.error || '发送验证码失败'
    }
  } catch (error) {
    console.error('Send verification code error:', error)
    errors.email = '发送验证码时发生错误'
  } finally {
    isSendingCode.value = false
  }
}

const handleVerification = async () => {
  if (!isFormValid.value) return
  
  submitError.value = ''
  isSubmitting.value = true
  
  try {
    // Get CSRF token first if not available
    let csrfToken = getCookie('csrftoken')
    if (!csrfToken) {
      const tokenResponse = await fetch('/api/account/get-csrf-token/')
      if (tokenResponse.ok) {
        const tokenData = await tokenResponse.json()
        csrfToken = tokenData.csrfToken
      }
    }
    
    // Create account with verification
    const userData = {
      ...props.userData,
      email: formData.email.trim(),
      password: formData.password,
      verification_code: formData.verificationCode,
      invitation_code: props.serverInfo?.invitationCode || ''  // Include invitation code
    }
    
    const response = await fetch('/api/account/register-with-verification/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify(userData),
      credentials: 'include'
    })
    
    const data = await response.json()
    
    if (response.ok && data.success) {
      // Registration and login successful
      emit('verification-success')
      // Redirect to tool page
      router.push({ name: 'tool' })
    } else {
      submitError.value = data.error || '注册失败'
    }
  } catch (error) {
    console.error('Verification error:', error)
    submitError.value = '验证时发生错误，请稍后重试'
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  // Auto-fill user data if available
  if (props.userData) {
    // Set any pre-filled data
  }
})

onUnmounted(() => {
  if (countdownTimer) {
    clearInterval(countdownTimer)
  }
})
</script>

<style scoped>
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>