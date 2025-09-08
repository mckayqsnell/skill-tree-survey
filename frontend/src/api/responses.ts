import { apiClient } from './client';
import type {
  Response,
  ResponseCreate,
  BulkResponseCreate,
  ResponseWithQuestion,
  CategoryStatistics,
  SkillDepthAnalysis,
} from '@/types';

export const responsesApi = {
  async createResponse(sessionId: number, response: ResponseCreate): Promise<Response> {
    const { data } = await apiClient.post<Response>(
      `/api/responses/session/${sessionId}`,
      response
    );
    return data;
  },

  async createBulkResponses(bulk: BulkResponseCreate): Promise<Response[]> {
    const { data } = await apiClient.post<Response[]>('/api/responses/bulk', bulk);
    return data;
  },

  async getSessionResponses(sessionId: number): Promise<Response[]> {
    const { data } = await apiClient.get<Response[]>(
      `/api/responses/session/${sessionId}`
    );
    return data;
  },

  async getSessionResponsesDetailed(sessionId: number): Promise<ResponseWithQuestion[]> {
    const { data } = await apiClient.get<ResponseWithQuestion[]>(
      `/api/responses/session/${sessionId}/detailed`
    );
    return data;
  },

  async getCategoryStatistics(sessionId: number): Promise<CategoryStatistics[]> {
    const { data } = await apiClient.get<CategoryStatistics[]>(
      `/api/responses/session/${sessionId}/category-stats`
    );
    return data;
  },

  async getSkillDepthAnalysis(sessionId: number): Promise<SkillDepthAnalysis> {
    const { data } = await apiClient.get<SkillDepthAnalysis>(
      `/api/responses/session/${sessionId}/depth-analysis`
    );
    return data;
  },

  async deleteResponse(responseId: number): Promise<void> {
    await apiClient.delete(`/api/responses/${responseId}`);
  },
};