<script setup>
    const props = defineProps(['FirstName', 'LastName', 'Pronouns', 'PhoneNumber', 'Email', 'TimeZone']);
</script>

<template>
    <div class="contact-card">
        <div class='personal-info'>
            <div class='name'> <span class='name'> {{ FirstName }} {{ LastName }} </span> <span class= 'pronouns'> ({{Pronouns}}) </span></div>
        </div>
        <div class='contact'>
            <i class="fa-solid fa-phone"></i>
            {{ PhoneNumber }}  
        </div>
        <div class='contact'>
            <i class="fa-solid fa-envelope-open"></i>
            {{ Email }}  
        </div>
        <div class='contact'>
            <i class="fa-solid fa-clock"></i>
            GMT {{ TimeZone }}
        </div>
    </div>
</template>

<style scoped>
    .name {
        font-size: 20px;
        margin: 0 0 15px 0;
    }

    .contact {
        font-size: 16px;
        margin-bottom: 2.5px;
    }

    .contact i {
        margin-right: 5px;
    }
    
    .contact-card {
        border: 2px solid var(--jet);
        min-height: 110px;
        min-width: 260px;
        border-radius: 5px;
        width: calc(40% - 40px);
        position: relative;
        bottom: 50px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
        padding: 15px 20px;
    }

    .name {
        font-size: 25px;
        text-align: left;
    }

    .pronouns {
        font-size: 12px;
        text-align: left;
        margin: 0;
        padding: 0;
    }
</style>
