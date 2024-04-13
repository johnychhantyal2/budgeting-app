import type { Category, CategoryCreateRequest } from '../../types/types';
import secureFetch from './api-utils';

/**
 * Fetches categories from the API.
 * @param apiUrl - The URL of the API.
 * @param token - The authentication token.
 * @returns A promise that resolves to the fetched categories.
 * @throws If there is an error fetching the categories.
 */
export async function fetchCategories(apiUrl: string, token: string) {
	try {
		const response = await secureFetch(`${apiUrl}/v1/categories`, {
			method: 'GET',
			headers: {
				Authorization: `Bearer ${token}`
			}
		});

		const categories = await response.json();
		return categories;
	} catch (error) {
		console.error('Error fetching Categories:', error);
		throw error; // Rethrow the error so the calling function can handle it
	}
}

// In /lib/api/categories.ts

export async function createCategory(
	apiUrl: string,
	token: string,
	categoryData: CategoryCreateRequest
) {
	try {
		const response = await secureFetch(`${apiUrl}/v1/categories`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			},
			body: JSON.stringify(categoryData)
		});

		const category = await response.json();
		return category;
	} catch (error) {
		console.error('Error creating category:', error);
		throw error;
	}
}

/**
 * Deletes a category by its ID.
 * @param apiUrl - The URL of the API.
 * @param token - The authentication token.
 * @param categoryId - The ID of the category to be deleted.
 * @throws If there is an error deleting the category.
 */
export async function deleteCategory(apiUrl: string, token: string, categoryId: number) {
	try {
		const response = await secureFetch(`${apiUrl}/v1/categories/${categoryId}`, {
			method: 'DELETE',
			headers: {
				Authorization: `Bearer ${token}`
			}
		});

		if (response.status === 404) {
			throw new Error('Category not found');
		}

		// Since the response for a DELETE request might not have a body,
		// the success message is generated here rather than from response.json()
		return `Category with ID ${categoryId} deleted successfully.`;
	} catch (error) {
		console.error('Error deleting category:', error);
		throw error;
	}
}

/**
 * Updates a category by its ID.
 */
export async function updateCategory(
	apiUrl: string,
	token: string,
	categoryId: number,
	categoryData: Partial<CategoryCreateRequest>
) {
	try {
		const response = await secureFetch(`${apiUrl}/v1/categories/${categoryId}`, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			},
			body: JSON.stringify(categoryData)
		});

		const updatedCategory = await response.json();
		return updatedCategory;
	} catch (error) {
		console.error('Error updating category:', error);
		throw error;
	}
}