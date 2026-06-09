import { ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { sessionsApi, adminClient } from '@/api';
import { logger } from '@/api/client';

// Global state for admin authentication
const authenticated = ref(false);
const password = ref('');
const authError = ref('');
const loading = ref(false);

export function useAdminAuth() {
  const router = useRouter();
  const route = useRoute();

  // Check if already authenticated from storage
  const checkExistingAuth = async (): Promise<boolean> => {
    const storedPassword = sessionStorage.getItem('adminPassword');
    if (!storedPassword) {
      return false;
    }

    try {
      // Test the stored password by making an admin API call
      adminClient.defaults.headers['X-Admin-Password'] = storedPassword;
      await sessionsApi.getAllSessions(0, 1); // Test auth
      
      // Success - restore auth state
      authenticated.value = true;
      password.value = storedPassword;
      authError.value = '';
      
      if (import.meta.env.DEV) {
        logger.info('Admin authentication restored from storage');
      }
      
      return true;
    } catch {
      // Stored password is invalid, clear it
      sessionStorage.removeItem('adminPassword');
      adminClient.defaults.headers['X-Admin-Password'] = '';
      authenticated.value = false;
      password.value = '';
      
      if (import.meta.env.DEV) {
        logger.warn('Stored admin password is invalid, clearing auth');
      }
      
      return false;
    }
  };

  const authenticate = async (inputPassword: string): Promise<boolean> => {
    try {
      loading.value = true;
      authError.value = '';
      
      // Update admin client with password
      adminClient.defaults.headers['X-Admin-Password'] = inputPassword;
      
      // Test authentication by fetching sessions
      await sessionsApi.getAllSessions(0, 1);
      
      // Success
      authenticated.value = true;
      password.value = inputPassword;
      sessionStorage.setItem('adminPassword', inputPassword);
      
      if (import.meta.env.DEV) {
        logger.info('Admin authenticated successfully');
      }
      
      return true;
    } catch (err: any) {
      logger.error('Authentication failed', err);
      authError.value = 'Invalid password';
      password.value = '';
      authenticated.value = false;
      adminClient.defaults.headers['X-Admin-Password'] = '';
      return false;
    } finally {
      loading.value = false;
    }
  };

  const logout = () => {
    if (import.meta.env.DEV) {
      logger.info('Admin logging out');
    }
    
    // Clear all state
    authenticated.value = false;
    password.value = '';
    authError.value = '';
    sessionStorage.removeItem('adminPassword');
    adminClient.defaults.headers['X-Admin-Password'] = '';
    
    // Navigate to home, preserving mode if present
    const query = route.query.mode === 'stiff' ? { mode: 'stiff' } : {};
    router.push({ path: '/', query });
  };

  const requireAuth = async (): Promise<boolean> => {
    // First check if already authenticated
    if (authenticated.value) {
      return true;
    }
    
    // Try to restore from storage
    const restored = await checkExistingAuth();
    if (restored) {
      return true;
    }
    
    // Need authentication
    return false;
  };

  return {
    // State
    authenticated: computed(() => authenticated.value),
    authError: computed(() => authError.value),
    loading: computed(() => loading.value),
    
    // Methods
    checkExistingAuth,
    authenticate,
    logout,
    requireAuth,
    
    // For form binding
    passwordInput: password
  };
}