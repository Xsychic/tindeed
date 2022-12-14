<script setup>
    import AreYouSureModal from './AreYouSureModal.vue'
    import api, { apiCatchError } from '@/assets/js/api';
    
    import { onMounted, ref } from 'vue';

    const props = defineProps(['stats', 'vacancyName', 'vacancy', 'showingThis']);
    const emit = defineEmits(['showApplication', 'hideApplication', 'unmatch']);

    const details = {};
    const showModal = ref(false);
    const { application = {}, profile = {} } = props.stats;

    //download button
    /*
    const downloadApplication = () => {
        alert('download application');
    };*/

    const unmatch = async () => {
        const response = await api({
            url: `/v1/e/vacancies/${ application.VacancyId }/review/${ application.ApplicationId }/`,
            method: 'put',
            data: {
                setStatus: "reject"
            },
            responseType: 'json'
        }).catch(apiCatchError);


        if(!response) {
            return false;
        }

        const { data = {} } = response;

        emit('unmatch');

        return data;
    };

    const getDetails = async (options) => {
        const { applicantId = application.UserId } = options;

        const response = await api({
            method: 'get',
            url: `/v1/e/matches/card/${ applicantId }/`,
            responseType: 'json',
        }).catch((err) => {
            console.log(`oops ${ err }`);
        });

        if(!response || !response.data)
            return false;

        const { data } = response;

        if(!data)
            return false;

        const {
            details: newDetails = details.value
        } = data;

        details.value = newDetails;

        return true;
    };

    onMounted(async () => {
        const result = getDetails({ applicantId: application.UserId });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        };
    });

</script>

<template>
    <article class='application'>
        <div class='application-left'>
            <div class='title'>
                <span class='name'>
                    {{ profile.FirstName }} {{ profile.LastName }}
                </span> 
                <span class='pronouns' v-if='profile.Pronouns'>
                    ({{ profile.Pronouns }}) 
                </span>
            </div>
            <div class='contact'>
                <i class="fa-solid fa-phone"></i>
                {{ profile.PhoneNumber }}  
            </div>
            <div class='contact'>
                <i class="fa-solid fa-envelope-open"></i>
                {{ profile.Email }}  
            </div>
            <div class='contact'>
                <i class="fa-solid fa-clock"></i>
                GMT {{ profile.TimeZone }}
            </div>
        </div>

        <div class='application-right'>
            <button class='application-button application-button-blue' @click='emit("hideApplication", details);' id='hide' v-if='showingThis'>Hide Application</button>
            <button class='application-button application-button-grey' @click='emit("showApplication", details)' id='show' v-else>Show Application</button>
            <!-- download button -->
            <!-- <button class='application-button application-button-grey' @click='downloadApplication'>Download Application</button> -->
            <button class='application-button application-button-red' @click='showModal = true'>Unmatch</button>
            <AreYouSureModal v-if='showModal' :name='profile.FirstName + " " + profile.LastName' :vacancyName='vacancyName' :employer='true' @close-modal='showModal = false' @unmatch='unmatch' />
        </div>
    </article>
    <hr class='slim-hr' />
</template>


<style scoped>
    .application {
        display: flex;
        justify-content: space-between;
        padding: 8px 12px;
        height: 100px;
    }

    .application-button {
        font-weight: 500; /* required for some reason */
        border-radius: 7px;
        color: #fff;
        border: 2.2px solid #333;
        min-width: 150px;
        font-size: 12px;
        text-decoration: none;
        padding: 3px 4px;
        font-family: Poppins, Avenir, Helvetica, Arial, sans-serif;
        margin: 2px;
    }

    .application-button-blue {
        background: var(--blue);
    }

    .application-button-blue:hover, .application-button-blue:focus, .application-button-blue:active {
        background: var(--blue-focus);
        cursor: pointer;
    } 

    .application-button-grey {
        background: var(--slate-focus);
    }

    .application-button-grey:hover, .application-button-grey:focus, .application-button-grey:active {
        background: #4e626c;
        cursor: pointer;
    } 

    .application-button-red {
        background: var(--red);
    }

    .application-button-red:hover, .application-button-red:focus, .application-button-red:active {
        background: var(--red-focus);
        cursor: pointer;
    } 

    .application-left {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: flex-start;
    }

    .application-right {
        display: flex;
        flex-direction: column;
        height: calc(100% - 4px);
        justify-content: center;
        padding: 2px 0; 
        gap: 3px;
    }

    .contact {
        font-size: 14px;
    }

    .contact i {
        margin-right: 5px;
    }

    .name {
        font-size: 18px;
    }

    .pronouns {
        color: var(--slate-focus);
        font-size: 14px;
    }

    .slim-hr {
        margin: 1px 0;
    }

    .title {
        display: flex;
        gap: 4px;
        align-items: center;
    }
</style>