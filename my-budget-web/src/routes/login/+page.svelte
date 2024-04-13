<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { isAuthenticated } from '$lib/store';
	import { userProfile } from '$lib/store';
	import toast from 'svelte-french-toast';
	import { Button } from '$lib/components/ui/button';
	import { buttonVariants } from '$lib/components/ui/button';
	import * as Card from '$lib/components/ui/card/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';

	onMount(() => {
		isAuthenticated.subscribe((value) => {
			if (value) {
				goto('/dashboard');
			}
		});
	});

	let username: string = '';
	let password: string = '';
	let errorMessage: string = '';

	const apiUrl: string = import.meta.env.VITE_API_URL || '';

	onMount(() => {
		const isAuth = !!localStorage.getItem('access_token');
		isAuthenticated.set(isAuth);
	});

	async function handleLogin(): Promise<void> {
		try {
			const response = await fetch(`${apiUrl}/v1/auth/login`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ username, password })
			});

			// Inside handleLogin function
			if (!response.ok) {
				// Handle failed login
				toast.error('Failed to login. Please check your credentials and try again.');
				// Instead of throwing a new Error and revealing the response's error message:
				// throw new Error('Failed to login');
				// Use a generic error message:
				errorMessage = 'Login failed. Please check your credentials and try again.';
			} else {
				// Handle successful login
				const { access_token, refresh_token } = await response.json();
				localStorage.setItem('access_token', access_token);
				localStorage.setItem('refresh_token', refresh_token);
				isAuthenticated.set(true);
				userProfile.set({ username: username });
				toast.success('You are authenticated!');
				goto('/dashboard');
			}
		} catch (error) {
			errorMessage = (error as Error).message;
			toast.error("This didn't work.");
		}
	}
</script>

<div class="flex justify-center items-center h-screen overscroll-none">
	<Card.Root class="container max-w-xl mx-auto mt-10 form-glass-effect">
		<Card.Header>
			<Card.Title>Sign In</Card.Title>
			<Card.Description>Please enter your credentials to continue.</Card.Description>
		</Card.Header>
		<Card.Content>
			<form on:submit|preventDefault={handleLogin} class="space-y-6">
				<div class="flex flex-col space-y-1.5">
					<Label for="username">Username</Label>
					<Input
						type="text"
						id="username"
						bind:value={username}
						required
						placeholder="Your username"
					/>
				</div>
				<div class="flex flex-col space-y-1.5">
					<Label for="password">Password</Label>
					<Input
						type="password"
						id="password"
						bind:value={password}
						required
						placeholder="Your password"
					/>
				</div>
				{#if errorMessage}
					<p class="text-red-500 text-xs italic">{errorMessage}</p>
				{/if}
				<div class="flex justify-between items-center mt-4">
					<Button variant="default" type="submit">Sign In</Button>
					<a href="/register" class={buttonVariants({ variant: 'link' })}
						>Don't have an account? Register</a
					>
				</div>
			</form>
		</Card.Content>
	</Card.Root>
</div>

<style>
	.form-glass-effect {
		/* background-color: rgba(255, 255, 255, 0.2); */
		backdrop-filter: blur(10px);
		border-radius: 12px;
		border: 1px solid rgba(255, 255, 255, 0.3);
		padding: 2rem;
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
	}

	.input-hover-effect:focus {
		border-color: rgba(59, 130, 246, 0.5);
		box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5);
	}

	.no-scroll {
		overflow: hidden;
		height: 100%;
	}
</style>
