<template>
  <div class="min-h-screen bg-black star-field flex items-center justify-center px-4 py-8 md:py-0" :class="{ 'stiff-mode': isStiffMode }">
    <div class="max-w-2xl w-full">
      <!-- Success Message -->
      <div class="text-center mb-6 md:mb-8">
        <div class="inline-block mb-4">
          <svg class="w-12 md:w-16 h-12 md:h-16 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        <h1 class="text-2xl md:text-3xl font-bold text-primary mb-2 font-heading">
          ASSESSMENT COMPLETE
        </h1>
        <p class="text-xs md:text-sm text-primary-dim font-mono-primary">Your skill profile has been recorded</p>
      </div>

      <!-- Stats Display -->
      <div v-if="!loading && summary" class="glass-card p-4 md:p-6 mb-6">

        <div class="grid grid-cols-2 gap-3 md:grid-cols-4 md:gap-4 mb-6">
          <div class="text-center">
            <p class="text-2xl font-bold text-primary">{{ summary.total_responses }}</p>
            <p class="text-xs text-primary-dim font-mono-primary">Questions</p>
          </div>
          <div class="text-center">
            <p class="text-2xl font-bold text-cyan-400">{{ summary.yes_responses }}</p>
            <p class="text-xs text-cyan-400/50 font-mono-primary">Skills</p>
          </div>
          <div class="text-center">
            <p class="text-2xl font-bold text-accent">{{ summary.is_completed ? 100 : 0 }}%</p>
            <p class="text-xs text-accent-dim font-mono-primary">Complete</p>
          </div>
          <div class="text-center">
            <p class="text-2xl font-bold text-primary">{{ Math.round(summary.completion_time_minutes || 0) || '< 1' }}</p>
            <p class="text-xs text-primary-dim font-mono-primary">Minutes</p>
          </div>
        </div>

        <!-- Category Breakdown -->
        <div v-if="categoryStats.length > 0">
          <h3 class="text-sm font-mono-primary text-primary-dim mb-3">Skills by Category</h3>
          <div class="space-y-2">
            <div 
              v-for="cat in categoryStats"
              :key="cat.category"
              class="flex items-center justify-between"
            >
              <span class="text-sm text-primary-subtle">{{ cat.category }}</span>
              <div class="flex items-center gap-2">
                <div class="w-24 h-2 bg-primary/10 overflow-hidden">
                  <div 
                    class="h-full bg-primary/50 transition-all duration-1000"
                    :style="{ width: `${isNaN(cat.percentage_yes) ? 0 : cat.percentage_yes}%` }"
                  ></div>
                </div>
                <span class="text-xs text-primary-dim w-10 text-right">{{ isNaN(cat.percentage_yes) ? 0 : Math.round(cat.percentage_yes) }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-else-if="loading" class="glass-card text-center">
        <div class="inline-block w-8 h-8 border-2 border-primary-faint border-t-primary rounded-full animate-spin mb-4"></div>
        <p class="text-primary-dim font-mono-primary text-sm">Loading results...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="glass-card">
        <p class="text-danger font-mono-primary text-sm">{{ error }}</p>
      </div>

      <!-- Thank You -->
      <div class="text-center mb-6">
        <p class="text-primary-subtle">Thank you for completing the skill assessment</p>
      </div>

      <!-- Actions -->
      <div class="flex flex-col md:flex-row gap-3 md:gap-4 justify-center">
        <button
          @click="startNewSurvey"
          class="btn-primary w-full md:w-auto"
          type="button"
        >
          New Survey
        </button>
        <button
          @click="goToAdmin"
          class="btn-secondary w-full md:w-auto"
          type="button"
        >
          Admin Panel
        </button>
      </div>

      <!-- Session Info -->
      <div class="mt-8 text-center text-xs text-primary-faint font-mono-primary">
        <p v-if="summary?.completed_at">Completed: {{ formatDate(summary.completed_at) }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { sessionsApi, responsesApi } from '@/api';
import { logger } from '@/api/client';
import type { SessionSummary, CategoryStatistics } from '@/types';

// Props
const props = defineProps<{
  sessionId: string
}>();

const router = useRouter();
const route = useRoute();

// Check if stiff mode is active
const isStiffMode = computed(() => route.query.mode === 'stiff');

// State
const loading = ref(true);
const error = ref('');
const summary = ref<SessionSummary | null>(null);
const categoryStats = ref<CategoryStatistics[]>([]);

// Load session summary
const loadSummary = async () => {
  try {
    loading.value = true;
    error.value = '';
    
    if (import.meta.env.DEV) {
      logger.info('Loading session summary', { sessionId: props.sessionId });
    }
    
    // Get session summary
    const sessionSummary = await sessionsApi.getSessionSummary(Number(props.sessionId));
    summary.value = sessionSummary;
    
    // Get category statistics
    try {
      const stats = await responsesApi.getCategoryStatistics(Number(props.sessionId));
      // Calculate percentage_yes if not provided by backend
      categoryStats.value = stats
        .map(s => ({
          ...s,
          percentage_yes: (s.total && s.total > 0) ? (s.yes_count / s.total) * 100 :
                        (s.total_questions > 0) ? (s.yes_count / s.total_questions) * 100 : 0
        }))
        .filter(s => s.yes_count > 0 && s.category !== 'Pokemon') // Filter out Pokemon category
        .sort((a, b) => b.percentage_yes - a.percentage_yes);
      if (import.meta.env.DEV) {
        logger.info(`Loaded ${categoryStats.value.length} category statistics`);
      }
    } catch (err) {
      logger.warn('Failed to load category stats', err);
      // Non-critical, continue
    }
    
  } catch (err: any) {
    logger.error('Failed to load session summary', err);
    error.value = err.message || 'Failed to load results';
  } finally {
    loading.value = false;
  }
};

// Format date
const formatDate = (dateStr: string | null): string => {
  if (!dateStr) return 'Not available';
  try {
    const date = new Date(dateStr);
    return date.toLocaleString();
  } catch {
    return dateStr;
  }
};

// Start new survey
const startNewSurvey = () => {
  if (import.meta.env.DEV) {
    logger.info('Starting new survey from complete page');
  }
  router.push({
    path: '/',
    query: isStiffMode.value ? { mode: 'stiff' } : {}
  });
};

// Go to admin panel
const goToAdmin = () => {
  if (import.meta.env.DEV) {
    logger.info('Navigating to admin from complete page');
  }
  // Clear any existing admin session to force re-authentication
  sessionStorage.removeItem('adminPassword');
  router.push({
    path: '/admin',
    query: isStiffMode.value ? { mode: 'stiff' } : {}
  });
};

// Lifecycle
onMounted(() => {
  loadSummary();
});
</script>