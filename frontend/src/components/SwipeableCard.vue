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
      <h2 class="text-xl md:text-2xl lg:text-3xl font-semibold text-primary text-center px-4">
        {{ text }}
      </h2>

      <!-- Technology Icons -->
      <div v-if="detectedTechnologies.length > 0" class="mt-4 flex flex-wrap justify-center gap-2">
        <div
          v-for="tech in detectedTechnologies"
          :key="tech.key"
          class="flex items-center gap-1 px-2 py-1"
        >
          <img
            :src="tech.icon.url"
            :alt="tech.icon.alt"
            :aria-label="tech.icon.ariaLabel"
            :data-tech-key="tech.key"
            :class="[
              'w-16 h-16',
              tech.key === 'kafka' ? 'kafka-icon' : '',
              tech.key === 'neo4j' ? 'bg-white p-3' : '',
            ]"
            loading="lazy"
            decoding="async"
            @error="handleImageError"
          />
          <!-- <span class="text-xs text-primary-subtle font-mono-primary">{{ tech.name }}</span> -->
        </div>
      </div>

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
      <div class="flex items-center gap-2 text-red-500/60 swipe-hint-no">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
        </svg>
        <span class="text-xs font-mono-primary swipe-hint-text">Swipe for NO</span>
      </div>
      <div class="flex items-center gap-2 text-green-400/60 swipe-hint-yes">
        <span class="text-xs font-mono-primary swipe-hint-text">Swipe for YES</span>
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
import { icons } from '@/constants/icons';

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

// Handle image loading errors
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement;
  console.warn(`Failed to load icon: ${img.src}`);
  // Hide the broken image
  img.style.display = 'none';
};

// Technology detection patterns
const technologyPatterns = {
  // Programming Languages
  'python': /\b(python)\b/i,
  'nodejs': /\b(node\.?js|nodejs)\b/i,
  'typescript': /\b(typescript|ts)\b/i,
  'java': /\b(java)\b/i,
  'go': /\b(go|golang)\b/i,
  'rust': /\b(rust)\b/i,
  'swift': /\b(swift)\b/i,
  'kotlin': /\b(kotlin|jetpack compose)\b/i,
  'dart': /\b(dart|flutter)\b/i,
  
  // Frameworks & Libraries
  'react': /\b(react)\b/i,
  'vue': /\b(vue)\b/i,
  'angular': /\b(angular)\b/i,
  'svelte': /\b(svelte)\b/i,
  'express': /\b(express)\b/i,
  'django': /\b(django)\b/i,
  'fastapi': /\b(fastapi)\b/i,
  'tailwind': /\b(tailwind|tailwind css)\b/i,
  'graphql': /\b(graphql)\b/i,
  
  // Databases
  'mongodb': /\b(mongodb|mongo)\b/i,
  'mysql': /\b(mysql)\b/i,
  'postgres': /\b(postgresql|postgres)\b/i,
  'dynamodb': /\b(dynamodb)\b/i,
  'couchbase': /\b(couchbase)\b/i,
  'redis': /\b(redis)\b/i,
  'memcached': /\b(memcached)\b/i,
  
  // Cloud & Infrastructure
  'docker': /\b(docker)\b/i,
  'kubernetes': /\b(kubernetes|k8s)\b/i,
  'helm': /\b(helm|argo cd|flux)\b/i,
  'terraform': /\b(terraform)\b/i,
  'ansible': /\b(ansible)\b/i,
  'aws': /\b(aws)\b/i,
  'azureDevops': /\b(azure devops)\b/i,
  'azureServiceBus': /\b(azure service bus)\b/i,
  
  // Testing
  'jest': /\b(jest)\b/i,
  'cypress': /\b(cypress)\b/i,
  'playwright': /\b(playwright)\b/i,
  'selenium': /\b(selenium)\b/i,
  'jmeter': /\b(jmeter)\b/i,
  'k6': /\b(k6)\b/i,
  
  // Tools & Services
  'git': /\b(git)\b/i,
  'github': /\b(github)\b/i,
  'gitlab': /\b(gitlab)\b/i,
  'jenkins': /\b(jenkins)\b/i,
  'circleci': /\b(circleci)\b/i,
  'travis': /\b(travis ci)\b/i,
  'prometheus': /\b(prometheus)\b/i,
  'grafana': /\b(grafana)\b/i,
  'jaeger': /\b(jaeger)\b/i,
  'zipkin': /\b(zipkin)\b/i,
  'kafka': /\b(kafka)\b/i,
  'rabbitmq': /\b(rabbitmq)\b/i,
  'pubsub': /\b(pubsub|google pub\/sub)\b/i,
  'postman': /\b(postman)\b/i,
  'figma': /\b(figma)\b/i,
  'sketch': /\b(sketch)\b/i,
  'adobeXd': /\b(adobe xd)\b/i,
  'nginx': /\b(nginx)\b/i,
  'vite': /\b(vite)\b/i,
  'webpack': /\b(webpack)\b/i,
  'babel': /\b(babel)\b/i,
  'reactNative': /\b(react native)\b/i,
  'xamarin': /\b(xamarin)\b/i,
  
  // Data Science & ML (individual patterns for technologies not covered by python pattern)
  'lightgbm': /\b(lightgbm)\b/i,
  'sagemaker': /\b(sagemaker)\b/i,
  'mlflow': /\b(mlflow)\b/i,
  'kubeflow': /\b(kubeflow)\b/i,

  'grpc': /\b(grpc)\b/i,
};

// Detect technologies mentioned in the question text
const detectedTechnologies = computed(() => {
  const technologies: Array<{ key: string; name: string; icon: any }> = [];
  
  for (const [key, pattern] of Object.entries(technologyPatterns)) {
    if (pattern.test(props.text)) {
      const iconKey = key as keyof typeof icons;
      if (icons[iconKey]) {
        technologies.push({
          key,
          name: key.charAt(0).toUpperCase() + key.slice(1).replace(/([A-Z])/g, ' $1').trim(),
          icon: icons[iconKey]
        });
        if (import.meta.env.DEV) {
          console.log(`Detected technology: ${key} for text: "${props.text}"`);
        }
      } else {
        if (import.meta.env.DEV) {
          console.warn(`No icon found for technology: ${key}`);
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
/* Kafka icon styling */
.kafka-icon {
  background-color: white;
  border-radius: 8px;
  padding: 4px;
}
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
}

.swipe-indicator.swipe-no {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
  border: 2px solid #ef4444;
}

.swipe-hints {
  opacity: 0.9;
  transition: opacity 0.3s;
}

/* Regular mode swipe hints - bolder and more readable */
.swipe-hint-text {
  font-size: 0.875rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.025em;
}

.swipe-hint-no {
  color: rgb(239 68 68 / 0.8) !important;
}

.swipe-hint-yes {
  color: rgb(74 222 128 / 0.8) !important;
}

.swipe-hint-no svg,
.swipe-hint-yes svg {
  width: 1.375rem !important;
  height: 1.375rem !important;
  stroke-width: 2.5 !important;
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

/* Stiff mode swipe hints - bolder and more readable */
.stiff-mode .swipe-hint-no {
  color: #dc2626 !important;
}

.stiff-mode .swipe-hint-yes {
  color: #2563eb !important;
}

.stiff-mode .swipe-hint-text {
  font-size: 0.875rem !important;
  font-weight: 600 !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
}

.stiff-mode .swipe-hint-no svg,
.stiff-mode .swipe-hint-yes svg {
  width: 1.5rem !important;
  height: 1.5rem !important;
  stroke-width: 2.5 !important;
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

/* Technology icons styling */
.technology-icon {
  transition: all 0.2s ease;
}

.technology-icon img {
  transition: opacity 0.3s ease;
}

.technology-icon img[style*="display: none"] {
  opacity: 0;
}

.technology-icon:hover {
  transform: scale(1.05);
  background: rgba(74, 222, 128, 0.15);
}

.technology-icon img {
  filter: brightness(0.9);
  transition: filter 0.2s ease;
}

.technology-icon:hover img {
  filter: brightness(1.1);
}

/* Stiff mode technology icons */
.stiff-mode .technology-icon {
  background: rgba(37, 99, 235, 0.1);
  border-color: rgba(37, 99, 235, 0.2);
}

.stiff-mode .technology-icon:hover {
  background: rgba(37, 99, 235, 0.15);
}

.stiff-mode .technology-icon span {
  color: #1e40af;
}

@media (min-width: 768px) {
  .swipeable-card {
    padding: 3rem 2rem;
    min-height: 250px;
  }
}
</style>