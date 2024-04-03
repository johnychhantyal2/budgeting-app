// lib/api/reports.ts

import type { CategoryExpenseReport, BudgetOverviewReport } from '../../types/types';
import secureFetch from './api-utils';

export async function fetchCategoryExpenses(
	apiUrl: string,
	token: string,
	year: number,
	month: number
): Promise<CategoryExpenseReport[]> {
	const response = await secureFetch(`${apiUrl}/v1/reports/categories/expenses/${year}/${month}`, {
		method: 'GET',
		headers: {
			Authorization: `Bearer ${token}`
		}
	});

	return await response.json();
}

export async function fetchBudgetOverview(
	apiUrl: string,
	token: string,
	year: number,
	month: number
): Promise<BudgetOverviewReport> {
	const response = await secureFetch(
		`${apiUrl}/v1/reports/budgets/${year}/${month}/budget-overview`,
		{
			method: 'GET',
			headers: {
				Authorization: `Bearer ${token}`
			}
		}
	);

	return await response.json();
}
