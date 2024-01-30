<template>
  <div class="signup">
    <div class="su-block">
      <div class="su-wrapper">
        <ul
          class="stepper w-96 m-auto"
          data-mdb-stepper="stepper"
        >
          <li
            class="stepper-step"
            :class="{ 'stepper-active': !if_in_ouc }"
          >
            <div class="stepper-head">
              <span class="stepper-head-icon"> 1 </span>
              <span class="stepper-head-text"> 验证身份 </span>
            </div>
            <div class="stepper-content">
              通过验证你的ouc在校或者校友身份来获得注册资格,所有信息都将只用于一次性验证而没有其他用途。
            </div>
          </li>
          <li
            class="stepper-step"
            :class="{ 'stepper-active': if_in_ouc }"
          >
            <div class="stepper-head">
              <span class="stepper-head-icon"> 2 </span>
              <span class="stepper-head-text"> 重置密码 </span>
            </div>
            <div class="stepper-content">重新设置您的密码</div>
          </li>
        </ul>

        <div class="two-forms">
          <!-- validate identity form part -->
          <IfInOuc
            v-show="!if_in_ouc"
            :csrftoken="csrftoken"
            :cmt="cmt"
            :choice="1"
            @go-to-reset="goToReset"
          >
          </IfInOuc>

          <!-- sign up form part -->
          <div
            v-show="if_in_ouc"
            class="su-container h-fit"
          >
            <div class="msg w-72 h-fit m-auto">
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
                v-show="stu_not_signup"
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
                该学号没有注册,&nbsp;&nbsp; <a class="text-lime-600" href="/user/signup">立即注册？</a>
              </div>
              <div
                v-show="stu_credentials_wrong"
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
                信息门户密码不正确
              </div>
            </div>
            <div class="flex justify-center">
              <div>
                <form
                  @submit.prevent="changePassword()"
                  method="POST"
                >
                  <div class="mb-3 xl:w-80 flex flex-col">
                    <label
                      for="exampleFormControlInput4"
                      class="form-label inline-block mb-2 text-gray-700 text-sm text-left"
                      >关联的学号</label
                    >
                    <div class="relative flex flex-row text-xs">
                      <input
                        disabled
                        class="form-control block w-full px-3 py-1.5 font-normal text-gray-700 bg-gray-100 bg-clip-padding border border-r-0 border-solid border-gray-300 rounded-l transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                        type="text"
                        placeholder="关联的学号"
                        autocomplete="nope"
                        v-model="stu_id"
                      />
                      <button
                        class="block font-normal px-3 text-gray-700 bg-gray-100 bg-clip-padding border border-solid border-gray-300 rounded-r transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none whitespace-nowrap"
                        type="button"
                        @click="goBeforeReset()"
                      >
                        返回
                      </button>
                    </div>
                  </div>
                  <div class="mb-3 xl:w-80 flex flex-col">
                    <label
                      for="exampleFormControlInput4"
                      class="form-label inline-block mb-2 text-gray-700 text-sm text-left"
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
                        disabled
                        class="form-control block w-full px-2 py-1 text-sm font-normal text-gray-700 bg-gray-100 bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                        type="text"
                        id="username"
                        name="username"
                        placeholder="账号"
                        autocomplete="nope"
                        v-model="username"
                      />
                    </div>
                  </div>
                  <div class="mb-3 xl:w-80">
                    <label
                      for="exampleFormControlInput4"
                      class="form-label inline-block mb-2 text-gray-700 text-sm text-left w-full"
                      >新密码</label
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
                    />
                  </div>
                  <div class="mb-3 xl:w-80">
                    <label
                      for="exampleFormControlInput4"
                      class="form-label inline-block mb-2 text-gray-700 text-sm text-left w-full"
                      >验证码</label
                    >
                    <div class="relative">
                      <img ref="vcodeImg" @click="refreshVcode()" id="vcode" class="rounded-r absolute h-full right-0 w-14" href="/api/user/Vcode/" alt="">
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
                      class="inline-block px-6 py-2.5 my-2 bg-blue-600 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
                    >
                      确认
                    </button>
                    <div class="relative py-2 text-sm">
                      又想起来密码啦，<a class="text-blue-600 " href="/user/signin/">去登录？</a>
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
import $ from "jquery";
import IfInOuc from "./IfInOuc.vue";

const if_in_ouc = ref(false);
const stu_not_signup = ref(false);
const signup_varification_correct = ref(true);
const stu_credentials_wrong = ref(false);

const signup_pwd_match = ref(true);

const username = ref("");
const stu_pwd = ref("");
const stu_id = ref("");
const pwd = ref("");
const pwd2 = ref("");
const vcode = ref("");
const vcodeImg = ref(null);

const csrftoken = getCookie("csrftoken");
const cmt = ref("");

async function h256(string) {
  const utf8 = new TextEncoder().encode(string);
  const r = await crypto.subtle.digest('SHA-256', utf8).then((hashBuffer) => {
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray
      .map((bytes) => bytes.toString(16).padStart(2, '0'))
      .join('');
    return hashHex;
  });
  return r;
}

function refreshVcode() {
  $(vcodeImg.value).attr('src', '/api/user/Vcode/');
}

function checkPwdMatch() {
  if (pwd2.value == '') return;
  if (pwd2.value == pwd.value) signup_pwd_match.value = true;
  else signup_pwd_match.value = false;
}

const invalid_style = ref(
  "border-pink-500 text-pink-600 focus:border-pink-500 focus:ring-pink-500"
);

function goReset() {
  console.log("now we know u r signed up, reset p");
  if_in_ouc.value = true;
}

async function goBeforeReset() {
  
  if_in_ouc.value = false;
  
}

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
    cmt.value = text.toString();
  });
}
getToken();

async function goToReset(ps) {
  stu_id.value = ps[0];
  stu_pwd.value = ps[1];
  const d = {
    csrfmiddlewaretoken: cmt.value,
    stu_id: stu_id.value,
    stu_pwd: stu_pwd.value,
  };
  var form_data = new FormData();
  for (var v in d) {
    form_data.append(v, d[v]);
  }
  const res = await $.ajax({
    url: "/api/user/getUsername/",
    method: "POST",
    headers: { "X-CSRFToken": csrftoken },
    processData: false,
    contentType: false,
    data: form_data,
  })
    .done(function (data, textStatus, xhr) {})
    .fail(function (jqXHR, textStatus, errorThrown) {
      console.log(jqXHR.status);
    });
  const r = JSON.parse(res);
  console.log(r);
  if (r["state"]) {
    username.value = r['username'];
    goReset();
  }
}

async function changePassword() {
  signup_varification_correct.value = true;
  stu_not_signup.value = false;
  stu_credentials_wrong.value = false;
  if (!signup_pwd_match.value) return;
  const d = {
    csrfmiddlewaretoken: cmt.value,
    stu_id: stu_id.value,
    stu_pwd: stu_pwd.value,
    code: vcode.value,
    pwd: await h256(pwd.value),
  };
  var form_data = new FormData();
  for (var v in d) {
    form_data.append(v, d[v]);
  }
  const res = await $.ajax({
    url: "/api/user/resetPwd/",
    method: "POST",
    headers: { "X-CSRFToken": csrftoken },
    processData: false,
    contentType: false,
    data: form_data,
  })
    .done(function (data, textStatus, xhr) {
      refreshVcode();
      const r = JSON.parse(data);
      console.log(r);
      if (r["state"]) {
        console.log('修改成功');
      } else {
        switch (r["msg"]) {
          case 1:
            signup_varification_correct.value = false;
            console.log("验证码错误");
            break;
          case 3:
            stu_not_signup.value = true;
            console.log("该学号没有注册信息");
            break;
          case 2:
            stu_credentials_wrong.value = true;
            console.log("未知错误，请刷新重新验证学号"); // 密码不正确
            break;
        }
      }
    })
    .fail(function (jqXHR, textStatus, errorThrown) {
      console.log(jqXHR.status);
    });
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
