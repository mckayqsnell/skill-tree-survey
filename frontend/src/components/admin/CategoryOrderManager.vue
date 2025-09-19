<template>
  <div>
    <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4 mb-6">
      <h2 class="text-base sm:text-lg text-primary">Report Category Display Order</h2>
      <div class="flex flex-col sm:flex-row gap-2">
        <button
          v-if="hasChanges"
          @click="saveCategoryOrder"
          class="btn-primary text-xs sm:text-sm px-3 py-2 sm:px-4"
          :disabled="saving"
        >
          {{ saving ? 'Saving...' : 'Save Order' }}
        </button>
        <button
          @click="resetToDefaults"
          class="btn-secondary text-xs sm:text-sm px-3 py-2 sm:px-4"
          :disabled="saving"
        >
          Reset to Default
        </button>
      </div>
    </div>

    <!-- Important Notice -->
    <div class="mb-4 sm:mb-6 p-3 sm:p-4 bg-amber-500/10 border border-amber-500/30 rounded">
      <div class="flex gap-2 sm:gap-3">
        <svg class="w-4 h-4 sm:w-5 sm:h-5 text-amber-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <div class="space-y-1">
          <p class="text-amber-500 font-semibold text-xs sm:text-sm">Important: Display Order Only</p>
          <p class="text-amber-500/80 text-xs leading-relaxed">
            This setting controls how categories appear in session reports and analytics charts.
            It does <strong>NOT</strong> affect the order in which questions are presented during the survey.
          </p>
          <p class="text-amber-500/60 text-xs mt-2 leading-relaxed">
            To change question presentation order, use the Questions tab to modify individual question order_index values.
          </p>
        </div>
      </div>
    </div>

    <div v-if="loading" class="text-center py-8">
      <div class="inline-block w-8 h-8 border-2 border-primary-faint border-t-primary rounded-full animate-spin mb-2"></div>
      <p class="text-primary-dim text-sm">Loading category order...</p>
    </div>

    <div v-else-if="error" class="text-center py-8">
      <p class="text-danger text-sm mb-4">{{ error }}</p>
      <button @click="loadCategories" class="btn-primary text-sm">
        Retry
      </button>
    </div>

    <div v-else-if="localCategories.length > 0" class="space-y-4">
      <p class="text-xs sm:text-sm text-primary-dim mb-4 font-mono-primary">
        Drag and drop categories below to change their display order in session reports and radar charts.
        This ensures consistent category ordering across all analytics views.
      </p>

      <draggable
        v-model="localCategories"
        @change="onOrderChange"
        item-key="id"
        handle=".drag-handle"
        animation="200"
        ghost-class="sortable-ghost"
        chosen-class="sortable-chosen"
        drag-class="sortable-drag"
      >
        <template #item="{element, index}">
          <div
            class="flex items-center gap-2 sm:gap-3 p-3 sm:p-4 bg-black/30 border border-green-400/20 rounded hover:border-green-400/40 transition-colors"
          >
            <div class="drag-handle cursor-move p-1 hover:text-primary transition-colors">
              <svg class="w-4 h-4 sm:w-5 sm:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16"></path>
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex flex-col sm:flex-row sm:items-center">
                <span class="text-sm sm:text-base text-primary font-semibold truncate">{{ element.category }}</span>
                <span class="text-xs text-primary-dim sm:ml-3 font-mono">Position: {{ index + 1 }}</span>
              </div>
            </div>
            <div class="hidden sm:block text-xs text-primary-faint font-mono whitespace-nowrap">
              Updated: {{ formatDate(element.updated_at) }}
            </div>
          </div>
        </template>
      </draggable>

      <div v-if="hasChanges" class="mt-4 p-2 sm:p-3 bg-amber-500/10 border border-amber-500/30 rounded">
        <p class="text-xs sm:text-sm text-amber-500">
          <svg class="w-3 h-3 sm:w-4 sm:h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
          </svg>
          You have unsaved changes. Click "Save Order" to apply them.
        </p>
      </div>
    </div>

    <div v-else class="text-center py-8">
      <svg class="w-16 h-16 text-primary-dim mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
      </svg>
      <p class="text-primary-dim text-sm">No categories found</p>
      <button @click="loadCategories" class="btn-primary text-sm mt-4">
        Load Categories
      </button>
    </div>
  </div>
</template>

<style scoped>
/* Style for the placeholder/ghost element where the item will be dropped */
:deep(.sortable-ghost) {
  opacity: 0.3 !important;
  background: rgba(74, 222, 128, 0.1) !important;
  border: 2px dashed rgba(74, 222, 128, 0.5) !important;
}

/* Style the element being dragged - attached to cursor */
:deep(.sortable-drag) {
  opacity: 0.95 !important;
  cursor: grabbing !important;
  background: rgba(0, 0, 0, 0.98) !important;
  border: 1px solid rgba(74, 222, 128, 0.6) !important;
  box-shadow: 0 4px 16px rgba(0, 255, 65, 0.4) !important;
}

/* Style the chosen element (when mousedown but not yet dragging) */
:deep(.sortable-chosen) {
  opacity: 0.6 !important;
  cursor: grabbing !important;
}

/* Ensure drag handle has proper cursor */
.drag-handle {
  cursor: grab !important;
}

.drag-handle:active {
  cursor: grabbing !important;
}

/* Ensure all buttons have pointer cursor */
button {
  cursor: pointer !important;
}

/* Disabled button styles */
button:disabled {
  cursor: not-allowed !important;
  opacity: 0.5;
}
</style>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import draggable from 'vuedraggable';
import { categoriesApi } from '@/api';
import { logger } from '@/api/client';
import type { CategoryOrder } from '@/api/categories';
import { useAdminAuth } from '@/composables/useAdminAuth';

// State
const loading = ref(false);
const saving = ref(false);
const error = ref('');
const localCategories = ref<CategoryOrder[]>([]);
const originalOrder = ref<CategoryOrder[]>([]);

// Computed
const hasChanges = computed(() => {
  if (localCategories.value.length !== originalOrder.value.length) return true;

  return localCategories.value.some((cat, index) => {
    const original = originalOrder.value[index];
    return !original || cat.id !== original.id;
  });
});

// Methods
const loadCategories = async () => {
  try {
    loading.value = true;
    error.value = '';

    const categories = await categoriesApi.getAdminCategoryOrder();
    localCategories.value = [...categories];
    originalOrder.value = [...categories];

    logger.info(`Loaded ${categories.length} category orders`);
  } catch (err: any) {
    logger.error('Failed to load category orders', err);
    error.value = err.response?.data?.detail || 'Failed to load category orders';
  } finally {
    loading.value = false;
  }
};

const saveCategoryOrder = async () => {
  if (!hasChanges.value) return;

  try {
    saving.value = true;
    error.value = '';

    // Prepare the bulk update with new order indices
    const bulkUpdate = {
      categories: localCategories.value.map((cat, index) => ({
        category: cat.category,
        order_index: index
      }))
    };

    const updated = await categoriesApi.updateCategoryOrder(bulkUpdate);

    // Update both local and original to reflect saved state
    localCategories.value = [...updated];
    originalOrder.value = [...updated];

    logger.info('Category order saved successfully');
  } catch (err: any) {
    logger.error('Failed to save category order', err);
    error.value = err.response?.data?.detail || 'Failed to save category order';
  } finally {
    saving.value = false;
  }
};

const resetToDefaults = async () => {
  try {
    saving.value = true;
    error.value = '';

    const defaults = await categoriesApi.resetCategoryOrder();

    localCategories.value = [...defaults];
    originalOrder.value = [...defaults];

    logger.info('Category order reset to defaults');
  } catch (err: any) {
    logger.error('Failed to reset category order', err);
    error.value = err.response?.data?.detail || 'Failed to reset category order';
  } finally {
    saving.value = false;
  }
};

const onOrderChange = () => {
  // This is called when draggable changes the order
  // The v-model binding automatically updates localCategories
  logger.debug('Category order changed');
};

const formatDate = (dateStr: string): string => {
  try {
    const date = new Date(dateStr);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  } catch {
    return 'Unknown';
  }
};

// Get admin auth
const { requireAuth } = useAdminAuth();

// Lifecycle
onMounted(async () => {
  // Ensure authentication is set up before loading
  const isAuthenticated = await requireAuth();
  if (isAuthenticated) {
    await loadCategories();
  } else {
    error.value = 'Authentication required to manage category order';
  }
});
</script>