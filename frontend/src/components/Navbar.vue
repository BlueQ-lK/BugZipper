<script setup>
  import { Icon } from '@iconify/vue';
</script>

<template>
    <div class="top-bar">
         <div class="logo">
          <Icon icon="material-symbols:bug-report" width="25" height="25"  style="color: white" />
            <span>BugZipper</span>
         </div>
         <ul class="nav-menu">
            <li>
                <router-link to="/" class="aa">
                  <Icon icon="material-symbols:dashboard" width="20" height="20"  style="color: white; margin-right: 2px;" />
                    <span>Dashboard</span>
                </router-link>
            </li>
            <li>
                
                <router-link class="aa" to="/history">
                  <Icon icon="ri:folder-history-fill" width="20" height="20"  style="color: white; margin-right: 2px;" />
                    <span>History</span>
                </router-link>
            </li>
            <li>
                
                <router-link class="aa" to="/details/0">
                  <Icon icon="clarity:details-solid" width="20" height="20"  style="color: white; margin-right: 2px;" />
                    <span>Details</span>
                </router-link>
            </li>
            <li>
                
                <router-link class="aa" to="/comingsoon">
                  <Icon icon="ic:sharp-people" width="20" height="20"  style="color: white; margin-right: 2px;" />
                    <span>Community</span>
                </router-link>
            </li>
            <li>
                <router-link class="aa" to="/comingsoon">
                  <Icon icon="ant-design:setting-filled" width="20" height="20"  style="color: white; margin-right: 2px;" />
                    <span>Settings</span>
                </router-link>
            </li>
            <li>
                <router-link class="aa" to="/comingsoon">
                  <Icon icon="iconamoon:profile-fill" width="20" height="20"  style="color: white; margin-right: 2px;" />
                    <span>Profile</span>
                </router-link>
            </li>
        </ul>
        <div class="pfp-box">
            <div class="search-bar">
              <Icon icon="majesticons:search-line" width="25" height="25"  style="color: white" class="seach-icon"/>
              <input type="text" placeholder="Search " class="search-input">
            </div>
            <div class="profile">
              <Icon icon="iconamoon:notification" width="25" height="25"  style="color: white; margin-right: 10px;" />
                <img src="@/assets/pfp.jpg" id="pfp-img">
            </div>
        </div>
      </div>
</template>

<style scoped>
    /* Nav Bar */
  .top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 3rem;
    color: var(--color-text-white);
  }

  .logo {
    background-color: var(--color-card-dark);
    padding: 12px  2rem;
    display: flex;
    justify-content: center;
    border-radius: 30px;
    box-shadow: 0 0 15px  var(--color-box-shadow);
  }


  .logo span {
    font-weight: 700;
    margin-left: 5px;
    font-size: 17px;
  }

  .nav-menu {
    display: flex;
    list-style: none;
    background: var(--color-card-dark);
    padding:6px 0px 6px 30px;
    border-radius: 30px;
    box-shadow: 0 0 15px  var(--color-box-shadow);
  }

  .nav-menu .aa {
    margin-right: 10px;
    text-decoration: none;
    color: var(--color-dark);
  }

  .aa {
    padding: 6px 10px;
    border-radius: 20px;
    transition: all .4s ease;
    display: flex;
    align-items: center;
  }



  .aa:hover {
    transform: scale(1.1);
    border-bottom: 1px solid var(--color-search);
  }


  ul li {
    margin-right: 15px;
  }

  .pfp-box {
    width: 350px;
    padding: 7px 0px;
    background-color: var(--color-card-dark);
    display: flex;
    align-items: center;
    border-radius: 30px;
    box-shadow: 0 0 15px  var(--color-box-shadow);
  }

  .search-bar {
    display: flex;
    align-items: center;
    width: 250px;
    height: 30px;
    margin-right: 10px;
    margin-left: 10px;
    border: 0px;
    border-radius: 30px;
    background-color: var(--color-search);
  }

  .search-input {
    background-color: transparent;
    width: 100%;
    height: 100%;
    border: none;
    outline: none;
    font-size: 16px;
    border-radius: 30px;
    color: white;
  }

  .seach-icon {
    margin-left: 5px;
    margin-right: 5px;

  }

  .profile {
    display: flex;
    align-items: center;
  }

  .profile img{
    margin-right: 10px;
    width: 35px;
    border: 3px solid white;
    background-color: var(--color-search);
    font-size: 20px;
    margin-right: 15px;
    color: white;
    border-radius: 50%;
  }

</style>

