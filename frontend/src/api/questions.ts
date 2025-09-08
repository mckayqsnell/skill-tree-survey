import { apiClient, adminClient, logger, ApiError } from './client';
import type {
  Question,
  QuestionWithChildren,
  QuestionTree,
  QuestionCreate,
  QuestionUpdate,
  QuestionReorder,
  QuestionMove,
} from '@/types';

export const questionsApi = {
  // Public endpoints
  async getBaseQuestions(category?: string): Promise<Question[]> {
    try {
      logger.info('Fetching base questions', { category });
      const params = category ? { category } : {};
      const { data } = await apiClient.get<Question[]>('/api/questions/base', { params });
      logger.info(`Retrieved ${data.length} base questions`);
      return data;
    } catch (error) {
      logger.error('Failed to fetch base questions', error);
      throw error;
    }
  },

  async getQuestionTree(): Promise<QuestionTree[]> {
    try {
      logger.info('Fetching question tree');
      const { data } = await apiClient.get<QuestionTree[]>('/api/questions/tree');
      logger.info(`Retrieved question tree with ${data.length} root nodes`);
      return data;
    } catch (error) {
      logger.error('Failed to fetch question tree', error);
      throw error;
    }
  },

  async getCategories(): Promise<string[]> {
    try {
      logger.info('Fetching categories');
      const { data } = await apiClient.get<string[]>('/api/questions/categories');
      logger.info(`Retrieved ${data.length} categories`);
      return data;
    } catch (error) {
      logger.error('Failed to fetch categories', error);
      throw error;
    }
  },

  async getQuestion(questionId: number): Promise<Question> {
    try {
      logger.info('Fetching question', { questionId });
      const { data } = await apiClient.get<Question>(`/api/questions/${questionId}`);
      logger.info(`Retrieved question: ${data.text}`);
      return data;
    } catch (error) {
      logger.error(`Failed to fetch question ${questionId}`, error);
      throw error;
    }
  },

  async getQuestionWithChildren(questionId: number): Promise<QuestionWithChildren> {
    try {
      logger.info('Fetching question with children', { questionId });
      const { data } = await apiClient.get<QuestionWithChildren>(
        `/api/questions/${questionId}/with-children`
      );
      logger.info(`Retrieved question with ${data.children?.length || 0} children`);
      return data;
    } catch (error) {
      logger.error(`Failed to fetch question with children ${questionId}`, error);
      throw error;
    }
  },

  async getChildQuestions(questionId: number): Promise<Question[]> {
    try {
      logger.info('Fetching child questions', { questionId });
      const { data } = await apiClient.get<Question[]>(
        `/api/questions/${questionId}/children`
      );
      logger.info(`Retrieved ${data.length} child questions`);
      return data;
    } catch (error) {
      logger.error(`Failed to fetch child questions for ${questionId}`, error);
      throw error;
    }
  },

  // Admin endpoints
  async createQuestion(question: QuestionCreate): Promise<Question> {
    try {
      logger.info('Creating new question', question);
      const { data } = await adminClient.post<Question>('/api/admin/questions', question);
      logger.info(`Question created with ID: ${data.id}`);
      return data;
    } catch (error) {
      logger.error('Failed to create question', { error, question });
      if (error instanceof ApiError && error.statusCode === 401) {
        throw new Error('Admin authentication failed. Please check your password.');
      }
      throw error;
    }
  },

  async updateQuestion(questionId: number, update: QuestionUpdate): Promise<Question> {
    try {
      logger.info('Updating question', { questionId, update });
      const { data } = await adminClient.put<Question>(
        `/api/admin/questions/${questionId}`,
        update
      );
      logger.info(`Question ${questionId} updated successfully`);
      return data;
    } catch (error) {
      logger.error(`Failed to update question ${questionId}`, { error, update });
      if (error instanceof ApiError && error.statusCode === 401) {
        throw new Error('Admin authentication failed. Please check your password.');
      }
      throw error;
    }
  },

  async deleteQuestion(questionId: number): Promise<void> {
    try {
      logger.info('Deleting question', { questionId });
      await adminClient.delete(`/api/admin/questions/${questionId}`);
      logger.info(`Question ${questionId} deleted successfully`);
    } catch (error) {
      logger.error(`Failed to delete question ${questionId}`, error);
      if (error instanceof ApiError && error.statusCode === 401) {
        throw new Error('Admin authentication failed. Please check your password.');
      }
      throw error;
    }
  },

  async reorderQuestions(reorder: QuestionReorder): Promise<{ success: boolean }> {
    try {
      logger.info('Reordering questions', reorder);
      const { data } = await adminClient.put<{ success: boolean }>(
        '/api/admin/questions/reorder',
        reorder
      );
      logger.info('Questions reordered successfully');
      return data;
    } catch (error) {
      logger.error('Failed to reorder questions', { error, reorder });
      if (error instanceof ApiError && error.statusCode === 401) {
        throw new Error('Admin authentication failed. Please check your password.');
      }
      throw error;
    }
  },

  async moveQuestion(move: QuestionMove): Promise<Question> {
    try {
      logger.info('Moving question', move);
      const { data } = await adminClient.put<Question>('/api/admin/questions/move', move);
      logger.info(`Question ${move.question_id} moved successfully`);
      return data;
    } catch (error) {
      logger.error('Failed to move question', { error, move });
      if (error instanceof ApiError && error.statusCode === 401) {
        throw new Error('Admin authentication failed. Please check your password.');
      }
      throw error;
    }
  },

  // Admin-only: Get all questions for management
  async getAllQuestions(): Promise<QuestionTree[]> {
    try {
      logger.info('Fetching all questions for admin');
      // This should use an admin endpoint once available
      // For now using public endpoint, but admin auth is verified separately
      const { data } = await apiClient.get<QuestionTree[]>('/api/questions/tree');
      logger.info(`Retrieved ${data.length} question trees for admin`);
      return data;
    } catch (error) {
      logger.error('Failed to fetch all questions', error);
      throw error;
    }
  },
};