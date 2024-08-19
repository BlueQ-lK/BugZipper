<template>
  <div class="scanner">
   <div class="container">
<!-- Box 1 -->
   <div class="dashboard">
        <div class="box-1">
            <div class="card-1">
                <div class="port-sacn">                 
                      <div class="first-line">
                        <div class="input-field">
                        <input 
                        type="text" required v-model="insertnumber.ip_addr" :style="'border:'+ scan_message.border" placeholder="Enter IP Address"
                        />
                      </div>
                      <div class="port-input-box" >
                          <input type="text" v-model="insertnumber.port" placeholder="Port Number" title=" Ex: 22 | 1-65535 | 53,111,137"
                          >
                      </div>
                      </div>
                      <div class="second-line">
                        <fieldset>
                          <legend>Scan Type</legend>
                          <input type="radio" name="sctype" id="sca" checked>
                          <label for="sca">TCP Connect Scan</label><br>
                          <input type="radio" name="sctype" id="scb">
                          <label for="scb">SYN Scan</label><br>
                          <input type="radio" name="sctype" id="scc">
                          <label for="scc">UDP Scan</label>
                        </fieldset>
                        <div style="margin-top: 1rem;">
                          <div class="save-btn">
                          <button @click="insertnumber.save = !insertnumber.save"
                            :style="{ backgroundColor: insertnumber.save ? 'green' : '' }"
                          >SAVE</button>
                          <input type="text"  placeholder="New Scan" v-model="insertnumber.saveName" v-if="insertnumber.save">
                          <input type="text"  placeholder="New Scan" v-model="insertnumber.saveName" v-else readonly style="opacity: 0.3;">
                          <div class="aggscan">
                            <button @click="insertnumber.aggscan = !insertnumber.aggscan" 
                            :style="{ backgroundColor: insertnumber.aggscan ? 'green' : '' }"
                            >Deep<span style="color: red;">|</span>scan</button>
                          </div>
                        </div>
                        <div class="speed-type">
                          <input type="radio" name="rad" value="T1" id="rad1" class="radio-input"/>
                              <label for="rad1" class="radio-label">T1</label>
                              <input type="radio" name="rad" value="T2" id="rad2" class="radio-input"/>
                              <label for="rad2" class="radio-label">T2</label>
                              <input type="radio" name="rad" value="T3" id="rad3" class="radio-input"/>
                              <label for="rad3" class="radio-label">T3</label>
                              <input type="radio" name="rad" value="T4" id="rad4" class="radio-input" checked/>
                              <label for="rad4" class="radio-label">T4</label>
                              <input type="radio" name="rad" value="T5" id="rad5" class="radio-input"/>
                              <label for="rad5" class="radio-label">T5</label>
                          </div>
                        </div>
                        
                      </div>
                    <div class="fa-btn">
                        <button @click="sendToBackend">Start</button>                    
                    </div>
                </div>
            </div>
            <div class="fa-text-middle">
              <span :style="'color:'+ scan_message.color" style="position: absolute; top: -0.6rem;">{{ scan_message.rmessage }}</span>
            </div>
            <!-- card-2 -->
            <div class="card-2">
                   <div class="result-view">
                    <div class="table-container">
                      <table class="list-table">
                          <thead>
                              <tr>
                                  <th>
                                    <select name="" id="stat" v-model="selectedaddr">
                                        <option value="stat-id">Index</option>
                                        <option value="stat-ip" style="color: white;">IpList</option>
                                    </select>
                                  </th>
                                  <th>Port<span style="font-size: 13px;"> /tcp</span></th>
                                  <th>
                                    <select name="status-o-c" id="stat" v-model="selectedStatus">
                                      <option value="Status">Status</option>
                                      <option value="closed">Closed</option>
                                      <option value="open">Open</option>
                                    </select>
                                  </th>
                                  <th>Service</th>
                                  <th>Version</th>
                                  <th>Banner Grabbing</th>
                              </tr>
                          </thead>
                          <tbody>
                            <tr v-for="(scan, index) in filterD()" :key="index" @click="showResultterminal(scan.portid)">
                                    <td v-if="selectedaddr === 'stat-id'">{{ index + 1 }}</td>
                                    <td v-else-if="selectedaddr === 'stat-ip'">{{ insertnumber.ip_addr }}</td>
                                    <td>{{ scan.portid }}</td>
                                    <td v-if="scan.state === 'open'" :style="{color: 'green'} ">
                                      <p>{{ scan.state }}</p>
                                    </td>
                                    <td v-else :style="{color: 'red'} ">
                                      <p>{{ scan.state }}</p>
                                    </td>
                                    <td class="stretch">{{ scan.service_name }}</td>
                                    <td>{{ scan.service_version }}</td>
                                    <td>{{ scan.service_product }}</td>
                            </tr>
                          </tbody>
                      </table>
                    </div>
                  </div>                 
            </div>
          </div>
          <div class="side-box">
            <!-- card-3 -->
            <div class="card-3">
                <div class="result" style="background-color: #1c1c1c;">
                  <div class="welc-txt animation-1">
                    <p>
                      ██████╗░██╗░░░██╗░██████╗░███████╗██╗██████╗░██████╗░███████╗██████╗░
                      ██╔══██╗██║░░░██║██╔════╝░╚════██║██║██╔══██╗██╔══██╗██╔════╝██╔══██╗
                      ██████╦╝██║░░░██║██║░░██╗░░░███╔═╝██║██████╔╝██████╔╝█████╗░░██████╔╝
                      ██╔══██╗██║░░░██║██║░░╚██╗██╔══╝░░██║██╔═══╝░██╔═══╝░██╔══╝░░██╔══██╗
                      ██████╦╝╚██████╔╝╚██████╔╝███████╗██║██║░░░░░██║░░░░░███████╗██║░░██║
                      ╚═════╝░░╚═════╝░░╚═════╝░╚══════╝╚═╝╚═╝░░░░░╚═╝░░░░░╚══════╝╚═╝░░╚═╝  V 0.1    
                              <span> █ Author: CodeNinja █ Started On: 10 Dec 2023 █ </span>
                    </p>
                    <br><hr>
                  </div>
                  <br>
                  <div class="db-msg">
                    <p v-if="loadResponse == 'Success'">Successfully connected to database</p>
                    <p v-else>Database Connection error</p>
                  </div>
                  <div class="terminalText" v-if="isButtonClicked">
                    <p>Starting BugZipper ( https://bugzipper.org ) at Scanner v1.0</p>
                    <p>Initiating SYN Stealth Scan</p>
                    <p>Scanning {{ insertnumber.ip_addr }}</p>
                    <div v-for="(scan, index) in scan_info.port_info" :key="index">
                      <p v-if="scan.state == 'open'">Discovered open port {{ scan.portid + "/" + scan.protocol}} on {{ insertnumber.ip_addr }}</p>
                      <p v-else style="display: none;"></p>
                    </div>
                    <p>{{ scan_message.rmessage }}</p>
                    <p>---------------------------------------</p>
                    <p v-html="checkForIgnored"></p>
                    <div v-if="showResultterminalValue[0] === true">
                      <div class="de-port-result" v-for="(scan, index) in scan_info.port_info" :key="index">
                          <dl v-if="scan.portid == showResultterminalValue[1]">
                              <dt> {{ scan.portid  }}<span style="font-size: 12px;">{{ scan.protocol }}</span></dt>
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
                            </dd>
                        </dl>
                    </div>
                    </div>
                  </div>
                </div>
            </div>
          </div>
      </div>
   </div>
  </div>
</template>


<!-- Script -->

<script setup>
  import { onMounted, readonly, ref } from 'vue';
  import axios from 'axios';

  let insertnumber = ref({
    ip_addr: '',
    port: '',
    aggscan: false,
    save: false,
    saveName: 'New Scan'
  });

  const selectedStatus = ref('Status');
  const isButtonClicked = ref(false);
  const selectedaddr = ref('stat-id');
  const scan_message = ref({
    rError: false,
    rmessage: '',
    color: '',
    border: '',
  });
  const scan_info = ref({
        host_info: ref([]),
        port_info: ref([]),
        script_info: ref([]),
  });
  let showResultterminalValue = ref([false, '']);
  const checkForIgnored = ref();
  const loadResponse = ref({});

  onMounted(async () => {
        try {
            const response = await axios.get('http://127.0.0.1:4000/');
            loadResponse.value = response.data.status;
            console.log(loadResponse.value)
        } catch (err) {
            console.log(err);
        }
    })

  const sendToBackend = async () => {
    const ipPattern = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    let ipError = !ipPattern.test(insertnumber.value.ip_addr);


    if (insertnumber.value.ip_addr === "" || ipError) {
      scan_message.value.rError = true;
      scan_message.value.rmessage = "Invalid IP address.";
      scan_message.value.color = 'red';
      scan_message.value.border = '1px solid red';
      
    } else {
      isButtonClicked.value = true
      scan_message.value.rError = false;
      scan_message.value.rmessage = "Scan Started....";
      scan_message.value.color = 'green';
      scan_message.value.border = '1px solid rgb(153, 151, 154)';
      
      try {
        const response = await axios.post('http://127.0.0.1:4000/', {
          ip_addr: insertnumber.value.ip_addr,
          port: insertnumber.value.port,
          aggscan: insertnumber.value.aggscan,
          save: insertnumber.value.save,
          saveName: insertnumber.value.saveName,
        });
        scan_info.value.host_info = response.data.infoHost;
        scan_info.value.port_info = response.data.infoPort;
        scan_info.value.script_info = response.data.infoScript;
        checkForIgnored.value = scan_info.value.port_info.length <= 0 ? `All scanned ports on ${insertnumber.value.ip_addr} are in ignored states.<br>Not shown: ${insertnumber.value.port.replace('-', ' to ')} closed tcp ports (reset)` : null;
        scan_message.value.rmessage = "Scan Completed!!";
        scan_message.value.color = 'yellow';
      } catch (err) {
        console.error(err);
        scan_message.value.rmessage = "Error during scan";
        scan_message.value.color = 'red';
      
      }
    }
  };

  const filterD = () => {
    const filteredByStatus = selectedStatus.value == 'Status' ? scan_info.value.port_info : scan_info.value.port_info.filter(item => item.state === selectedStatus.value)
    return filteredByStatus.filter(scan => scan.state === 'open' || scan.Service !== '')
  };

  const showResultterminal = (id) => {
    showResultterminalValue.value[0] = true;
    showResultterminalValue.value[1] = id;
    console.log(showResultterminalValue.value);
     
  };

</script>

<!-- Style -->

<style scoped>
  @import '@/assets/Home.css';
</style>

