<template>
  <div class="min-h-screen bg-black star-field">
    <!-- Auth Modal -->
    <div v-if="!authenticated" class="min-h-screen flex items-center justify-center px-4">
      <div class="max-w-md w-full">
        <div class="glass-card">
          <h2 class="text-xl font-bold mb-6 text-green-400" style="font-family: 'Orbitron', monospace;">ADMIN ACCESS</h2>
          <form @submit.prevent="authenticate">
            <div class="mb-6">
              <label for="password" class="block text-xs text-green-400/70 mb-2 font-mono uppercase">
                Password
              </label>
              <input
                id="password"
                v-model="password"
                type="password"
                required
                class="input-field"
                placeholder="Enter password"
                :class="{ 'border-red-500': authError }"
              />
              <p v-if="authError" class="text-red-500 text-xs mt-2">{{ authError }}</p>
            </div>
            <button type="submit" class="w-full btn-primary">
              Authenticate
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
          @click="handleTabSwitch('questions')"
          type="button"
          class="px-4 py-2 text-sm transition-all cursor-pointer"
          :class="activeTab === 'questions' ? 'bg-green-400/10 border border-green-400 text-green-400' : 'border border-green-400/30 text-green-400/60 hover:border-green-400/50 hover:text-green-400/80'"
        >
          Questions
        </button>
        <button
          @click="handleTabSwitch('sessions')"
          type="button"
          class="px-4 py-2 text-sm transition-all cursor-pointer"
          :class="activeTab === 'sessions' ? 'bg-green-400/10 border border-green-400 text-green-400' : 'border border-green-400/30 text-green-400/60 hover:border-green-400/50 hover:text-green-400/80'"
        >
          Sessions
        </button>
        <button
          @click="handleTabSwitch('analytics')"
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
          <h2 class="text-lg text-green-400 mb-6">Recent Sessions</h2>
          
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
                </tr>
              </thead>
              <tbody>
                <tr v-for="session in sessions" :key="session.id" class="border-b border-green-400/10">
                  <td class="py-2 px-3 text-green-400/80">{{ session.id }}</td>
                  <td class="py-2 px-3 text-green-400/80">{{ session.user_name }}</td>
                  <td class="py-2 px-3 text-green-400/80">{{ session.user_email }}</td>
                  <td class="py-2 px-3 text-green-400/80">{{ session.company }}</td>
                  <td class="py-2 px-3 text-green-400/80">{{ formatDate(session.started_at) }}</td>
                  <td class="py-2 px-3">
                    <span v-if="session.completed_at" class="text-green-400">Complete</span>
                    <span v-else class="text-amber-500">Active</span>
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
          <h2 class="text-lg text-green-400 mb-6">Analytics Overview</h2>
          
          <!-- Loading State -->
          <div v-if="loading" class="text-center py-8">
            <div class="inline-block w-8 h-8 border-2 border-green-400/30 border-t-green-400 rounded-full animate-spin mb-2"></div>
            <p class="text-green-400/60 text-sm">Loading analytics...</p>
          </div>

          <!-- Analytics Data -->
          <div v-else-if="analytics" class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="bg-black/30 border border-green-400/20 p-4 text-center">
              <p class="text-2xl font-bold text-cyan-400">{{ analytics.total_sessions }}</p>
              <p class="text-xs text-green-400/50">Total Sessions</p>
            </div>
            <div class="bg-black/30 border border-green-400/20 p-4 text-center">
              <p class="text-2xl font-bold text-green-400">{{ analytics.completed_sessions }}</p>
              <p class="text-xs text-green-400/50">Completed</p>
            </div>
            <div class="bg-black/30 border border-green-400/20 p-4 text-center">
              <p class="text-2xl font-bold text-amber-500">{{ isNaN(analytics.completion_rate) ? 0 : Math.round(analytics.completion_rate) }}%</p>
              <p class="text-xs text-green-400/50">Completion Rate</p>
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { questionsApi, sessionsApi, adminClient } from '@/api';
import { logger } from '@/api/client';
import type { QuestionTree, Session, SessionAnalytics } from '@/types';
import QuestionTreeItem from '@/components/admin/QuestionTreeItem.vue';

// Router
const router = useRouter();

// State
const authenticated = ref(false);
const password = ref('');
const authError = ref('');
const activeTab = ref<'questions' | 'sessions' | 'analytics'>('questions');
const loading = ref(false);
const error = ref('');

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

// Authentication
const authenticate = async () => {
  try {
    authError.value = '';
    
    // Update admin client with password
    adminClient.defaults.headers['X-Admin-Password'] = password.value;
    
    // Test authentication by fetching sessions (admin-protected endpoint)
    await sessionsApi.getAllSessions(0, 1); // Fetch just 1 session to test auth
    
    // Success
    authenticated.value = true;
    sessionStorage.setItem('adminPassword', password.value);
    if (import.meta.env.DEV) {
      logger.info('Admin authenticated successfully');
    }
    
    // Load initial data
    await loadData();
    
    // Ensure button functionality after authentication
    ensureButtonFunctionality();
  } catch (err: any) {
    logger.error('Authentication failed', err);
    authError.value = 'Invalid password';
    password.value = '';
    // Clear the invalid password from admin client
    adminClient.defaults.headers['X-Admin-Password'] = '';
  }
};

// Tab switching handler
const handleTabSwitch = (tab: 'questions' | 'sessions' | 'analytics') => {
  switchTab(tab);
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

// Logout handler
const handleLogout = () => {
  logout();
};

// Logout
const logout = () => {
  if (import.meta.env.DEV) {
    logger.info('Admin logging out');
  }
  
  try {
    // Clear all state
    authenticated.value = false;
    password.value = '';
    authError.value = '';
    sessionStorage.removeItem('adminPassword');
    adminClient.defaults.headers['X-Admin-Password'] = '';
    // Reset all data
    questions.value = [];
    sessions.value = [];
    analytics.value = null;
    error.value = '';
    loading.value = false;
    // Reset to questions tab
    activeTab.value = 'questions';
    
    // Navigate back to home page
    router.push('/');
  } catch (err) {
    logger.error('Error during logout', err);
  }
};

// Load data based on active tab
const loadData = async () => {
  // Don't load if not authenticated
  if (!authenticated.value) return;
  
  try {
    loading.value = true;
    error.value = '';
    
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
  } catch (err: any) {
    logger.error(`Failed to load ${activeTab.value}`, err);
    error.value = err.message || `Failed to load ${activeTab.value}`;
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

// Watch tab changes - removed since we're calling loadData directly in switchTab

// Ensure button functionality after render
const ensureButtonFunctionality = () => {
  // Only in development mode for fallback click handling
  if (import.meta.env.DEV) {
    setTimeout(() => {
      const buttons = document.querySelectorAll('button');
      const navButtons = ['Logout', 'Sessions', 'Analytics', 'Questions'];
      
      buttons.forEach((btn) => {
        const text = btn.textContent?.trim();
        // Add fallback listeners only for navigation buttons
        if (text && navButtons.includes(text)) {
          btn.removeEventListener('click', () => {});
          btn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            if (text === 'Logout') {
              handleLogout();
            } else if (text === 'Sessions') {
              handleTabSwitch('sessions');
            } else if (text === 'Analytics') {
              handleTabSwitch('analytics');
            } else if (text === 'Questions') {
              handleTabSwitch('questions');
            }
          });
        }
      });
    }, 500);
  }
};

// Watch for authentication changes
watch(authenticated, async (newVal) => {
  if (newVal) {
    await nextTick();
    ensureButtonFunctionality();
  }
});

// Lifecycle
onMounted(async () => {
  // Clear any existing auth on mount to force re-authentication
  authenticated.value = false;
  sessionStorage.removeItem('adminPassword');
  adminClient.defaults.headers['X-Admin-Password'] = '';
  password.value = '';
  
  // Ensure button functionality
  ensureButtonFunctionality();
});
</script>