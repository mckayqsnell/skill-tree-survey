import { apiClient, adminClient } from './client';
import type {
  Session,
  SessionCreate,
  SessionSummary,
  UserSkillsSummary,
  SessionAnalytics,
} from '@/types';

export const sessionsApi = {
  // Public endpoints
  async createSession(sessionData: SessionCreate): Promise<Session> {
    const { data } = await apiClient.post<Session>('/api/sessions/', sessionData);
    return data;
  },

  async getSession(sessionId: number): Promise<Session> {
    const { data } = await apiClient.get<Session>(`/api/sessions/${sessionId}`);
    return data;
  },

  async getSessionSummary(sessionId: number): Promise<SessionSummary> {
    const { data } = await apiClient.get<SessionSummary>(
      `/api/sessions/${sessionId}/summary`
    );
    return data;
  },

  async completeSession(sessionId: number): Promise<Session> {
    const { data } = await apiClient.post<Session>(
      `/api/sessions/${sessionId}/complete`
    );
    return data;
  },

  async getSessionsByEmail(email: string): Promise<Session[]> {
    const { data } = await apiClient.get<Session[]>(`/api/sessions/by-email/${email}`);
    return data;
  },

  async getSessionsByCompany(company: string): Promise<Session[]> {
    const { data } = await apiClient.get<Session[]>(
      `/api/sessions/by-company/${company}`
    );
    return data;
  },

  async getUserSkillsSummary(email: string): Promise<UserSkillsSummary> {
    const { data } = await apiClient.get<UserSkillsSummary>(
      `/api/sessions/user-skills/${email}`
    );
    return data;
  },

  // Admin endpoints
  async getAllSessions(
    skip = 0,
    limit = 100,
    completedOnly = false
  ): Promise<SessionSummary[]> {
    const { data } = await adminClient.get<SessionSummary[]>('/api/admin/sessions', {
      params: { skip, limit, completed_only: completedOnly },
    });
    return data;
  },

  async getAnalytics(company?: string): Promise<SessionAnalytics> {
    const params = company ? { company } : {};
    const { data } = await adminClient.get<SessionAnalytics>(
      '/api/admin/analytics',
      { params }
    );
    return data;
  },

  async deleteSession(sessionId: number): Promise<void> {
    await adminClient.delete(`/api/admin/sessions/${sessionId}`);
  },

  async cleanupIncompleteSessions(hoursThreshold = 24): Promise<{ deleted_sessions: number }> {
    const { data } = await adminClient.post<{ deleted_sessions: number }>(
      '/api/admin/sessions/cleanup',
      null,
      { params: { hours_threshold: hoursThreshold } }
    );
    return data;
  },
};