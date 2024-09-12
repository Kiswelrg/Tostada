<template>
<div class="flex z-[2] h-[var(--m-userbar-height)] grow-0 shrink-0 mb-px w-full pr-2 pl-[6px] bg-userbar-bg items-center">

    <div class="flex min-w-[120px] h-[42px] mr-2 pl-0.5 hover:bg-userbar-hoverbg rounded-md items-center">
        <div class="h-8 w-8 shrink-0 rounded-full bg-hui-800 cursor-pointer">
            <img class="rounded-full h-full w-full" :src="userAvatarUrl" alt="">
        </div>
        <div class="h-[42px] grow mr-1 cursor-pointer py-1 pl-2 min-w-0 text-left">
            
            <div class="username-text whitespace-nowrap text-ellipsis overflow-hidden">
                <div>
                    {{ UserInfo?.username }}
                </div>
            </div>
            <div class="status-text whitespace-nowrap text-ellipsis overflow-hidden">
                <div>
                    Online
                </div>
            </div>
            
        </div>
    </div>
    <div class="buttonlist flex flex-initial nowrap justify-start items-stretch">
        <div class="h-8 w-8 flex justify-center items-center rounded-md hover:bg-userbar-hoverbg">
            <font-awesome-icon :icon="['fas', 'microphone']"
                class="block h-5 w-5 object-contain text-interactive-normal"
                />
        </div>
        <div class="h-8 w-8 flex justify-center items-center rounded-md hover:bg-userbar-hoverbg">
            <font-awesome-icon :icon="['fas', 'headphones']"
                class="block h-5 w-5 object-contain text-interactive-normal"
                />
        </div>
        <div class="h-8 w-8 flex justify-center items-center rounded-md hover:bg-userbar-hoverbg">
            <font-awesome-icon :icon="['fas', 'gear']"
                class="block h-5 w-5 object-contain text-interactive-normal"
                />
        </div>
    </div>
    <div class="bg-red-400 h-5 w-5 absolute bottom-0 hidden"></div>
</div>
</template>

<script setup>
import { computed, onBeforeMount, ref } from 'vue'
import { jsonWithBigInt } from '@/util/parse'

const UserInfo = ref(undefined);
onBeforeMount(async () => {
    const fetchedInfo = await getOwnInfo()
    UserInfo.value = jsonWithBigInt(fetchedInfo)

})

const userAvatarUrl = computed(() => {
    if (UserInfo.value === undefined || UserInfo.value.avatar == '' || UserInfo.value.avatar == '#') return '/static/tool/main/user-solid.svg'
    return UserInfo.value.avatar + '?size=128'
})


const getOwnInfo = async () => {
  const r = await fetch("/api/account/info/", {
    method: "GET",
    headers: {
      "Content-type": "application/json",
    },
  });
  if (!r.ok) {
    return {'username': 'loading', 'avatar': '#'}
  }
  const text = await r.text(); // Fetch the response text
  return text; // Return it from the function
}


</script>


<style lang="scss">
:root {
    --m-userbar-height: 53px;
}
</style>

<style lang="scss" scoped>
.username-text {
    font-size: 14px;
    line-height: 18px;
    color: #f2f3f5;
}

.status-text {
    font-size: 12px;
    line-height: 16px;
    color: #b5bac1;
}
</style>