<script setup>
    import Joi from 'joi';
    import validateForm from '@/assets/js/formValidator';
    import FormButtons from '@/components/employee/profile/formComponents/FormButtons.vue';
    import FormText from '@/components/employer/newVacancy/formComponents/FormText.vue';
    import FormHeader from '@/components/employer/newVacancy/formComponents/FormHeader.vue';

    const props = defineProps(['companyName']);
    const emit = defineEmits(['next']);

    const validate = () => {
        // define schema
        const schema = Joi.object({
            'FirstName': Joi.string().alphanum().max(50).required().label('first name'),
            'LastName': Joi.string().alphanum().max(50).required().label('last name'),
            'Pronouns': Joi.string().max(50).required().label('pronouns'),
            'PhoneNumber': Joi.string().min(11).required().label('phone number'),
        });

        // get input data
        const data = {
            'FirstName': document.querySelector('input[name="FirstName"]').value,
            'LastName': document.querySelector('input[name="LastName"]').value,
            'Pronouns': document.querySelector('input[name="Pronouns"]').value,
            'PhoneNumber': document.querySelector('input[name="PhoneNumber"]').value,
        }

        // validate and handle any errors
        if(validateForm(schema, data))
            emit('next');
    }


</script>

<template>
    <FormHeader title='Personal Details'>
        Let's start off with the simple stuff. Enter your name, pronouns and phone number.
    </FormHeader>

    <FormText type='text' label='first name' name='FirstName' />
    <FormText type='text' label='last name' name='LastName' />
    <FormText type='text' label='pronouns' name='Pronouns' />
    <FormText type='text' label='phone number' name='PhoneNumber' />

    <FormButtons :next='true' @next='validate()' />
</template>

<style>

</style>