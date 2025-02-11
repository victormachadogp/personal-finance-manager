import type { Router, RouteLocationNormalizedLoaded } from 'vue-router'

export class UrlService {
  constructor(
    private router: Router,
    private route: RouteLocationNormalizedLoaded,
  ) {}

  updateURL(showAll: boolean, month?: string) {
    this.router.replace({
      query: {
        ...(showAll ? { showAll: 'true' } : {}),
        ...(!showAll && month ? { month } : {}),
      },
    })
  }

  getInitialState(): { month?: string; showAll: boolean } {
    const monthFromUrl = this.route.query.month as string
    const showAllFromUrl = this.route.query.showAll === 'true'

    return {
      month: monthFromUrl,
      showAll: showAllFromUrl,
    }
  }
}
