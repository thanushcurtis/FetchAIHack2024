import { createRouter, createWebHistory } from 'vue-router';

// Import components
import Home from '@/components/Home.vue';
import Auth from '@/components/Auth.vue';
import Register from '@/components/Register.vue'; 
import NewPage from '@/components/QueryPage.vue';


// Define routes
const routes = [
  {
    path: '/new-page/:fileName',
    name: 'NewPage',
    component: NewPage
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
  },
  {
    path: '/',
    name: 'Auth',
    component: Auth,
  },
  {
    path: '/register', // Define the path for the Register component
    name: 'Register',
    component: Register,
  },
];

// Create router instance
const router = createRouter({
  history: createWebHistory(), // Use browser history
  routes, // short for `routes: routes`
});

export default router;
