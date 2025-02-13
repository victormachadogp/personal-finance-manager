export interface TransactionServiceInterface {
  fetchTransactions(month?: string, showAll?: boolean): Promise<Transaction[]>
  fetchCategories(): Promise<Category[]>
  fetchAnalytics(month?: string, showAll?: boolean): Promise<AnalyticsResponse>
}
