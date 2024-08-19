<template>
    <div style="padding-left: 15px; padding-right: 15px;">
        <div class="terminal-box">
            <p style="text-align: center; background-color: var(--secondary-color); color: aquamarine; letter-spacing: 2px; font-weight: 600; font-size: 20px; margin-bottom: 1rem;">Scan Report</p>
            <div style="display: flex; margin-bottom: 0.6rem;">
                <div class="de-box-1">
                <p>Scanner <span>BugZipper</span></p>
                <p>Version <span style="margin-left: 3.5rem;">1.0</span></p>
                <p>Editor  <span style="margin-left: 4.4rem;">Code Ninja</span></p>
                <p>Website <span style="margin-left: 3.2rem;">www.bugzipper.com</span></p>
            </div>
               <div class="de-box-first-2">
                <p>BugZipper scan report for {{ singleValue('addr') }} </p>
            <div style="margin-left: 1rem; margin-top: 1rem;">
                <table class="start-result">
                    <tr>
                        <td>Target :</td>
                        <td>{{  singleValue('addr') }}</td>
                    </tr>
                    <tr>
                        <td>Device State : </td>
                        <td>{{  singleValue('state')  }}</td>
                    </tr>
                    <tr>
                        <td>Scan Start Time :</td>
                        <td>{{  singleValue('startstr')  }}</td>
                    </tr>
                    <tr>
                        <td>Last Boot :</td>
                        <td>{{  singleValue('lastboot')  }}</td>
                    </tr>
                </table>
                
            </div>
               </div>
            </div>
            
            
            <div class="de-table">
                <table class="de-port-table">
                    <thead>
                        <tr>
                            <th>INDEX</th>
                            <th>PORT</th>
                            <th>STATUS</th>
                            <th>SERVICE</th>
                            <th>VERSION</th>
                            <th>REASON</th>
                            <th>GO TO</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(scan, index) in scan_info.port_info" :key="index"> 
                            <td>{{ index + 1 }}</td>
                            <td>{{ scan.portid + "/" + scan.protocol }}</td>
                            <td>{{ scan.state }}</td>
                            <td>{{ scan.service_name }}</td>
                            <td>{{ (scan.service_product || '') + ' ' + (scan.service_version || '') }}</td>
                            <td>{{ scan.reason }}</td>
                            <td>
                                <a :href="'#'+scan.portid">
                                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 48 48">
                                    <path fill="none" stroke="#00acd7" stroke-linecap="round" stroke-linejoin="round" stroke-width="4" d="m14 12l12 12l-12 12m20-24v24" />
                                </svg>
                                </a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <p style="text-align: center; background-color: var(--secondary-color); color: aquamarine; letter-spacing: 2px; font-weight: 600; font-size: 20px; margin: 4rem 0 2rem 0;">Os Detection</p>
            <div class="os-container">
            <div class="de-os-system" v-for="(scan, index) in scan_info.host_info" :key="index">
                <table v-if="scan.os_name || scan.os_family || scan.os_gen || scan.os_accuracy || scan.os_vendor">
                    <tr v-if="scan.os_name">
                        <th>Running :</th>
                        <td>{{ scan.os_name }}</td>
                    </tr>
                    <tr v-if="scan.os_family">
                        <th>Family : </th>
                        <td>{{ scan.os_family }}</td>
                    </tr>
                    <tr v-if="scan.os_name">
                        <th>OS Detail :</th>
                        <td>{{ scan.os_name + " / Generation " + scan.os_gen }}</td>
                    </tr>
                    <tr v-if="scan.os_accuracy">
                        <th>Accuracy :</th>
                        <td>{{ scan.os_accuracy + "%" }}</td>
                    </tr>
                    <tr v-if="scan.os_vendor">
                        <th>Vendoor :</th>
                        <td>{{ scan.os_vendor }}</td>
                    </tr>
                </table>
                <p v-else>No operating system detected</p>
                
            </div>
            </div>
            <p id="hhh" style="text-align: center; background-color: var(--secondary-color); color: aquamarine; letter-spacing: 2px;font-weight: 600; font-size: 20px; margin: 4rem 0 2rem 0;">Port Results</p>
            <div class="de-port-result" v-for="(scan, index) in scan_info.port_info" :key="index">
                <dl v-if="scan.service_name !== 'Unknown'">
                    <dt style="color: greenyellow;" :id="scan.portid"> {{ scan.portid  }}<span style="font-size: 12px;">/{{ scan.protocol }}</span></dt>
                    <dd>
                        <table class="start-result">
                        <tr v-if="scan.service_name">
                            <td>Service Name:</td>
                            <td>{{ scan.service_name }}</td>
                        </tr>
                        <tr v-if="scan.service_product">
                            <td>Service Product:</td>
                            <td>{{ scan.service_product }}</td>
                        </tr>
                        <tr v-if="scan.service_version">
                            <td>Service Version:</td>
                            <td>{{ scan.service_version }}</td>
                        </tr>
                        <tr v-if="scan.state">
                            <td>State:</td>
                            <td>{{ scan.state }}</td>
                        </tr>
                        <tr v-if="scan.service_extrainfo">
                            <td>Extra Info:</td>
                            <td>{{ scan.service_extrainfo }}</td>
                        </tr>
                    </table>
                    <div v-if="scan_info.script_info.some(scanScript => scanScript.port_id === scan.id)" class="script-display">
                        <h3 class="h3-deta">Details :</h3>
                        <div v-for="(scanScript, index) in scan_info.script_info" :key="index">
                            <dl v-if="scan.id === scanScript.port_id">
                                <dt v-html="scanScript.script_id"></dt>
                                <dd>{{ scanScript.output }}</dd>
                            </dl>
                        </div>
                    </div>
                    <hr style="margin-top: 1rem; width: 100%;"/>
                    </dd>
                </dl>
            </div>
        </div>
    </div>
</template>

<script setup>
    import axios from 'axios';
    import { ref, onMounted } from 'vue';
    import { useRoute } from 'vue-router';

    const route = useRoute();
    const scan_info_id = ref(route.params.id);
    const scan_info = ref({
        host_info: ref([]),
        port_info: ref([]),
        script_info: ref([])
    });
    onMounted(async () => {
        try {
            const response = await axios.get('http://127.0.0.1:4000/details', {
                params: {
                    "scan_info_id": scan_info_id.value
                }
            });
            scan_info.value.host_info = response.data.infoHost;
            scan_info.value.port_info = response.data.infoPort;
            scan_info.value.script_info = response.data.infoScript;
        } catch (err) {
            console.log(err);
        }
    });

    const singleValue = (key) => {
        let check = Boolean;
        for(let obj of scan_info.value.host_info) {
            if(obj.hasOwnProperty(key)) {
                check = false
                return obj[key]
            } else {
                check = true
            }
        }
        if(check === true) {
            for(let obj of scan_info.value.port_info) {
                if(obj.hasOwnProperty(key)) {
                    check = false
                    return obj[key]
                }
                else {
                    check = true
                    return "[ Something went wrong ]"
                }
            }
        }
};
</script>

<style scoped>
.terminal-box {
    width: 93rem;
    height: 41rem;
    margin-top: 1rem;
    border-radius: 10px;
    overflow-x: hidden;
    overflow-y: auto;
    padding: 1.7rem;
    color: #c3d1c3;
    background: var(--color-bg);
    box-shadow: 0 0 8px var(--color-box-shadow) inset;
}

.de-box-1 {
    border: 2px solid var(--color-search);
    width:60%;
    height: 12.5rem;
    border-radius: 5px;
    padding: 2rem;
    text-align: left;
    background: #13111c69;
}
.de-box-first-2 {
    margin-left: 3rem;
    width: 40%;
    height: 12.5rem;
    border-radius: 5px;
    padding: 20px 0 0 20px;
    border: 2px solid var(--color-search);
    background: #13111c69;
}

.de-box-1 p{
    margin-bottom: 0.8rem;
    display: flex;
    text-align: end;
}

.de-box-1 span {
    margin-left: 3rem;
    color: white;
}

.de-table {
    width: 100%;
    border-radius: 0.5rem;
    overflow: hidden;
    margin-top: 1.5rem;
    border: 2px solid var(--color-search);
    max-height: 21rem;
    overflow-y: scroll;
    background: #13111c69;
}

.de-port-table tr:nth-child(even) {
    background: rgba(71, 71, 71, 0.162);
}

.de-port-table {
    width: 100%;
    border: none;
    border-collapse: collapse;
    text-align: center;
}


.de-port-table thead th{
    background-color: #383838;
    padding: 0.3rem;
}

.de-port-table tbody td {
    padding: 0.2rem 0.3rem;
}

.os-container {
    margin: 1.5rem 0;
    border: 2px solid var(--color-search);
    border-radius: 5px;
    padding: 20px 5px;
    width: 70rem;
    background: #13111c69;
}

.de-os-system {
    margin-left: 2rem;
    width: 70rem;
}


.de-os-system table th{
    text-align: start;
    width: 6rem;
    font-weight: 300;
}


.de-port-result {
    width: 70rem;
    height: auto;
    margin-left: 2rem;
}

.de-port-result dt {
    font-size: 20px;
    font-weight: 500;
    margin-bottom: 0.5rem;
}

.de-port-result dd {
    margin-bottom: 2px;
    margin-left: 2rem;
    text-align: start;
}

.de-port-result dd:nth-last-child(1) {
    margin-bottom: 1rem;
}

.start-result {
    text-align: left;
}


.start-result tr td {
    padding-left: 1rem;
}

/* script-display */

.h3-deta {
    background-color: rgb(171, 171, 171);
    display: inline-block;
    color: black;
    font-weight: 600;
    padding: 0rem 1rem;
    margin-top: 2rem;
    margin-bottom: 1rem;
}

.script-display {
    margin-left: 2rem;
}

.script-display dt {
    font-size: 19px;
    font-weight: 400;
}

.script-display dd {
    white-space: pre-line;
}

</style>


