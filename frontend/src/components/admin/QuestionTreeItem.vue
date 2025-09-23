<template>
  <div class="border-l-2 border-primary-faint pl-2 md:pl-4">
    <div
      class="flex flex-col md:flex-row md:items-center md:justify-between p-2 md:p-2 hover:bg-primary/5 group"
      :class="{ 'cursor-pointer': isMobile, 'bg-primary/5': isExpanded && isMobile }"
      @click="toggleExpanded"
    >
      <div class="flex-1 pr-2">
        <div class="flex items-start justify-between">
          <div class="flex items-center gap-2">
            <span class="text-primary-subtle text-sm md:text-base">{{ question.text }}</span>
            <span v-if="question.category" class="ml-2 text-xs text-accent-dim">
              [{{ question.category }}]
            </span>
            <!-- Technology Icons -->
            <div v-if="detectedTechnologies.length > 0" class="flex items-center gap-1">
              <img
                v-for="tech in detectedTechnologies"
                :key="tech.key"
                :src="tech.icon.url"
                :alt="tech.icon.alt"
                :aria-label="tech.icon.ariaLabel"
                :class="[
                  'w-6 h-6',
                  tech.key === 'kafka' ? 'bg-white p-1 rounded' : '',
                  tech.key === 'neo4j' ? 'bg-white p-1 rounded' : '',
                  tech.key === 'flyway' ? 'bg-white p-1 rounded' : '',
                  tech.key === 'django' ? 'bg-white p-1 rounded' : '',
                  tech.key === 'astro' ? 'bg-white p-1 rounded' : '',
                  tech.key === 'github' ? 'bg-white p-1 rounded' : '',
                  tech.key === 'remix' ? 'bg-white p-1 rounded' : '',
                  tech.key === 'helm' ? 'bg-white p-1 rounded' : '',
                  tech.key === 'aws' ? 'bg-white p-1 rounded' : '',
                  tech.key === 'flask' ? 'bg-white p-1 rounded' : '',
                  tech.key === 'express' ? 'bg-white p-1 rounded' : '',
                  tech.key === 'nextjs' ? 'bg-white p-1 rounded' : '',
                  tech.key === 'splunk' ? 'bg-white p-1 rounded' : '',
                  tech.key === 'dbt' ? 'bg-white p-1 rounded' : '',
                  tech.key === 'flink' ? 'bg-white p-1 rounded' : '',
                  tech.key === 'scikitLearn' ? 'bg-white p-1 rounded' : '',
                  tech.key === 'seaborn' ? 'bg-white p-1 rounded' : '',
                  tech.key === 'jmeter' ? 'bg-white p-1 rounded' : '',
                  tech.key === 'cypress' ? 'bg-white p-1 rounded' : '',
                  tech.key === 'pandas' ? 'bg-white p-1 rounded' : '',
                  tech.key === 'feast' ? 'bg-white p-1 rounded' : '',
                ]"
                loading="lazy"
                decoding="async"
                @error="handleImageError"
              />
            </div>
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
import { ref, onMounted, onUnmounted, computed } from 'vue';
import type { QuestionTree } from '@/types';
import { icons } from '@/constants/icons';

const props = defineProps<{
  question: QuestionTree;
}>();

defineEmits<{
  edit: [question: QuestionTree];
  delete: [questionId: number];
  'add-child': [parentId: number];
}>();

// Technology detection patterns (same as SurveyView)
const technologyPatterns = {
  'python': /\b(python)\b/i,
  'nodejs': /\b(node\.?js|nodejs)\b/i,
  'typescript': /\b(typescript|ts)\b/i,
  'java': /\b(java)\b/i,
  'go': /\b(go|golang)\b/i,
  'rust': /\b(rust)\b/i,
  'swift': /\b(swift)\b/i,
  'kotlin': /\b(kotlin|jetpack compose)\b/i,
  'dart': /\b(dart)\b/i,
  'swiftui': /\b(swiftui)\b/i,
  'jetpackcompose': /\b(jetpack compose)\b/i,
  
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
  'flask': /\b(flask)\b/i,
  'nestjs': /\b(nestjs)\b/i,
  
  // Databases
  'mongodb': /\b(mongodb|mongo)\b/i,
  'mysql': /\b(mysql)\b/i,
  'postgres': /\b(postgresql|postgres)\b/i,
  'dynamodb': /\b(dynamodb)\b/i,
  'couchbase': /\b(couchbase)\b/i,
  'redis': /\b(redis)\b/i,
  'memcached': /\b(memcached)\b/i,
  
  // Cloud & Infrastructure
  'docker': /\b(docker|dockerfile)\b/i,
  'kubernetes': /\b(kubernetes|k8s)\b/i,
  'helm': /\b(helm)\b/i,
  'terraform': /\b(terraform)\b/i,
  'ansible': /\b(ansible)\b/i,
  'ec2': /\b(ec2)\b/i,
  'ecs': /\b(ecs)\b/i,
  'eks': /\b(eks)\b/i,
  'fargate': /\b(fargate)\b/i,
  'iam': /\b(iam)\b/i,
  'sagemaker': /\b(sagemaker)\b/i,
  'secretsManager': /\b(secrets\s*manager)\b/i,
  'ebs': /\b(ebs)\b/i,
  'apiGateway': /\b(api\s*gateway|apigateway)\b/i,
  's3': /\b(s3)\b/i,
  'cloudfront': /\b(cloudfront)\b/i,
  'cloudformation': /\b(cloudformation)\b/i,
  'documentdb': /\b(documentdb)\b/i,
  'rds': /\b(rds)\b/i,
  'redshift': /\b(redshift)\b/i,
  'sns': /\b(sns)\b/i,
  'sqs': /\b(sqs)\b/i,
  'efs': /\b(efs)\b/i,
  'lambda': /\b(lambda)\b/i,
  'azureDevops': /\b(azure devops)\b/i,
  'azureServiceBus': /\b(azure service bus)\b/i,
  'azurefunctions': /\b(azure functions)\b/i,
  'azureappservice': /\b(azure app service)\b/i,
  'snowflake': /\b(snowflake)\b/i,
  // Testing
  'jest': /\b(jest)\b/i,
  'cypress': /\b(cypress)\b/i,
  'playwright': /\b(playwright)\b/i,
  'selenium': /\b(selenium)\b/i,
  'jmeter': /\b(jmeter)\b/i,
  'k6': /\b(k6)\b/i,
  'hashicorpVault': /\b(hashicorp vault)\b/i,
  'kong': /\b(kong)\b/i,
  'dvc': /\b(dvc)\b/i,
  
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
  'pubsub': /\b(pub\/sub|google pub\/sub)\b/i,
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
  'flutter': /\b(flutter)\b/i,
  'openapi': /\b(openapi)\b/i,
  'swagger': /\b(swagger)\b/i,
  
  // Data Science & ML
  'numpy': /\b(numpy)\b/i,
  'pandas': /\b(pandas)\b/i,
  'matplotlib': /\b(matplotlib)\b/i,
  'seaborn': /\b(seaborn)\b/i,
  'plotly': /\b(plotly)\b/i,
  'scikitLearn': /\b(scikit-learn|scikit learn)\b/i,
  'tensorflow': /\b(tensorflow)\b/i,
  'pytorch': /\b(pytorch)\b/i,
  'xgboost': /\b(xgboost)\b/i,
  'lightgbm': /\b(lightgbm)\b/i,
  'scipy': /\b(scipy)\b/i,
  'mlflow': /\b(mlflow)\b/i,
  'kubeflow': /\b(kubeflow)\b/i,

  'android': /\b(android)\b/i,
  'airflow': /\b(airflow)\b/i,
  'hadoop': /\b(hadoop)\b/i,
  'spark': /\b(spark)\b/i,
  'apigee': /\b(apigee)\b/i,
  'appengine': /\b(app engine)\b/i,
  'appservice': /\b(appservice)\b/i,
  'argoCD': /\b(argo cd)\b/i,
  'astro': /\b(astro)\b/i,
  'azuresql': /\b(azure sql)\b/i,
  'cosmosdb': /\b(cosmosdb)\b/i,
  'bigquery': /\b(bigquery)\b/i,
  'chaosMonkey': /\b(chaos monkey)\b/i,
  'consul': /\b(consul)\b/i,
  'dagster': /\b(dagster)\b/i,
  'deltaLake': /\b(delta lake)\b/i,
  'feast': /\b(feast)\b/i,
  'firestore': /\b(firestore)\b/i,
  'flink': /\b(flink)\b/i,
  'flyway': /\b(flyway)\b/i,
  'gin': /\b(gin)\b/i,
  'grpc': /\b(grpc)\b/i,
  'iceberg': /\b(iceberg)\b/i,
  'jax': /\b(jax)\b/i,
  'jotai': /\b(jotai)\b/i,
  'kibana': /\b(kibana)\b/i,
  'langchain': /\b(langchain)\b/i,
  'lightGBM': /\b(lightgbm)\b/i,
  'llamaindex': /\b(llamaindex)\b/i,
  'logstash': /\b(logstash)\b/i,
  'materialUi': /\b(material-ui)\b/i,
  'mobx': /\b(mobx|MobX)\b/i,
  'neo4j': /\b(neo4j|Neo4j)\b/i,
  'ngrx': /\b(ngrx)\b/i,
  'ngxs': /\b(ngxs)\b/i,
  'nuxt': /\b(nuxt)\b/i,
  'pinia': /\b(pinia)\b/i,
  'prefect': /\b(prefect)\b/i,
  'redux': /\b(redux)\b/i,
  'sass': /\b(sass)\b/i,
  'scala': /\b(scala)\b/i,
  'splunk': /\b(splunk)\b/i,
  'spring': /\b(spring)\b/i,
  'tecton': /\b(tecton)\b/i,
  'teradata': /\b(teradata)\b/i,
  'travisci': /\b(travis ci)\b/i,
  'uikit': /\b(uikit)\b/i,
  'vuex': /\b(vuex)\b/i,
  'xml': /\b(xml)\b/i,
  'zustand': /\b(zustand)\b/i,
  'less': /\b(less)\b/i,
  'nextjs': /\b(next.js|nextjs)\b/i,
  'remix': /\b(remix)\b/i,
  'gatsby': /\b(gatsby)\b/i,
  'antDesign': /\b(ant design)\b/i,
  'elasticsearch': /\b(elasticsearch)\b/i,
  'flux': /\b(flux)\b/i,
  'echo': /\b(echo)\b/i,
  'googleCloudFunctions': /\b(google cloud functions)\b/i,
  'pulumi': /\b(pulumi)\b/i,
  'dbt': /\b(dbt)\b/i,
  'hf': /\b(hugging face)\b/i,
  'plotly': /\b(plotly)\b/i,
  'seaborn': /\b(seaborn)\b/i,
};

// Detect technologies mentioned in the question text
const detectedTechnologies = computed(() => {
  if (!props.question.text) return [];
  
  const technologies: Array<{ key: string; name: string; icon: any }> = [];
  
  for (const [key, pattern] of Object.entries(technologyPatterns)) {
    if (pattern.test(props.question.text)) {
      const iconKey = key as keyof typeof icons;
      if (icons[iconKey]) {
        technologies.push({
          key,
          name: key.charAt(0).toUpperCase() + key.slice(1).replace(/([A-Z])/g, ' $1').trim(),
          icon: icons[iconKey]
        });
      }
    }
  }
  
  // Remove duplicates and limit to 3 technologies max for admin view
  const unique = technologies.filter((tech, index, self) => 
    index === self.findIndex(t => t.key === tech.key)
  ).slice(0, 3);
  
  return unique;
});

// Handle image loading errors
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement;
  console.warn(`Failed to load icon: ${img.src}`);
  // Hide the broken image
  img.style.display = 'none';
};

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