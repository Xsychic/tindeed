<script setup>
    document.title = 'Vacansee';
    document.documentElement.setAttribute('lang', 'en');
</script>

<template>
    <router-view></router-view>
</template>


<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,400;0,500;0,700;1,400;1,700&display=swap');
    @import url('@/assets/fontawesome/css/all.min.css');

    :root {
        --fonts: Poppins, Avenir, Helvetica, Arial, sans-serif;

        /* standard colours */
        
        --red: #cc2936;
        --red-focus: #bb2531; /* 8% darker */

        --background-blue: #f0f8fa;
        --blue: #08415c;
        --blue-focus: #0a567a; /* 8% lighter */

        --green: #009e0f;
        --green-focus: #00910d; /* 8% darker */

        /* grey */
        --accent-grey: #bbbbbb;
        --slate: #6b818c;
        --slate-focus: #627680; /* 8% darker */
        --jet: #333;
    }

    body {
        margin: 0;
        overflow-x: hidden;
    }

    #app {
        font-family: var(--fonts);
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        font-weight: 500;
        position: relative;
        /* min-height: 100vh; */
    }
</style>
