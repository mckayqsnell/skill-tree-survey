<template>
  <div class="border-l-2 border-primary-faint pl-4">
    <div class="flex items-center justify-between p-2 hover:bg-primary/5 group">
      <div class="flex-1">
        <span class="text-primary-subtle">{{ question.text }}</span>
        <span v-if="question.category" class="ml-2 text-xs text-accent-dim">
          [{{ question.category }}]
        </span>
      </div>
      <div class="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
        <button
          @click="$emit('add-child', question.id)"
          class="text-primary hover:text-primary-subtle text-xs font-mono-primary"
        >
          +Child
        </button>
        <button
          @click="$emit('edit', question)"
          class="text-accent hover:text-accent-dim text-xs font-mono-primary"
        >
          Edit
        </button>
        <button
          @click="$emit('delete', question.id)"
          class="text-danger hover:text-danger text-xs font-mono-primary opacity-80 hover:opacity-100"
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
import type { QuestionTree } from '@/types';

defineProps<{
  question: QuestionTree;
}>();

defineEmits<{
  edit: [question: QuestionTree];
  delete: [questionId: number];
  'add-child': [parentId: number];
}>();
</script>