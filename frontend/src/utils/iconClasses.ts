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
  'feast'
] as const;

/**
 * Special styling for specific technologies
 */
export const SPECIAL_TECHNOLOGY_STYLES = {
  kafka: {
    survey: 'kafka-icon',
    card: 'kafka-icon',
    admin: 'kafka-icon'
  }
} as const;

/**
 * Background classes for different component contexts
 */
export const BACKGROUND_CLASSES = {
  survey: 'bg-white p-3',
  card: 'bg-white p-3',
  admin: 'bg-white p-1 rounded'
} as const;

/**
 * Get the appropriate CSS classes for a technology icon based on context
 * @param techKey - The technology key
 * @param context - The component context (survey, card, admin)
 * @returns Array of CSS classes
 */
export function getTechnologyIconClasses(
  techKey: string, 
  context: 'survey' | 'card' | 'admin'
): string[] {
  const classes: string[] = [BASE_ICON_CLASSES[context]];
  
  // Add special styling for specific technologies
  if (techKey in SPECIAL_TECHNOLOGY_STYLES) {
    const specialClass = SPECIAL_TECHNOLOGY_STYLES[techKey as keyof typeof SPECIAL_TECHNOLOGY_STYLES][context];
    if (specialClass) {
      classes.push(specialClass);
    }
  }
  
  // Add background styling for technologies that need it
  if (TECHNOLOGIES_WITH_BACKGROUND.includes(techKey as any)) {
    classes.push(BACKGROUND_CLASSES[context]);
  }
  
  return classes;
}

/**
 * Get a single string of CSS classes for a technology icon
 * @param techKey - The technology key
 * @param context - The component context (survey, card, admin)
 * @returns Space-separated string of CSS classes
 */
export function getTechnologyIconClassString(
  techKey: string, 
  context: 'survey' | 'card' | 'admin'
): string {
  return getTechnologyIconClasses(techKey, context).join(' ');
}
