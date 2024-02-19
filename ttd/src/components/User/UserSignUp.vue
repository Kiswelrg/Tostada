<template>
  <div class="signup">
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
              >注册</a
            >
          </li>
          
        </ul>

        <div class="two-forms">
          <!-- validate identity form part -->
          <!-- <IfInOuc
            v-show="!if_in_ouc"
            :csrftoken="csrftoken"
            :cmt="cmt"
            @ifCanSignup="ifCanSignup"
          >
          </IfInOuc> -->

          <!-- sign up form part -->
          <div
            class="su-container h-fit"
          >
            <div class="msg w-72 h-fit m-auto">
              <div
                v-show="!signup_pwd_match"
                class="text-sm bg-red-100 rounded-lg py-2 px-6 mb-3 text-red-700 inline-flex items-center w-full"
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
                两次密码不匹配
              </div>
              <div
                v-show="!signup_varification_correct"
                class="text-sm bg-red-100 rounded-lg py-2 px-6 mb-3 text-red-700 inline-flex items-center w-full"
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
                v-show="username_taken"
                class="bg-yellow-100 rounded-lg py-2 px-6 mb-3 text-sm text-yellow-700 inline-flex items-center w-full"
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
                该用户名已经被注册了,&nbsp;&nbsp; 哭哭
              </div>
            </div>
            <div class="flex justify-center">
              <div>
                <form
                  @submit.prevent="signUp()"
                  method="POST"
                >
                  <div class="mb-3 xl:w-80 flex flex-col">
                    <label
                      for="exampleFormControlInput4"
                      class="form-label inline-block mb-2 text-gray-700 text-sm"
                      >账号</label
                    >
                    <div class="relative">
                      <svg
                        aria-hidden="true"
                        focusable="false"
                        data-prefix="fas"
                        data-icon="info-circle"
                        title="设置在本站使用的账号密码，为了安全起见，不和信息门户账号一致"
                        class="w-4 h-4 mr-2 fill-current absolute right-0 top-1/2 transform -translate-y-1/2"
                        role="img"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 512 512"
                      >
                        <path
                          fill="currentColor"
                          d="M256 8C119.043 8 8 119.083 8 256c0 136.997 111.043 248 248 248s248-111.003 248-248C504 119.083 392.957 8 256 8zm0 110c23.196 0 42 18.804 42 42s-18.804 42-42 42-42-18.804-42-42 18.804-42 42-42zm56 254c0 6.627-5.373 12-12 12h-88c-6.627 0-12-5.373-12-12v-24c0-6.627 5.373-12 12-12h12v-64h-12c-6.627 0-12-5.373-12-12v-24c0-6.627 5.373-12 12-12h64c6.627 0 12 5.373 12 12v100h12c6.627 0 12 5.373 12 12v24z"
                        ></path>
                      </svg>
                      <input
                        class="form-control block w-full px-2 py-1 text-sm font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                        type="text"
                        id="username"
                        name="username"
                        pattern="[a-zA-Z0-9 ]+"
                        placeholder="账号"
                        autocomplete="nope"
                        v-model="username"
                        required
                        oninvalid="this.setCustomValidity('用户名只能是6-20字母数字下划线的组合，只能字母开头，且不能下划线结尾')"
                        oninput="this.setCustomValidity('')"
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
                      class="form-control block w-full px-2 py-1 text-sm font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                      :class="{ invalid_style: !signup_varification_correct }"
                      type="password"
                      id="pwd"
                      name="pwd"
                      placeholder="密码"
                      autocomplete="new-password"
                      v-model="pwd"
                      required
                      @input="checkPwdMatch()"
                    />
                  </div>
                  <div class="mb-3 xl:w-80">
                    <label
                      for="exampleFormControlInput4"
                      class="form-label inline-block mb-2 text-gray-700 text-sm"
                      >确认密码</label
                    >
                    <input
                      class="form-control block w-full px-2 py-1 text-sm font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                      :class="{ invalid_style: !signup_varification_correct }"
                      type="password"
                      id="pwd2"
                      name="pwd2"
                      placeholder="密码"
                      autocomplete="new-password"
                      v-model="pwd2"
                      required
                      @input="checkPwdMatch()"
                    />
                  </div>
                  <div class="mb-3 xl:w-80">
                    <label
                      for="exampleFormControlInput4"
                      class="form-label inline-block mb-2 text-gray-700 text-sm"
                      >验证码</label
                    >
                    <div class="relative">
                      <img ref="vcodeImg" @click="refreshVcode()" id="vcode" :src="VcodeUrl" class="rounded-r absolute h-full right-0 w-14" href="/api/user/Vcode/" alt="">
                      <input
                      class="
                        form-control
                        block
                        w-full
                        px-2
                        py-1
                        text-gray-700
                        text-sm
                        font-normal
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
                      pattern="[a-zA-Z0-9]{4}"
                      placeholder=""
                      autocomplete="new-password"
                      v-model="vcode"
                      required
                      oninvalid="this.setCustomValidity('验证码格式不正确')"
                      oninput="this.setCustomValidity('')"
                      />
                    </div>
                  </div>
                  <div class="flex flex-col space-x-2 justify-center mt-4 relative">
                    <button
                      type="submit"
                      data-mdb-ripple="true"
                      data-mdb-ripple-color="light"
                      class="inline-block px-6 py-2.5 my-2 bg-blue-600 font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
                    >
                      注册
                    </button>
                    <div class="relative py-2 text-[12px]">
                      已经注册了？&nbsp;<a class="text-blue-600" href="/user/login/">登录</a>
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
import { ref } from "vue";
import h256 from "@/util/encrypt";

const signup_pwd_match = ref(true);
const username = ref("");
const pwd = ref("");
const pwd2 = ref("");
const signup_varification_correct = ref(true);
const username_taken = ref(false);
const csrftoken = getCookie("csrftoken");
const cmt = ref("");
const vcode = ref("");
const vcodeImg = ref(null);
const VcodeUrl = ref('/api/user/Vcode/');

function refreshVcode() {
  VcodeUrl.value = '/api/user/Vcode/?h=' + Date.now().toString();
}

function checkPwdMatch() {
  if (pwd2.value == '') return;
  if (pwd2.value == pwd.value) signup_pwd_match.value = true;
  else signup_pwd_match.value = false;
}

const invalid_style = ref(
  "border-pink-500 text-pink-600 focus:border-pink-500 focus:ring-pink-500"
);


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

async function getToken() {
  const r = await fetch("/api/user/Token/", {
    method: "GET",
    headers: {
      "Content-type": "application/json",
    },
  });
  r.text().then(function (text) {
    return text.toString();
  });
}

async function signUp() {
  signup_varification_correct.value = true;
  username_taken.value = false;
  if (!signup_pwd_match.value) return;
  const d = {
    csrfmiddlewaretoken: cmt.value,
    username: username.value,
    code: vcode.value,
    pwd: await (pwd.value),
  };
  var form_data = new FormData();
  for (var v in d) {
    form_data.append(v, d[v]);
  }
  // try {
    const response = await fetch("/api/user/dosignup/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
      },
      body: form_data, // Assuming form_data is FormData; no need for processData: false as fetch does not automatically process data like jQuery
    });

    if (response.ok) {
      console.log(response);
      const data = await response.json(); // Assuming the server response is JSON
      refreshVcode();
      if (data["state"]) {
        console.log('sign up success');
      } else {
        switch (data["msg"]) {
          case 1:
            signup_varification_correct.value = false;
            console.log("code wrong");
            break;
          case 2:
            // handle case 2
            console.log("invalid request for you buddy!");
            break;
          case 3:
            username_taken.value = true;
            console.log("username already signed up");
            break;
          // Add more cases as needed
        }
      }
    } else {
      // If the server response was not ok (200-299)
      console.log(response.status);
    }
  // } catch (error) {
  //   // Catch network errors or issues with the fetch call itself
  //   console.error("Fetch error: " + error.message);
  // }

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
