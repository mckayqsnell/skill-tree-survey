import { apiClient, adminClient, logger } from './client';

export interface CategoryOrder {
  id: number;
  category: string;
  order_index: number;
  updated_at: string;
}

export interface CategoryBulkUpdate {
  categories: Array<{
    category: string;
    order_index: number;
  }>;
}

export const categoriesApi = {
  /**
   * Get current category display order (public endpoint)
   */
  async getCategoryOrder(): Promise<CategoryOrder[]> {
    try {
      logger.info('Fetching category display order');
      const response = await apiClient.get<CategoryOrder[]>('/api/categories/order');
      logger.info('Category order fetched successfully', { count: response.data.length });
      return response.data;
    } catch (error: any) {
      logger.error('Failed to fetch category order', error);
      throw error;
    }
  },

  /**
   * Get category order for admin (requires authentication)
   */
  async getAdminCategoryOrder(): Promise<CategoryOrder[]> {
    try {
      logger.info('Fetching admin category display order');
      const response = await adminClient.get<CategoryOrder[]>('/api/admin/categories/order');
      logger.info('Admin category order fetched successfully', { count: response.data.length });
      return response.data;
    } catch (error: any) {
      logger.error('Failed to fetch admin category order', error);
      throw error;
    }
  },

  /**
   * Update category display order (admin only)
   */
  async updateCategoryOrder(bulkUpdate: CategoryBulkUpdate): Promise<CategoryOrder[]> {
    try {
      logger.info('Updating category display order', { count: bulkUpdate.categories.length });
      const response = await adminClient.put<CategoryOrder[]>('/api/admin/categories/order', bulkUpdate);
      logger.info('Category order updated successfully');
      return response.data;
    } catch (error: any) {
      logger.error('Failed to update category order', error);
      throw error;
    }
  },

  /**
   * Reset category order to defaults (admin only)
   */
  async resetCategoryOrder(): Promise<CategoryOrder[]> {
    try {
      logger.info('Resetting category order to defaults');
      const response = await adminClient.post<CategoryOrder[]>('/api/admin/categories/order/reset');
      logger.info('Category order reset successfully');
      return response.data;
    } catch (error: any) {
      logger.error('Failed to reset category order', error);
      throw error;
    }
  }
};