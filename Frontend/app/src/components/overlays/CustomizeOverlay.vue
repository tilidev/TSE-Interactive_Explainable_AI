<template>
  <div
        class="fixed overflow-y-auto inset-0 flex justify-center items-center z-50 "
        v-if="toggleCustomize">
        <div class="relative mx-auto w-auto max-w-2xl">
          <div class="bg-white w-100 rounded-lg">
         <div class="py-8">
           <h4 class="text-lg font-bold">Select up to 5 Attributes to display in the table</h4>
         </div>
         <div class="grid grid-cols-8 gap-1 pr-10">
           <div class="col-span-4 pt-4 pr-40">Loan</div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div class="col-span-6"></div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div><gray-button>Apply Changes</gray-button></div>

           <div class="col-span-4 pt-4 pr-40 pl-5">Personal</div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div><gray-button>Apply Changes</gray-button></div>
           <div class="col-span-7"></div>
           <div><gray-button>Apply Changes</gray-button></div>

           <div class="col-span-4 pt-4 pr-40 pl-5">Financial</div>
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
         
      </div>
</template>

<script>

import GrayButton from "../buttons/GrayButton.vue"
import OutlineButton from "../buttons/OutlineButton.vue"
import DefaultButton from "../buttons/DefaultButton.vue"

export default {
    name: 'customize',
  data() {
    return {
      toggleCustomize: false
    };
  },
  methods: {},

  components: {OutlineButton, DefaultButton, GrayButton},

}
</script>