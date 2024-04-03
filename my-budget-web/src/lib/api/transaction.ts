import type { TransactionCreateRequest } from '../../types/types';
import secureFetch from './api-utils';

/**
 * Fetches transactions from the API.
 *
 * @param apiUrl - The URL of the API.
 * @param token - The authentication token.
 * @returns A promise that resolves to the fetched transactions.
 * @throws If there is an error fetching the transactions.
 */
export async function fetchTransactions(apiUrl: string, token: string) {
	const response = await secureFetch(`${apiUrl}/v1/transactions`, {
		method: 'GET',
		headers: {
			Authorization: `Bearer ${token}`
		}
	});

	const transactions = await response.json();
	return transactions;
}

export async function deleteTransaction(
	apiUrl: string,
	token: string,
	transactionId: number
): Promise<void> {
	const endpoint = `${apiUrl}/v1/transactions/${transactionId}`;
	try {
		const response = await secureFetch(endpoint, {
			method: 'DELETE',
			headers: {
				Authorization: `Bearer ${token}`,
				'Content-Type': 'application/json'
			}
		});

		// After the successful deletion, there's no need to parse JSON
		// since we're not expecting any response body for a DELETE operation.
	} catch (error) {
		console.error('Error deleting transaction:', error);
		throw error; // Rethrow to let calling function handle it.
	}
}

export async function createTransaction(
	apiUrl: string,
	token: string,
	transactionData: TransactionCreateRequest
): Promise<void> {
	// Preprocess transactionData to ensure optional fields are either null or provided value
	const processedData = {
		...transactionData,
		Description: transactionData.Description || null,
		Note: transactionData.Note || null,
		Location: transactionData.Location || null,
		CategoryID: transactionData.CategoryID || null
	};

	try {
		const response = await secureFetch(`${apiUrl}/v1/transactions`, {
			method: 'POST',
			headers: {
				Authorization: `Bearer ${token}`,
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(processedData)
		});

		// Handling the response data if needed
		const data = await response.json();
		console.log('Transaction created successfully', data);
	} catch (error) {
		console.error('Error creating transaction:', error);
		throw error; // Ensures the calling component can handle the error
	}
}

/**
 * Updates a transaction.
 * @param apiUrl - The base URL of your API.
 * @param token - The authentication token.
 * @param transactionId - The ID of the transaction to update.
 * @param transactionData - The transaction data to update.
 * @returns {Promise<Transaction>} The updated transaction.
 */
export async function updateTransaction(
	apiUrl: string,
	token: string,
	transactionId: number,
	transactionData: Partial<TransactionCreateRequest>
): Promise<any> {
	try {
		const response = await secureFetch(`${apiUrl}/v1/transactions/${transactionId}`, {
			method: 'PUT', // or 'PATCH' if your API supports partial updates
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			},
			body: JSON.stringify(transactionData)
		});

		// Handle the response data if needed
		const updatedTransaction = await response.json();
		console.log('Transaction updated successfully', updatedTransaction);
		return updatedTransaction;
	} catch (error) {
		console.error('Error updating transaction:', error);
		throw error; // Ensures the calling function can handle the error
	}
}
