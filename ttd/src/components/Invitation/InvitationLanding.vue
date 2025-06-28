<template>
  <div class="min-h-screen relative overflow-hidden bg-gradient-to-br from-blue-900 via-purple-900 to-blue-800">
    <!-- Animated background particles -->
    <div class="absolute inset-0">
      <div v-for="i in 50" :key="i" 
           class="absolute bg-white rounded-full opacity-20 animate-pulse"
           :style="particleStyle(i)">
      </div>
    </div>
    
    <!-- Header -->
    <div class="relative z-10 p-6">
      <div class="flex items-center">
        <div class="site-icon shrink-0 grow-0">
          <img src="/static/favicon.svg"
               alt=""
               class="h-12 w-12 aspect-square rounded-full">
        </div>
        <div class="site-title mx-2 text-xl text-white">
          <a href="/">
            Tostada
          </a>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <div class="relative z-10 flex items-center justify-center min-h-[calc(100vh-120px)]">
      <div class="bg-gray-800 rounded-xl shadow-2xl w-full max-w-md mx-4 overflow-hidden">
        
        <!-- Server Preview (Initial State) -->
        <div v-if="currentView === 'preview'" class="p-8 text-center">
          <div v-if="!loading && serverInfo" class="space-y-6">
            <!-- Server Avatar -->
            <div class="flex justify-center">
              <div class="relative">
                <img 
                  :src="serverInfo.logoSrc" 
                  :alt="serverInfo.name"
                  class="w-20 h-20 rounded-xl bg-gray-700"
                  @error="onImageError"
                >
                <div class="absolute -bottom-1 -right-1 bg-gray-800 rounded-lg p-1">
                  <div class="w-4 h-4 bg-green-600 rounded text-xs text-white flex items-center justify-center font-bold">
                    SFF
                  </div>
                </div>
              </div>
            </div>

            <!-- Server Info -->
            <div>
              <h1 class="text-white text-xl font-semibold mb-1">您已被邀请加入</h1>
              <h2 class="text-white text-2xl font-bold mb-3">{{ serverInfo.name }}</h2>
              <div class="flex justify-center items-center space-x-4 text-sm">
                <div class="flex items-center">
                  <div class="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                  <span class="text-gray-300">{{ serverInfo.onlineCount || '2,374' }} 人在线</span>
                </div>
                <div class="flex items-center">
                  <div class="w-2 h-2 bg-gray-400 rounded-full mr-2"></div>
                  <span class="text-gray-400">{{ serverInfo.memberCount || '9,162' }} 位成员</span>
                </div>
              </div>
            </div>

            <!-- Accept Button -->
            <button 
              @click="acceptInvitation"
              :disabled="isProcessing"
              class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200"
            >
              {{ isProcessing ? '处理中...' : '接受邀请' }}
            </button>
          </div>

          <!-- Loading State -->
          <div v-else-if="loading" class="space-y-4">
            <div class="w-20 h-20 bg-gray-700 rounded-xl mx-auto animate-pulse"></div>
            <div class="space-y-2">
              <div class="h-4 bg-gray-700 rounded animate-pulse"></div>
              <div class="h-6 bg-gray-700 rounded animate-pulse w-3/4 mx-auto"></div>
            </div>
          </div>

          <!-- Error State -->
          <div v-else class="space-y-4">
            <div class="text-red-400 text-center">
              <h2 class="text-xl font-semibold mb-2">邀请无效</h2>
              <p class="text-sm">{{ errorMessage }}</p>
            </div>
          </div>
        </div>

        <!-- Registration Form -->
        <div v-else-if="currentView === 'register'" class="p-8">
          <InvitationRegister 
            :server-info="serverInfo"
            @back="currentView = 'preview'"
            @login="currentView = 'login'"
            @continue-registration="handleContinueRegistration"
          />
        </div>

        <!-- Login Form -->
        <div v-else-if="currentView === 'login'" class="p-8">
          <InvitationLogin 
            :server-info="serverInfo"
            @back="currentView = 'preview'"
            @register="currentView = 'register'"
            @login-success="handleLoginSuccess"
          />
        </div>

        <!-- Email Verification -->
        <div v-else-if="currentView === 'email-verify'" class="p-8">
          <InvitationEmailVerify 
            :server-info="serverInfo"
            :user-data="pendingUserData"
            @back="currentView = 'register'"
            @verification-success="handleVerificationSuccess"
          />
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCookie } from '@/util/session'
import InvitationRegister from './InvitationRegister.vue'
import InvitationLogin from './InvitationLogin.vue'
import InvitationEmailVerify from './InvitationEmailVerify.vue'

const props = defineProps({
  code: {
    type: String,
    required: true
  }
})

const router = useRouter()
const loading = ref(true)
const serverInfo = ref(null)
const errorMessage = ref('')
const currentView = ref('preview') // 'preview', 'register', 'login', 'email-verify'
const isProcessing = ref(false)
const pendingUserData = ref(null)

// Generate random particle styles
const particleStyle = () => {
  const size = Math.random() * 4 + 1
  const left = Math.random() * 100
  const top = Math.random() * 100
  const delay = Math.random() * 2
  
  return {
    width: `${size}px`,
    height: `${size}px`,
    left: `${left}%`,
    top: `${top}%`,
    animationDelay: `${delay}s`,
    animationDuration: `${2 + Math.random() * 2}s`
  }
}

// Check invitation validity on mount
onMounted(async () => {
  await checkInvitation()
})

const checkInvitation = async () => {
  try {
    loading.value = true
    const response = await fetch(`/api/i/invitation/${props.code}/check/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })

    const data = await response.json()
    
    if (data.r && data.valid) {
      serverInfo.value = data.server
      // Add default values if not provided by backend
      serverInfo.value.onlineCount = data.server.onlineCount || '2,374'
      serverInfo.value.memberCount = data.server.memberCount || '9,162'
      // Include the invitation code for registration
      serverInfo.value.invitationCode = props.code
    } else {
      errorMessage.value = data.error || '邀请链接无效或已过期'
    }
  } catch (error) {
    console.error('Error checking invitation:', error)
    errorMessage.value = '检查邀请时发生错误'
  } finally {
    loading.value = false
  }
}

const onImageError = (event) => {
  event.target.src = '/media/default/server/logo/logo.svg'
}

const acceptInvitation = async () => {
  // Check if user is logged in
  try {
    const authResponse = await fetch('/api/account/check-auth/', {
      method: 'GET',
      credentials: 'include'
    })
    
    if (authResponse.ok) {
      const authData = await authResponse.json()
      if (authData.r && authData.logged_in) {
        // User is logged in, proceed with invitation
        await useInvitation()
      } else {
        // User not logged in, show registration/login options
        currentView.value = 'register'
      }
    } else {
      // Assume not logged in
      currentView.value = 'register'
    }
  } catch (error) {
    console.error('Error checking auth:', error)
    currentView.value = 'register'
  }
}

const useInvitation = async () => {
  try {
    isProcessing.value = true
    
    // Get CSRF token first if not available
    let csrfToken = getCookie('csrftoken')
    if (!csrfToken) {
      const tokenResponse = await fetch('/api/account/get-csrf-token/')
      if (tokenResponse.ok) {
        const tokenData = await tokenResponse.json()
        csrfToken = tokenData.csrfToken
      }
    }
    
    const response = await fetch(`/api/i/invitation/${props.code}/use/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      credentials: 'include'
    })

    const data = await response.json()
    
    if (data.r) {
      // Successfully joined server, redirect to main app
      router.push('/i')
    } else {
      errorMessage.value = data.error || '加入服务器失败'
    }
  } catch (error) {
    console.error('Error using invitation:', error)
    errorMessage.value = '加入服务器时发生错误'
  } finally {
    isProcessing.value = false
  }
}

const handleContinueRegistration = (userData) => {
  pendingUserData.value = userData
  currentView.value = 'email-verify'
}

const handleLoginSuccess = async () => {
  // After successful login, use the invitation
  await useInvitation()
}

const handleVerificationSuccess = async () => {
  // After successful verification, use the invitation
  await useInvitation()
}
</script>

<style scoped>
@keyframes pulse {
  0%, 100% {
    opacity: 0.2;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>