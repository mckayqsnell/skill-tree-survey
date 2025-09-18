<template>
  <div class="border-l-2 border-primary-faint pl-2 md:pl-4">
    <div
      class="flex flex-col md:flex-row md:items-center md:justify-between p-2 md:p-2 hover:bg-primary/5 group"
      :class="{ 'cursor-pointer': isMobile, 'bg-primary/5': isExpanded && isMobile }"
      @click="toggleExpanded"
    >
      <div class="flex-1 pr-2">
        <div class="flex items-start justify-between">
          <div>
            <span class="text-primary-subtle text-sm md:text-base">{{ question.text }}</span>
            <span v-if="question.category" class="ml-2 text-xs text-accent-dim">
              [{{ question.category }}]
            </span>
          </div>
          <!-- Mobile indicator -->
          <span v-if="isMobile" class="md:hidden text-primary-dim ml-2">
            <svg class="w-5 h-5 transition-transform" :class="{ 'rotate-180': isExpanded }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
          </span>
        </div>
      </div>

      <!-- Desktop: Show on hover | Mobile: Show always or when expanded -->
      <div
        class="flex gap-2 mt-2 md:mt-0 transition-opacity"
        :class="{
          'opacity-0 group-hover:opacity-100': !isMobile && !isExpanded,
          'opacity-100': isMobile || isExpanded
        }"
        @click.stop
      >
        <button
          @click="$emit('add-child', question.id)"
          class="px-3 py-1.5 md:px-2 md:py-1 text-primary hover:text-primary-subtle hover:bg-primary/10 text-xs font-mono-primary rounded border border-primary/30 md:border-0"
        >
          +Child
        </button>
        <button
          @click="$emit('edit', question)"
          class="px-3 py-1.5 md:px-2 md:py-1 text-accent hover:text-accent-dim hover:bg-accent/10 text-xs font-mono-primary rounded border border-accent/30 md:border-0"
        >
          Edit
        </button>
        <button
          @click="$emit('delete', question.id)"
          class="px-3 py-1.5 md:px-2 md:py-1 text-danger hover:text-danger hover:bg-danger/10 text-xs font-mono-primary opacity-80 hover:opacity-100 rounded border border-danger/30 md:border-0"
        >
          Delete
        </button>
      </div>
    </div>
    
    <!-- Children -->
    <div v-if="question.children && question.children.length > 0" class="ml-4">
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
import { ref, onMounted, onUnmounted } from 'vue';
import type { QuestionTree } from '@/types';

defineProps<{
  question: QuestionTree;
}>();

defineEmits<{
  edit: [question: QuestionTree];
  delete: [questionId: number];
  'add-child': [parentId: number];
}>();

// Track if on mobile or touch device
const isMobile = ref(false);
const isExpanded = ref(false);

// Check if device is mobile or has touch
const checkIfMobile = () => {
  isMobile.value = window.innerWidth < 768 || 'ontouchstart' in window;
};

// Toggle expanded state for mobile
const toggleExpanded = () => {
  if (isMobile.value) {
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