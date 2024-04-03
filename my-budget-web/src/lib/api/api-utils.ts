// api-utils.ts

import { goto } from '$app/navigation';
import { isAuthenticated, userProfile } from '$lib/store';
import { toast } from 'svelte-french-toast';

// A utility function to handle the fetch calls
async function secureFetch(url: string, options: RequestInit): Promise<Response> {
	const response = await fetch(url, options);

	// Check for token expiration or invalid token
	if (response.status === 401) {
		// Here you would typically refresh the token or redirect to login
		// For simplicity, we'll just log the user out
		localStorage.removeItem('access_token');
		localStorage.removeItem('refresh_token');
		isAuthenticated.set(false);
		userProfile.set({});
		goto('/login');
		throw new Error('Session expired. Please log in again.');
	}

	if (response.status === 429) {
		// Handle too many requests
		localStorage.removeItem('access_token');
		localStorage.removeItem('refresh_token');
		isAuthenticated.set(false);
		userProfile.set({});
		goto('/login');
		throw new Error('Too many requests. Please wait for some time.');
	}

	if (!response.ok) {
		// Handle other errors as needed
		throw new Error('Network response was not ok.');
	}

	return response;
}

export default secureFetch;
