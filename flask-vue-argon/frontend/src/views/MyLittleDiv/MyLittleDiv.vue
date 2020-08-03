<template>
    <div class="MyLittleDiv">
        <div class="card-header border-0">
            <div class="row align-items-center">
                <div class="col">
                    <h3 class="mb-0">Korea BaseBall</h3>
                </div>
            </div>
        </div>
        <div class="text-md-center">
            <div class="table-responsive">
                <base-table thead-classes="thead-light"
                            :data="new_data">
                    <template slot="columns">
                        <th>순위</th>
                        <th>팀</th>
                        <th>경기수</th>
                        <th>승</th>
                        <th>패</th>
                        <th>무</th>
                        <th>승률</th>
                        <th>게임차</th>
                        <th>출루율</th>
                        <th>최근10경기</th>
                    </template>

                    <template slot-scope="{row}">
                        <th scope="row">
                            {{row.rank}} 위
                        </th>
                        <td>
                            <img :src='row.img_url'> {{row.name}}
                        </td>
                        <td>
                            {{row.total_cnt}}
                        </td>
                        <td>
                            {{row.total_win}}
                        </td>
                        <td>
                            {{row.total_lose}}
                        </td>
                        <td>
                            {{row.total_draw}}
                        </td>
                        <td>
                            {{row.win_rate}}
                        </td>
                        <td>
                            {{row.total_diff}}
                        </td>
                        <td>
                            {{row.total_run}}
                        </td>
                        <td>
                            {{row.recent_ten_game}}
                        </td>
                    </template>
                </base-table>
            </div>

        </div>
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: 'my-little-div',
        data() {
            return {
                new_data: [],
            }
        },
        methods: {
            getNewData() {
                let path = "http://" + window.location.hostname + ":5000/baseball_data";
                axios.get(path).then((res) => {
                    this.new_data = res.data;
                }).catch((error) => {
                    console.error(error);
                });
            },
            // getCookie(cname) {
            //     var name = cname + "=";
            //     var decodedCookie = decodeURIComponent(document.cookie);
            //     var ca = decodedCookie.split(';');
            //     for (var i = 0; i < ca.length; i++) {
            //         var c = ca[i];
            //         while (c.charAt(0) == ' ') {
            //             c = c.substring(1);
            //         }
            //         if (c.indexOf(name) == 0) {
            //             return c.substring(name.length, c.length);
            //         }
            //     }
            //     return "";
            // }
        },
        created() {
            this.getNewData();
        }
    };
</script>
