<script setup>
    import { ref, watch } from 'vue';

    const props = defineProps(['name', 'label', 'placeholder', 'max', 'expectValue', 'value'])

    let fields = [];
    let activeFields = [];
    const numFields = ref(1);
    
    watch(props, async () => {
        if(props.expectValue && props.value || !props.expectValue) {
            // get fields and add event listeners

            // timeout to make sure fields are populated if value passed
            await new Promise(r => setTimeout(r, 100));

            const fieldPane = document.getElementById(`expanding-${ props.name }`);
            fields = document.querySelectorAll(`.input-${ props.name }`);

            fields.forEach((field, i, arr) => {
                if(i == 0) {
                    activeFields.push(field);
                }

                if(field.value && i+1 < props.max) {
                    activeFields.push(arr[i+1]);
                }
            });

            fieldPane.addEventListener('keyup', () => {
                for(let i = 0; i < activeFields.length; i++) {
                    let field = activeFields[i];
                    listenerAction(field);
                }
            });
                
            const listenerAction = (input) => {
                let value = input.value;
                const id = input.id.split('-');
                let inputNum = parseInt(id[1]);
                let nextInputNum = ( inputNum + 1 <= props.max ? inputNum + 1 : false );
                let nextInput = document.querySelector(`#${ id[0] }-${ nextInputNum }`);

                if(value && nextInputNum && nextInput.classList.contains('input-hidden')) {
                    // field has been populated, add another field if not at max
                    nextInput.classList.remove('input-hidden');
                    activeFields.push(nextInput);
                }

                // TODO: fix when populate all 3 fields, empty first and second
                
                if(!value && inputNum < activeFields.length && !nextInput?.value) {
                    // if current and next fields are empty, a field needs to be removed
                    if(activeFields.length > inputNum + 1) {
                        // if there is a field after the next one, its value needs shuffling down
                        shuffleInputValues(inputNum)
                    } else {
                        // if the next field is last, it can just be removed
                        activeFields.pop().classList.add('input-hidden')
                    }
                }
            };
        }
    }, {immediate: true});

    const shuffleInputValues = (startIndex) => {
        for(let i = --startIndex; i + 2 < activeFields.length; i++) {
            // move fields values up two places
            activeFields[i].value = activeFields[i+2].value;
            activeFields[i+2].value = '';
        }
        
        // remove last input from form and active fields array
        activeFields.pop().classList.add('input-hidden');
    }


</script>

<template>
    <div class='form-group' :id='`expanding-${ name }`'>
        <label :for='`${ name }-1`' class='label'>{{ label }}:</label>
        <input 
            v-for='i in max'
            :key='i' 
            type='text' 
            :name='`${ name }-${ i }`' 
            :class='"input " + `input-${ name }` + " " + ( i == 1 || (value && value[i-2]) ? "" : "input-hidden" )'
            :id='`${ name }-${ i }`' 
            :placeholder='placeholder ? placeholder : "" ' 
            :value='value && value[i-1] ? value[i-1] : ""'
        >
    </div>
</template>

<style scoped>
    .form-group {
        display: flex;
        flex-direction: column;
        width: calc(100% - 8px);
        margin: 0 4px 25px 4px;
    }

    .input {
        padding: 4px 2px;
        font-size: 16px;
    }

    .input:not(:first-of-type) {
        margin-top: 12px;
    }

    .input-hidden {
        display: none;
    }

    .label {
        font-weight: bold;
        font-size: 11px;
        margin: 0;
        position: relative;
        left: 1px;
        text-align: left;
    }
</style>