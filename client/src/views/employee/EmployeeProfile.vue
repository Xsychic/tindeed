<script setup>
    import Joi from 'joi';
    import api, { apiCatchError } from '@/assets/js/api';
    import Footer from '@/components/partials/Footer.vue';
    import EmployeeNavbar from '@/components/employee/EmployeeNavbar.vue';
    import FormStepper from '@/components/employee/profile/FormStepper.vue';
    import TutorialModal from '@/components/employee/tutorial/TutorialModal.vue';

    
    // form pages
    import PersonalDetailsForm from '@/components/employee/profile/PersonalDetailsForm.vue';
    import LocationForm from '@/components/employee/profile/LocationForm.vue';
    import SoftSkillsForm from '@/components/employee/profile/SoftSkillsForm.vue';
    import ExperienceForm from '@/components/employee/profile/ExperienceForm.vue';
    import QualificationsForm from '@/components/employee/profile/QualificationsForm.vue';
    import ReviewForm from '@/components/employee/profile/ReviewForm.vue';

    import { onMounted, ref } from 'vue';

    let pages;
    const formData = ref([]);
    const notifs = ref(2);
    const currentPageNum = ref(0);
	const isNewUser = ref(window.localStorage.getItem('newUserEmployeeProfile') === 'true');

    document.title = 'Profile | Vacansee'

    onMounted(() => {
        pages = document.querySelectorAll('.form-page-container');
    });

    const changePage = (incr) => {
        const maxPage = pages.length;
        const oldPage = currentPageNum.value;
        const newPage = currentPageNum.value + incr;

        if(newPage > maxPage || newPage < 0)
            return;

        if(newPage < maxPage) {
            pages[oldPage].classList.add('form-page-container-hidden');
            pages[newPage].classList.remove('form-page-container-hidden');
        }

        currentPageNum.value += incr;

        if(newPage == pages.length - 1) {
            // review page, get form data
            const form = document.querySelector('form');
            formData.value = new FormData(form);
            console.log('formData:');
            console.log(formData.value);
        }
    }

    const finishTutorial = () => {
        window.localStorage.removeItem('newUserEmployeeProfile');
        isNewUser.value = false;
    }


</script>

<template>
    <!-- <EmployeeNavbar page='home' :numNotifs='notifs'> </EmployeeNavbar> -->
    <EmployeeNavbar page='home' />

    
    <main class='container'>
        <div class='header'>
            <h1 class='title'>User Profile Setup</h1>
            <hr />
        </div>
    </main>

    <nav class='form-progress'>
        <FormStepper :stepNum='currentPageNum' />
    </nav>

    <form class='form-pane'>
        <div class='form-page-container'>
            <PersonalDetailsForm @next='changePage(1)' />
        </div>
        <div class='form-page-container form-page-container-hidden'>
            <LocationForm @next='changePage(1)' @back='changePage(-1)' />
        </div>
        <div class='form-page-container form-page-container-hidden'>
            <SoftSkillsForm @next='changePage(1)' @back='changePage(-1)' />
        </div>
        <div class='form-page-container form-page-container-hidden'>
            <ExperienceForm @next='changePage(1)' @back='changePage(-1)' />
        </div>
        <div class='form-page-container form-page-container-hidden'>
            <QualificationsForm @next='changePage(1)' @back='changePage(-1)' />
        </div>
        <div class='form-page-container form-page-container-hidden'>
            <ReviewForm :formData='formData' @next='changePage(1)' @back='changePage(-1)' />
        </div>
        
    </form>


    <TutorialModal v-if='isNewUser' @close-modal='finishTutorial' >
        <template #modal-header>
            <h3>Set Up Profile</h3>
        </template>
        <template #modal-body> 
            <div class='modal-body'>
                <p class='desc'>
                    Welcome to Vacansee!
                </p>
                <p class='desc'>
                    Before you get started looking for your next job, you first just need to set up your profile with this quick and easy form.           
                </p>
                <p class='desc'>
                    Your profile is what employers will see when you apply to a vacancy.
                </p>
            </div>

        </template>
    </TutorialModal>


    <Footer></Footer>

</template>

<style scoped>
    *:deep(.invalid-input) {
        border: 3px solid var(--red) !important;
    }
    
    hr {
        width: 100%;
        margin: 8px 0 12px 0;
        border: 0;
        border-top: 1px solid #555;
    } 

    .container {
        width: calc(100vw - 80px);
        padding: 0 40px;
    }

    .form-page-container-hidden {
        visibility: hidden;
        position: absolute;
        top: 0;
        left: 0;
    }

    .form-pane {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 280px;
        margin: 70px auto;
        min-height: 100px;
    }
 
    .header {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }

    .title {
        margin: 0;
        font-size: 32px;
        position: relative;
        left: 5px;
        font-weight: 400;
    }
    
</style>
