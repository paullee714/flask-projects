<template>
    <div class="row justify-content-center">
        <div class="col-lg-5 col-md-7">
            <div class="card bg-secondary shadow border-0">
                <div class="card-header bg-transparent pb-5">
                    <div class="text-muted text-center mt-2 mb-3"><small>Sign in with</small></div>
                    <div class="btn-wrapper text-center">
                        <a href="#" class="btn btn-neutral btn-icon">
                            <span class="btn-inner--icon"><img src="img/icons/common/github.svg"></span>
                            <span class="btn-inner--text">Github</span>
                        </a>
                        <a href="#" class="btn btn-neutral btn-icon">
                            <span class="btn-inner--icon"><img src="img/icons/common/google.svg"></span>
                            <span class="btn-inner--text">Google</span>
                        </a>
                    </div>
                </div>
                <div class="card-body px-lg-5 py-lg-5">
                    <div class="text-center text-muted mb-4">
                        <small>Or sign in with credentials</small>
                    </div>
                    <form role="form">
                        <base-input class="input-group-alternative mb-3"
                                    placeholder="text"
                                    addon-left-icon="ni ni-email-83"
                                    v-model="userInfo.username">
                        </base-input>

                        <base-input class="input-group-alternative"
                                    placeholder="Password"
                                    type="password"
                                    addon-left-icon="ni ni-lock-circle-open"
                                    v-model="userInfo.userpwd">
                        </base-input>

                        <base-checkbox class="custom-control-alternative">
                            <span class="text-muted">Remember me</span>
                        </base-checkbox>
                        <div class="text-center">
                            <base-button type="primary" class="my-4" v-on:click="makeLogin">Sign in</base-button>
                        </div>
                    </form>
                </div>
            </div>
            <div class="row mt-3">
                <div class="col-6">
                    <a href="#" class="text-light"><small>Forgot password?</small></a>
                </div>
                <div class="col-6 text-right">
                    <router-link to="/register" class="text-light"><small>Create new account</small></router-link>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import axios from 'axios';
    import jwt_decode from 'jwt-decode';

    // var jwtDecode = require('jwt-decode')
    export default {
        name: 'login',
        data() {
            return {
                userInfo: {
                    username: '',
                    userpwd: ''
                }
            }
        },
        methods: {
            setCookie(cookie_name, cookie) {
                var cookie_value = cookie_name + '=' + cookie;
                document.cookie = cookie_value;
            },
            makeLogin() {
                let path = "http://" + window.location.hostname + ":5000/api/auth/login";
                axios.post(path, {
                    username: this.userInfo.username,
                    userpwd: this.userInfo.userpwd
                }, {withCredential: true}).then((res) => {
                    // document.cookie = 'login-token' + '=' + res.data.token
                    let decode_user = jwt_decode(res.data.token)
                    if (decode_user.identity == this.userInfo.username) {
                        alert(this.userInfo.username + " 님, 반갑습니다!")
                        document.cookie = 'login-token' + '=' + res.data.token
                    }

                    // if(this.userInfo.username == )
                }).catch((error) => {
                    console.log(error);
                });
            },
        },
    }
</script>
<style>
</style>
