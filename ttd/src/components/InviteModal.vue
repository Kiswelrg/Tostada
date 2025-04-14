<template>
  <Teleport to="body">
    <div v-if="isOpen" class="fixed inset-0 z-50">
      <!-- Backdrop -->
      <div class="absolute inset-0 bg-black bg-opacity-80" @click="close"></div>
      
      <!-- Main Modal -->
      <div v-if="!showEditLinkSettings" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-[#313338] rounded-md w-[480px]">
        <div class="relative p-4">
          <!-- Close button -->
          <button @click="close" class="absolute top-4 right-4 text-gray-400 hover:text-white">
            <IconSystem name="close" :size="24" />
          </button>

          <!-- Header -->
          <div class="mb-4">
            <h2 class="text-xl text-white font-semibold">Invite friends to {{ serverName }}</h2>
            <div class="flex items-center mt-2">
              <div class="text-white text-base"># {{ channelName }}</div>
            </div>
          </div>

          <!-- Search input -->
          <div class="relative mb-4">
            <input 
              type="text" 
              placeholder="Search for friends" 
              class="w-full bg-[#1e1f22] text-white px-4 py-2 rounded-md focus:outline-none"
              v-model="searchQuery"
            >
            <div class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400">
              <IconSystem name="search" :size="20" />
            </div>
          </div>

          <!-- Friends list -->
          <div class="mb-6">
            <div 
              v-for="friend in friends" 
              :key="friend.id"
              class="flex items-center justify-between p-2 rounded hover:bg-[#2b2d31] cursor-pointer mb-1"
            >
              <div class="flex items-center">
                <img :src="friend.avatar" class="w-10 h-10 rounded-full mr-3">
                <span class="text-white">{{ friend.name }}</span>
              </div>
              <button 
                class="px-4 py-1 rounded-md bg-[#dbdee1] hover:bg-white text-black"
              >
                Invite
              </button>
            </div>
          </div>

          <!-- Server invite link section -->
          <div class="mt-6 border-t border-[#3f4147] pt-4">
            <h3 class="text-lg text-white mb-3">Or, Send A Server Invite Link To A Friend</h3>
            <div class="flex gap-2">
              <input 
                type="text" 
                :value="inviteLink" 
                readonly 
                class="flex-1 bg-[#1e1f22] text-white px-4 py-2 rounded-md"
              >
              <button 
                @click="copyLink" 
                class="px-4 py-2 rounded-md bg-[#5865f2] hover:bg-[#4752c4] text-white"
              >
                Copy
              </button>
            </div>
            <div class="text-gray-400 text-sm mt-2">
              Your invite link expires in 7 days. 
              <button @click="showEditLinkSettings = true" class="text-[#00a8fc] hover:underline">
                Edit invite link
              </button>.
            </div>
          </div>
        </div>
      </div>

      <!-- Edit Link Settings (same modal, different content) -->
      <div v-if="showEditLinkSettings" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-[#313338] rounded-md w-[480px]">
        <div class="relative p-4">
          <!-- Close button -->
          <button @click="close" class="absolute top-4 right-4 text-gray-400 hover:text-white">
            <IconSystem name="close" :size="24" />
          </button>

          <!-- Header -->
          <div class="mb-6">
            <h2 class="text-xl text-white font-semibold">Server invite link settings</h2>
          </div>

          <div class="space-y-4">
            <div>
              <label class="text-white text-base block mb-2">Expire After</label>
              <div class="relative">
                <select class="w-full bg-[#1e1f22] text-white px-4 py-2 rounded-md appearance-none">
                  <option>7 days</option>
                  <option>1 day</option>
                  <option>12 hours</option>
                  <option>Never</option>
                </select>
                <div class="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none text-gray-400">
                  <IconSystem name="chevron-down" :size="20" />
                </div>
              </div>
            </div>

            <div>
              <label class="text-white text-base block mb-2">Max Number Of Uses</label>
              <div class="relative">
                <select class="w-full bg-[#1e1f22] text-white px-4 py-2 rounded-md appearance-none">
                  <option>No limit</option>
                  <option>1 use</option>
                  <option>5 uses</option>
                  <option>10 uses</option>
                </select>
                <div class="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none text-gray-400">
                  <IconSystem name="chevron-down" :size="20" />
                </div>
              </div>
            </div>

            <div class="flex items-center justify-between">
              <div>
                <label class="text-white text-base">Grant temporary membership</label>
                <p class="text-gray-400 text-sm mt-1">
                  Temporary members are automatically kicked when they disconnect unless a role has been assigned
                </p>
              </div>
              <div class="relative">
                <label class="switch">
                  <input type="checkbox">
                  <span class="slider round"></span>
                </label>
              </div>
            </div>

            <div class="flex justify-end gap-3 mt-6 pt-4 border-t border-[#3f4147]">
              <button 
                @click="showEditLinkSettings = false"
                class="px-4 py-2 rounded-md text-white hover:underline"
              >
                Cancel
              </button>
              <button 
                class="px-6 py-2 rounded-md bg-[#5865f2] hover:bg-[#4752c4] text-white"
              >
                Generate a New Link
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'
import IconSystem from './IconSystem.vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  serverName: {
    type: String,
    default: 'kiswelrg'
  },
  channelName: {
    type: String,
    default: 'general'
  }
})

const emit = defineEmits(['close'])

const searchQuery = ref('')
const showEditLinkSettings = ref(false)
const inviteLink = ref('https://discord.gg/YqVXe3tZ')

// Mock friends data - replace with real data later
const friends = ref([
  { id: 1, name: 'classymeerkat', avatar: '/static/tool/main/chevron-down-solid.svg' },
  { id: 2, name: 'NightMeow', avatar: '/static/tool/main/chevron-down-solid.svg' },
  { id: 3, name: 'Hansail', avatar: '/static/tool/main/chevron-down-solid.svg' },
])

const close = () => {
  emit('close')
  showEditLinkSettings.value = false
}

const copyLink = () => {
  navigator.clipboard.writeText(inviteLink.value)
  // Could add a toast notification here
}
</script>

<style scoped>
.switch {
  position: relative;
  display: inline-block;
  width: 46px;
  height: 26px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #2d2d2d;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .4s;
}

input:checked + .slider {
  background-color: #5865f2;
}

input:checked + .slider:before {
  transform: translateX(20px);
}

.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}
</style> 