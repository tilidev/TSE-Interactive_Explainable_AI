<template>
  <div class="bg-black">  
    <outline-button @click="toggleCustomize = !toggleCustomize"
    >Customize</outline-button>
     <transition name="fade">
      <div
        v-if="toggleCustomize"
        class="fixed overflow-y-auto inset-0 flex justify-center items-center z-50">
        <div class="relative mx-auto w-auto max-w-3xl">
         <div class="py-8">
           <h4 class="text-lg font-bold">Select up to 5 Attributes to display in the table</h4>
         </div>
         <div class="grid grid-cols-8 gap-1">
           <div class="col-span-4 pl-2">Loan</div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div class="col-span-6"></div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div><gray-button>Apply Changes</gray-button></div>

           <div class="col-span-4 pl-6">Personal</div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div class="col-span-7"></div>
           <div><gray-button>Apply Changes</gray-button></div>

           <div class="col-span-4 pl-6">Financial</div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div class="col-span-5"></div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div><gray-button>Apply Changes</gray-button></div>
         </div>
         <div class="flex flex-row-reverse">
            <div class="basis-1/2"> 
               <outline-button @click="toggleCustomize = false">Cancel</outline-button> 
            </div> 
            <div class="basis-1/2"> 
               <default-button>Apply Changes</default-button>
            </div> 
         </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import OutlineButton from "../components/buttons/OutlineButton.vue"
import DefaultButton from '../components/buttons/DefaultButton.vue';
import GrayButton from "../components/buttons/GrayButton.vue";

export default {
  name: 'customize',
  data() {
    return {
      toggleCustomize: false
    };
  },
  methods: {},

  components: {OutlineButton, DefaultButton, GrayButton},
};
</script>

<style scoped>
   .fade-enter-from{
     opacity: 0;
   }
   .fade-enter-to{
     opacity: 1;
   }
   .fade-enter-active{
     transition: all 1s ease;
   }
   .fade-leave-from{
     opacity: 1;
   }
   .fade-leave-to{
     opacity: 0;
   }
   .fade-leave-active{
     transition: all 1s ease;
   }
</style>
