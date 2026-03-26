import { createApp } from 'vue';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import 'element-plus/theme-chalk/dark/css-vars.css';
import zhCn from 'element-plus/es/locale/lang/zh-cn';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import './assets/styles/global.css';

const app = createApp(App);
const pinia = createPinia();

app.use(ElementPlus, { locale: zhCn });
app.use(router);
app.use(pinia);

app.mount('#app');
