<template>
  <div class="border-l-2 border-green-400/20 pl-4">
    <div class="flex items-center justify-between p-2 hover:bg-green-400/5 group">
      <div class="flex-1">
        <span class="text-green-400/80">{{ question.text }}</span>
        <span v-if="question.category" class="ml-2 text-xs text-cyan-400/60">
          [{{ question.category }}]
        </span>
      </div>
      <div class="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
        <button
          @click="$emit('add-child', question.id)"
          class="text-green-400 hover:text-green-300 text-xs font-mono"
        >
          +Child
        </button>
        <button
          @click="$emit('edit', question)"
          class="text-cyan-400 hover:text-cyan-300 text-xs font-mono"
        >
          Edit
        </button>
        <button
          @click="$emit('delete', question.id)"
          class="text-red-500 hover:text-red-400 text-xs font-mono"
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