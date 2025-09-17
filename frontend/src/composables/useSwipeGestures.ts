import { ref, reactive, computed } from 'vue';

export interface SwipeState {
  startX: number;
  startY: number;
  currentX: number;
  currentY: number;
  deltaX: number;
  deltaY: number;
  isSwiping: boolean;
  direction: 'left' | 'right' | null;
}

export interface SwipeConfig {
  threshold?: number;
  velocityThreshold?: number;
  preventScroll?: boolean;
}

export function useSwipeGestures(config: SwipeConfig = {}) {
  const {
    threshold = 50,
    velocityThreshold = 0.3,
    preventScroll = true
  } = config;

  const state = reactive<SwipeState>({
    startX: 0,
    startY: 0,
    currentX: 0,
    currentY: 0,
    deltaX: 0,
    deltaY: 0,
    isSwiping: false,
    direction: null
  });

  const startTime = ref(0);
  const elementRef = ref<HTMLElement | null>(null);

  const swipeDistance = computed(() => Math.abs(state.deltaX));
  const swipeProgress = computed(() => Math.min(swipeDistance.value / threshold, 1));

  const rotation = computed(() => {
    if (!state.isSwiping) return 0;
    const maxRotation = 10;
    return (state.deltaX / threshold) * maxRotation;
  });

  const opacity = computed(() => {
    if (!state.isSwiping) return 1;
    return Math.max(0.5, 1 - swipeProgress.value * 0.5);
  });

  const handleTouchStart = (e: TouchEvent) => {
    const touch = e.touches[0];
    state.startX = touch.clientX;
    state.startY = touch.clientY;
    state.currentX = touch.clientX;
    state.currentY = touch.clientY;
    state.deltaX = 0;
    state.deltaY = 0;
    state.isSwiping = true;
    state.direction = null;
    startTime.value = Date.now();
  };

  const handleTouchMove = (e: TouchEvent) => {
    if (!state.isSwiping) return;

    const touch = e.touches[0];
    state.currentX = touch.clientX;
    state.currentY = touch.clientY;
    state.deltaX = state.currentX - state.startX;
    state.deltaY = state.currentY - state.startY;

    if (Math.abs(state.deltaX) > Math.abs(state.deltaY) && preventScroll) {
      e.preventDefault();
    }

    if (Math.abs(state.deltaX) > 10) {
      state.direction = state.deltaX > 0 ? 'right' : 'left';
    }
  };

  const handleTouchEnd = () => {
    if (!state.isSwiping) return;

    const endTime = Date.now();
    const timeDiff = (endTime - startTime.value) / 1000;
    const velocity = Math.abs(state.deltaX) / timeDiff;

    let swipeDetected = false;
    let finalDirection: 'left' | 'right' | null = null;

    if (Math.abs(state.deltaX) > threshold || velocity > velocityThreshold) {
      finalDirection = state.deltaX > 0 ? 'right' : 'left';
      swipeDetected = true;
    }

    const result = {
      direction: finalDirection,
      distance: Math.abs(state.deltaX),
      velocity,
      swipeDetected
    };

    reset();

    return result;
  };

  const handleTouchCancel = () => {
    reset();
  };

  const reset = () => {
    state.startX = 0;
    state.startY = 0;
    state.currentX = 0;
    state.currentY = 0;
    state.deltaX = 0;
    state.deltaY = 0;
    state.isSwiping = false;
    state.direction = null;
  };

  const bind = (element: HTMLElement) => {
    elementRef.value = element;
    element.addEventListener('touchstart', handleTouchStart, { passive: true });
    element.addEventListener('touchmove', handleTouchMove, { passive: false });
    element.addEventListener('touchend', handleTouchEnd);
    element.addEventListener('touchcancel', handleTouchCancel);
  };

  const unbind = () => {
    if (!elementRef.value) return;

    elementRef.value.removeEventListener('touchstart', handleTouchStart);
    elementRef.value.removeEventListener('touchmove', handleTouchMove);
    elementRef.value.removeEventListener('touchend', handleTouchEnd);
    elementRef.value.removeEventListener('touchcancel', handleTouchCancel);
    elementRef.value = null;
  };

  return {
    state,
    swipeDistance,
    swipeProgress,
    rotation,
    opacity,
    bind,
    unbind,
    handleTouchStart,
    handleTouchMove,
    handleTouchEnd,
    handleTouchCancel,
    reset
  };
}