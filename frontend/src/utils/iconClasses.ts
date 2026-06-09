/**
 * Utility functions for generating conditional CSS classes for technology icons.
 * Different components may need different styling approaches for the same technologies.
 */

/**
 * Base classes that apply to all technology icons
 */
export const BASE_ICON_CLASSES = {
  survey: 'w-16 h-16',
  card: 'w-16 h-16', 
  admin: 'w-6 h-6'
} as const;

/**
 * Technologies that need special background styling
 */
export const TECHNOLOGIES_WITH_BACKGROUND = [
  'kafka',
  'neo4j', 
  'flyway',
  'django',
  'astro',
  'github',
  'remix',
  'helm',
  'aws',
  'flask',
  'express',
  'nextjs',
  'splunk',
  'dbt',
  'flink',
  'scikitLearn',
  'seaborn',
  'jmeter',
  'cypress',
  'pandas',
  'feast',
] as const;

/**
 * Background classes for different component contexts
 */
export const BACKGROUND_CLASSES = {
  survey: 'bg-white p-3',
  card: 'bg-white p-3',
  admin: 'bg-white p-1 rounded'
} as const;

/**
 * Transform a technology key into a human-readable name
 * @param techKey - The technology key (e.g., 'reactNative', 'scikitLearn')
 * @returns Human-readable name (e.g., 'React Native', 'Scikit Learn')
 * 
 * @example
 * formatTechnologyName('reactNative') // 'React Native'
 * formatTechnologyName('scikitLearn') // 'Scikit Learn'
 * formatTechnologyName('kafka') // 'Kafka'
 */
export function formatTechnologyName(techKey: string): string {
  return techKey.charAt(0).toUpperCase() + techKey.slice(1).replace(/([A-Z])/g, ' $1').trim();
}

/**
 * Get the appropriate CSS classes for a technology icon based on context
 * @param techKey - The technology key
 * @param context - The component context (survey, card, admin)
 * @returns Space-separated string of CSS classes
 */
export function getTechnologyIconClasses(
  techKey: string, 
  context: 'survey' | 'card' | 'admin'
): string {
  const classes: string[] = [BASE_ICON_CLASSES[context]];
  
  // Add background styling for technologies that need it
  if (TECHNOLOGIES_WITH_BACKGROUND.includes(techKey as any)) {
    classes.push(BACKGROUND_CLASSES[context]);
  }
  
  return classes.join(' ');
}