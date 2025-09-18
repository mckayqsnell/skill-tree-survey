<template>
  <div class="swipeable-container">
    <div
      ref="cardElement"
      class="swipeable-card"
      :style="cardStyle"
      @touchstart="handleTouchStart"
      @touchmove="handleTouchMove"
      @touchend="handleTouchEnd"
      @touchcancel="swipe.handleTouchCancel"
    >
      <div v-if="category" class="text-center mb-4">
        <p class="text-sm text-primary-dim font-mono-primary">
          {{ category }}
        </p>
      </div>

      <h2 class="text-xl md:text-2xl lg:text-3xl font-semibold text-primary text-center px-4">
        {{ text }}
      </h2>

      <div
        v-if="swipe.state.isSwiping && swipe.state.direction"
        class="swipe-indicator"
        :class="{
          'swipe-yes': swipe.state.direction === 'right',
          'swipe-no': swipe.state.direction === 'left'
        }"
      >
        <span v-if="swipe.state.direction === 'right'" class="text-4xl font-bold">YES</span>
        <span v-else class="text-4xl font-bold">NO</span>
      </div>
    </div>

    <div class="swipe-hints mt-6 flex justify-between px-8">
      <div class="flex items-center gap-2 text-red-500/60">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
        </svg>
        <span class="text-xs font-mono-primary">Swipe for NO</span>
      </div>
      <div class="flex items-center gap-2 text-green-400/60">
        <span class="text-xs font-mono-primary">Swipe for YES</span>
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
        </svg>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useSwipeGestures } from '@/composables/useSwipeGestures';

interface Props {
  text: string;
  category?: string;
  animating?: boolean;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  swipeLeft: [];
  swipeRight: [];
  swipeStart: [];
}>();

const cardElement = ref<HTMLElement | null>(null);
const isAnimatingOut = ref(false);

const swipe = useSwipeGestures({
  threshold: 80,
  velocityThreshold: 300,
  preventScroll: true
});

const cardStyle = computed(() => {
  if (isAnimatingOut.value) {
    return {
      transform: `translateX(${swipe.state.direction === 'right' ? '150%' : '-150%'}) rotate(${swipe.state.direction === 'right' ? '20deg' : '-20deg'})`,
      opacity: '0',
      transition: 'all 0.3s ease-out'
    };
  }

  if (props.animating) {
    return {
      transform: 'scale(0.95)',
      transition: 'transform 0.2s ease-out'
    };
  }

  if (swipe.state.isSwiping) {
    return {
      transform: `translateX(${swipe.state.deltaX}px) rotate(${swipe.rotation.value}deg)`,
      opacity: swipe.opacity.value,
      transition: 'none'
    };
  }

  return {
    transform: 'translateX(0) rotate(0)',
    opacity: 1,
    transition: 'all 0.2s ease-out'
  };
});

const handleTouchStart = (e: TouchEvent) => {
  if (props.animating || isAnimatingOut.value) return;
  emit('swipeStart');
  swipe.handleTouchStart(e);
};

const handleTouchMove = (e: TouchEvent) => {
  if (props.animating || isAnimatingOut.value) return;
  swipe.handleTouchMove(e);
};

const handleTouchEnd = async () => {
  if (props.animating || isAnimatingOut.value) return;

  const result = swipe.handleTouchEnd();

  if (result && result.swipeDetected && result.direction) {
    isAnimatingOut.value = true;

    await new Promise(resolve => setTimeout(resolve, 300));

    if (result.direction === 'right') {
      emit('swipeRight');
    } else {
      emit('swipeLeft');
    }

    setTimeout(() => {
      isAnimatingOut.value = false;
      swipe.reset();
    }, 50);
  }
};

onMounted(() => {
  if (cardElement.value) {
    swipe.bind(cardElement.value);
  }
});

onUnmounted(() => {
  swipe.unbind();
});
</script>

<style scoped>
.swipeable-container {
  position: relative;
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
  user-select: none;
  -webkit-user-select: none;
  -webkit-touch-callout: none;
}

.swipeable-card {
  position: relative;
  background: rgba(0, 0, 0, 0.9);
  border: 1px solid rgba(74, 222, 128, 0.2);
  border-radius: 16px;
  padding: 2rem 1rem;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: grab;
  will-change: transform, opacity;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.swipeable-card:active {
  cursor: grabbing;
}

.swipe-indicator {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
  padding: 0.5rem 2rem;
  border-radius: 8px;
  font-family: 'Orbitron', monospace;
  animation: pulse 0.5s ease-out;
}

.swipe-indicator.swipe-yes {
  color: #4ade80;
  background: rgba(74, 222, 128, 0.1);
  border: 2px solid #4ade80;
  text-shadow: 0 0 20px rgba(74, 222, 128, 0.5);
}

.swipe-indicator.swipe-no {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
  border: 2px solid #ef4444;
  text-shadow: 0 0 20px rgba(239, 68, 68, 0.5);
}

.swipe-hints {
  opacity: 0.8;
  transition: opacity 0.3s;
}

.stiff-mode .swipeable-card {
  background: white;
  border: 1px solid #e5e7eb;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stiff-mode .swipe-indicator.swipe-yes {
  color: #2563eb;
  background: rgba(37, 99, 235, 0.1);
  border: 2px solid #2563eb;
  text-shadow: none;
}

.stiff-mode .swipe-indicator.swipe-no {
  color: #dc2626;
  background: rgba(220, 38, 38, 0.1);
  border: 2px solid #dc2626;
  text-shadow: none;
}

@keyframes pulse {
  0% {
    transform: translate(-50%, -50%) scale(0.8);
    opacity: 0;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.1);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }
}

@media (min-width: 768px) {
  .swipeable-card {
    padding: 3rem 2rem;
    min-height: 250px;
  }
}
</style>