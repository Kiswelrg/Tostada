<template>
  <Teleport to="body">
    <div v-if="isOpen" class="fixed inset-0 z-50">
      <!-- Backdrop -->
      <div class="absolute inset-0 bg-black bg-opacity-80" @click="close"></div>
      
      <!-- Main Modal -->
      <div v-if="!showEditLinkSettings" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-[#393a41] rounded-xl w-[480px]">
        <div class="relative p-0">
          <div class="py-4 px-6 pb-0">
            <!-- Close button -->
            <div class="absolute top-3 right-7 w-3 h-3">
              <button @click="close" class="flex h-6 w-auto p-1 box-content border-0 focus:border-0 focus:outline-0 justify-center cursor-pointer top-2 right-2 text-gray-400 hover:text-white bg-transparent">
                <IconSystem name="close" :size="24" />
              </button>
            </div>

            <div>
              <!-- Header -->
              <div class="mb-4">
                <h2 class="text-sm text-white font-semibold">Invite friends to {{ serverName }}</h2>
                <div class="flex items-center mt-1">
                  <div class="text-white text-base"># {{ channelName }}</div>
                </div>
              </div>

              <!-- Search input -->
              <div class="relative mb-4">
                <input 
                  type="text" 
                  placeholder="Search for friends" 
                  class="w-full bg-[var(--input-background)] bg-[#1e1f22] text-white text-sm px-4 py-2 rounded-md focus:outline-none"
                  v-model="searchQuery"
                >
                <div class="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400">
                  <IconSystem name="search" :size="20" />
                </div>
              </div>
            </div>
          </div>

          <!-- Friends list -->
          <div class="px-3 py-2 pb-4">
            <div 
              v-for="friend in friends" 
              :key="friend.id"
              class="group/friend flex items-center justify-between p-2 py-1 rounded hover:bg-[var(--background-modifier-hover)] cursor-pointer mb-1"
            >
              <div class="flex items-center">
                <img :src="friend.avatar" class="w-8 h-8 rounded-full mr-3">
                <span class="text-interactive-normal">{{ friend.name }}</span>
              </div>
              <button 
                class="px-4 py-1 rounded-md border-[#40a258] bg-transparent hover:bg-[#028137] group-hover/friend:bg-[#028137] group-hover/friend:border-[#028137] text-white text-sm"
              >
                Invite
              </button>
            </div>
          </div>

          <div class="px-6 py-4 rounded-b-lg bg-[var(--background-secondary)]">
            <!-- Server invite link section -->
            <div class="mt-0 border-t border-[#3f4147] pt-0">
              <h3 class="text-base font-medium text-white mb-3">Or, Send A Server Invite Link To A Friend</h3>
              <div class="border border-solid border-[var(--input-border)] rounded-lg bg-[var(--input-background)] box-border cursor-pointer h-10 overflow-hidden relative outline-0">
                <div class="flex bottom-0 inset-0 absolute flex-nowrap justify-start flex-row items-stretch outline-0">
                  <div class="flex flex-row flex-auto m-0 mr-[10px] p-0 relative flex-nowrap justify-start items-stretch outline-0 border-0 align-baseline">
                    <input 
                    type="text" 
                    :value="inviteLink" 
                    readonly 
                    class="flex-auto outline-none bg-transparent text-[var(--text-normal)] px-4 py-2 rounded-l-md cursor-text min-w-0 box-border"
                  >
                  </div>
                  <div class="flex flex-initial m-0 flex-nowrap justify-start items-stretch flex-row bg-[#1e1f22] rounded-r-md">
                    <button 
                      @click="copyLink" 
                      class="relative box-border m-1 ml-0 pt-1 pr-5 inline h-auto items-center rounded-md bg-[#5865f2] hover:bg-[#4752c4] text-white text-sm"
                    >
                      <div class="mx-auto my-0 overflow-hidden text-ellipsis whitespace-nowrap outline-0">Copy</div>
                    </button>
                  </div>
                </div>
              </div>
              <div class="text-gray-400 text-xs mt-2">
                Your invite link {{ expirationText }}. 
                <a @click="showEditLinkSettings = true" class="text-[#00a8fc] hover:underline cursor-pointer">
                  Edit invite link
                </a>.
              </div>
            </div>
          </div>

        </div>
      </div>

      <!-- Edit Link Settings (same modal, different content) -->
      <div v-if="showEditLinkSettings" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-[#393a41] rounded-md w-[480px]">
        <div class="relative p-4">
          <!-- Close button -->
          <div class="absolute top-3 right-7 w-3 h-3">
            <button @click="close" class="flex h-6 w-auto p-1 box-content border-0 focus:border-0 focus:outline-0 justify-center cursor-pointer top-2 right-2 text-gray-400 hover:text-white bg-transparent">
              <IconSystem name="close" :size="24" />
            </button>
          </div>

          <!-- Header -->
          <div class="mb-6">
            <h2 class="text-lg text-white font-semibold">Server invite link settings</h2>
          </div>

          <div class="space-y-4">
            <div>
              <label class="text-white text-base block mb-2">Expire After</label>
              <div class="relative">
                <select v-model="expireAfter" class="w-full bg-[#1e1f22] text-white px-4 py-2 rounded-md appearance-none">
                  <option value="30min">30 minutes</option>
                  <option value="1h">1 hour</option>
                  <option value="6h">6 hours</option>
                  <option value="12h">12 hours</option>
                  <option value="1d">1 day</option>
                  <option value="7d">7 days</option>
                  <option value="never">Never</option>
                </select>
                <div class="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none text-gray-400">
                  <IconSystem name="chevron-down" :size="20" />
                </div>
              </div>
            </div>

            <div>
              <label class="text-white text-base block mb-2">Max Number Of Uses</label>
              <div class="relative">
                <select v-model="maxUses" class="w-full bg-[#1e1f22] text-white px-4 py-2 rounded-md appearance-none">
                  <option value="0">No limit</option>
                  <option value="1">1 use</option>
                  <option value="5">5 uses</option>
                  <option value="10">10 uses</option>
                  <option value="25">25 uses</option>
                  <option value="50">50 uses</option>
                  <option value="100">100 uses</option>
                </select>
                <div class="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none text-gray-400">
                  <IconSystem name="chevron-down" :size="20" />
                </div>
              </div>
            </div>

            <div class="flex items-center justify-between">
              <div>
                <div class="flex items-center w-full">
                  <label class="flex-1 text-white text-sm">Grant temporary membership</label>
                  <div class="relative flex-initial shrink-0 h-[28px] rounded-[16px] border-1 border-solid border-transparent">
                    <div class="relative block w-[42px] h-[26px] rounded-[14px] cursor-pointer transition-colors duration-150 opacity-100" :class="{ 'bg-[#5865f2]': temporaryMembership, 'bg-[#2d2d2d]': !temporaryMembership }">
                      <div class="absolute top-[3px] h-[20px] w-[28px] transition-all duration-150" :class="{ 'left-[15px]': temporaryMembership, 'left-0': !temporaryMembership }">
                        <svg class="absolute" width="28" height="20" viewBox="0 0 28 20">
                          <rect fill="white" x="4" y="0" height="20" width="20" rx="10"></rect>
                        </svg>
                        <IconSystem 
                          v-if="temporaryMembership" 
                          name="toggle-check"
                          colorClass="text-[#5865f2]"
                          :size="20"
                          class="absolute left-[4px]"
                        />
                        <IconSystem 
                          v-else 
                          name="toggle-cross"
                          colorClass="text-[#2d2d2d]"
                          :size="20"
                          class="absolute left-[4px]"
                        />
                      </div>
                      <input id="temporaryMembership" v-model="temporaryMembership" type="checkbox" class="absolute opacity-0 w-full h-full cursor-pointer m-0" tabindex="0">
                    </div>
                  </div>
                </div>
                <div>
                  <p class="text-gray-400 text-sm mt-1">
                    Temporary members are automatically kicked when they disconnect unless a role has been assigned
                  </p>
                </div>
              </div>
              
            </div>

            <div class="flex justify-end gap-3 mt-6 pt-4 border-t border-[#3f4147]">
              <button 
                @click="showEditLinkSettings = false"
                class="text-white text-sm hover:underline bg-transparent border-0 cursor-pointer px-0 py-0 flex items-center"
              >
                Cancel
              </button>
              <button 
                @click="generateNewLink"
                class="px-6 py-2 text-sm rounded-md bg-[#5865f2] hover:bg-[#4752c4] text-white"
                :disabled="isGenerating"
              >
                {{ isGenerating ? 'Generating...' : 'Generate a New Link' }}
              </button>
            </div>
          </div>
        </div>
      </div>

    </div>
  </Teleport>
</template>

<script setup>
import { ref, watch, onMounted, computed, inject } from 'vue'
import IconSystem from './IconSystem.vue'
import { getCookie } from '@/util/session'

const server = inject('active-server')

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  channelName: {
    type: String,
    default: 'general'
  }
})

// Computed properties from server object
const serverName = computed(() => server?.value.name || '')

const emit = defineEmits(['close'])

const searchQuery = ref('')
const showEditLinkSettings = ref(false)
const inviteLink = ref('')
const inviteCode = ref('')
const temporaryMembership = ref(false)
const expireAfter = ref('7d')
const maxUses = ref('0')
const isLoading = ref(false)
const isGenerating = ref(false)
const expirationText = ref('expires in 7 days')
const currentInvitation = ref(null)

// Mock friends data - replace with real data later
const friends = ref([
  { id: 1, name: 'bro1', avatar: '/media/avatar/1/bdbc994d934c23096e02a768984d7b36.gif' },
  { id: 2, name: 'bro2', avatar: '/media/avatar/1/bdbc994d934c23096e02a768984d7b36.gif' },
  { id: 3, name: 'friend1', avatar: '/media/avatar/1/bdbc994d934c23096e02a768984d7b36.gif' },
])

// Convert expireAfter to minutes
const getExpirationMinutes = () => {
  switch (expireAfter.value) {
    case '30min': return 30
    case '1h': return 60
    case '6h': return 360
    case '12h': return 720
    case '1d': return 1440
    case '7d': return 10080
    case 'never': return 0
    default: return 10080 // Default 7 days
  }
}

// Watch for when the modal opens to fetch an invitation code
watch(() => props.isOpen, async (isOpen) => {
  if (isOpen && server.value?.cid) {
    await fetchOrCreateInvitation()
  }
})

// Watch for changes in expiration settings to update UI
watch([expireAfter, maxUses], () => {
  if (currentInvitation.value) {
    updateExpirationText()
  }
})

// Fetch an existing invitation or create a new one
const fetchOrCreateInvitation = async () => {
  if (!server.value?.cid) {
    console.error('Server ID is missing')
    return
  }

  isLoading.value = true
  try {
    // First try to get existing invitations
    const response = await fetch(`/api/i/server/${server.value.cid}/invitations/`, {
      method: 'GET',
      headers: {
        'Content-type': 'application/json',
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      if (data.r && data.invitations && data.invitations.length > 0) {
        // Find the best invitation based on our preferences:
        // 1. Prioritize unlimited uses (max_uses = 0)
        // 2. Prioritize 7-day expiry or never expires
        
        // First, try to find an invitation with unlimited uses and 7-day expiry
        let bestInvitation = data.invitations.find(inv => 
          inv.max_uses === 0 && inv.valid_duration_minutes === 10080);
        
        // If not found, look for unlimited uses with any expiry
        if (!bestInvitation) {
          bestInvitation = data.invitations.find(inv => inv.max_uses === 0);
        }
        
        // If still not found, use the first invitation (already prioritized by backend)
        if (!bestInvitation) {
          bestInvitation = data.invitations[0];
        }
        
        // Use the selected invitation
        currentInvitation.value = bestInvitation;
        inviteCode.value = currentInvitation.value.code;
        updateInviteLink();
        
        // Set the dropdown values based on the current invitation
        setFormValuesFromInvitation(currentInvitation.value);
        
        updateExpirationText();
      } else {
        // No invitations found, create a default one (7 days, unlimited uses)
        await createNewInvitation();
      }
    } else {
      console.error('Failed to fetch invitations');
      await createNewInvitation();
    }
  } catch (error) {
    console.error('Error fetching invitations:', error);
    await createNewInvitation();
  } finally {
    isLoading.value = false;
  }
}

// Set form values based on the current invitation
const setFormValuesFromInvitation = (invitation) => {
  // Set expireAfter value
  if (invitation.is_permanent || invitation.expires_at === 'Never') {
    expireAfter.value = 'never'
  } else {
    // Try to determine the expiry duration from the invitation
    const durationMinutes = invitation.valid_duration_minutes || 10080 // Default to 7 days
    switch (durationMinutes) {
      case 30: expireAfter.value = '30min'; break
      case 60: expireAfter.value = '1h'; break
      case 360: expireAfter.value = '6h'; break
      case 720: expireAfter.value = '12h'; break
      case 1440: expireAfter.value = '1d'; break
      case 10080: expireAfter.value = '7d'; break
      default: expireAfter.value = '7d'; break
    }
  }
  
  // Set maxUses value
  maxUses.value = invitation.max_uses?.toString() || '0'
}

const sendInvitationRequest = async (durationMinutes, maxUses) => {
  if (!server.value?.cid) {
    console.error('Server ID is missing')
    return
  }

  const form_data = new FormData()
  form_data.append('duration_minutes', durationMinutes)
  form_data.append('max_uses', maxUses)

  const response = await fetch(`/api/i/server/${server.value.cid}/create_invitation/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: form_data
  })

  return response
}

const handleInvitationResponse = async (response) => {
  if (response.ok) {
    const data = await response.json()
    console.log('Invitation response:', data)
    if (data.r) {
      currentInvitation.value = data
      inviteCode.value = data.code
      updateInviteLink()
      updateExpirationText()
      return true
    } else {
      console.error('Failed to create invitation:', data.error)
    }
  } else {
    console.error('Failed to create invitation')
  }
  return false
}

// Create a new invitation with default settings (7 days, unlimited uses)
const createNewInvitation = async () => {
  isLoading.value = true
  try {
    const response = await sendInvitationRequest(10080, 0)
    await handleInvitationResponse(response)
  } catch (error) {
    console.error('Error creating invitation:', error)
  } finally {
    isLoading.value = false
  }
}

// Apply selected settings and get an invitation code matching those settings
const generateNewLink = async () => {
  isGenerating.value = true
  try {
    const response = await sendInvitationRequest(getExpirationMinutes(), maxUses.value)
    const success = await handleInvitationResponse(response)
    if (success) {
      showEditLinkSettings.value = false
    }
  } catch (error) {
    console.error('Error creating invitation:', error)
  } finally {
    isGenerating.value = false
  }
}

// Update the invite link based on the current code
const updateInviteLink = () => {
  if (inviteCode.value) {
    const hostname = window.location.hostname
    const port = window.location.port
    const protocol = window.location.protocol
    const host = port ? `${hostname}:${port}` : hostname
    inviteLink.value = `${protocol}//${host}/invitation/${inviteCode.value}`
  }
}

// Update the expiration text based on the current settings
const updateExpirationText = () => {
  if (!currentInvitation.value) return
  
  if (expireAfter.value === 'never') {
    expirationText.value = 'never expires'
  } else {
    expirationText.value = `expires in ${expireAfter.value === '1d' ? '1 day' : expireAfter.value}`
  }
  
  if (maxUses.value === '0') {
    expirationText.value += ' and has unlimited uses'
  } else {
    expirationText.value += ` and has ${maxUses.value} use${parseInt(maxUses.value) > 1 ? 's' : ''}`
  }
}

const close = () => {
  emit('close')
  showEditLinkSettings.value = false
}

const copyLink = () => {
  navigator.clipboard.writeText(inviteLink.value)
  // Could add a toast notification here
}
</script> 