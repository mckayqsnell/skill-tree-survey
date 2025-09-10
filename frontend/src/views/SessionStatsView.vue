<template>
  <div class="min-h-screen bg-black star-field">
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
          <h1 class="text-2xl font-bold text-green-400" style="font-family: 'Orbitron', monospace;">
            SESSION ANALYSIS
          </h1>
        </div>
        <div class="text-right">
          <p class="text-xs text-green-400/50 font-mono">Session ID: {{ sessionId }}</p>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="glass-card text-center">
        <div class="inline-block w-8 h-8 border-2 border-green-400/30 border-t-green-400 rounded-full animate-spin mb-4"></div>
        <p class="text-green-400/60 font-mono text-sm">Loading session data...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="glass-card">
        <div class="text-center mb-4">
          <svg class="w-12 h-12 text-red-500 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <p class="text-red-500 font-mono text-sm mb-2">{{ error }}</p>
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
            <h2 class="text-lg text-green-400" style="font-family: 'Orbitron', monospace;">USER PROFILE</h2>
            <div class="flex items-center gap-2">
              <div v-if="summary.is_completed" class="flex items-center gap-1">
                <svg class="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span class="text-xs text-green-400 font-mono">COMPLETED</span>
              </div>
              <div v-else class="flex items-center gap-1">
                <svg class="w-4 h-4 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span class="text-xs text-amber-500 font-mono">IN PROGRESS</span>
              </div>
            </div>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="space-y-2">
              <p class="text-xs text-green-400/50 font-mono uppercase">Name</p>
              <p class="text-green-400 font-semibold">{{ summary.user_name }}</p>
            </div>
            <div class="space-y-2">
              <p class="text-xs text-green-400/50 font-mono uppercase">Email</p>
              <p class="text-green-400 font-mono text-sm">{{ summary.user_email }}</p>
            </div>
            <div class="space-y-2">
              <p class="text-xs text-green-400/50 font-mono uppercase">Company</p>
              <p class="text-green-400 font-semibold">{{ summary.company }}</p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6 pt-4 border-t border-green-400/20">
            <div class="space-y-2">
              <p class="text-xs text-green-400/50 font-mono uppercase">Started</p>
              <p class="text-green-400/80 text-sm">{{ formatDate(summary.started_at) }}</p>
            </div>
            <div class="space-y-2">
              <p class="text-xs text-green-400/50 font-mono uppercase">Duration</p>
              <p class="text-cyan-400 font-semibold">
                <span v-if="summary.completion_time_minutes">{{ Math.round(summary.completion_time_minutes) }} min</span>
                <span v-else-if="!summary.is_completed">{{ getElapsedTime() }}</span>
                <span v-else>< 1 min</span>
              </p>
            </div>
            <div class="space-y-2">
              <p class="text-xs text-green-400/50 font-mono uppercase">Progress</p>
              <p class="text-amber-500 font-semibold">{{ getCompletionStatus() }}</p>
            </div>
          </div>
        </div>

        <!-- Stats Overview -->
        <div class="glass-card">
          <h2 class="text-lg text-green-400 mb-6" style="font-family: 'Orbitron', monospace;">PERFORMANCE METRICS</h2>
          
          <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div class="text-center bg-black/30 border border-green-400/20 p-4 rounded group relative">
              <p class="text-3xl font-bold text-green-400 mb-1">{{ summary.total_responses }}</p>
              <div class="flex items-center justify-center gap-1">
                <p class="text-xs text-green-400/50 font-mono uppercase">Total Questions</p>
                <svg class="w-3 h-3 text-green-400/40 cursor-help" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <!-- Tooltip -->
              <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-black border border-green-400/30 text-xs text-green-400 rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10">
                Number of questions answered in this session
              </div>
            </div>
            
            <div class="text-center bg-black/30 border border-cyan-400/20 p-4 rounded group relative">
              <p class="text-3xl font-bold text-cyan-400 mb-1">{{ summary.yes_responses }}</p>
              <div class="flex items-center justify-center gap-1">
                <p class="text-xs text-cyan-400/50 font-mono uppercase">Skills Confirmed</p>
                <svg class="w-3 h-3 text-cyan-400/40 cursor-help" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <!-- Tooltip -->
              <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-black border border-cyan-400/30 text-xs text-cyan-400 rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10">
                Number of "YES" answers - skills the user has
              </div>
            </div>
            
            <div class="text-center bg-black/30 border border-red-400/20 p-4 rounded group relative">
              <p class="text-3xl font-bold text-red-400 mb-1">{{ summary.no_responses }}</p>
              <div class="flex items-center justify-center gap-1">
                <p class="text-xs text-red-400/50 font-mono uppercase">Skills Declined</p>
                <svg class="w-3 h-3 text-red-400/40 cursor-help" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <!-- Tooltip -->
              <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-black border border-red-400/30 text-xs text-red-400 rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10">
                Number of "NO" answers - areas for potential growth
              </div>
            </div>
            
            <div class="text-center bg-black/30 border border-amber-500/20 p-4 rounded group relative">
              <p class="text-3xl font-bold text-amber-500 mb-1">{{ getConfidenceScore() }}%</p>
              <div class="flex items-center justify-center gap-1">
                <p class="text-xs text-amber-500/50 font-mono uppercase">Confidence Score</p>
                <svg class="w-3 h-3 text-amber-500/40 cursor-help" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <!-- Tooltip -->
              <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-black border border-amber-500/30 text-xs text-amber-500 rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10">
                Percentage of questions answered "YES" - overall skill confidence level
              </div>
            </div>
          </div>
        </div>

        <!-- No Category Data Message -->
        <div v-if="categoryStats.length === 0 && summary" class="glass-card">
          <h2 class="text-lg text-green-400 mb-4" style="font-family: 'Orbitron', monospace;">SKILL PROFILE</h2>
          <div class="text-center py-8">
            <svg class="w-16 h-16 text-amber-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
            </svg>
            <p class="text-amber-500/80 mb-2">No category data available</p>
            <p class="text-xs text-green-400/60 font-mono">
              This session may not have category-specific questions or the data hasn't been processed yet.
            </p>
            <div class="mt-4 p-4 bg-amber-500/10 border border-amber-500/20 rounded">
              <p class="text-sm text-amber-500/80">
                {{ summary.total_responses }} total responses recorded
              </p>
            </div>
          </div>
        </div>

        <!-- Skill Radar Chart -->
        <div v-else-if="categoryStats.length > 0" class="glass-card">
          <h2 class="text-lg text-green-400 mb-6" style="font-family: 'Orbitron', monospace;">SKILL PROFILE</h2>
          
          <div class="flex flex-col lg:flex-row gap-8 items-center">
            <!-- Radar Chart -->
            <div class="flex-shrink-0">
              <div class="relative w-96 h-96 mx-auto p-4">
                <svg width="384" height="384" viewBox="0 0 384 384" class="transform">
                  <!-- Background Grid -->
                  <g class="opacity-20">
                    <!-- Concentric circles -->
                    <circle cx="192" cy="192" r="50" fill="none" stroke="rgba(0, 255, 65, 0.3)" stroke-width="1"/>
                    <circle cx="192" cy="192" r="100" fill="none" stroke="rgba(0, 255, 65, 0.3)" stroke-width="1"/>
                    <circle cx="192" cy="192" r="150" fill="none" stroke="rgba(0, 255, 65, 0.3)" stroke-width="1"/>
                    
                    <!-- Radial lines -->
                    <g v-for="(_, index) in categoryStats" :key="`line-${index}`">
                      <line 
                        x1="192" 
                        y1="192" 
                        :x2="192 + Math.cos((index * 2 * Math.PI / categoryStats.length) - Math.PI/2) * 150"
                        :y2="192 + Math.sin((index * 2 * Math.PI / categoryStats.length) - Math.PI/2) * 150"
                        stroke="rgba(0, 255, 65, 0.3)" 
                        stroke-width="1"
                      />
                    </g>
                  </g>
                  
                  <!-- Data Polygon -->
                  <polygon 
                    :points="getRadarPoints()" 
                    fill="rgba(6, 182, 212, 0.2)" 
                    stroke="rgba(6, 182, 212, 0.8)" 
                    stroke-width="2"
                  />
                  
                  <!-- Data Points -->
                  <g v-for="(cat, index) in categoryStats" :key="`point-${index}`">
                    <circle 
                      :cx="192 + Math.cos((index * 2 * Math.PI / categoryStats.length) - Math.PI/2) * (cat.percentage_yes / 100 * 150)"
                      :cy="192 + Math.sin((index * 2 * Math.PI / categoryStats.length) - Math.PI/2) * (cat.percentage_yes / 100 * 150)"
                      r="5" 
                      :fill="getRadarPointColor(cat.percentage_yes)"
                      stroke="white" 
                      stroke-width="2"
                    />
                  </g>
                  
                  <!-- Category Labels -->
                  <g v-for="(cat, index) in categoryStats" :key="`label-${index}`">
                    <text 
                      :x="192 + Math.cos((index * 2 * Math.PI / categoryStats.length) - Math.PI/2) * 175"
                      :y="192 + Math.sin((index * 2 * Math.PI / categoryStats.length) - Math.PI/2) * 175 - 2"
                      text-anchor="middle"
                      dominant-baseline="middle"
                      class="fill-green-400 text-xs font-mono font-semibold"
                      style="font-size: 10px;"
                    >
                      {{ cat.category }}
                    </text>
                    <text 
                      :x="192 + Math.cos((index * 2 * Math.PI / categoryStats.length) - Math.PI/2) * 175"
                      :y="192 + Math.sin((index * 2 * Math.PI / categoryStats.length) - Math.PI/2) * 175 + 10"
                      text-anchor="middle"
                      dominant-baseline="middle"
                      class="fill-cyan-400 text-xs font-mono font-bold"
                      style="font-size: 9px;"
                    >
                      {{ Math.round(cat.percentage_yes) }}%
                    </text>
                  </g>
                  
                  <!-- Center Dot -->
                  <circle cx="192" cy="192" r="3" fill="rgba(0, 255, 65, 0.8)"/>
                  
                  <!-- Percentage Scale Labels -->
                  <g class="opacity-60">
                    <text x="197" y="147" class="fill-green-400 text-xs font-mono" style="font-size: 8px;" text-anchor="start">25%</text>
                    <text x="197" y="97" class="fill-green-400 text-xs font-mono" style="font-size: 8px;" text-anchor="start">50%</text>
                    <text x="197" y="47" class="fill-green-400 text-xs font-mono" style="font-size: 8px;" text-anchor="start">75%</text>
                  </g>
                </svg>
              </div>
            </div>
            
            <!-- Legend & Stats -->
            <div class="flex-1 space-y-4 min-w-0">
              <div class="grid grid-cols-1 gap-3">
                <div 
                  v-for="cat in categoryStats"
                  :key="cat.category"
                  class="flex items-center justify-between p-3 bg-black/30 border border-green-400/10 rounded"
                >
                  <div class="flex items-center gap-3">
                    <div 
                      class="w-3 h-3 rounded-full"
                      :style="{ backgroundColor: getRadarPointColor(cat.percentage_yes) }"
                    ></div>
                    <div>
                      <h3 class="text-green-400 font-semibold text-sm">{{ cat.category }}</h3>
                      <p class="text-xs text-green-400/60 font-mono">
                        {{ cat.yes_count }}/{{ cat.total_questions }}
                      </p>
                    </div>
                  </div>
                  <div class="text-right">
                    <p class="text-lg font-bold text-cyan-400">{{ Math.round(cat.percentage_yes) }}%</p>
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
          <h2 class="text-lg text-green-400 mb-4" style="font-family: 'Orbitron', monospace;">SKILL ASSESSMENT</h2>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Strongest Skills -->
            <div>
              <h3 class="text-sm text-cyan-400/80 font-mono uppercase mb-3">Strongest Areas</h3>
              <div class="space-y-2">
                <div 
                  v-for="skill in getTopSkills()"
                  :key="skill.category"
                  class="flex items-center justify-between p-2 bg-green-400/5 rounded"
                >
                  <span class="text-green-400 text-sm">{{ skill.category }}</span>
                  <span class="text-cyan-400 font-semibold text-sm">{{ Math.round(skill.percentage_yes) }}%</span>
                </div>
              </div>
            </div>
            
            <!-- Growth Areas -->
            <div>
              <h3 class="text-sm text-amber-500/80 font-mono uppercase mb-3">Growth Opportunities</h3>
              <div class="space-y-2">
                <div 
                  v-for="skill in getGrowthAreas()"
                  :key="skill.category"
                  class="flex items-center justify-between p-2 bg-amber-500/5 rounded"
                >
                  <span class="text-green-400 text-sm">{{ skill.category }}</span>
                  <span class="text-amber-500 font-semibold text-sm">{{ Math.round(skill.percentage_yes) }}%</span>
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
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { sessionsApi, responsesApi, questionsApi } from '@/api';
import { logger } from '@/api/client';
import type { SessionSummary, CategoryStatistics } from '@/types';
import { useAdminAuth } from '@/composables/useAdminAuth';

// Props
const props = defineProps<{
  sessionId: string
}>();

const router = useRouter();

// Admin authentication
const { requireAuth } = useAdminAuth();

// State
const loading = ref(true);
const error = ref('');
const summary = ref<SessionSummary | null>(null);
const categoryStats = ref<CategoryStatistics[]>([]);

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
      
      // Get both response stats and all questions to calculate proper totals
      const [stats, allQuestions] = await Promise.all([
        responsesApi.getCategoryStatistics(Number(props.sessionId)),
        questionsApi.getAllQuestions()
      ]);
      
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
      
      categoryStats.value = allCategoryStats
        .sort((a, b) => b.percentage_yes - a.percentage_yes);
      
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
  if (percentage >= 80) return 'text-green-400';
  if (percentage >= 60) return 'text-cyan-400';
  if (percentage >= 40) return 'text-amber-400';
  if (percentage >= 20) return 'text-orange-400';
  return 'text-red-400';
};

const getTopSkills = () => {
  return categoryStats.value
    .filter(s => s.percentage_yes >= 50)
    .sort((a, b) => b.percentage_yes - a.percentage_yes)
    .slice(0, 3);
};

const getGrowthAreas = () => {
  return categoryStats.value
    .filter(s => s.percentage_yes < 50 && s.percentage_yes > 0)
    .sort((a, b) => a.percentage_yes - b.percentage_yes)
    .slice(0, 3);
};

// Radar chart functions
const getRadarPoints = (): string => {
  if (categoryStats.value.length === 0) return '';
  
  const points = categoryStats.value.map((cat, index) => {
    const angle = (index * 2 * Math.PI / categoryStats.value.length) - Math.PI/2;
    const radius = (cat.percentage_yes / 100) * 150;
    const x = 192 + Math.cos(angle) * radius;
    const y = 192 + Math.sin(angle) * radius;
    return `${x},${y}`;
  });
  
  return points.join(' ');
};

const getRadarPointColor = (percentage: number): string => {
  if (percentage >= 80) return '#10b981'; // green-500
  if (percentage >= 60) return '#06b6d4'; // cyan-500  
  if (percentage >= 40) return '#f59e0b'; // amber-500
  if (percentage >= 20) return '#f97316'; // orange-500
  return '#ef4444'; // red-500
};

const goBack = () => {
  router.push({ name: 'Admin' });
};

// Lifecycle
onMounted(async () => {
  // Check authentication first
  const isAuthenticated = await requireAuth();
  if (!isAuthenticated) {
    // Redirect to admin login
    router.push('/admin');
    return;
  }
  
  // Load data if authenticated
  loadSessionData();
});
</script>