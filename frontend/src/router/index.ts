import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import { logger } from '@/api/client';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),
    meta: { title: 'Skill Tree Survey' }
  },
  {
    path: '/survey/:sessionId',
    name: 'Survey',
    component: () => import('@/views/SurveyView.vue'),
    props: true,
    meta: { title: 'Take Survey' }
  },
  {
    path: '/complete/:sessionId',
    name: 'Complete',
    component: () => import('@/views/CompleteView.vue'),
    props: true,
    meta: { title: 'Survey Complete' }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('@/views/AdminView.vue'),
    meta: { title: 'Admin Panel', requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFoundView.vue'),
    meta: { title: '404 Not Found' }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

// Navigation guard for logging and title updates
router.beforeEach((to, from, next) => {
  logger.info(`Navigating from ${from.path} to ${to.path}`);
  
  // Update document title
  document.title = to.meta.title ? `${to.meta.title} | Skill Tree` : 'Skill Tree Survey';
  
  // Check for admin auth
  if (to.meta.requiresAuth) {
    const adminPassword = sessionStorage.getItem('adminPassword');
    if (!adminPassword) {
      logger.warn('Admin access attempted without authentication');
      // In a real app, redirect to login
      // For now, we'll handle auth in the component
    }
  }
  
  next();
});

router.afterEach((to, from) => {
  logger.debug(`Navigation complete: ${from.path} -> ${to.path}`);
});

export default router;