// Question types
export interface Question {
  id: number;
  text: string;
  parent_id: number | null;
  is_base: boolean;
  category: string | null;
  order_index: number;
  created_at: string;
  updated_at: string | null;
}

export interface QuestionWithChildren extends Question {
  children: QuestionWithChildren[];
}

export interface QuestionTree {
  id: number;
  text: string;
  is_base: boolean;
  category: string | null;
  order_index: number;
  children: QuestionTree[];
}

export interface QuestionCreate {
  text: string;
  parent_id?: number | null;
  is_base?: boolean;
  category?: string | null;
  order_index?: number;
}

export interface QuestionUpdate {
  text?: string;
  parent_id?: number | null;
  is_base?: boolean;
  category?: string | null;
  order_index?: number;
}

export interface QuestionReorder {
  parent_id: number | null;
  question_ids: number[];
}

export interface QuestionMove {
  question_id: number;
  new_parent_id: number | null;
}

// Session types
export interface SessionCreate {
  user_name: string;
  user_email: string;
  company: string;
}

export interface Session {
  id: number;
  user_name: string;
  user_email: string;
  company: string;
  started_at: string;
  completed_at: string | null;
}

export interface SessionSummary extends Session {
  is_completed: boolean;
  completion_time_minutes: number | null;
  total_responses: number;
  yes_responses: number;
  no_responses: number;
}

// Response types
export interface ResponseCreate {
  question_id: number;
  answer: boolean;
}

export interface Response {
  id: number;
  session_id: number;
  question_id: number;
  answer: boolean;
  answered_at: string;
}

export interface BulkResponseCreate {
  session_id: number;
  responses: ResponseCreate[];
}

export interface ResponseWithQuestion extends Response {
  question: Question;
}

// Analytics types
export interface CategoryStatistics {
  category: string;
  total_questions: number;
  yes_count: number;
  no_count: number;
  total?: number;  // Added for backend compatibility
  percentage_yes: number;
}

export interface SkillDepthAnalysis {
  max_depth_reached: number;
  average_depth: number;
  skill_paths: Array<{
    path: string[];
    depth: number;
  }>;
}

export interface UserSkillsSummary {
  user_email: string;
  user_name: string;
  total_sessions: number;
  skills: string[];
  strongest_categories: CategoryStatistics[];
}

export interface SessionAnalytics {
  total_sessions: number;
  completed_sessions: number;
  completion_rate: number;
  average_completion_time_minutes: number | null;
  unique_users: number;
  total_users: number;
  top_skills: Array<{
    skill: string;
    count: number;
  }>;
  category_breakdown: CategoryStatistics[];
}