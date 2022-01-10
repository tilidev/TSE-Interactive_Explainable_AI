import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/tailwind.css'
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { fas } from "@fortawesome/free-solid-svg-icons";

library.add(fas);


const app = createApp(App).use(router).component("fa-icon", FontAwesomeIcon).mount('#app');
app.provide('apiUrl', 'localhost:8000/')
