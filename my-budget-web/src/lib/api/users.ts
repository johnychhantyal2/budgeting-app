import secureFetch from './api-utils';

/**
 * Fetches the user profile from the API.
 * @param apiUrl - The URL of the API.
 * @param token - The authentication token.
 * @returns A Promise that resolves to the user profile data.
 * @throws If there is an error fetching the profile.
 */
export async function fetchUserProfile(apiUrl: string, token: string) {
	const response = await secureFetch(`${apiUrl}/v1/user/profile`, {
		method: 'GET', // It's a good practice to explicitly specify the HTTP method
		headers: {
			Authorization: `Bearer ${token}`
		}
	});

	const data = await response.json();
	return data;
}
