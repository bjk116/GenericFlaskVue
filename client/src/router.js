import Vue from 'vue';
import Router from 'vue-router';
//import Ping from './components/Ping.vue';
import Home from './components/Homepage.vue';
import Settings from './components/Settings/Settings.vue';
import Login from './components/Login.vue';
import NotFound from './components/NotFound.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
  	{
  		path: '/',
  		name: 'Home',
  		component: Home,
    },
    {
      path: '*',
      name: 'NotFound',
      component: NotFound
    },
    {
      path: '/settings',
      name: 'Settings',
      component: Settings
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    }
  ],
});
