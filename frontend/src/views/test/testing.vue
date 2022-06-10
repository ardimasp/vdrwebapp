<template>
    <div>
        <button @click="setToken">set token</button> <br>
        <button @click="getProfile">fetch data</button>
        <p>{{profile}}</p>
        <p>{{token}}</p>
        <p>{{encrypt}}</p>
    </div>
</template>

<script>
import { defineComponent, ref, } from '@vue/composition-api'
import { decryptToken, encryptToken } from '../../function';
import axios from "axios"

export default defineComponent({
    setup() {
        const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiJ2eW5zc3MiLCJ0eXBlIjoiUmVndWxhciBVc2VyIiwibmFtZSI6InZpY2t5IHZhbmVzc2FhIiwiZXhwaXJ5X2RhdGUiOiIyMDIzLTA1LTMwIiwiYWZmaWxpYXRpb24iOiJCaW51cyIsImV4cCI6MTY1NDY5NzQ4N30.5aQdvYV9PVkOnPy0LVtuDKQPF0RUd3trcI-EHgtgwhA"

        const setToken = () => {
            localStorage.setItem("token", encryptToken(token));
            localStorage.setItem("string", 11111111)
        }

        const encrypt = localStorage.getItem("token");

        const profile = ref()
        const getProfile = async () => {
            await axios.get("https://ec2-13-250-37-201.ap-southeast-1.compute.amazonaws.com/api/v1/registration/profile/vynsss", {
                headers: {
                    Authorization: "Bearer " + decryptToken(localStorage.getItem("token"))
                }
            })
                .then(
                    (res) => {
                        console.log(res);
                        profile.value = res;
                        return res;
                    },
                    (err) => {
                        console.log(err);
                        return err;
                    }
                )
        }

        return {setToken, getProfile, profile, token, encrypt};
    },
})
</script>
