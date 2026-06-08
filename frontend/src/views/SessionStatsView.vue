<template>
  <div class="min-h-screen bg-black star-field" :class="{ 'stiff-mode': isStiffMode }">
    <div class="p-6">
      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center gap-4">
          <button 
            @click="goBack"
            class="btn-secondary text-sm"
          >
            ← Back to Sessions
          </button>
          <h1 class="text-2xl font-bold text-primary font-heading">
            SESSION ANALYSIS
          </h1>
        </div>
        <div class="text-right">
          <p class="text-xs text-primary-dim font-mono-primary">Session ID: {{ sessionId }}</p>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="glass-card text-center">
        <div class="inline-block w-8 h-8 border-2 border-primary-faint border-t-primary rounded-full animate-spin mb-4"></div>
        <p class="text-primary-dim font-mono-primary text-sm">Loading session data...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="glass-card">
        <div class="text-center mb-4">
          <svg class="w-12 h-12 text-red-500 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <p class="text-danger font-mono-primary text-sm mb-2">{{ error }}</p>
        </div>
        <div class="text-center">
          <button @click="loadSessionData" class="btn-primary mr-2">Retry</button>
          <button @click="goBack" class="btn-secondary">Go Back</button>
        </div>
      </div>

      <!-- Main Content -->
      <div v-else-if="summary" class="space-y-6">
        <!-- User Info Card -->
        <div class="glass-card">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg text-primary font-heading">USER PROFILE</h2>
            <div class="flex items-center gap-2">
              <div v-if="summary.is_completed" class="flex items-center gap-1">
                <svg class="w-4 h-4 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span class="text-xs text-primary font-mono-primary">COMPLETED</span>
              </div>
              <div v-else class="flex items-center gap-1">
                <svg class="w-4 h-4 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span class="text-xs text-accent font-mono-primary">IN PROGRESS</span>
              </div>
            </div>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="space-y-2">
              <p class="text-xs text-primary-dim font-mono-primary uppercase">Name</p>
              <p class="text-primary font-semibold">{{ summary.user_name }}</p>
            </div>
            <div class="space-y-2">
              <p class="text-xs text-primary-dim font-mono-primary uppercase">Email</p>
              <p class="text-primary font-mono-primary text-sm">{{ summary.user_email }}</p>
            </div>
            <div class="space-y-2">
              <p class="text-xs text-primary-dim font-mono-primary uppercase">Company</p>
              <p class="text-primary font-semibold">{{ summary.company }}</p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6 pt-4 border-t border-primary-faint">
            <div class="space-y-2">
              <p class="text-xs text-primary-dim font-mono-primary uppercase">Started</p>
              <p class="text-primary-subtle text-sm">{{ formatDate(summary.started_at) }}</p>
            </div>
            <div class="space-y-2">
              <p class="text-xs text-primary-dim font-mono-primary uppercase">Duration</p>
              <p class="text-info font-semibold">
                <span v-if="summary.completion_time_minutes">{{ Math.round(summary.completion_time_minutes) }} min</span>
                <span v-else-if="!summary.is_completed">{{ getElapsedTime() }}</span>
                <span v-else>&lt; 1 min</span>
              </p>
            </div>
            <div class="space-y-2">
              <p class="text-xs text-primary-dim font-mono-primary uppercase">Progress</p>
              <p class="text-accent font-semibold">{{ getCompletionStatus() }}</p>
            </div>
          </div>
        </div>

        <!-- Pokemon Warning Alert -->
        <div v-if="(pokemonStats?.yes_count || 0) > 0" class="glass-card border-2 border-red-600 bg-red-900/20 mb-6">
          <div class="flex items-center gap-3">
            <svg class="w-8 h-8 text-red-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
            </svg>
            <div>
              <h3 class="text-red-600 font-bold text-lg">PRODUCTIVITY ALERT</h3>
              <p class="text-red-400 text-sm mt-1">
                This developer has demonstrated knowledge of {{ pokemonStats?.yes_count || 0 }} Pokémon. 
                Studies show inverse correlation between Pokémon knowledge and code quality.
              </p>
            </div>
          </div>
        </div>

        <!-- Stats Overview -->
        <div class="glass-card">
          <h2 class="text-lg text-primary mb-6 font-heading">PERFORMANCE METRICS</h2>
          
          <div class="grid grid-cols-2 md:grid-cols-5 gap-6">
            <div class="metric-card border-primary-faint group">
              <p class="text-3xl font-bold text-primary mb-1">{{ summary.total_responses }}</p>
              <div class="flex items-center justify-center gap-1">
                <p class="text-xs text-primary-dim font-mono-primary uppercase">Total Questions</p>
                <svg class="w-3 h-3 text-primary-dimmer cursor-help" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <!-- Tooltip -->
              <div class="tooltip-base border border-primary-dim text-primary">
                Number of questions answered in this session
              </div>
            </div>
            
            <div class="metric-card border-info-faint group">
              <p class="text-3xl font-bold text-info mb-1">{{ summary.yes_responses }}</p>
              <div class="flex items-center justify-center gap-1">
                <p class="text-xs text-info-dimmer font-mono-primary uppercase">Skills Confirmed</p>
                <svg class="w-3 h-3 text-info-faint cursor-help" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <!-- Tooltip -->
              <div class="tooltip-base border border-info-dim text-info">
                Number of "YES" answers - skills the user has
              </div>
            </div>
            
            <div class="metric-card border-red-400/20 group">
              <p class="text-3xl font-bold text-red-400 mb-1">{{ summary.no_responses }}</p>
              <div class="flex items-center justify-center gap-1">
                <p class="text-xs text-red-400/50 font-mono-primary uppercase">Skills Declined</p>
                <svg class="w-3 h-3 text-red-400/40 cursor-help" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <!-- Tooltip -->
              <div class="tooltip-base border border-red-400/30 text-red-400">
                Number of "NO" answers - areas for potential growth
              </div>
            </div>
            
            <div class="metric-card border-amber-500/20 group">
              <p class="text-3xl font-bold text-amber-500 mb-1">{{ getConfidenceScore() }}%</p>
              <div class="flex items-center justify-center gap-1">
                <p class="text-xs text-amber-500/50 font-mono-primary uppercase">Confidence Score</p>
                <svg class="w-3 h-3 text-amber-500/40 cursor-help" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <!-- Tooltip -->
              <div class="tooltip-base border border-amber-500/30 text-amber-500">
                Percentage of questions answered "YES" - overall skill confidence level
              </div>
            </div>
            
            <div class="metric-card border-red-600/30 group">
              <div class="flex items-center gap-2 justify-center">
                <p class="text-3xl font-bold mb-1" :class="(pokemonStats?.yes_count || 0) > 0 ? 'text-red-600' : 'text-gray-500'">
                  {{ pokemonStats?.yes_count || 0 }}/{{ pokemonStats?.total_questions || 0 }}
                </p>
                <svg v-if="(pokemonStats?.yes_count || 0) > 0" class="w-6 h-6 text-red-600 animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                </svg>
              </div>
              <div class="flex items-center justify-center gap-1">
                <p class="text-xs font-mono-primary uppercase" :class="(pokemonStats?.yes_count || 0) > 0 ? 'text-red-600 font-bold' : 'text-gray-500'">
                  Pokémon Alert
                </p>
                <svg class="w-3 h-3 cursor-help" :class="(pokemonStats?.yes_count || 0) > 0 ? 'text-red-600' : 'text-gray-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <!-- Tooltip -->
              <div class="tooltip-base border text-white" :class="(pokemonStats?.yes_count || 0) > 0 ? 'border-red-600 bg-red-700' : 'border-gray-500 bg-gray-700'">
                <span v-if="(pokemonStats?.yes_count || 0) > 0">
                  ⚠️ WARNING: Strong correlation detected between Pokémon knowledge and code quality issues. Recommend immediate code review.
                </span>
                <span v-else>
                  No Pokémon knowledge detected. Focus on programming maintained successfully.
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- No Category Data Message -->
        <div v-if="categoryStats.length === 0 && summary" class="glass-card">
          <h2 class="text-lg text-primary mb-4 font-heading">SKILL PROFILE</h2>
          <div class="text-center py-8">
            <svg class="w-16 h-16 text-accent mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
            </svg>
            <p class="text-accent-dim mb-2">No category data available</p>
            <p class="text-xs text-primary-dim font-mono-primary">
              This session may not have category-specific questions or the data hasn't been processed yet.
            </p>
            <div class="mt-4 p-4 bg-accent/10 border border-accent/20 rounded">
              <p class="text-sm text-accent-dim">
                {{ summary.total_responses }} total responses recorded
              </p>
            </div>
          </div>
        </div>

        <!-- Skill Radar Chart -->
        <div v-else-if="categoryStats.length > 0" class="glass-card p-4 md:p-6 skill-profile-section">
          <h2 class="text-lg text-primary mb-3 md:mb-6 font-heading">SKILL PROFILE</h2>
          
          <div class="flex flex-col sm:flex-row gap-4 sm:gap-6 items-start skill-profile-container">
            <!-- Radar Chart -->
            <div class="flex-shrink-0 w-full md:w-auto skill-chart-wrapper" :class="isStiffMode ? 'order-2 md:order-2' : ''">
              <div class="relative w-[320px] md:w-[380px] h-[320px] md:h-[380px] mx-auto p-1 skill-chart-container">
                <svg width="100%" height="100%" viewBox="-15 0 395 380" class="transform" preserveAspectRatio="xMidYMid meet">
                  <!-- Background Grid -->
                  <g :class="isStiffMode ? 'opacity-60' : 'opacity-20'">
                    <!-- Concentric circles -->
                    <circle cx="190" cy="190" r="50" fill="none" :stroke="isStiffMode ? 'rgba(37, 99, 235, 0.5)' : 'rgba(0, 255, 65, 0.3)'" stroke-width="1"/>
                    <circle cx="190" cy="190" r="100" fill="none" :stroke="isStiffMode ? 'rgba(37, 99, 235, 0.5)' : 'rgba(0, 255, 65, 0.3)'" stroke-width="1"/>
                    <circle cx="190" cy="190" r="150" fill="none" :stroke="isStiffMode ? 'rgba(37, 99, 235, 0.5)' : 'rgba(0, 255, 65, 0.3)'" stroke-width="1"/>
                    
                    <!-- Radial lines -->
                    <g v-for="(_, index) in categoryStats" :key="`line-${index}`">
                      <line 
                        x1="190" 
                        y1="190" 
                        :x2="190 + Math.cos((index * 2 * Math.PI / categoryStats.length) - Math.PI/2) * 150"
                        :y2="190 + Math.sin((index * 2 * Math.PI / categoryStats.length) - Math.PI/2) * 150"
                        :stroke="isStiffMode ? 'rgba(37, 99, 235, 0.5)' : 'rgba(0, 255, 65, 0.3)'" 
                        stroke-width="1"
                      />
                    </g>
                  </g>
                  
                  <!-- Data Polygon -->
                  <polygon 
                    :points="getRadarPoints()" 
                    :fill="isStiffMode ? 'rgba(37, 99, 235, 0.2)' : 'rgba(6, 182, 212, 0.2)'" 
                    :stroke="isStiffMode ? 'rgba(37, 99, 235, 0.8)' : 'rgba(6, 182, 212, 0.8)'" 
                    stroke-width="2"
                  />
                  
                  <!-- Data Points -->
                  <g v-for="(cat, index) in categoryStats" :key="`point-${index}`">
                    <circle 
                      :cx="190 + Math.cos((index * 2 * Math.PI / categoryStats.length) - Math.PI/2) * (cat.percentage_yes / 100 * 150)"
                      :cy="190 + Math.sin((index * 2 * Math.PI / categoryStats.length) - Math.PI/2) * (cat.percentage_yes / 100 * 150)"
                      r="5" 
                      :fill="getRadarPointColor(cat.percentage_yes)"
                      stroke="white" 
                      stroke-width="2"
                    />
                  </g>
                  
                  <!-- Category Labels -->
                  <g v-for="(cat, index) in categoryStats" :key="`label-${index}`">
                    <!-- Background rect for better readability -->
                    <rect
                      :x="190 + Math.cos((index * 2 * Math.PI / categoryStats.length) - Math.PI/2) * 170 - 40"
                      :y="190 + Math.sin((index * 2 * Math.PI / categoryStats.length) - Math.PI/2) * 170 - 12"
                      width="80"
                      height="24"
                      :fill="isStiffMode ? 'rgba(255, 255, 255, 0.9)' : 'rgba(0, 0, 0, 0.8)'"
                      rx="2"
                    />
                    <text 
                      :x="190 + Math.cos((index * 2 * Math.PI / categoryStats.length) - Math.PI/2) * 170"
                      :y="190 + Math.sin((index * 2 * Math.PI / categoryStats.length) - Math.PI/2) * 170 - 2"
                      text-anchor="middle"
                      dominant-baseline="middle"
                      :class="isStiffMode ? 'fill-gray-800' : 'fill-green-400'"
                      style="font-size: 11px; font-weight: 600;"
                    >
                      {{ cat.category }}
                    </text>
                    <text 
                      :x="190 + Math.cos((index * 2 * Math.PI / categoryStats.length) - Math.PI/2) * 170"
                      :y="190 + Math.sin((index * 2 * Math.PI / categoryStats.length) - Math.PI/2) * 170 + 10"
                      text-anchor="middle"
                      dominant-baseline="middle"
                      :class="isStiffMode ? 'fill-gray-600' : 'fill-cyan-400'"
                      style="font-size: 10px; font-weight: 700;"
                    >
                      {{ Math.round(cat.percentage_yes) }}%
                    </text>
                  </g>
                  
                  <!-- Center Dot -->
                  <circle cx="190" cy="190" r="3" :fill="isStiffMode ? 'rgba(37, 99, 235, 0.8)' : 'rgba(0, 255, 65, 0.8)'"/>
                  
                  <!-- Percentage Scale Labels - Removed -->
                  <!-- <g class="opacity-60">
                    <text x="215" y="155" class="fill-primary text-xs font-mono-primary" style="font-size: 8px;" text-anchor="start">25%</text>
                    <text x="215" y="95" class="fill-primary text-xs font-mono-primary" style="font-size: 8px;" text-anchor="start">50%</text>
                    <text x="215" y="35" class="fill-primary text-xs font-mono-primary" style="font-size: 8px;" text-anchor="start">75%</text>
                  </g> -->
                </svg>
              </div>
            </div>
            
            <!-- Legend & Stats -->
            <div class="flex-1 space-y-2 min-w-0 w-full skill-stats-container" :class="isStiffMode ? 'md:max-w-sm order-1 md:order-1' : ''">
              <div class="grid grid-cols-1" :class="isStiffMode ? 'gap-1' : 'gap-2'">
                <div 
                  v-for="cat in categoryStats"
                  :key="cat.category"
                  class="flex items-center justify-between bg-overlay border border-primary-faint rounded"
                  :class="isStiffMode ? 'px-2 py-1' : 'p-3'"
                >
                  <div class="flex items-center" :class="isStiffMode ? 'gap-2' : 'gap-3'">
                    <div
                      class="rounded-full flex-shrink-0"
                      :class="isStiffMode ? 'w-2 h-2' : 'w-3 h-3'"
                      :style="{ backgroundColor: getRadarPointColor(cat.percentage_yes) }"
                    ></div>
                    <div class="min-w-0 flex-1">
                      <div v-if="isStiffMode" class="flex items-baseline gap-2">
                        <h3 class="text-primary font-semibold text-sm truncate">{{ cat.category }}</h3>
                        <p class="text-xs text-primary-dim font-mono-primary">
                          {{ cat.yes_count }}/{{ cat.total_questions }}
                        </p>
                      </div>
                      <div v-else>
                        <h3 class="text-primary font-semibold text-sm">{{ cat.category }}</h3>
                        <p class="text-xs text-primary-dim font-mono-primary">
                          {{ cat.yes_count }}/{{ cat.total_questions }}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div v-if="isStiffMode" class="flex items-center gap-2 flex-shrink-0">
                    <p class="text-sm font-bold text-info">{{ Math.round(cat.percentage_yes) }}%</p>
                    <p 
                      class="text-xs font-mono font-semibold"
                      :class="getSkillLevelClass(cat.percentage_yes)"
                    >
                      {{ getSkillLevel(cat.percentage_yes) }}
                    </p>
                  </div>
                  <div v-else class="text-right flex-shrink-0">
                    <p class="text-lg font-bold text-info">{{ Math.round(cat.percentage_yes) }}%</p>
                    <p 
                      class="text-xs font-mono font-semibold"
                      :class="getSkillLevelClass(cat.percentage_yes)"
                    >
                      {{ getSkillLevel(cat.percentage_yes) }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Skill Summary -->
        <div v-if="categoryStats.length > 0" class="glass-card">
          <h2 class="text-lg text-primary mb-4 font-heading">SKILL ASSESSMENT</h2>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Strongest Skills -->
            <div>
              <h3 class="text-sm text-info-dim font-mono-primary uppercase mb-3">Strongest Areas</h3>
              <div class="space-y-2">
                <div 
                  v-for="skill in getTopSkills()"
                  :key="skill.category"
                  class="flex items-center justify-between p-2 bg-primary/5 rounded"
                >
                  <span class="text-primary text-sm">{{ skill.category }}</span>
                  <span class="text-info font-semibold text-sm">{{ Math.round(skill.percentage_yes) }}%</span>
                </div>
              </div>
            </div>
            
            <!-- Growth Areas -->
            <div>
              <h3 class="text-sm text-accent-dim font-mono-primary uppercase mb-3">Growth Opportunities</h3>
              <div class="space-y-2">
                <div 
                  v-for="skill in getGrowthAreas()"
                  :key="skill.category"
                  class="flex items-center justify-between p-2 bg-accent/5 rounded"
                >
                  <span class="text-primary text-sm">{{ skill.category }}</span>
                  <span class="text-accent font-semibold text-sm">{{ Math.round(skill.percentage_yes) }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { sessionsApi, responsesApi, questionsApi, categoriesApi } from '@/api';
import { logger } from '@/api/client';
import type { SessionSummary, CategoryStatistics } from '@/types';
import type { CategoryOrder } from '@/api/categories';
import { useAdminAuth } from '@/composables/useAdminAuth';

// Props
const props = defineProps<{
  sessionId: string
}>();

const router = useRouter();
const route = useRoute();

// Check if stiff mode is active
const isStiffMode = computed(() => route.query.mode === 'stiff');

// Admin authentication
const { requireAuth } = useAdminAuth();

// State
const loading = ref(true);
const error = ref('');
const summary = ref<SessionSummary | null>(null);
const categoryStats = ref<CategoryStatistics[]>([]);
const pokemonStats = ref<CategoryStatistics | null>(null);
const categoryOrders = ref<CategoryOrder[]>([]);

// Load session data
const loadSessionData = async () => {
  try {
    loading.value = true;
    error.value = '';
    
    if (import.meta.env.DEV) {
      logger.info('Loading session stats', { sessionId: props.sessionId });
    }
    
    // Get session summary
    const sessionSummary = await sessionsApi.getSessionSummary(Number(props.sessionId));
    summary.value = sessionSummary;
    
    // Get category statistics and all available questions
    try {
      if (import.meta.env.DEV) {
        logger.info(`Fetching category stats for session ${props.sessionId}`);
      }
      
      // Get response stats, all questions, and category order
      const [stats, allQuestions, categoryOrderData] = await Promise.all([
        responsesApi.getCategoryStatistics(Number(props.sessionId)),
        questionsApi.getAllQuestions(),
        categoriesApi.getCategoryOrder()
      ]);

      categoryOrders.value = categoryOrderData;
      
      if (import.meta.env.DEV) {
        logger.info('Raw category stats from API:', stats);
        logger.info('All questions from API:', allQuestions);
      }
      
      // Count total questions per category from all available questions
      const categoryTotals: Record<string, number> = {};
      const countQuestionsInTree = (questions: any[]) => {
        for (const question of questions) {
          const category = question.category || 'Uncategorized';
          categoryTotals[category] = (categoryTotals[category] || 0) + 1;
          
          // Count children recursively
          if (question.children && question.children.length > 0) {
            countQuestionsInTree(question.children);
          }
        }
      };
      
      countQuestionsInTree(allQuestions);
      
      if (import.meta.env.DEV) {
        logger.info('Category totals calculated:', categoryTotals);
      }
      
      // Create stats for all categories, including those with 0 responses
      const allCategoryStats = Object.keys(categoryTotals).map(category => {
        const responseStats = stats.find(s => s.category === category);
        const yesCount = responseStats?.yes_count || 0;
        const totalQuestions = categoryTotals[category];
        
        return {
          category,
          yes_count: yesCount,
          no_count: responseStats?.no_count || 0,
          total_questions: totalQuestions,
          total: responseStats?.total || 0, // questions answered in this category
          percentage_yes: totalQuestions > 0 ? (yesCount / totalQuestions) * 100 : 0
        };
      });
      
      // Separate Pokemon category from other skills
      const pokemonCat = allCategoryStats.find(cat => cat.category.toLowerCase() === 'pokemon');
      if (pokemonCat) {
        pokemonStats.value = pokemonCat;
      }
      
      // Filter out Pokemon from skill profile and sort by defined category order
      const filteredStats = allCategoryStats
        .filter(cat => cat.category.toLowerCase() !== 'pokemon');

      // Create a map of category to order_index for efficient lookup
      const categoryOrderMap: Record<string, number> = {};
      categoryOrders.value.forEach((order) => {
        categoryOrderMap[order.category] = order.order_index;
      });

      // Sort by the defined order, with any unknown categories at the end
      categoryStats.value = filteredStats.sort((a, b) => {
        const orderA = categoryOrderMap[a.category] ?? 999;
        const orderB = categoryOrderMap[b.category] ?? 999;

        // If both have the same order (e.g., both unknown), sort alphabetically
        if (orderA === orderB) {
          return a.category.localeCompare(b.category);
        }

        return orderA - orderB;
      });
      
      if (import.meta.env.DEV) {
        logger.info(`Processed ${categoryStats.value.length} category statistics:`, categoryStats.value);
      }
    } catch (err) {
      logger.error('Failed to load category stats', err);
      // Try to get some basic stats from session summary as fallback
      if (summary.value && summary.value.total_responses > 0) {
        if (import.meta.env.DEV) {
          logger.info('Using fallback category stats from session summary');
        }
        // Create a simple fallback category
        categoryStats.value = [{
          category: 'General Skills',
          total_questions: summary.value.total_responses,
          yes_count: summary.value.yes_responses,
          no_count: summary.value.no_responses,
          percentage_yes: (summary.value.yes_responses / summary.value.total_responses) * 100
        }];
      }
    }
    
  } catch (err: any) {
    logger.error('Failed to load session data', err);
    error.value = err.message || 'Failed to load session data';
  } finally {
    loading.value = false;
  }
};

// Helper functions
const formatDate = (dateStr: string): string => {
  try {
    const date = new Date(dateStr);
    return date.toLocaleString();
  } catch {
    return dateStr;
  }
};

const getElapsedTime = (): string => {
  if (!summary.value?.started_at) return 'Unknown';
  
  const started = new Date(summary.value.started_at);
  const now = new Date();
  const diffMinutes = Math.floor((now.getTime() - started.getTime()) / (1000 * 60));
  
  if (diffMinutes < 1) return '< 1 min';
  if (diffMinutes < 60) return `${diffMinutes} min`;
  
  const hours = Math.floor(diffMinutes / 60);
  const mins = diffMinutes % 60;
  return `${hours}h ${mins}m`;
};

const getCompletionStatus = (): string => {
  if (!summary.value) return 'Unknown';
  return summary.value.is_completed ? 'Complete' : 'In Progress';
};

const getConfidenceScore = (): number => {
  if (!summary.value || summary.value.total_responses === 0) return 0;
  return Math.round((summary.value.yes_responses / summary.value.total_responses) * 100);
};

const getSkillLevel = (percentage: number): string => {
  if (percentage >= 80) return 'Expert';
  if (percentage >= 60) return 'Advanced';
  if (percentage >= 40) return 'Intermediate';
  if (percentage >= 20) return 'Beginner';
  return 'Novice';
};

const getSkillLevelClass = (percentage: number): string => {
  if (percentage >= 80) return 'text-primary';
  if (percentage >= 60) return 'text-info';
  if (percentage >= 40) return 'text-accent';
  if (percentage >= 20) return 'text-accent';
  return 'text-danger';
};

const getTopSkills = () => {
  return categoryStats.value
    .filter(s => s.percentage_yes >= 50 && s.category.toLowerCase() !== 'pokemon')
    .sort((a, b) => b.percentage_yes - a.percentage_yes)
    .slice(0, 3);
};

const getGrowthAreas = () => {
  return categoryStats.value
    .filter(s => s.percentage_yes < 50 && s.percentage_yes > 0 && s.category.toLowerCase() !== 'pokemon')
    .sort((a, b) => a.percentage_yes - b.percentage_yes)
    .slice(0, 3);
};

// Radar chart functions
const getRadarPoints = (): string => {
  if (categoryStats.value.length === 0) return '';
  
  const points = categoryStats.value.map((cat, index) => {
    const angle = (index * 2 * Math.PI / categoryStats.value.length) - Math.PI/2;
    const radius = (cat.percentage_yes / 100) * 150;
    const x = 190 + Math.cos(angle) * radius;
    const y = 190 + Math.sin(angle) * radius;
    return `${x},${y}`;
  });
  
  return points.join(' ');
};

const getRadarPointColor = (percentage: number): string => {
  if (isStiffMode.value) {
    // Apple-style colors
    if (percentage >= 80) return '#2563eb'; // blue-600
    if (percentage >= 60) return '#3b82f6'; // blue-500
    if (percentage >= 40) return '#60a5fa'; // blue-400
    if (percentage >= 20) return '#93bbfc'; // blue-300
    return '#dbeafe'; // blue-100
  } else {
    // Terminal-style colors
    if (percentage >= 80) return '#10b981'; // green-500
    if (percentage >= 60) return '#06b6d4'; // cyan-500  
    if (percentage >= 40) return '#f59e0b'; // amber-500
    if (percentage >= 20) return '#f97316'; // orange-500
    return '#ef4444'; // red-500
  }
};

const goBack = () => {
  router.push({ 
    name: 'Admin',
    query: isStiffMode.value ? { mode: 'stiff', tab: 'sessions' } : { tab: 'sessions' }
  });
};

// Handle print shortcut
const handlePrintShortcut = (event: KeyboardEvent) => {
  if ((event.ctrlKey || event.metaKey) && event.key === 'p') {
    console.log('Ctrl+P pressed');
    
    // If not already in stiff mode, refresh with stiff mode
    if (!isStiffMode.value) {
      event.preventDefault(); // Prevent print dialog
      
      // Refresh the page with stiff mode
      router.push({
        name: 'SessionStats',
        params: { sessionId: props.sessionId },
        query: { mode: 'stiff' }
      });
      
      // After navigation completes, trigger print
      setTimeout(() => {
        window.print();
      }, 500);
    }
    // If already in stiff mode, let normal print behavior continue
  }
};

// Lifecycle
onMounted(async () => {
  // Add print shortcut listener
  window.addEventListener('keydown', handlePrintShortcut);
  
  // Check authentication first
  const isAuthenticated = await requireAuth();
  if (!isAuthenticated) {
    // Redirect to admin login
    router.push({
      path: '/admin',
      query: isStiffMode.value ? { mode: 'stiff' } : {}
    });
    return;
  }
  
  // Load data if authenticated
  loadSessionData();
});

// Cleanup
onUnmounted(() => {
  window.removeEventListener('keydown', handlePrintShortcut);
});
</script>