<template>
	<div style="padding: 0px 15px;">
        <div class="filter-box">
            <div style="position: relative;">
                <div class="fil-input" >
                <Icon icon="majesticons:search-line" width="25" height="25"  style="color: white" class="seach-icon"/>
                <input type="text" placeholder="Search" v-model="filterText"  @mousedown="showOption = true" @mouseleave="showOption = false">
            </div>
            <div v-if="showOption" class="options-list">
                <option><span style="margin-right: 10px; color: white;">ip:127.0.0.1</span> --Sort by IP (use ip:)</option>
            </div>
            </div>
            <div class="search-btn">
                <button type="button" @click="filterSearch()">Search</button>
            </div>
            <div class="sort-option">
                <button type="button" @click="sort()">Sort</button>
                <Icon icon="bx:sort" width="23" height="23"  style="color: white" class="sort-icon" @click="sort()"/>
            </div>
            <div class="sort-option" style="margin-left: 15px;">
                <button type="button" @click="sortName()">Name</button>
                <Icon v-if="nameVar === true" icon="bi:sort-alpha-up" width="23" height="23"  style="color: white" class="sort-icon" @click="sortName()"/>
                <Icon v-else icon="bi:sort-alpha-down" width="23" height="23"  style="color: white" class="sort-icon" @click="sortName()"/>
            </div>
            <div class="sort-option" style="margin-left: 15px;">
                <button type="button" @click="reset()">reset</button>
                <Icon icon="carbon:reset" width="25" height="25"  style="color: white; padding-right: 5px;" class="sort-icond" @click="reset()"/>
            </div>
            <div class="to-result">
                <p>Result: </p><span>{{ filterDD().length }}</span>
                <p>Total Rows:</p><span>{{ onLoadresult.length }}</span>
            </div>
        </div>
            <div class="outer-table-box">
            <table style="box-shadow: 0 0 7px var(--color-box-shadow) inset; ">
                <thead>
                    <tr>
                        <td><input type="checkbox"></td>
                        <td>Index</td>
                        <td>Name</td>
                        <td>Address</td>
                        <td>Date</td>
                        <td>Version</td>
                        <td>Action</td>
                    </tr>
                </thead>
                <tbody>
                <tr v-for="(scan, index) in filterDD()" :key="scan.id" :id="scan.id">
                    <td>
                        <div class="checkbox-wrapper-39">
                        <label>
                            <input type="checkbox" 
                            :value="scan.id"
                            @input="event => event.target.checked ? delid.push(scan.id) : delid.pop()" 
                            />
                            <span class="checkbox"></span>
                        </label>
                        </div>
                    </td>
                    <td v-if="sortVar === true">{{ onLoadresult.length - index }}</td>
                    <td v-else-if="sortVar === false">{{ index + 1}}</td>
                    <td>{{ scan.scanner }}</td>
                    <td>{{ scan.addr }}</td>
                    <td>{{ scan.startstr }}</td>
                    <td>{{ scan.version }}</td>
                    <td>
                       <div style="display: flex; justify-content: center; align-items: center;">
                        <div class="del-icon">
                            <Icon icon="material-symbols:delete" width="20" height="20" @click="del_function(scan.id)"/>
                        </div>
                        <router-link :to="`/details/${scan.id}`" class="view">
                            view
                        </router-link>
                       </div>
                    </td>
                </tr>
                </tbody>
            </table>
        </div >
        </div>

</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import axios from 'axios';
    import { Icon } from '@iconify/vue';

    const onLoadresult = ref([]);
    let delid = ref([]);
    const sortVar = ref(false);
    const nameVar = ref(false);
    const filterText = ref('');
    let showOption = ref(false);

    onMounted(async () => {
        try {
            const response = await axios.get('http://127.0.0.1:4000/history');
            onLoadresult.value = response.data.dbmainresult;
        } catch (err) {
            console.log(err);
        }
    })  

        const del_function = async (id) => {
            if(id !== '' && id !== null) {
                delid.value.push(id)
            }
        try {
            const uniqueid = [...new Set(delid.value)];
            const response = await axios.delete('http://127.0.0.1:4000/history', {
                data: {
                    "delid": uniqueid
                }
            })
            if(response.data.status === 'Success') {
                for(const item of uniqueid) {
                    document.getElementById(item).remove();
                }
                onLoadresult.value = response.data.dbmainresult;
                delid.value.length = 0;
                uniqueid.length = 0
            } 
            else if (response.data.status === 'Failed') {
                delid.value.length = 0;
                uniqueid.length = 0
                alert("Row could not be delted");
            } 
            else {
                alert("error");
            }
            
        } catch (err) {
            console.log(err)
        }
    }    

    const sort = () => {
        sortVar.value =  !sortVar.value;
        if(sortVar.value) {
            // desc
            onLoadresult.value.reverse();
        } else {
            // asc
            onLoadresult.value.reverse();
        }
    }

    const sortName = () => {
        nameVar.value = !nameVar.value;
        if(nameVar.value) {
            // asc
            onLoadresult.value.sort((a, b) => a.scanner.localeCompare(b.scanner));
        } else {
            // desc
            onLoadresult.value.sort((a, b) => b.scanner.localeCompare(a.scanner));
        }
    }

    const reset = () => {
        onLoadresult.value.sort((a, b) => a.id - b.id);
        sortVar.value = false;
        nameVar.value = false;
    }

    const filterDD = () => {
        if (!filterText.value.includes("ip:")) {
            let filter = new RegExp(filterText.value, 'i');
            return  onLoadresult.value.filter(item => item.scanner.match(filter));
        }
        else if (filterText.value.includes("ip:")) {
            let sliceValue = filterText.value.slice(3, filterText.value.length).trim();
            return onLoadresult.value.filter(item => item.addr.match(sliceValue));
        }
        
    }
</script>


<style scoped>
.filter-box {
    background-color: var(--color-card-dark);
    width: 100%;
    height: 6rem;
    margin-top: 1rem;
    border-radius: 10px;
    display: flex;
    align-items: center;
    padding: 0 2rem;
    box-shadow: 0 0 15px  rgb(0, 0, 0);
    border: 1px solid var(--color-border);
}

.fil-input {
    width: 400px;
    height: 40px;
    display: flex;
    align-items: center;
    border-radius: 5px;
    border: 2px solid var(--color-border-bold);
}

.fil-input input {
    width: 100%;
    height: 100%;
    outline: none;
    border: none;
    background: transparent;
    color: white;
    font-size: 17px;
    padding-right: 10px;
}

.fil-input:focus-within{
    border: 2px solid var(--color-search);
}

.fil-input .seach-icon {
   margin-left: 10px;
   margin-right: 10px;
}

.options-list {
  border-bottom: 1px solid var(--color-search);
  border-left: 1px solid var(--color-search);
  border-right: 1px solid var(--color-search);
  background-color: var(--primary-color);
  position: absolute;
  max-height: 150px;
  overflow-y: auto;
  z-index: 10;
  padding: 6px 10px;
}

.options-list option {
    font-size: 14px;
    color: rgb(206, 206, 206);
}

.search-btn {
    width: 100px;
    height: 40px;
    margin-left: 1rem;
}

.search-btn button {
    width: 100%;
    height: 100%;
    font-size: 17px;
    font-weight: 600;
    border-radius: 5px;
    background: #0861bd;
    border: none;
    color: white;
}

.search-btn button:hover {
    background: #023f7d;
}

.sort-option {
    background: transparent;
    margin-left: 2rem;
    width: 80px;
    height: 40px;
    border-radius: 5px;
    border: 2px solid var(--color-search);
    display: flex;
    align-items: center;
}

.sort-option button {
    border: none;
    width: 70%;
    font-size: 17px;
    height: 100%;
    background: transparent;
    color: white;

}

.sort-option:hover{
    background: rgb(71, 71, 71);
}

.to-result {
    margin-left: 20rem;
    display: flex;
    height: 3rem;
    align-items: center;
    padding: 10px;
    border: 1px solid var(--color-border);
    border-radius: 5px;
}

.to-result p {
    font-weight: 600;
    margin-right: 10px;
}

.to-result span {
    color: greenyellow;
    font-size: 25px;
}

.to-result span:nth-child(2) {
    margin-right: 1rem;
}

/* table */

.outer-table-box {
    background-color: var(--color-card-dark);
    height: 34rem;
    margin-top: 1rem;
    padding: 1rem 1.5rem;
    color: #b1b1b1;
    border-radius: 10px;
    overflow-x: scroll;
    box-shadow: 0 0 15px  var(--color-box-shadow);
    border: 1px solid var(--color-border);
}


.outer-table-box table {
    width: 100%;
    height: auto;
    border-collapse: collapse;
}

.outer-table-box thead tr {
    background: #171717;
    text-align: center;
    letter-spacing: 1px;
    font-weight: 600;
}


.outer-table-box  td{
    border: 1px solid rgba(50, 50, 50, 0.732);
    text-align: center;
    padding: 4px;
}

.outer-table-box tbody tr:nth-child(even) {
    background: rgba(34, 34, 34, 0.214);
}

.outer-table-box tbody tr:hover {
    background: rgb(61, 61, 61);
}

.checkbox-wrapper-39 *,
  .checkbox-wrapper-39 *::before,
  .checkbox-wrapper-39 *::after {
    box-sizing: border-box;
    position: relative;
    left: 12px;
  }

  .checkbox-wrapper-39 label {
    display: block;
    width: 30px;
    height: 22px;
    cursor: pointer;
  }

  .checkbox-wrapper-39 input {
    visibility: hidden;
    display: none;
  }

  .checkbox-wrapper-39 input:checked ~ .checkbox {
   transform: rotate(45deg);
   width: 14px;
   margin-left: 12px;
   border-color: #24c78e;
   border-top-color: transparent;
   border-left-color: transparent;
   border-radius: 0;
  }

  .checkbox-wrapper-39 .checkbox {
    display: block;
    width: inherit;
    height: inherit;
    border: 3px solid #434343;
    border-radius: 6px;
    transition: all 0.1s;
  }

  .checkbox-wrapper-39 input:not(:checked) + span:hover {
    background: rgba(99, 99, 99, 0.345);
  }


.view {
    background-color: #0095ff8b;
    padding: 6px 5px;
    height: 32px;
    text-decoration: none;
    color: white;
    border-radius: 2px;
    margin-left: 10px;
    text-transform: uppercase;
    font-size: 15px;
    font-weight: 600;
    letter-spacing: 1px;
}

.view:hover {
    background: #0A46E4;
}

.del-icon {
    color: white;
    background: rgb(125, 3, 3);
    padding: 4px 3px;
    height: 29px;
    border-radius: 3px;
    cursor: pointer;
}

.del-icon:hover {
    background-color: red;
}


</style>

