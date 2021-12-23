<template>
  <div>
    <div class="flex flex-row-reverse pr-20">
    <outline-button @click="toggleCustomize = !toggleCustomize"
      >Customize</outline-button
    >
    <outline-button @click="toggleFilter = !toggleFilter"
      >Filter</outline-button
    >
    </div>
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
        v-if="toggleCustomize"
      >
        <div class="relative mx-auto w-auto max-w-2xl">
          <div class="bg-white w-100 rounded-lg">
            <div class="py-8">
              <h4 class="text-lg font-bold flex flex-row pl-10">
                Select up to 5 Attributes to display in the table
              </h4>
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
                <outline-button @click="toggleCustomize = false"
                  >Cancel</outline-button
                >
              </div>
              <div class="basis-1/2">
                <default-button>Apply Changes</default-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
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
        v-if="toggleFilter"
      >
        <div class="relative mx-auto w-auto max-w-2xl">
          <div class="bg-white w-100 rounded-lg">
            <div class="py-8">
              <h4 class="text-lg font-bold flex flex-row pl-10">
                Add Filters
              </h4>
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
                <outline-button @click="toggleFilter = false"
                  >Cancel</outline-button
                >
              </div>
              <div class="basis-1/2">
                <default-button>Apply Changes</default-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
    <div
      v-if="toggleCustomize||toggleFilter"
      class="absolute inset-0 z-40 opacity-25 bg-black"
    ></div>
  </div>
</template>

<script>
import OutlineButton from "../components/buttons/OutlineButton.vue";
import GrayButton from "../components/buttons/GrayButton.vue";
import DefaultButton from "../components/buttons/DefaultButton.vue";

export default {
  name: "customize",
  methods: {},
  data() {
    return {
      toggleCustomize: false,
      toggleFilter: false,
    };
  },

  components: { OutlineButton, GrayButton, DefaultButton },
};
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
