<template>
  <div class="border-l-2 border-primary-faint pl-2 md:pl-4">
    <div
      class="flex flex-col md:flex-row md:items-center md:justify-between p-2 md:p-2 hover:bg-primary/5 group"
      :class="{ 'cursor-pointer': hasChildren, 'bg-primary/5': isExpanded && isMobile }"
      @click="toggleExpanded"
    >
      <div class="flex-1 pr-2">
        <div class="flex items-start justify-between">
          <div class="flex items-center">
            <!-- Expand/Collapse indicator for questions with children -->
            <button
              v-if="hasChildren"
              @click.stop="toggleExpanded"
              class="mr-2 text-primary-dim hover:text-primary transition-colors"
            >
              <svg class="w-4 h-4 transition-transform" :class="{ 'rotate-90': isExpanded }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
              </svg>
            </button>
            <span class="text-primary-subtle text-sm md:text-base">{{ question.text }}</span>
            <span v-if="question.category" class="ml-2 text-xs text-accent-dim">
              [{{ question.category }}]
            </span>
          </div>
        </div>
      </div>

      <!-- Desktop: Show on hover | Mobile: Show when expanded -->
      <div
        class="flex gap-2 mt-2 md:mt-0 transition-opacity"
        :class="{
          'opacity-0 group-hover:opacity-100': !isMobile,
          'opacity-100': isMobile && isExpanded,
          'hidden': isMobile && !isExpanded
        }"
        @click.stop
      >
        <button
          @click="$emit('add-child', question.id)"
          class="px-3 py-1.5 md:px-2 md:py-1 text-primary hover:text-primary-subtle hover:bg-primary/10 text-xs font-mono-primary rounded border border-green-400/30 md:border-0"
        >
          +Child
        </button>
        <button
          @click="$emit('edit', question)"
          class="px-3 py-1.5 md:px-2 md:py-1 text-accent hover:text-accent-dim hover:bg-accent/10 text-xs font-mono-primary rounded border border-amber-500/30 md:border-0"
        >
          Edit
        </button>
        <button
          @click="$emit('delete', question.id)"
          class="px-3 py-1.5 md:px-2 md:py-1 text-danger hover:text-danger hover:bg-danger/10 text-xs font-mono-primary opacity-80 hover:opacity-100 rounded border border-red-500/30 md:border-0"
        >
          Delete
        </button>
      </div>
    </div>
    
    <!-- Children -->
    <div v-if="hasChildren && isExpanded" class="ml-4">
      <QuestionTreeItem
        v-for="child in question.children"
        :key="child.id"
        :question="child"
        @edit="$emit('edit', $event)"
        @delete="$emit('delete', $event)"
        @add-child="$emit('add-child', $event)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import type { QuestionTree } from '@/types';

const props = defineProps<{
  question: QuestionTree;
}>();

defineEmits<{
  edit: [question: QuestionTree];
  delete: [questionId: number];
  'add-child': [parentId: number];
}>();

// Track if on mobile or touch device
const isMobile = ref(false);
const isExpanded = ref(true); // Start expanded by default

// Check if this question has children
const hasChildren = computed(() => {
  return props.question.children && props.question.children.length > 0;
});

// Check if device is mobile or has touch
const checkIfMobile = () => {
  isMobile.value = window.innerWidth < 768 || 'ontouchstart' in window;
};

// Toggle expanded state - works for both mobile and desktop
const toggleExpanded = () => {
  if (hasChildren.value) {
    isExpanded.value = !isExpanded.value;
  }
};

onMounted(() => {
  checkIfMobile();
  window.addEventListener('resize', checkIfMobile);
});

onUnmounted(() => {
  window.removeEventListener('resize', checkIfMobile);
});
</script>