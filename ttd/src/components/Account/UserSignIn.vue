<template>
  <div class="signin">
    <div class="su-block">
      <div class="su-wrapper">
        <ul
          class="
            justify-center
            nav nav-tabs
            flex flex-col
            md:flex-row
            flex-wrap
            list-none
            border-b-0
            pl-0
            mb-4
          "
          id="tabs-tab"
          role="tablist"
        >
          <li class="nav-item" role="presentation">
            <a
              href="#tabs-home"
              class="
                mx-auto
                w-32
                nav-link
                block
                font-medium
                text-xs
                leading-tight
                uppercase
                border-x-0 border-t-0 border-b-2 border-transparent
                px-6
                py-3
                my-2
                hover:border-transparent hover:bg-gray-100
                focus:border-transparent
                active
              "
              id="tabs-home-tab"
              data-bs-toggle="pill"
              data-bs-target="#tabs-home"
              role="tab"
              aria-controls="tabs-home"
              aria-selected="true"
              >登录</a
            >
          </li>
          
        </ul>
        <div class="tab-content" id="tabs-tabContent">
          <div
            class="tab-pane fade show active"
            id="tabs-home"
            role="tabpanel"
            aria-labelledby="tabs-home-tab"
          >
            
          </div>
          
        </div>

        <div class="two-forms">
          <!-- sign in form part -->
          <div class="su-container h-fit">
            <div class="msg w-72 h-fit m-auto">
              <div
                v-show="!varification_correct"
                class="
                  text-sm
                  bg-red-100
                  rounded-lg
                  py-2
                  px-6
                  mb-3
                  text-red-700
                  inline-flex
                  items-center
                  w-full
                "
                role="alert"
              >
                <svg
                  aria-hidden="true"
                  focusable="false"
                  data-prefix="fas"
                  data-icon="times-circle"
                  class="w-4 h-4 mr-2 fill-current"
                  role="img"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 512 512"
                >
                  <path
                    fill="currentColor"
                    d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zm121.6 313.1c4.7 4.7 4.7 12.3 0 17L338 377.6c-4.7 4.7-12.3 4.7-17 0L256 312l-65.1 65.6c-4.7 4.7-12.3 4.7-17 0L134.4 338c-4.7-4.7-4.7-12.3 0-17l65.6-65-65.6-65.1c-4.7-4.7-4.7-12.3 0-17l39.6-39.6c4.7-4.7 12.3-4.7 17 0l65 65.7 65.1-65.6c4.7-4.7 12.3-4.7 17 0l39.6 39.6c4.7 4.7 4.7 12.3 0 17L312 256l65.6 65.1z"
                  ></path>
                </svg>
                验证码不正确
              </div>
              <div
                v-show="!pwd_validity"
                class="
                  bg-yellow-100
                  rounded-lg
                  py-2
                  px-6
                  mb-3
                  text-sm text-yellow-700
                  inline-flex
                  items-center
                  w-full
                "
                role="alert"
              >
                <svg
                  aria-hidden="true"
                  focusable="false"
                  data-prefix="fas"
                  data-icon="exclamation-triangle"
                  class="w-4 h-4 mr-2 fill-current"
                  role="img"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 576 512"
                >
                  <path
                    fill="currentColor"
                    d="M569.517 440.013C587.975 472.007 564.806 512 527.94 512H48.054c-36.937 0-59.999-40.055-41.577-71.987L246.423 23.985c18.467-32.009 64.72-31.951 83.154 0l239.94 416.028zM288 354c-25.405 0-46 20.595-46 46s20.595 46 46 46 46-20.595 46-46-20.595-46-46-46zm-43.673-165.346l7.418 136c.347 6.364 5.609 11.346 11.982 11.346h48.546c6.373 0 11.635-4.982 11.982-11.346l7.418-136c.375-6.874-5.098-12.654-11.982-12.654h-63.383c-6.884 0-12.356 5.78-11.981 12.654z"
                  ></path>
                </svg>
                账号或密码错误, &nbsp;&nbsp;
                <a class="text-lime-600" href="/account/forgetpassword"
                  >忘记密码？</a
                >
              </div>
            </div>
            <div class="flex justify-center">
              <div>
                <form @submit.prevent="signIn()" method="POST">
                  <div class="mb-3 xl:w-80 flex flex-col">
                    <label
                      for="exampleFormControlInput4"
                      class="form-label inline-block mb-2 text-gray-700 text-sm"
                      >账号/邮箱</label
                    >
                    <div class="relative">
                      <input
                        class="
                          form-control
                          block
                          w-full
                          px-2
                          py-1
                          text-sm
                          font-normal
                          text-gray-700
                          bg-white bg-clip-padding
                          border border-solid border-gray-300
                          rounded
                          transition
                          ease-in-out
                          m-0
                          focus:text-gray-700
                          focus:bg-white
                          focus:border-blue-600
                          focus:outline-none
                        "
                        type="text"
                        id="username"
                        name="username"
                        placeholder="账号或邮箱"
                        autocomplete="nope"
                        v-model="username"
                      />
                    </div>
                  </div>
                  <div class="mb-3 xl:w-80">
                    <label
                      for="exampleFormControlInput4"
                      class="form-label inline-block mb-2 text-gray-700 text-sm"
                      >密码</label
                    >
                    <input
                      class="
                        form-control
                        block
                        w-full
                        px-2
                        py-1
                        text-sm
                        font-normal
                        text-gray-700
                        bg-white bg-clip-padding
                        border border-solid border-gray-300
                        rounded
                        transition
                        ease-in-out
                        m-0
                        focus:text-gray-700
                        focus:bg-white
                        focus:border-blue-600
                        focus:outline-none
                      "
                      type="password"
                      id="pwd"
                      name="pwd"
                      placeholder="密码"
                      autocomplete="new-password"
                      v-model="pwd"
                      @input="checkPwdValidity()"
                    />
                  </div>
                  <div class="mb-3 xl:w-80">
                    <label
                      for="exampleFormControlInput4"
                      class="form-label inline-block mb-2 text-gray-700 text-sm"
                      >验证码</label
                    >
                    <div class="relative">
                      <img ref="vcodeImg" @click="refreshVcode()" id="vcode"  :src="VcodeUrl" class="rounded-r absolute h-full right-0 w-14" href="/api/account/Vcode/" alt="">
                      <input
                      class="
                        form-control
                        block
                        w-full
                        px-2
                        py-1
                        text-sm
                        font-normal
                        text-gray-700
                        bg-white bg-clip-padding
                        border border-solid border-gray-300
                        rounded
                        transition
                        ease-in-out
                        m-0
                        focus:text-gray-700
                        focus:bg-white
                        focus:border-blue-600
                        focus:outline-none
                      "
                      type="text"
                      pattern="[a-zA-Z0-9]+"
                      placeholder=""
                      autocomplete="new-password"
                      v-model="vcode"
                      />
                    </div>
                  </div>
                  <div class="flex flex-col justify-center mt-4 relative">
                    <button
                      type="submit"
                      data-mdb-ripple="true"
                      data-mdb-ripple-color="light"
                      class="
                        inline-block
                        px-6
                        py-2.5
                        my-2
                        text-lime-600
                        bg-blue-600
                        font-medium
                        text-xs
                        leading-tight
                        uppercase
                        rounded
                        shadow-md
                        hover:bg-blue-700 hover:shadow-lg
                        focus:bg-blue-700
                        focus:shadow-lg
                        focus:outline-none
                        focus:ring-0
                        active:bg-blue-800 active:shadow-lg
                        transition
                        duration-150
                        ease-in-out
                      "
                    >
                      登录
                    </button>
                    <div class="flex text-[12px] justify-between relative py-2 text-blue-600 text-sm">
                      <a href="/account/signup/">还没注册？</a>
                      <a href="/account/forgetpassword/">忘记密码</a>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  mounted() {
    this.$refs.vcodeImg.click()
  },
  methods: {
    
  }
}
</script>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from 'vue-router';
// import h256 from "@/util/encrypt";
import { getCookie, getToken } from '@/util/session'
const varification_correct = ref(true);
const pwd_validity = ref(true);
const username = ref("");
const pwd = ref("");
const vcode = ref("");
const vcodeImg = ref(null);
const VcodeUrl = ref('/api/account/Vcode/');
const cmt = ref("");
const router = useRouter();
let csrftoken;
onMounted(() => {
  (async ()=> {
    csrftoken = getCookie("csrftoken");
    cmt.value = await getToken();
  })();
});



function refreshVcode() {
  VcodeUrl.value = '/api/account/Vcode/?h=' + Date.now().toString();
}

function checkPwdValidity() {

}

async function signIn() {

  const d = {
    csrfmiddlewaretoken: cmt.value,
    username: username.value,
    pwd: pwd.value,
    code: vcode.value,
  };
  var form_data = new FormData();
  for (var v in d) {
    form_data.append(v, d[v]);
  }

  // for (let [key, value] of form_data.entries()) {
  //   console.log(`${key}: ${value}`);
  // }

  const response = await fetch(
    "/api/account/dosignin/",
    {
      method: "POST",
      headers: { "X-CSRFToken": csrftoken },
      body: form_data,
    }
  );
  
  if (response.ok) {
    refreshVcode();
    const r = await response.json();
    if (r["state"]) {
      varification_correct.value = true;
      pwd_validity.value = true;
      console.log("登陆成功");
      router.push({name: 'tool'});
    } else {
      console.log(r);
      switch (r["msg"]) {
        case 1:
          varification_correct.value = false;
          pwd_validity.value = true;
          console.log("验证码错误");
          break;
        case 2:
          pwd_validity.value = false;
          varification_correct.value = true;
          console.log("帐号/密码错误");
          break;
      }
    }
  } else {
    console.log(response.status);
  }
}
</script>

<style
  lang="scss"
  scoped
>
.form-control:focus:invalid {
  box-shadow: 0 0 3px 1px #eb2525;
}
</style>
