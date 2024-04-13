<script lang="ts">
	import { goto } from '$app/navigation';
	import { isAuthenticated } from '$lib/store';
	import toast from 'svelte-french-toast';
	import { Button } from '$lib/components/ui/button';
	import * as Card from '$lib/components/ui/card/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import { onMount } from 'svelte';

	onMount(() => {
		isAuthenticated.subscribe((value) => {
			if (value) {
				goto('/dashboard');
			}
		});
	});

	let username = '';
	let email = '';
	let password = '';
	let firstName = '';
	let lastName = '';
	let errorMessage = '';

	const apiUrl = import.meta.env.VITE_API_URL || '';

	async function handleRegister(): Promise<void> {
		try {
			const response = await fetch(`${apiUrl}/v1/auth/register`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ username, email, password, firstName, lastName })
			});

			if (!response.ok) {
				const errorData = await response.json();
				errorMessage = errorData.message || 'Registration failed. Please try again.';
				toast.error(errorMessage);
			} else {
				toast.success('Registration successful! Please log in.');
				goto('/login'); // Adjust this as necessary to match your login route
			}
		} catch (error) {
			errorMessage = (error as Error).message;
			toast.error('There was a problem with registration.');
		}
	}
</script>

<div class="flex justify-center items-center h-screen">
	<Card.Root class="container max-w-xl mx-auto mt-10 form-glass-effect">
		<Card.Header>
			<Card.Title>Register</Card.Title>
			<Card.Description>Create your account.</Card.Description>
		</Card.Header>
		<Card.Content>
			<form on:submit|preventDefault={handleRegister} class="space-y-6">
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
					<Label for="email">Email</Label>
					<Input type="email" id="email" bind:value={email} required placeholder="Your email" />
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
				<div class="flex flex-col space-y-1.5">
					<Label for="firstName">First Name</Label>
					<Input
						type="text"
						id="firstName"
						bind:value={firstName}
						required
						placeholder="Your first name"
					/>
				</div>
				<div class="flex flex-col space-y-1.5">
					<Label for="lastName">Last Name</Label>
					<Input
						type="text"
						id="lastName"
						bind:value={lastName}
						required
						placeholder="Your last name"
					/>
				</div>
				{#if errorMessage}
					<p class="text-red-500 text-xs italic">{errorMessage}</p>
				{/if}
				<Button variant="default" type="submit">Register</Button>
			</form>
		</Card.Content>
	</Card.Root>
</div>
