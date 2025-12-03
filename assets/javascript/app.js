import * as JsCookie from "js-cookie";
import { DashboardCharts as AppDashboardCharts } from './dashboard/dashboard-charts';
export { AppDashboardCharts as DashboardCharts };
export const Cookies = JsCookie.default;

// Ensure SiteJS global exists
if (typeof window.SiteJS === 'undefined') {
  window.SiteJS = {};
}

// Assign this entry's exports to SiteJS.app
window.SiteJS.app = {
  DashboardCharts: AppDashboardCharts,
  Cookies: JsCookie.default,
};
