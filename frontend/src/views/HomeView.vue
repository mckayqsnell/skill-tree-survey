<template>
  <div class="min-h-screen bg-black star-field flex items-center justify-center px-4" :class="{ 'stiff-mode': isStiffMode }">
    <div class="max-w-xl w-full">
      <!-- Main Card -->
      <div class="glass-card">
        <!-- Header -->
        <div class="text-center mb-8">
          <h1 class="text-3xl font-bold text-primary mb-2 font-heading">
            SKILL TREE ASSESSMENT
          </h1>
          <p class="text-sm text-primary-dim font-mono-primary">Technical Competency Mapping System</p>
        </div>

        <div class="mb-6 p-3 border-l-2 border-primary-dim bg-overlay">
          <p class="status-ready">SYSTEM STATUS: READY</p>
          <p class="status-info">
            Assessment duration: 5-10 minutes
          </p>
        </div>

        <!-- Form Section -->
        <form @submit.prevent="startSurvey" class="space-y-4">
          <!-- First Name -->
          <div>
            <label for="firstName" class="block text-xs text-primary-subtle mb-1 font-mono-primary uppercase">
              First Name <span class="text-accent">*</span>
            </label>
            <input
              id="firstName"
              v-model="formData.firstName"
              type="text"
              required
              class="input-field"
              placeholder="John"
              :class="{ 'border-danger': errors.firstName }"
            />
            <p v-if="errors.firstName" class="text-danger text-xs mt-1">{{ errors.firstName }}</p>
          </div>

          <!-- Last Name -->
          <div>
            <label for="lastName" class="block text-xs text-primary-subtle mb-1 font-mono-primary uppercase">
              Last Name <span class="text-accent">*</span>
            </label>
            <input
              id="lastName"
              v-model="formData.lastName"
              type="text"
              required
              class="input-field"
              placeholder="Doe"
              :class="{ 'border-danger': errors.lastName }"
            />
            <p v-if="errors.lastName" class="text-danger text-xs mt-1">{{ errors.lastName }}</p>
          </div>

          <!-- Email -->
          <div>
            <label for="email" class="block text-xs text-primary-subtle mb-1 font-mono-primary uppercase">
              Email <span class="text-accent">*</span>
            </label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              required
              class="input-field"
              placeholder="john@example.com"
              :class="{ 'border-danger': errors.email }"
            />
            <p v-if="errors.email" class="text-danger text-xs mt-1">{{ errors.email }}</p>
          </div>

          <!-- Company -->
          <div>
            <label for="company" class="block text-xs text-primary-subtle mb-1 font-mono-primary uppercase">
              Company <span class="text-accent">*</span>
            </label>
            <input
              id="company"
              v-model="formData.company"
              type="text"
              required
              class="input-field"
              placeholder="Acme Corp"
              :class="{ 'border-danger': errors.company }"
            />
            <p v-if="errors.company" class="text-danger text-xs mt-1">{{ errors.company }}</p>
          </div>

          <!-- Submit Button -->
          <div class="pt-4">
            <button 
              type="submit" 
              class="btn-primary w-full"
              :disabled="loading"
            >
              <span v-if="!loading">START ASSESSMENT</span>
              <span v-else>INITIALIZING...</span>
            </button>
          </div>

          <!-- Error Display -->
          <div v-if="errorMessage" class="mt-4 p-3 border border-danger-dim bg-danger-overlay">
            <p class="text-danger text-sm font-mono-primary">{{ errorMessage }}</p>
          </div>
        </form>

        <!-- Footer Links -->
        <div class="mt-6 pt-6 border-t border-primary-faint text-center">
          <router-link 
            :to="{ path: '/admin', query: isStiffMode ? { mode: 'stiff' } : {} }" 
            class="admin-link"
          >
            Admin Access
          </router-link>
        </div>
      </div>

      <!-- Keyboard Hint -->
      <div class="mt-4 text-center">
        <p class="text-xs text-primary-dimmer font-mono-primary">
          Keyboard: [SPACE/ENTER] = Yes | [N] = No
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { sessionsApi } from '@/api';
import { logger } from '@/api/client';

const router = useRouter();
const route = useRoute();

// Check if stiff mode is active
const isStiffMode = computed(() => route.query.mode === 'stiff');

// Form data
const formData = reactive({
  firstName: '',
  lastName: '',
  email: '',
  company: ''
});

// Form state
const loading = ref(false);
const errorMessage = ref('');
const errors = reactive({
  firstName: '',
  lastName: '',
  email: '',
  company: ''
});

// Validation
const validateForm = (): boolean => {
  // Reset errors
  errors.firstName = '';
  errors.lastName = '';
  errors.email = '';
  errors.company = '';
  errorMessage.value = '';
  
  let isValid = true;
  
  // First name validation
  if (!formData.firstName.trim()) {
    errors.firstName = 'First name is required';
    isValid = false;
  } else if (formData.firstName.length < 2) {
    errors.firstName = 'First name must be at least 2 characters';
    isValid = false;
  }
  
  // Last name validation
  if (!formData.lastName.trim()) {
    errors.lastName = 'Last name is required';
    isValid = false;
  } else if (formData.lastName.length < 2) {
    errors.lastName = 'Last name must be at least 2 characters';
    isValid = false;
  }
  
  // Email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!formData.email) {
    errors.email = 'Email is required';
    isValid = false;
  } else if (!emailRegex.test(formData.email)) {
    errors.email = 'Please enter a valid email address';
    isValid = false;
  }
  
  // Company validation
  if (!formData.company.trim()) {
    errors.company = 'Company is required';
    isValid = false;
  } else if (formData.company.length < 2) {
    errors.company = 'Company name must be at least 2 characters';
    isValid = false;
  }
  
  return isValid;
};

// Start survey
const startSurvey = async () => {
  try {
    // Validate form
    if (!validateForm()) {
      if (import.meta.env.DEV) {
        logger.warn('Form validation failed', formData);
      }
      return;
    }
    
    loading.value = true;
    errorMessage.value = '';
    
    // Combine first and last name
    const userName = `${formData.firstName.trim()} ${formData.lastName.trim()}`;
    
    if (import.meta.env.DEV) {
      logger.info('Starting survey session', { userName, email: formData.email });
    }
    
    // Create session
    const session = await sessionsApi.createSession({
      user_name: userName,
      user_email: formData.email.toLowerCase().trim(),
      company: formData.company.trim()
    });
    
    if (import.meta.env.DEV) {
      logger.info('Session created successfully', { sessionId: session.id });
    }
    
    // Navigate to survey, preserving mode if present
    await router.push({
      name: 'Survey',
      params: { sessionId: session.id },
      query: isStiffMode.value ? { mode: 'stiff' } : {}
    });
  } catch (error: any) {
    logger.error('Failed to start survey', error);
    errorMessage.value = error.message || 'Failed to start survey. Please try again.';
  } finally {
    loading.value = false;
  }
};
</script>