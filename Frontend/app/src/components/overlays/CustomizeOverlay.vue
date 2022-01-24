
<template>
  
  <transition name="fade">
      <div
        class="
          fixed
          overflow-y-auto
          inset-0
          flex
          justify-center
          items-center
          z-50
        "
      >
        <div class="relative mx-auto w-auto max-w-2xl">
          <div class="bg-white w-100 rounded-lg">
            <div class="grid grid-cols-3 gap-2 py-5">
              <div class="col-span-2">
                <h4 class="text-lg font-bold flex flex-row pl-10">
                Select 5 Attributes to display in the table
              </h4>
              </div>
              <div class="pl-20">
                <button @click="close" class="
                bg-white 
                hover:bg-gray-light 
                px-2
                py-0.5
                rounded-full">
                  <fa-icon icon="times"></fa-icon>
                </button>
              </div>
              
            </div>
            <div class="grid grid-cols-8 gap-y-2 gap-x-2 pr-10">
              <div class="col-span-4 pt-4 pr-40">Loan</div>
              <div><gray-button @click="addToCustomizations('amount')">Amount</gray-button></div>
              <div><gray-button @click="addToCustomizations('duration')">Duration</gray-button></div>
              <div><gray-button @click="addToCustomizations('purpose')">Purpose</gray-button></div>
              <div><gray-button @click="addToCustomizations('people liable')">People Liable</gray-button></div>
              <div class="col-span-6"></div>
              <div ><gray-button @click="addToCustomizations('employment')">Employment</gray-button></div>
              <div><gray-button @click="addToCustomizations('other debtors')">Other debtors</gray-button></div>

              <div class="col-span-4 pt-4 pr-40 pl-5">Personal</div>
              <div><gray-button @click="addToCustomizations('age')">Age</gray-button></div>
              <div><gray-button @click="addToCustomizations('residence')">Residence</gray-button></div>
              <div><gray-button @click="addToCustomizations('job')">Job</gray-button></div>
              <div><gray-button @click="addToCustomizations('telephone')">Telephone</gray-button></div>
              <div class="col-span-7"></div>
              <div><gray-button @click="addToCustomizations('housing')">Housing</gray-button></div>

              <div class="col-span-4 pt-4 pr-40 pl-5">Financial</div>
              <div><gray-button @click="addToCustomizations('savings')">Savings</gray-button></div>
              <div><gray-button @click="addToCustomizations('assets')">Assets</gray-button></div>
              <div><gray-button @click="addToCustomizations('balance')">Balance</gray-button></div>
              <div><gray-button @click="addToCustomizations('available income')">Available Income</gray-button></div>
              <div class="col-span-5"></div>
              <div><gray-button @click="addToCustomizations('history')">History</gray-button></div>
              <div><gray-button @click="addToCustomizations('other loans')">Other loans</gray-button></div>
              <div><gray-button @click="addToCustomizations('previous loans')">Previous loans</gray-button></div>
            </div>
            <div class="flex flex-row-reverse">
              <div class="basis-1/2">
                <outline-button @click="cancelAttributes()">Cancel</outline-button>
              </div>
              <div class="basis-1/2">
                <default-button>Apply Changes</default-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
        
</template>

<script>
import DefaultButton from '../buttons/DefaultButton.vue';
import GrayButton from '../buttons/GrayButton.vue';
import OutlineButton from '../buttons/OutlineButton.vue';

export default {
    components: { OutlineButton, DefaultButton, GrayButton },
    name: 'Customize',

  
  data(){
    return{
      customizationMemory: [], 
      customization: ['balance', 'duration', 'amount', 'employment', 'age'] // default attributes
    };
  },

  methods: {
    close() {
        this.$emit('close');
      },
    
    addToCustomizations(attribute) {
    if(!(this.customizationMemory.includes(attribute))){
    this.customizationMemory.push(attribute);
    }else{
      this.removeAttribute(attribute);
    }
    },
    removeAttribute(attribute) {
      this.customizationMemory.splice(this.customizationMemory.indexOf(attribute),1)
    },
    cancelAttributes() {
      this.customizationMemory = [];
    }
  },
}
</script>

<style scoped>
.fade-enter-from {
  opacity: 0;
}
.fade-enter-to {
  opacity: 1;
}
.fade-enter-active {
  transition: all 1s ease;
}
.fade-leave-from {
  opacity: 1;
}
.fade-leave-to {
  opacity: 0;
}
.fade-leave-active {
  transition: all 1s ease;
}
</style>


