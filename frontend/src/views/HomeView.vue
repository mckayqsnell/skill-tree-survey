<template>
  <div class="min-h-screen bg-black star-field flex items-center justify-center px-4">
    <div class="max-w-xl w-full">
      <!-- Main Card -->
      <div class="glass-card">
        <!-- Header -->
        <div class="text-center mb-8">
          <h1 class="text-3xl font-bold text-green-400 mb-2" style="font-family: 'Orbitron', monospace;">
            SKILL TREE ASSESSMENT
          </h1>
          <p class="text-sm text-green-400/60 font-mono">Technical Competency Mapping System</p>
        </div>

        <div class="mb-6 p-3 border-l-2 border-green-400/50 bg-black/30">
          <p class="text-xs text-amber-500 font-mono mb-1">SYSTEM STATUS: READY</p>
          <p class="text-xs text-green-400/60 font-mono">
            Assessment duration: 5-10 minutes
          </p>
        </div>

        <!-- Form Section -->
        <form @submit.prevent="startSurvey" class="space-y-4">
          <!-- First Name -->
          <div>
            <label for="firstName" class="block text-xs text-green-400/70 mb-1 font-mono uppercase">
              First Name <span class="text-amber-500">*</span>
            </label>
            <input
              id="firstName"
              v-model="formData.firstName"
              type="text"
              required
              class="input-field"
              placeholder="John"
              :class="{ 'border-red-500': errors.firstName }"
            />
            <p v-if="errors.firstName" class="text-red-500 text-xs mt-1">{{ errors.firstName }}</p>
          </div>

          <!-- Last Name -->
          <div>
            <label for="lastName" class="block text-xs text-green-400/70 mb-1 font-mono uppercase">
              Last Name <span class="text-amber-500">*</span>
            </label>
            <input
              id="lastName"
              v-model="formData.lastName"
              type="text"
              required
              class="input-field"
              placeholder="Doe"
              :class="{ 'border-red-500': errors.lastName }"
            />
            <p v-if="errors.lastName" class="text-red-500 text-xs mt-1">{{ errors.lastName }}</p>
          </div>

          <!-- Email -->
          <div>
            <label for="email" class="block text-xs text-green-400/70 mb-1 font-mono uppercase">
              Email <span class="text-amber-500">*</span>
            </label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              required
              class="input-field"
              placeholder="john@example.com"
              :class="{ 'border-red-500': errors.email }"
            />
            <p v-if="errors.email" class="text-red-500 text-xs mt-1">{{ errors.email }}</p>
          </div>

          <!-- Company -->
          <div>
            <label for="company" class="block text-xs text-green-400/70 mb-1 font-mono uppercase">
              Company <span class="text-amber-500">*</span>
            </label>
            <input
              id="company"
              v-model="formData.company"
              type="text"
              required
              class="input-field"
              placeholder="Acme Corp"
              :class="{ 'border-red-500': errors.company }"
            />
            <p v-if="errors.company" class="text-red-500 text-xs mt-1">{{ errors.company }}</p>
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
          <div v-if="errorMessage" class="mt-4 p-3 border border-red-500/50 bg-red-500/10">
            <p class="text-red-500 text-sm font-mono">{{ errorMessage }}</p>
          </div>
        </form>

        <!-- Footer Links -->
        <div class="mt-6 pt-6 border-t border-green-400/20 text-center">
          <router-link 
            to="/admin" 
            class="text-xs text-amber-500/60 hover:text-amber-500 font-mono transition-colors"
          >
            Admin Access
          </router-link>
        </div>
      </div>

      <!-- Keyboard Hint -->
      <div class="mt-4 text-center">
        <p class="text-xs text-green-400/40 font-mono">
          Keyboard: [SPACE/ENTER] = Yes | [N] = No
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { sessionsApi } from '@/api';
import { logger } from '@/api/client';

const router = useRouter();

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
    
    // Navigate to survey
    await router.push({
      name: 'Survey',
      params: { sessionId: session.id }
    });
  } catch (error: any) {
    logger.error('Failed to start survey', error);
    errorMessage.value = error.message || 'Failed to start survey. Please try again.';
  } finally {
    loading.value = false;
  }
};
</script>