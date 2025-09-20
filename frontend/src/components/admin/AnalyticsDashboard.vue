<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-lg text-primary">Analytics Overview</h2>
      <!-- API Health Status -->
      <div class="flex items-center gap-2">
        <div class="flex items-center gap-1">
          <div
            class="w-2 h-2 rounded-full"
            :class="apiHealthy ? 'bg-primary' : 'bg-danger'"
          ></div>
          <span class="text-xs font-mono-primary" :class="apiHealthy ? 'text-primary' : 'text-danger'">
            API {{ apiHealthy ? 'CONNECTED' : 'DISCONNECTED' }}
          </span>
        </div>
        <span class="text-xs text-primary-faint">
          ({{ apiResponseTime }}ms)
        </span>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-8">
      <div class="inline-block w-8 h-8 border-2 border-primary-faint border-t-primary rounded-full animate-spin mb-2"></div>
      <p class="text-primary-dim text-sm">Loading analytics...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-8">
      <p class="text-danger text-sm mb-4">{{ error }}</p>
      <button @click="$emit('reload')" class="btn-primary text-sm">
        Retry
      </button>
    </div>

    <!-- Analytics Data -->
    <div v-else-if="analytics" class="space-y-6">
      <!-- Main Stats Grid -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="stat-card">
          <p class="text-2xl font-bold text-cyan-400">{{ analytics.total_sessions }}</p>
          <p class="text-xs text-primary-dim font-mono-primary uppercase">Total Sessions</p>
        </div>
        <div class="stat-card">
          <p class="text-2xl font-bold text-primary">{{ analytics.completed_sessions }}</p>
          <p class="text-xs text-primary-dim font-mono-primary uppercase">Completed</p>
        </div>
        <div class="stat-card-red">
          <p class="text-2xl font-bold text-red-400">{{ inProgressSessions }}</p>
          <p class="text-xs text-red-400/50 font-mono-primary uppercase">In Progress</p>
        </div>
        <div class="stat-card-amber">
          <p class="text-2xl font-bold text-amber-500">{{ completionRate }}%</p>
          <p class="text-xs text-amber-500/50 font-mono-primary uppercase">Completion Rate</p>
        </div>
      </div>

      <!-- Additional Stats -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- User Stats -->
        <div class="analytics-card">
          <h3 class="text-primary font-semibold mb-4">Survey Engagement</h3>
          <div class="space-y-3">
            <div class="flex justify-between">
              <span class="text-primary-dim text-sm">Total Participants:</span>
              <span class="text-primary font-mono-primary">{{ totalUsers }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-primary-dim text-sm">Avg Completion Time:</span>
              <span class="text-cyan-400 font-mono-primary">{{ estimatedAvgDuration }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-primary-dim text-sm">Abandonment Rate:</span>
              <span :class="abandonmentRate > 50 ? 'text-red-500' : 'text-amber-500'" class="font-mono-primary">{{ abandonmentRate }}%</span>
            </div>
          </div>
        </div>

        <!-- System Health -->
        <div class="analytics-card">
          <h3 class="text-primary font-semibold mb-4">System Health</h3>
          <div class="space-y-3">
            <div class="flex justify-between">
              <span class="text-primary-dim text-sm">API Status:</span>
              <span :class="apiHealthy ? 'text-primary' : 'text-red-500'" class="font-mono-primary">
                {{ apiHealthy ? 'Online' : 'Offline' }}
              </span>
            </div>
            <div class="flex justify-between">
              <span class="text-primary-dim text-sm">Response Time:</span>
              <span :class="apiResponseTime > 500 ? 'text-amber-500' : 'text-cyan-400'" class="font-mono-primary">{{ apiResponseTime }}ms</span>
            </div>
            <div class="flex justify-between">
              <span class="text-primary-dim text-sm">Last Check:</span>
              <span class="text-amber-500 font-mono-primary text-xs">{{ formatLastUpdate() }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Top Skills -->
      <div v-if="analytics.top_skills && analytics.top_skills.length > 0" class="analytics-card">
        <h3 class="text-primary font-semibold mb-4">Most Common Skills</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          <div
            v-for="skill in analytics.top_skills.slice(0, 6)"
            :key="skill.skill"
            class="skill-badge"
          >
            <span class="text-primary text-sm">{{ skill.skill }}</span>
            <span class="text-cyan-400 font-mono-primary text-sm">{{ skill.count }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-8">
      <svg class="w-16 h-16 text-primary-dim mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
      </svg>
      <p class="text-primary-dim text-sm">No analytics data available</p>
      <button @click="$emit('reload')" class="btn-primary text-sm mt-4">
        Load Analytics
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import type { SessionAnalytics } from '@/types';

// Props
const props = defineProps<{
  analytics: SessionAnalytics | null;
  loading: boolean;
  error: string;
  apiHealthy: boolean;
  apiResponseTime: number;
}>();

// Emits
defineEmits<{
  'reload': [];
}>();

// State
const lastApiCheck = ref(new Date());

// Computed properties
const inProgressSessions = computed(() => {
  if (!props.analytics) return 0;
  return props.analytics.total_sessions - props.analytics.completed_sessions;
});

const completionRate = computed(() => {
  if (!props.analytics || props.analytics.total_sessions === 0) return 0;
  return Math.round((props.analytics.completed_sessions / props.analytics.total_sessions) * 100);
});

const totalUsers = computed(() => {
  if (!props.analytics) return 0;
  // Use the unique_users count from the backend
  return props.analytics.unique_users || 0;
});

const estimatedAvgDuration = computed(() => {
  if (!props.analytics) return 'N/A';

  // Use the average_completion_time_minutes directly from the backend
  if (props.analytics.average_completion_time_minutes === null ||
      props.analytics.average_completion_time_minutes === undefined) {
    return 'N/A';
  }

  const avgMinutes = props.analytics.average_completion_time_minutes;
  return `${Math.round(avgMinutes)} min`;
});

const abandonmentRate = computed(() => {
  // Calculate how many sessions were started but not completed
  if (!props.analytics || props.analytics.total_sessions === 0) return 0;

  const inProgress = props.analytics.total_sessions - props.analytics.completed_sessions;
  const rate = (inProgress / props.analytics.total_sessions) * 100;
  return Math.round(rate);
});

// Methods
const formatLastUpdate = (): string => {
  return lastApiCheck.value.toLocaleTimeString();
};
</script>