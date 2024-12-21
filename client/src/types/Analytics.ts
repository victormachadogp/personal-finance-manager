export interface CategoryAnalytics {
  id: string | null
  total: string
}

export interface AnalyticsResponse {
  categories: CategoryAnalytics[]
  total: string
}

export interface AnalyticsItem {
  categoryId: string | null
  category: string
  total: number
  color: string
  percentage: number
}

export interface AnalyticsSummary {
  items: AnalyticsItem[]
  total: number
}
