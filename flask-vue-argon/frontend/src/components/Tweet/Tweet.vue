<template>
    <div class="Tweet">
        <div class="row" v-for="tweet in tweet_list" :key="tweet.id">
            <div class="col-xl-12 col-lg-12">
                <stats-card title="Total traffic"
                            type="gradient-red"
                            icon="ni ni-active-40"
                            class="mb-4 mb-xl-0"
                >
                    <span style="font-size: 30px">{{ tweet.words }}</span>
                    <template slot="footer">
                        <span class="text-success mr-2" style="font-size: 25px"><i class="fa fa-user"
                                                                                   aria-hidden="true"></i>  {{ tweet.creator }}</span>
                        <span class="text-nowrap">{{ tweet.created_at }}</span>
                    </template>
                </stats-card>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: 'all-tweet',
        data() {
            return {
                tweet_list: [],
            }
        },
        methods: {
            getTweet() {
                let path = "http://" + window.location.hostname + ":5000/api2/board/tweet";
                let token = localStorage.token
                axios.defaults.headers.common['Authorization'] = `Bearer: ${token}`
                axios.get(path).then((res) => {
                    this.tweet_list = res.data;
                }).catch((error) => {
                    console.error(error);
                });
            }
        },
        created() {
            this.getTweet();
        }
    };
</script>
