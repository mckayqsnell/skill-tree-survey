<template>
  <RouterView />
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { logger } from '@/api/client';

onMounted(() => {
  logger.info('Skill Tree Survey App initialized');
});
</script>
