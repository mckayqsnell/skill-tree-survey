<template>
  <div class="min-h-screen bg-black star-field flex flex-col" :class="{ 'stiff-mode': isStiffMode }">
    <!-- Progress Bar - Fixed at top -->
    <div class="fixed top-0 left-0 right-0 w-full px-4 pt-4 pb-2 bg-black/95 backdrop-blur-sm z-40 border-b border-green-400/20">
      <div class="max-w-3xl mx-auto">
        <div class="h-2 bg-primary/10 rounded-full overflow-hidden">
          <div
            class="h-full bg-gradient-to-r from-primary to-cyan-400 transition-all duration-500 rounded-full"
            :style="{ width: `${progressPercentage}%` }"
          />
        </div>
        <p class="text-xs text-primary-dim font-mono-primary mt-2 text-center">
          Progress: {{ Math.round(progressPercentage) }}%
        </p>
      </div>
    </div>

    <!-- Main Content with padding for fixed header and footer on mobile -->
    <div class="flex-1 flex items-center justify-center px-4 pt-20 pb-20 md:pb-4">
      <div v-if="loading" class="text-center">
        <div class="inline-block w-8 h-8 border-2 border-primary-faint border-t-primary rounded-full animate-spin mb-4"></div>
        <p class="text-primary-dim font-mono-primary text-sm">Loading questions...</p>
      </div>

      <div v-else-if="error" class="text-center max-w-md">
        <div class="glass-card">
          <p class="text-danger mb-4 font-mono-primary text-sm">{{ error }}</p>
          <button @click="retryLoad" class="btn-secondary">Retry</button>
        </div>
      </div>

      <div v-else-if="currentQuestion" class="w-full max-w-3xl">
        <!-- Mobile View with Swipeable Card (below md breakpoint) -->
        <div class="block md:hidden">
          <SwipeableCard
            :text="currentQuestion.text"
            :category="currentQuestion.category || undefined"
            :animating="animating"
            @swipeLeft="handleAnswer(false)"
            @swipeRight="handleAnswer(true)"
            @swipeStart="() => lastKey = null"
          />
        </div>

        <!-- Desktop View (md and above) -->
        <div class="hidden md:block">
          <!-- Question Card -->
          <div
            class="glass-card text-center"
            :key="currentQuestion.id"
            :class="{ 'scale-95': animating }"
          >
            <h2 class="text-2xl md:text-3xl font-semibold mb-8 text-primary">
              {{ currentQuestion.text }}
            </h2>

            <!-- Technology Icons for Desktop -->
            <div v-if="detectedTechnologies.length > 0" class="mb-8 flex flex-wrap justify-center gap-2">
              <div
                v-for="tech in detectedTechnologies"
                :key="tech.key"
                class="flex items-center gap-1 px-2 py-1"
              >
                <img
                  :src="tech.icon.url"
                  :alt="tech.icon.alt"
                  :aria-label="tech.icon.ariaLabel"
                  :class="getTechnologyIconClasses(tech.key, 'survey')"
                  loading="lazy"
                  decoding="async"
                  @error="handleImageError"
                />
              </div>
            </div>

            <!-- Response Buttons -->
            <div class="flex justify-center gap-6">
              <button
                @click="handleAnswer(true)"
                class="btn-yes group relative"
                :class="{ 'btn-yes-active': lastKey === 'yes' }"
              >
                <span class="btn-yes-text">YES</span>
                <div class="flex gap-1 text-xs opacity-70">
                  <kbd class="kbd-key kbd-yes">Y</kbd>
                  <span class="text-primary-dim">/</span>
                  <kbd class="kbd-key kbd-yes">↵</kbd>
                </div>
                <div class="absolute inset-0 bg-primary/5 opacity-0 group-hover:opacity-100 transition-opacity duration-200"></div>
              </button>

              <button
                @click="handleAnswer(false)"
                class="btn-no group relative"
                :class="{ 'btn-no-active': lastKey === 'no' }"
              >
                <span class="btn-no-text">NO</span>
                <kbd class="kbd-key kbd-no px-2">N</kbd>
                <div class="absolute inset-0 bg-danger/5 opacity-0 group-hover:opacity-100 transition-opacity duration-200"></div>
              </button>
            </div>
            <!-- Desktop Undo Button Container - Always present to maintain layout -->
            <div class="mt-6 min-h-[48px] flex items-center justify-center">
              <Transition name="fade-undo">
                <button
                  v-if="answerHistory.length > 0 && canUndo"
                  @click="undoAnswer"
                  class="text-xs flex-col items-center text-accent-dim hover:text-accent transition-colors group relative undo-button"
                >
                  <span class="text-accent-dim text-[14px] font-bold mb-1 tracking-wider font-heading"> ← Undo <br></span>
                  <kbd class="px-2 py-0.5 bg-accent/10 border border-accent-dim text-accent-dim text-[10px] rounded">BACKSPACE</kbd>
                  <div class="absolute inset-0 bg-accent/5 opacity-0 group-hover:opacity-100 transition-opacity duration-200 rounded undo-hover-bg"></div>
                </button>
              </Transition>
            </div>
          </div>
        </div>

        <!-- Mobile Undo Button Container - Always present to maintain layout -->
        <div class="block md:hidden mt-4 text-center min-h-[44px] flex items-center justify-center">
          <Transition name="fade-undo">
            <button
              v-if="answerHistory.length > 0 && canUndo"
              @click="undoAnswer"
              class="inline-flex items-center gap-2 px-4 py-2 text-accent-dim hover:text-accent transition-colors bg-black/50 border border-accent-dim/30 rounded mobile-undo-button"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6"></path>
              </svg>
              <span class="text-sm font-bold tracking-wider">Undo</span>
            </button>
          </Transition>
        </div>
      </div>

      <div v-else class="text-center">
        <p class="text-primary-dim font-mono-primary text-sm">Completing survey...</p>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { questionsApi, responsesApi, sessionsApi } from '@/api';
import { logger } from '@/api/client';
import type { Question, ResponseCreate, TechnologyIcon } from '@/types';
import SwipeableCard from '@/components/SwipeableCard.vue';
import { icons } from '@/constants/icons';
import { technologyPatterns } from '@/constants/technologyPatterns';
import { getTechnologyIconClasses, formatTechnologyName } from '@/utils/iconClasses';

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
const animating = ref(false);
const lastKey = ref<'yes' | 'no' | null>(null);

// Questions
const baseQuestions = ref<Question[]>([]);
const currentQuestion = ref<Question | null>(null);
const questionPath = ref<Question[]>([]);
const baseQuestionIndex = ref(0);
const answeredQuestions = ref(new Set<number>());
const pendingResponses = ref<ResponseCreate[]>([]);

// Progress tracking
const totalQuestionsCount = ref(0);
const questionsAnswered = ref(0);
const questionTree = ref<Map<number, number>>(new Map()); // Maps question ID to number of children

// Undo Logic
const UNDO_TIMEOUT = 10000;
const canUndo = ref(false);
let undoTimer: ReturnType<typeof setTimeout> | null = null;
let lastPendingSend: (() => void) | null = null;
const answerHistory = ref<Question[]>([]);

// Handle image loading errors
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement;
  logger.warn(`Failed to load icon: ${img.src}`);
  // Hide the broken image
  img.style.display = 'none';
};

// Computed
const progressPercentage = computed(() => {
  if (totalQuestionsCount.value === 0) return 0;
  const progress = (questionsAnswered.value / totalQuestionsCount.value) * 100;
  return Math.min(progress, 100);
});


// Detect technologies mentioned in the current question text
const detectedTechnologies = computed(() => {
  if (!currentQuestion.value) return [];
  
  const technologies: Array<{ key: string; name: string; icon: TechnologyIcon }> = [];
  
  for (const [key, pattern] of Object.entries(technologyPatterns)) {
    if (pattern.test(currentQuestion.value.text)) {
      const iconKey = key as keyof typeof icons;
      if (icons[iconKey]) {
        const name = formatTechnologyName(iconKey);
        technologies.push({
          key,
          name,
          icon: icons[iconKey]
        });
        if (import.meta.env.DEV) {
          logger.info(`Detected technology: ${key} for text: "${currentQuestion.value.text}"`);
        }
      } else {
        if (import.meta.env.DEV) {
          logger.warn(`No icon found for technology: ${key}`);
        }
      }
    }
  }
  
  // Remove duplicates and limit to 4 technologies max
  const unique = technologies.filter((tech, index, self) => 
    index === self.findIndex(t => t.key === tech.key)
  ).slice(0, 4);
  
  if (import.meta.env.DEV && unique.length > 0) {
    console.log(`Final detected technologies:`, unique.map(t => t.key));
  }
  
  return unique;
});

// Store the full question tree for efficient lookups
const fullQuestionTree = ref<any[]>([]);
const treeNodeMap = new Map<number, any>();

// Helper function to build the node map and count children (no API calls)
const buildNodeMapAndCount = (node: any): number => {
  // Store this node in the map
  treeNodeMap.set(node.id, node);

  let count = 0;
  if (node.children && node.children.length > 0) {
    count += node.children.length;
    for (const child of node.children) {
      const childCount = buildNodeMapAndCount(child); // Recursive call stores all descendants
      questionTree.value.set(child.id, childCount);
      count += childCount;
    }
  }
  return count;
};

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

    // Fetch the entire question tree in ONE API call instead of 382+ calls!
    const treeData = await questionsApi.getQuestionTree();
    if (import.meta.env.DEV) {
      logger.info(`Loaded complete question tree with ${treeData.length} base questions (single API call)`);
    }

    if (treeData.length === 0) {
      throw new Error('No questions available');
    }

    fullQuestionTree.value = treeData;

    // Build the node map and count all questions
    let total = 0;
    for (const node of treeData) {
      // This will store ALL nodes (including nested children) in treeNodeMap
      const childCount = buildNodeMapAndCount(node);
      questionTree.value.set(node.id, childCount);
      total += 1 + childCount; // 1 for the node itself + its children
    }

    if (import.meta.env.DEV) {
      logger.info(`TreeNodeMap contains ${treeNodeMap.size} nodes`);
    }

    // Extract base questions from the tree
    baseQuestions.value = treeData
      .filter(q => q.is_base)
      .sort((a, b) => a.order_index - b.order_index)
      .map(q => ({
        id: q.id,
        text: q.text,
        parent_id: null,
        is_base: true,
        category: q.category,
        order_index: q.order_index,
        created_at: new Date().toISOString(),
        updated_at: null
      }));

    totalQuestionsCount.value = total;
    if (import.meta.env.DEV) {
      logger.info(`Total questions count: ${total}`);
    }

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
    // Add answer to history for undo
    answerHistory.value.push(currentQuestion.value);

    // Mark as answered and update progress
    answeredQuestions.value.add(currentQuestion.value.id);
    questionsAnswered.value++;

    // If answering NO, add the number of skipped children to progress
    if (!answer) {
      const skippedCount = questionTree.value.get(currentQuestion.value.id) || 0;
      questionsAnswered.value += skippedCount;
      if (import.meta.env.DEV && skippedCount > 0) {
        logger.info(`Skipping ${skippedCount} child questions`);
      }
    }

    // Store response
    const response: ResponseCreate = {
      question_id: currentQuestion.value.id,
      answer
    };
    pendingResponses.value.push(response);

    // Clear Undo Timer if Exists
    if (undoTimer) {
      clearTimeout(undoTimer);
      undoTimer = null;
    }
    // If there is a pending response, send it
    if (lastPendingSend) {
      lastPendingSend();
      lastPendingSend = null;
    }
    // If this is the last question, send to API immediately
    const isLastBase =
      baseQuestionIndex.value === baseQuestions.value.length - 1;
    const isLastQuestion = isLastBase && questionPath.value.length === 0;
    if (isLastQuestion) {
      sendResponse(response);
      lastPendingSend = null;
      canUndo.value = false;
    } else {
      // Otherwise, set up a delayed send for when the response is certain
      lastPendingSend = () => {
        sendResponse(response);
      };
    }
    // Wait for animation to load next question
    setTimeout(async () => {
      animating.value = false;
      lastKey.value = null;
      // Determine next question
      if (answer) {
        // YES - try to go deeper
        await goDeeper();
      } else {
        // NO - go back or next base
        goBack();
      }
      canUndo.value = true;
      // Start new undo timer
      undoTimer = setTimeout(() => {
        canUndo.value = false;
        undoTimer = null;
        // Send the pending response if still present
        if (lastPendingSend) {
          lastPendingSend();
          lastPendingSend = null;
        }
        }, UNDO_TIMEOUT);
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
    // Get child questions from the cached tree (NO API CALL!)
    const currentNode = treeNodeMap.get(currentQuestion.value.id);

    if (import.meta.env.DEV) {
      logger.info(`Looking for node ${currentQuestion.value.id} in treeNodeMap`, {
        found: !!currentNode,
        hasChildren: currentNode?.children?.length > 0
      });
    }

    if (currentNode && currentNode.children && currentNode.children.length > 0) {
      // Convert tree children to Question format and find first unanswered
      const children = currentNode.children
        .sort((a: any, b: any) => a.order_index - b.order_index)
        .map((child: any) => ({
          id: child.id,
          text: child.text,
          parent_id: currentQuestion.value!.id,
          is_base: false,
          category: child.category,
          order_index: child.order_index,
          created_at: new Date().toISOString(),
          updated_at: null
        }));

      const nextChild = children.find((q: any) => !answeredQuestions.value.has(q.id));

      if (nextChild) {
        questionPath.value.push(currentQuestion.value);
        currentQuestion.value = nextChild;
        if (import.meta.env.DEV) {
          logger.info(`Going deeper to: ${nextChild.text} (from cached tree)`);
        }
        return;
      }
    }

    // No children or all answered, go back
    goBack();
  } catch (err) {
    logger.error('Failed to get child questions from tree', err);
    goBack();
  }
};
const undoAnswer = async () => {
  try{
    logger.info("Attempting to undo answer")
    if (animating.value || !currentQuestion.value || answerHistory.value.length === 0) return;
    if (undoTimer) {
      clearTimeout(undoTimer);
      undoTimer = null;
    }
    canUndo.value = false;
    lastPendingSend = null;
    const previousQuestion = answerHistory.value.pop();
    if (previousQuestion) {
      // Get the last response to check if it was a NO answer
      const lastResponse = pendingResponses.value[pendingResponses.value.length - 1];
      const wasNoAnswer = lastResponse && !lastResponse.answer;

      // Decrease progress for the question itself
      questionsAnswered.value--;

      // If it was a NO answer, also decrease by the number of skipped children
      if (wasNoAnswer) {
        const skippedCount = questionTree.value.get(previousQuestion.id) || 0;
        questionsAnswered.value -= skippedCount;
      }

      if (baseQuestions.value.some(q => q.id === currentQuestion.value!.id)) {
        baseQuestionIndex.value -= 1;
      } else {
        questionPath.value.pop();
      }
      currentQuestion.value = previousQuestion;
      pendingResponses.value.pop();
      answeredQuestions.value.delete(previousQuestion.id);
      if (import.meta.env.DEV) {
        logger.info(`Undoing to: ${previousQuestion.text}`);
      }
    }
  } catch (err) {
    logger.error("Failed to undo answer", err)
  }
};

// Go back in the tree or to next base
const goBack = async () => {
  // Pop up the tree and look for siblings
  while (questionPath.value.length > 0) {
    const parent = questionPath.value[questionPath.value.length - 1];

    // Get siblings from cached tree (NO API CALL!)
    const parentNode = treeNodeMap.get(parent.id);

    if (parentNode && parentNode.children && parentNode.children.length > 0) {
      // Convert tree children to Question format
      const siblings = parentNode.children
        .sort((a: any, b: any) => a.order_index - b.order_index)
        .map((child: any) => ({
          id: child.id,
          text: child.text,
          parent_id: parent.id,
          is_base: false,
          category: child.category,
          order_index: child.order_index,
          created_at: new Date().toISOString(),
          updated_at: null
        }));

      // Find the next unanswered sibling
      const nextSibling = siblings.find((q: any) => !answeredQuestions.value.has(q.id));

      if (nextSibling) {
        // Found an unanswered sibling
        currentQuestion.value = nextSibling;
        if (import.meta.env.DEV) {
          logger.info(`Moving to sibling: ${nextSibling.text} (from cached tree)`);
        }
        return;
      }
    }

    // No unanswered siblings at this level, go up one level
    questionPath.value.pop();
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
      params: { sessionId: props.sessionId },
      query: isStiffMode.value ? { mode: 'stiff' } : {}
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
    case 'y':
    case 'enter':
      event.preventDefault();
      handleAnswer(true);
      break;
    case 'n':
      event.preventDefault();
      handleAnswer(false);
      break;
    case 'backspace':
      if (canUndo.value) {
        event.preventDefault();
        undoAnswer();
      }
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

<style scoped>
/* Smooth fade transition for undo button - no transform to prevent layout shift */
.fade-undo-enter-active,
.fade-undo-leave-active {
  transition: opacity 0.4s ease, transform 0.4s ease;
}

.fade-undo-enter-from {
  opacity: 0;
  transform: scale(0.9);
}

.fade-undo-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

.fade-undo-enter-to,
.fade-undo-leave-from {
  opacity: 1;
  transform: scale(1);
}
</style>