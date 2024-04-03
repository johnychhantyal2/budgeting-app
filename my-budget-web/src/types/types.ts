// /src/types/types.ts

export type Transaction = {
	Amount: number;
	Date: string;
	Description: string;
	Note: string;
	Location: string;
	CategoryID: number;
	Is_Income: boolean;
	TransactionID: number;
	UserID: number;
	CreatedAt: string;
};

export type TransactionCreateRequest = {
	Amount?: number;
	Date?: string;
	Description?: string; // Optional
	Note?: string; // Optional
	Location?: string; // Optional
	CategoryID?: number; // Optional
	Is_Income?: boolean; // Optional
};

export type TransactionUpdateRequest = {
	Amount: number;
	Date: string;
	Description?: string; // Optional
	Note?: string; // Optional
	Location?: string; // Optional
	CategoryID?: number; // Optional
	Is_Income?: boolean; // Optional
};

export type Category = {
	id: number;
	name: string;
	budgeted_amount: number;
	budgeted_limit: number;
	color_code: string;
	created_at: string;
	updated_at: string;
	description: string;
	is_active: boolean;
	icon: string;
};

export type CategoryCreateRequest = {
	name: string;
	budgeted_amount: number;
	budgeted_limit: number;
	color_code: string;
	description: string;
	icon: string;
};

export type CategoryExpenseReport = {
	id: number;
	category_name: string;
	total_amount: number;
};

export type BudgetOverviewReport = {
	total_income: number;
	total_expenses: number;
	balance: number;
};
