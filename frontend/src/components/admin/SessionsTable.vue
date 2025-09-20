<template>
  <div>
    <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3 mb-6">
      <h2 class="text-base sm:text-lg text-primary">Recent Sessions</h2>
      <div class="flex flex-col sm:flex-row sm:items-center gap-3 sm:gap-4">
        <button
          @click="$emit('clear-all')"
          class="flex items-center justify-center gap-2 px-3 py-1.5 text-xs border border-red-500/50 text-red-500 hover:bg-red-500/10 hover:border-red-500 transition-all rounded"
          :disabled="sessions.length === 0"
        >
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
          </svg>
          Clear All
        </button>
        <p class="text-xs text-primary-dim font-mono-primary text-center sm:text-left">Click on a session to view detailed analysis</p>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-8">
      <div class="inline-block w-8 h-8 border-2 border-primary-faint border-t-primary rounded-full animate-spin mb-2"></div>
      <p class="text-primary-dim text-sm">Loading sessions...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-8">
      <p class="text-danger text-sm mb-4">{{ error }}</p>
      <button @click="$emit('reload')" class="btn-primary text-sm">
        Retry
      </button>
    </div>

    <!-- Sessions List -->
    <div v-else-if="sessions.length > 0" class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-primary-faint text-primary-subtle">
            <th class="text-left py-2 px-3">ID</th>
            <th class="text-left py-2 px-3">User</th>
            <th class="text-left py-2 px-3">Email</th>
            <th class="text-left py-2 px-3">Company</th>
            <th class="text-left py-2 px-3">Started</th>
            <th class="text-left py-2 px-3">Duration</th>
            <th class="text-left py-2 px-3">Status</th>
            <th class="text-left py-2 px-3">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="session in sessions"
            :key="session.id"
            class="border-b border-primary-faint hover:bg-primary/5 transition-colors cursor-pointer group"
            @click="viewSession(session.id)"
          >
            <td class="py-2 px-3 text-primary-subtle group-hover:text-primary">{{ session.id }}</td>
            <td class="py-2 px-3 text-primary-subtle group-hover:text-primary">{{ session.user_name }}</td>
            <td class="py-2 px-3 text-primary-subtle group-hover:text-primary font-mono-primary text-xs">{{ session.user_email }}</td>
            <td class="py-2 px-3 text-primary-subtle group-hover:text-primary">{{ session.company }}</td>
            <td class="py-2 px-3 text-primary-subtle group-hover:text-primary text-xs">{{ formatDate(session.started_at) }}</td>
            <td class="py-2 px-3 text-primary-subtle group-hover:text-primary text-xs font-mono-primary">
              {{ formatDuration(session.completion_time_minutes) }}
            </td>
            <td class="py-2 px-3">
              <span v-if="session.completed_at" class="flex items-center gap-1">
                <svg class="w-3 h-3 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span class="text-primary text-xs">Complete</span>
              </span>
              <span v-else class="flex items-center gap-1">
                <svg class="w-3 h-3 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span class="text-amber-500 text-xs">In Progress</span>
              </span>
            </td>
            <td class="py-2 px-3">
              <div class="flex items-center gap-2">
                <button
                  @click.stop="viewSession(session.id)"
                  class="btn-view-stats"
                >
                  View Stats
                </button>
                <button
                  @click.stop="$emit('delete-session', session)"
                  class="text-xs p-1 border border-red-500/30 text-red-500/80 hover:bg-red-500/10 hover:border-red-500 transition-all rounded"
                  title="Delete session"
                >
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                  </svg>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-8">
      <svg class="w-16 h-16 text-primary-dim mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
      </svg>
      <p class="text-primary-dim text-sm">No sessions found</p>
      <p class="text-xs text-primary-faint mt-2">Sessions will appear here as users complete the survey</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router';
import type { SessionSummary } from '@/types';

// Props
defineProps<{
  sessions: SessionSummary[];
  loading: boolean;
  error: string;
}>();

// Emits
defineEmits<{
  'clear-all': [];
  'delete-session': [session: SessionSummary];
  'reload': [];
}>();

const router = useRouter();
const route = useRoute();

// Check if stiff mode is active
const isStiffMode = route.query.mode === 'stiff';

// Methods
const viewSession = (sessionId: number) => {
  router.push({
    name: 'SessionStats',
    params: { sessionId: sessionId.toString() },
    query: isStiffMode ? { mode: 'stiff' } : {}
  });
};

const formatDate = (dateStr: string): string => {
  try {
    const date = new Date(dateStr);
    return date.toLocaleDateString();
  } catch {
    return dateStr;
  }
};

const formatDuration = (minutes: number | null): string => {
  if (!minutes) return 'N/A';
  if (minutes < 1) return '< 1 min';
  return `${Math.round(minutes)} min`;
};
</script>