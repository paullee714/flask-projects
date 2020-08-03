<template>
    <div>
        <base-header type="gradient-success" class="pb-6 pb-8 pt-5 pt-md-8">
            <!-- Card stats -->
            <div class="row mt-5">
                <div class="col-md-12">
                    <tweet></tweet>
                </div>
            </div>
        </base-header>


        <!-- my code            -->
        <div class="row mt-5">
            <div class="col-md-12">
                <my-little-div></my-little-div>
            </div>
        </div>

    </div>

</template>
<script>
    // Charts

    // axios
    import axios from 'axios';

    // my code
    import MyLittleDiv from "./MyLittleDiv/MyLittleDiv";
    import Tweet from "../components/Tweet/Tweet";

    export default {
        components: {
            // my componenets
            MyLittleDiv,
            Tweet
        },
        data() {
            return {
                my_data: '',
            };
        },
        methods: {
            getMyData() {
                let path = "http://" + window.location.hostname + ":5000/";
                axios.get(path).then((res) => {
                    this.my_data = res.data;
                }).catch((error) => {
                    console.error(error);
                });
            },
        },
        created() {
            this.getMyData();
        },
        mounted() {
        }
    };
</script>
<style></style>
