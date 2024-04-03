import { writable } from 'svelte/store';
import type { Category } from '../types/types';

// We remove the direct access to localStorage during initialization
export const isAuthenticated = writable(false);

export const userProfile = writable<{
	username?: string;
	email?: string;
	first_name?: string;
	last_name?: string;
	is_active?: boolean;
	role?: string;
	bio?: string;
	country?: string;
	city?: string;
	postal_code?: string;
	address_line?: string;
	last_login?: string;
}>({});

// This function could be called from a top-level component or layout to initialize the auth state
export function initializeAuth() {
	const token = localStorage.getItem('access_token');
	const storedUsername = localStorage.getItem('username');
	isAuthenticated.set(!!token);
	if (storedUsername) {
		userProfile.set({ username: storedUsername });
	}
}

export const categoriesStore = writable<Category[]>([]);
