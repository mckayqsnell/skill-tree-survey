<template>
  <div class="min-h-screen bg-black star-field">
    <!-- Auth Modal -->
    <div v-if="!authenticated" class="min-h-screen flex items-center justify-center px-4">
      <div class="max-w-md w-full">
        <div class="glass-card">
          <h2 class="text-xl font-bold mb-6 text-green-400" style="font-family: 'Orbitron', monospace;">ADMIN ACCESS</h2>
          <form @submit.prevent="handleAuthenticate">
            <div class="mb-6">
              <label for="password" class="block text-xs text-green-400/70 mb-2 font-mono uppercase">
                Password
              </label>
              <input
                id="password"
                v-model="passwordInput"
                type="password"
                required
                class="input-field"
                placeholder="Enter password"
                :class="{ 'border-red-500': authError }"
                :disabled="authLoading"
              />
              <p v-if="authError" class="text-red-500 text-xs mt-2">{{ authError }}</p>
            </div>
            <button type="submit" class="w-full btn-primary" :disabled="authLoading">
              <span v-if="!authLoading">Authenticate</span>
              <span v-else>Authenticating...</span>
            </button>
          </form>
        </div>
      </div>
    </div>

    <!-- Admin Panel -->
    <div v-else class="p-6">
      <!-- Header -->
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold text-green-400" style="font-family: 'Orbitron', monospace;">ADMIN PANEL</h1>
        <button 
          @click="handleLogout" 
          class="btn-secondary text-sm" 
          type="button"
          style="position: relative; z-index: 20;"
        >
          Logout
        </button>
      </div>

      <!-- Tabs -->
      <div class="flex gap-2 mb-6" style="position: relative; z-index: 10;">
        <button
          @click="switchTab('questions')"
          type="button"
          class="px-4 py-2 text-sm transition-all cursor-pointer"
          :class="activeTab === 'questions' ? 'bg-green-400/10 border border-green-400 text-green-400' : 'border border-green-400/30 text-green-400/60 hover:border-green-400/50 hover:text-green-400/80'"
        >
          Questions
        </button>
        <button
          @click="switchTab('sessions')"
          type="button"
          class="px-4 py-2 text-sm transition-all cursor-pointer"
          :class="activeTab === 'sessions' ? 'bg-green-400/10 border border-green-400 text-green-400' : 'border border-green-400/30 text-green-400/60 hover:border-green-400/50 hover:text-green-400/80'"
        >
          Sessions
        </button>
        <button
          @click="switchTab('analytics')"
          type="button"
          class="px-4 py-2 text-sm transition-all cursor-pointer"
          :class="activeTab === 'analytics' ? 'bg-green-400/10 border border-green-400 text-green-400' : 'border border-green-400/30 text-green-400/60 hover:border-green-400/50 hover:text-green-400/80'"
        >
          Analytics
        </button>
      </div>

      <!-- Content -->
      <div class="glass-card" style="position: relative; z-index: 5;">
        <!-- Questions Tab -->
        <div v-if="activeTab === 'questions'">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-lg text-green-400">Question Management</h2>
            <button @click="() => { parentQuestionId = null; newQuestionText = ''; newQuestionCategory = ''; showAddQuestion = true; }" class="btn-primary text-sm">
              Add Question
            </button>
          </div>

          <!-- Loading State -->
          <div v-if="loading" class="text-center py-8">
            <div class="inline-block w-8 h-8 border-2 border-green-400/30 border-t-green-400 rounded-full animate-spin"></div>
          </div>

          <!-- Question Tree -->
          <div v-else-if="questions.length > 0" class="space-y-4">
            <QuestionTreeItem
              v-for="question in questions"
              :key="question.id"
              :question="question"
              @edit="editQuestion"
              @delete="deleteQuestion"
              @add-child="addChildQuestion"
            />
          </div>

          <!-- Empty State -->
          <div v-else class="text-center py-8">
            <p class="text-green-400/50 text-sm">No questions found</p>
          </div>
        </div>

        <!-- Sessions Tab -->
        <div v-if="activeTab === 'sessions'">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-lg text-green-400">Recent Sessions</h2>
            <div class="flex items-center gap-4">
              <button
                @click="showDeleteAllConfirm = true"
                class="flex items-center gap-2 px-3 py-1 text-xs border border-red-500/50 text-red-500 hover:bg-red-500/10 hover:border-red-500 transition-all rounded"
                :disabled="sessions.length === 0"
              >
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                </svg>
                Clear All
              </button>
              <p class="text-xs text-green-400/50 font-mono">Click on a session to view detailed analysis</p>
            </div>
          </div>
          
          <!-- Loading State -->
          <div v-if="loading" class="text-center py-8">
            <div class="inline-block w-8 h-8 border-2 border-green-400/30 border-t-green-400 rounded-full animate-spin mb-2"></div>
            <p class="text-green-400/60 text-sm">Loading sessions...</p>
          </div>

          <!-- Sessions List -->
          <div v-else-if="sessions.length > 0" class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="border-b border-green-400/30 text-green-400/70">
                  <th class="text-left py-2 px-3">ID</th>
                  <th class="text-left py-2 px-3">User</th>
                  <th class="text-left py-2 px-3">Email</th>
                  <th class="text-left py-2 px-3">Company</th>
                  <th class="text-left py-2 px-3">Started</th>
                  <th class="text-left py-2 px-3">Status</th>
                  <th class="text-left py-2 px-3">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr 
                  v-for="session in sessions" 
                  :key="session.id" 
                  class="border-b border-green-400/10 hover:bg-green-400/5 transition-colors cursor-pointer group"
                  @click="viewSessionStats(session.id)"
                >
                  <td class="py-2 px-3 text-green-400/80 group-hover:text-green-400">{{ session.id }}</td>
                  <td class="py-2 px-3 text-green-400/80 group-hover:text-green-400">{{ session.user_name }}</td>
                  <td class="py-2 px-3 text-green-400/80 group-hover:text-green-400 font-mono text-xs">{{ session.user_email }}</td>
                  <td class="py-2 px-3 text-green-400/80 group-hover:text-green-400">{{ session.company }}</td>
                  <td class="py-2 px-3 text-green-400/80 group-hover:text-green-400 text-xs">{{ formatDate(session.started_at) }}</td>
                  <td class="py-2 px-3">
                    <span v-if="session.completed_at" class="flex items-center gap-1">
                      <svg class="w-3 h-3 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                      <span class="text-green-400 text-xs">Complete</span>
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
                        @click.stop="viewSessionStats(session.id)"
                        class="text-xs px-2 py-1 border border-cyan-400/30 text-cyan-400/80 hover:bg-cyan-400/10 hover:border-cyan-400 transition-all rounded"
                      >
                        View Stats
                      </button>
                      <button
                        @click.stop="confirmDeleteSession(session)"
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
            <p class="text-green-400/50 text-sm">No sessions found</p>
          </div>
        </div>

        <!-- Analytics Tab -->
        <div v-if="activeTab === 'analytics'">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-lg text-green-400">Analytics Overview</h2>
            <!-- API Health Status -->
            <div class="flex items-center gap-2">
              <div class="flex items-center gap-1">
                <div 
                  class="w-2 h-2 rounded-full"
                  :class="apiHealthy ? 'bg-green-400' : 'bg-red-500'"
                ></div>
                <span class="text-xs font-mono" :class="apiHealthy ? 'text-green-400' : 'text-red-500'">
                  API {{ apiHealthy ? 'CONNECTED' : 'DISCONNECTED' }}
                </span>
              </div>
            </div>
          </div>
          
          <!-- Loading State -->
          <div v-if="loading" class="text-center py-8">
            <div class="inline-block w-8 h-8 border-2 border-green-400/30 border-t-green-400 rounded-full animate-spin mb-2"></div>
            <p class="text-green-400/60 text-sm">Loading analytics...</p>
          </div>

          <!-- Analytics Data -->
          <div v-else-if="analytics" class="space-y-6">
            <!-- Main Stats Grid -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div class="bg-black/30 border border-green-400/20 p-4 text-center rounded">
                <p class="text-2xl font-bold text-cyan-400">{{ analytics.total_sessions }}</p>
                <p class="text-xs text-green-400/50 font-mono uppercase">Total Sessions</p>
              </div>
              <div class="bg-black/30 border border-green-400/20 p-4 text-center rounded">
                <p class="text-2xl font-bold text-green-400">{{ analytics.completed_sessions }}</p>
                <p class="text-xs text-green-400/50 font-mono uppercase">Completed</p>
              </div>
              <div class="bg-black/30 border border-red-400/20 p-4 text-center rounded">
                <p class="text-2xl font-bold text-red-400">{{ getInProgressSessions() }}</p>
                <p class="text-xs text-red-400/50 font-mono uppercase">In Progress</p>
              </div>
              <div class="bg-black/30 border border-amber-500/20 p-4 text-center rounded">
                <p class="text-2xl font-bold text-amber-500">{{ getCompletionRate() }}%</p>
                <p class="text-xs text-amber-500/50 font-mono uppercase">Completion Rate</p>
              </div>
            </div>

            <!-- Additional Stats -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- User Stats -->
              <div class="bg-black/30 border border-green-400/10 p-6 rounded">
                <h3 class="text-green-400 font-semibold mb-4">User Engagement</h3>
                <div class="space-y-3">
                  <div class="flex justify-between">
                    <span class="text-green-400/60 text-sm">Unique Users:</span>
                    <span class="text-green-400 font-mono">{{ getTotalUsers() }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-green-400/60 text-sm">Avg Sessions per User:</span>
                    <span class="text-cyan-400 font-mono">{{ getAvgSessionsPerUser() }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-green-400/60 text-sm">Est. Avg Duration:</span>
                    <span class="text-amber-500 font-mono">{{ getEstimatedAvgDuration() }}</span>
                  </div>
                </div>
              </div>

              <!-- Performance Stats -->
              <div class="bg-black/30 border border-green-400/10 p-6 rounded">
                <h3 class="text-green-400 font-semibold mb-4">System Performance</h3>
                <div class="space-y-3">
                  <div class="flex justify-between">
                    <span class="text-green-400/60 text-sm">API Response:</span>
                    <span class="text-green-400 font-mono">{{ apiResponseTime }}ms</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-green-400/60 text-sm">Success Rate:</span>
                    <span class="text-cyan-400 font-mono">{{ getSuccessRate() }}%</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-green-400/60 text-sm">Last Updated:</span>
                    <span class="text-amber-500 font-mono text-xs">{{ formatLastUpdate() }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Top Skills -->
            <div v-if="analytics.top_skills && analytics.top_skills.length > 0" class="bg-black/30 border border-green-400/10 p-6 rounded">
              <h3 class="text-green-400 font-semibold mb-4">Most Common Skills</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                <div 
                  v-for="skill in analytics.top_skills.slice(0, 6)"
                  :key="skill.skill"
                  class="flex justify-between items-center p-2 bg-black/20 rounded"
                >
                  <span class="text-green-400 text-sm">{{ skill.skill }}</span>
                  <span class="text-cyan-400 font-mono text-sm">{{ skill.count }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="mt-4 p-4 bg-red-500/10 border border-red-500/30">
        <p class="text-red-500 text-sm">{{ error }}</p>
      </div>
    </div>

    <!-- Add Question Modal -->
    <div v-if="showAddQuestion" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div class="glass-card max-w-md w-full">
        <h3 class="text-lg font-bold mb-4 text-green-400">Add New Question</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-xs text-green-400/70 mb-1 font-mono uppercase">Question Text</label>
            <input v-model="newQuestionText" type="text" class="input-field" placeholder="Enter question text..." />
          </div>
          <div>
            <label class="block text-xs text-green-400/70 mb-1 font-mono uppercase">Category (optional)</label>
            <input v-model="newQuestionCategory" type="text" class="input-field" placeholder="e.g. DevOps, Frontend..." />
          </div>
          <div class="flex gap-2">
            <button @click="createQuestion" class="btn-primary flex-1">Create</button>
            <button @click="showAddQuestion = false" class="btn-secondary flex-1">Cancel</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Question Modal -->
    <div v-if="showEditQuestion" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div class="glass-card max-w-md w-full">
        <h3 class="text-lg font-bold mb-4 text-green-400">Edit Question</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-xs text-green-400/70 mb-1 font-mono uppercase">Question Text</label>
            <input v-model="newQuestionText" type="text" class="input-field" placeholder="Enter question text..." />
          </div>
          <div>
            <label class="block text-xs text-green-400/70 mb-1 font-mono uppercase">Category (optional)</label>
            <input v-model="newQuestionCategory" type="text" class="input-field" placeholder="e.g. DevOps, Frontend..." />
          </div>
          <div class="flex gap-2">
            <button @click="saveEditQuestion" class="btn-primary flex-1">Save</button>
            <button @click="showEditQuestion = false" class="btn-secondary flex-1">Cancel</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Child Question Modal -->
    <div v-if="showAddChildQuestion" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div class="glass-card max-w-md w-full">
        <h3 class="text-lg font-bold mb-4 text-green-400">Add Child Question</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-xs text-green-400/70 mb-1 font-mono uppercase">Question Text</label>
            <input v-model="newQuestionText" type="text" class="input-field" placeholder="Enter question text..." />
          </div>
          <div>
            <label class="block text-xs text-green-400/70 mb-1 font-mono uppercase">Category (optional)</label>
            <input v-model="newQuestionCategory" type="text" class="input-field" placeholder="e.g. DevOps, Frontend..." />
          </div>
          <div class="flex gap-2">
            <button @click="createQuestion" class="btn-primary flex-1">Create</button>
            <button @click="showAddChildQuestion = false" class="btn-secondary flex-1">Cancel</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Session Confirmation Modal -->
    <div v-if="showDeleteConfirm" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div class="glass-card max-w-md w-full">
        <h3 class="text-lg font-bold mb-4 text-red-500">Delete Session</h3>
        <div class="space-y-4">
          <div v-if="sessionToDelete" class="p-4 bg-red-500/10 border border-red-500/20 rounded">
            <p class="text-sm text-green-400 mb-2">Are you sure you want to delete this session?</p>
            <div class="text-xs text-green-400/60 space-y-1">
              <p><strong>User:</strong> {{ sessionToDelete.user_name }}</p>
              <p><strong>Email:</strong> {{ sessionToDelete.user_email }}</p>
              <p><strong>Company:</strong> {{ sessionToDelete.company }}</p>
              <p><strong>Started:</strong> {{ formatDate(sessionToDelete.started_at) }}</p>
            </div>
          </div>
          <p class="text-xs text-red-500/80">This action cannot be undone. All responses and data for this session will be permanently deleted.</p>
          <div class="flex gap-2">
            <button @click="deleteSession" class="flex-1 px-4 py-2 bg-red-500/20 border border-red-500 text-red-500 hover:bg-red-500/30 transition-all rounded">
              Delete Session
            </button>
            <button @click="cancelDelete" class="btn-secondary flex-1">Cancel</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete All Sessions Confirmation Modal -->
    <div v-if="showDeleteAllConfirm" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div class="glass-card max-w-md w-full">
        <h3 class="text-lg font-bold mb-4 text-red-500">Clear All Sessions</h3>
        <div class="space-y-4">
          <div class="p-4 bg-red-500/10 border border-red-500/20 rounded">
            <p class="text-sm text-green-400 mb-2">Are you sure you want to delete ALL sessions?</p>
            <p class="text-xs text-green-400/60">
              This will permanently delete <strong>{{ sessions.length }} sessions</strong> and all associated data.
            </p>
          </div>
          <p class="text-xs text-red-500/80">This action cannot be undone. All user responses and session data will be permanently deleted.</p>
          <div class="flex gap-2">
            <button @click="deleteAllSessions" class="flex-1 px-4 py-2 bg-red-500/20 border border-red-500 text-red-500 hover:bg-red-500/30 transition-all rounded">
              Delete All Sessions
            </button>
            <button @click="cancelDelete" class="btn-secondary flex-1">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { questionsApi, sessionsApi } from '@/api';
import { logger } from '@/api/client';
import type { QuestionTree, Session, SessionAnalytics } from '@/types';
import QuestionTreeItem from '@/components/admin/QuestionTreeItem.vue';
import { useAdminAuth } from '@/composables/useAdminAuth';

// Router
const router = useRouter();

// Admin authentication
const { authenticated, authError, loading: authLoading, authenticate, logout, requireAuth, passwordInput } = useAdminAuth();

// State
const activeTab = ref<'questions' | 'sessions' | 'analytics'>('questions');
const loading = ref(false);
const error = ref('');

// API Health tracking
const apiHealthy = ref(true);
const apiResponseTime = ref(0);
const lastApiCheck = ref(new Date());

// Data
const questions = ref<QuestionTree[]>([]);
const sessions = ref<Session[]>([]);
const analytics = ref<SessionAnalytics | null>(null);
const showAddQuestion = ref(false);
const showEditQuestion = ref(false);
const showAddChildQuestion = ref(false);
const selectedQuestion = ref<QuestionTree | null>(null);
const parentQuestionId = ref<number | null>(null);
const newQuestionText = ref('');
const newQuestionCategory = ref('');

// Delete session state
const showDeleteConfirm = ref(false);
const showDeleteAllConfirm = ref(false);
const sessionToDelete = ref<Session | null>(null);

// Authentication
const handleAuthenticate = async () => {
  const success = await authenticate(passwordInput.value);
  if (success) {
    await loadData();
  }
};

// Tab switching
const switchTab = async (tab: 'questions' | 'sessions' | 'analytics') => {
  // Only switch if different from current tab
  if (activeTab.value === tab) {
    return;
  }
  
  if (import.meta.env.DEV) {
    logger.info(`Switching to ${tab} tab`);
  }
  activeTab.value = tab;
  // Clear any existing errors when switching tabs
  error.value = '';
  // Load data for the new tab
  await loadData();
};

// Clear data on logout 
const handleLogout = () => {
  // Reset all data
  questions.value = [];
  sessions.value = [];
  analytics.value = null;
  error.value = '';
  loading.value = false;
  activeTab.value = 'questions';
  
  logout();
};

// Load data based on active tab
const loadData = async () => {
  // Don't load if not authenticated
  if (!authenticated.value) return;
  
  try {
    loading.value = true;
    error.value = '';
    
    const startTime = performance.now();
    
    switch (activeTab.value) {
      case 'questions':
        await loadQuestions();
        break;
      case 'sessions':
        await loadSessions();
        break;
      case 'analytics':
        await loadAnalytics();
        break;
    }
    
    // Update API health metrics
    const endTime = performance.now();
    apiResponseTime.value = Math.round(endTime - startTime);
    apiHealthy.value = true;
    lastApiCheck.value = new Date();
    
  } catch (err: any) {
    logger.error(`Failed to load ${activeTab.value}`, err);
    error.value = err.message || `Failed to load ${activeTab.value}`;
    apiHealthy.value = false;
    lastApiCheck.value = new Date();
  } finally {
    loading.value = false;
  }
};

// Load questions
const loadQuestions = async () => {
  const data = await questionsApi.getAllQuestions();
  questions.value = data;
  if (import.meta.env.DEV) {
    logger.info(`Loaded ${data.length} question trees`);
  }
};

// Load sessions
const loadSessions = async () => {
  const data = await sessionsApi.getAllSessions(0, 50);
  sessions.value = data;
  if (import.meta.env.DEV) {
    logger.info(`Loaded ${data.length} sessions`);
  }
};

// Load analytics
const loadAnalytics = async () => {
  const data = await sessionsApi.getAnalytics();
  analytics.value = data;
  if (import.meta.env.DEV) {
    logger.info('Loaded analytics data');
  }
};

// Question operations
const editQuestion = (question: QuestionTree) => {
  if (import.meta.env.DEV) {
    logger.info('Editing question', { id: question.id });
  }
  selectedQuestion.value = question;
  newQuestionText.value = question.text;
  newQuestionCategory.value = question.category || '';
  showEditQuestion.value = true;
};

const saveEditQuestion = async () => {
  if (!selectedQuestion.value || !newQuestionText.value.trim()) return;
  
  try {
    await questionsApi.updateQuestion(selectedQuestion.value.id, {
      text: newQuestionText.value,
      category: newQuestionCategory.value || null
    });
    if (import.meta.env.DEV) {
      logger.info('Question updated');
    }
    showEditQuestion.value = false;
    await loadQuestions();
  } catch (err: any) {
    logger.error('Failed to update question', err);
    error.value = err.message || 'Failed to update question';
  }
};

const deleteQuestion = async (questionId: number) => {
  if (!confirm('Are you sure you want to delete this question and all its children?')) {
    return;
  }
  
  try {
    await questionsApi.deleteQuestion(questionId);
    if (import.meta.env.DEV) {
      logger.info(`Question ${questionId} deleted`);
    }
    await loadQuestions();
  } catch (err: any) {
    logger.error('Failed to delete question', err);
    error.value = err.message || 'Failed to delete question';
  }
};

const addChildQuestion = (parentId: number) => {
  if (import.meta.env.DEV) {
    logger.info('Adding child question', { parentId });
  }
  parentQuestionId.value = parentId;
  newQuestionText.value = '';
  newQuestionCategory.value = '';
  showAddChildQuestion.value = true;
};

const createQuestion = async () => {
  if (!newQuestionText.value.trim()) return;
  
  try {
    await questionsApi.createQuestion({
      text: newQuestionText.value,
      parent_id: parentQuestionId.value,
      is_base: parentQuestionId.value === null,
      category: newQuestionCategory.value || null
    });
    if (import.meta.env.DEV) {
      logger.info('Question created');
    }
    showAddQuestion.value = false;
    showAddChildQuestion.value = false;
    await loadQuestions();
  } catch (err: any) {
    logger.error('Failed to create question', err);
    error.value = err.message || 'Failed to create question';
  }
};

// Format date
const formatDate = (dateStr: string): string => {
  try {
    const date = new Date(dateStr);
    return date.toLocaleDateString();
  } catch {
    return dateStr;
  }
};

// Analytics helper functions
const getInProgressSessions = (): number => {
  if (!analytics.value || typeof analytics.value.total_sessions !== 'number' || typeof analytics.value.completed_sessions !== 'number') {
    return 0;
  }
  return Math.max(0, analytics.value.total_sessions - analytics.value.completed_sessions);
};

const getCompletionRate = (): number => {
  if (!analytics.value || typeof analytics.value.completion_rate !== 'number' || isNaN(analytics.value.completion_rate)) {
    return 0;
  }
  return Math.round(analytics.value.completion_rate);
};

const getTotalUsers = (): string => {
  if (!analytics.value || typeof analytics.value.total_users !== 'number' || analytics.value.total_users === 0) {
    return '0';
  }
  return analytics.value.total_users.toString();
};

const getAvgSessionsPerUser = (): string => {
  if (!analytics.value || 
      typeof analytics.value.total_sessions !== 'number' || 
      typeof analytics.value.total_users !== 'number' || 
      analytics.value.total_users === 0) {
    return '0.0';
  }
  const avg = analytics.value.total_sessions / analytics.value.total_users;
  return isNaN(avg) ? '0.0' : avg.toFixed(1);
};

const getEstimatedAvgDuration = (): string => {
  if (!analytics.value || typeof analytics.value.completed_sessions !== 'number' || analytics.value.completed_sessions === 0) {
    return '< 1 min';
  }
  return '7-10 min';
};

const getSuccessRate = (): number => {
  if (!analytics.value || typeof analytics.value.completion_rate !== 'number' || isNaN(analytics.value.completion_rate)) {
    return 0;
  }
  return Math.round(analytics.value.completion_rate);
};

const formatLastUpdate = (): string => {
  try {
    return lastApiCheck.value.toLocaleTimeString();
  } catch {
    return 'Unknown';
  }
};

// Session deletion
const confirmDeleteSession = (session: Session) => {
  sessionToDelete.value = session;
  showDeleteConfirm.value = true;
};

const deleteSession = async () => {
  if (!sessionToDelete.value) return;
  
  try {
    await sessionsApi.deleteSession(sessionToDelete.value.id);
    if (import.meta.env.DEV) {
      logger.info(`Session ${sessionToDelete.value.id} deleted`);
    }
    showDeleteConfirm.value = false;
    sessionToDelete.value = null;
    await loadSessions(); // Reload the sessions list
  } catch (err: any) {
    logger.error('Failed to delete session', err);
    error.value = err.message || 'Failed to delete session';
  }
};

const deleteAllSessions = async () => {
  try {
    // Delete all sessions one by one
    const deletePromises = sessions.value.map(session => 
      sessionsApi.deleteSession(session.id)
    );
    
    await Promise.all(deletePromises);
    
    if (import.meta.env.DEV) {
      logger.info(`Deleted ${sessions.value.length} sessions`);
    }
    
    showDeleteAllConfirm.value = false;
    await loadSessions(); // Reload the sessions list
  } catch (err: any) {
    logger.error('Failed to delete all sessions', err);
    error.value = err.message || 'Failed to delete sessions';
  }
};

const cancelDelete = () => {
  showDeleteConfirm.value = false;
  showDeleteAllConfirm.value = false;
  sessionToDelete.value = null;
};

// Navigation
const viewSessionStats = (sessionId: number) => {
  if (import.meta.env.DEV) {
    logger.info('Navigating to session stats', { sessionId });
  }
  router.push({
    name: 'SessionStats',
    params: { sessionId: sessionId.toString() }
  });
};

// Watch tab changes - removed since we're calling loadData directly in switchTab


// Lifecycle
onMounted(async () => {
  // Check if already authenticated
  const isAuthenticated = await requireAuth();
  if (isAuthenticated) {
    await loadData();
  }
});
</script>