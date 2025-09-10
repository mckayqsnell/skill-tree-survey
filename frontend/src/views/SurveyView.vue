<template>
  <div class="min-h-screen bg-black star-field flex flex-col">
    <!-- Progress Bar -->
    <div class="w-full px-4 pt-4">
      <div class="max-w-3xl mx-auto">
        <div class="h-2 bg-green-400/10 rounded-full overflow-hidden">
          <div 
            class="h-full bg-gradient-to-r from-green-400 to-cyan-400 transition-all duration-500 rounded-full"
            :style="{ width: `${progressPercentage}%` }"
          />
        </div>
        <p class="text-xs text-green-400/50 font-mono mt-2 text-center">
          Progress: {{ Math.round(progressPercentage) }}%
        </p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex items-center justify-center px-4">
      <div v-if="loading" class="text-center">
        <div class="inline-block w-8 h-8 border-2 border-green-400/30 border-t-green-400 rounded-full animate-spin mb-4"></div>
        <p class="text-green-400/60 font-mono text-sm">Loading questions...</p>
      </div>

      <div v-else-if="error" class="text-center max-w-md">
        <div class="glass-card">
          <p class="text-red-500 mb-4 font-mono text-sm">{{ error }}</p>
          <button @click="retryLoad" class="btn-secondary">Retry</button>
        </div>
      </div>

      <div v-else-if="currentQuestion" class="w-full max-w-3xl">
        <!-- Category Display -->
        <div class="text-center mb-6">
          <p v-if="currentQuestion.category" class="text-sm text-green-400/60 font-mono">
            {{ currentQuestion.category }}
          </p>
        </div>

        <!-- Question Card -->
        <div 
          class="glass-card text-center"
          :key="currentQuestion.id"
          :class="{ 'scale-95': animating }"
        >
          <h2 class="text-2xl md:text-3xl font-semibold mb-8 text-green-400">
            {{ currentQuestion.text }}
          </h2>

          <!-- Response Buttons -->
          <div class="flex justify-center gap-6">
            <button
              @click="handleAnswer(true)"
              class="flex flex-col items-center gap-2 px-8 py-4 bg-black/50 border border-green-400/50 hover:bg-green-400/10 hover:border-green-400 transition-all"
              :class="{ 'scale-105 bg-green-400/10': lastKey === 'yes' }"
            >
              <span class="text-green-400 text-xl font-bold">YES</span>
              <div class="flex gap-1 text-xs">
                <kbd class="px-2 py-0.5 bg-green-400/10 border border-green-400/30 text-green-400/60">Space</kbd>
                <kbd class="px-2 py-0.5 bg-green-400/10 border border-green-400/30 text-green-400/60">Enter</kbd>
              </div>
            </button>

            <button
              @click="handleAnswer(false)"
              class="flex flex-col items-center gap-2 px-8 py-4 bg-black/50 border border-red-500/50 hover:bg-red-500/10 hover:border-red-500 transition-all"
              :class="{ 'scale-105 bg-red-500/10': lastKey === 'no' }"
            >
              <span class="text-red-500 text-xl font-bold">NO</span>
              <kbd class="px-2 py-0.5 bg-red-500/10 border border-red-500/30 text-red-500/60 text-xs">N</kbd>
            </button>
          </div>
        </div>
      </div>

      <div v-else class="text-center">
        <p class="text-green-400/60 font-mono text-sm">Completing survey...</p>
      </div>
    </div>

    <!-- Footer -->
    <div class="p-4 text-center">
      <p class="text-xs text-green-400/30 font-mono">Session: {{ sessionId }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { questionsApi, responsesApi, sessionsApi } from '@/api';
import { logger } from '@/api/client';
import type { Question, ResponseCreate } from '@/types';

// Props
const props = defineProps<{
  sessionId: string
}>();

const router = useRouter();

// State
const loading = ref(true);
const error = ref('');
const animating = ref(false);
const lastKey = ref<'yes' | 'no' | null>(null);

// Questions
const baseQuestions = ref<Question[]>([]);
const currentQuestion = ref<Question | null>(null);
const questionPath = ref<Question[]>([]);
const baseQuestionIndex = ref(0);
const answeredQuestions = ref(new Set<number>());
const pendingResponses = ref<ResponseCreate[]>([]);

// Computed
const progressPercentage = computed(() => {
  if (baseQuestions.value.length === 0) return 0;
  const progress = (baseQuestionIndex.value / baseQuestions.value.length) * 100;
  return Math.min(progress, 100);
});

// Load initial data
const loadSurvey = async () => {
  try {
    loading.value = true;
    error.value = '';
    
    // Verify session exists
    if (import.meta.env.DEV) {
      logger.info('Loading survey for session', { sessionId: props.sessionId });
    }
    await sessionsApi.getSession(Number(props.sessionId));
    
    // Load base questions
    const questions = await questionsApi.getBaseQuestions();
    if (import.meta.env.DEV) {
      logger.info(`Loaded ${questions.length} base questions`);
    }
    
    if (questions.length === 0) {
      throw new Error('No questions available');
    }
    
    baseQuestions.value = questions.sort((a, b) => a.order_index - b.order_index);
    currentQuestion.value = baseQuestions.value[0];
  } catch (err: any) {
    logger.error('Failed to load survey', err);
    error.value = err.message || 'Failed to load survey';
  } finally {
    loading.value = false;
  }
};

// Retry loading
const retryLoad = () => {
  loadSurvey();
};

// Handle answer
const handleAnswer = async (answer: boolean) => {
  if (!currentQuestion.value || animating.value) return;
  
  try {
    animating.value = true;
    lastKey.value = answer ? 'yes' : 'no';
    
    // Log the answer
    if (import.meta.env.DEV) {
      logger.info(`Question answered: ${answer ? 'YES' : 'NO'}`, {
        questionId: currentQuestion.value.id,
        question: currentQuestion.value.text
      });
    }
    
    // Mark as answered
    answeredQuestions.value.add(currentQuestion.value.id);
    
    // Store response
    const response: ResponseCreate = {
      question_id: currentQuestion.value.id,
      answer
    };
    pendingResponses.value.push(response);
    
    // Send response to API (fire and forget for speed)
    sendResponse(response);
    
    // Determine next question
    if (answer) {
      // YES - try to go deeper
      await goDeeper();
    } else {
      // NO - go back or next base
      goBack();
    }
    
    // Animation cleanup
    setTimeout(() => {
      animating.value = false;
      lastKey.value = null;
    }, 300);
    
  } catch (err: any) {
    logger.error('Error handling answer', err);
    error.value = 'Failed to submit answer';
    animating.value = false;
  }
};

// Go deeper into the tree
const goDeeper = async () => {
  if (!currentQuestion.value) return;
  
  try {
    // Get child questions
    const children = await questionsApi.getChildQuestions(currentQuestion.value.id);
    
    if (children.length > 0) {
      // Go to first unanswered child
      const nextChild = children
        .sort((a, b) => a.order_index - b.order_index)
        .find(q => !answeredQuestions.value.has(q.id));
      
      if (nextChild) {
        questionPath.value.push(currentQuestion.value);
        currentQuestion.value = nextChild;
        if (import.meta.env.DEV) {
          logger.info(`Going deeper to: ${nextChild.text}`);
        }
        return;
      }
    }
    
    // No children or all answered, go back
    goBack();
  } catch (err) {
    logger.error('Failed to get child questions', err);
    goBack();
  }
};

// Go back in the tree or to next base
const goBack = async () => {
  // Pop up the tree and look for siblings
  while (questionPath.value.length > 0) {
    const parent = questionPath.value[questionPath.value.length - 1];
    
    try {
      // Get siblings (children of the parent)
      const siblings = await questionsApi.getChildQuestions(parent.id);
      const sortedSiblings = siblings.sort((a, b) => a.order_index - b.order_index);
      
      // Find the next unanswered sibling
      const nextSibling = sortedSiblings.find(q => !answeredQuestions.value.has(q.id));
      
      if (nextSibling) {
        // Found an unanswered sibling
        currentQuestion.value = nextSibling;
        if (import.meta.env.DEV) {
          logger.info(`Moving to sibling: ${nextSibling.text}`);
        }
        return;
      }
      
      // No unanswered siblings at this level, go up one level
      questionPath.value.pop();
    } catch (err) {
      logger.error('Failed to get siblings', err);
      questionPath.value.pop();
    }
  }
  
  // We're back at the base level with no more children to explore
  goToNextBase();
};

// Move to next base question
const goToNextBase = () => {
  baseQuestionIndex.value++;
  
  if (baseQuestionIndex.value < baseQuestions.value.length) {
    currentQuestion.value = baseQuestions.value[baseQuestionIndex.value];
    questionPath.value = [];
    if (import.meta.env.DEV) {
      logger.info(`Moving to base question ${baseQuestionIndex.value + 1}`);
    }
  } else {
    // Survey complete
    completeSurvey();
  }
};

// Send response to API
const sendResponse = async (response: ResponseCreate) => {
  try {
    await responsesApi.createResponse(Number(props.sessionId), response);
    if (import.meta.env.DEV) {
      logger.debug('Response sent successfully');
    }
  } catch (err) {
    logger.error('Failed to send response', err);
    // Continue survey even if response fails
  }
};

// Complete survey
const completeSurvey = async () => {
  try {
    if (import.meta.env.DEV) {
      logger.info('Completing survey');
    }
    currentQuestion.value = null;
    
    // Mark session as complete
    await sessionsApi.completeSession(Number(props.sessionId));
    
    // Navigate to completion page
    await router.push({
      name: 'Complete',
      params: { sessionId: props.sessionId }
    });
  } catch (err: any) {
    logger.error('Failed to complete survey', err);
    error.value = 'Failed to complete survey';
  }
};

// Keyboard event handler
const handleKeyPress = (event: KeyboardEvent) => {
  if (animating.value || !currentQuestion.value) return;
  
  switch (event.key.toLowerCase()) {
    case ' ':
    case 'enter':
      event.preventDefault();
      handleAnswer(true);
      break;
    case 'n':
      event.preventDefault();
      handleAnswer(false);
      break;
  }
};

// Lifecycle
onMounted(() => {
  loadSurvey();
  window.addEventListener('keydown', handleKeyPress);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyPress);
});
</script>