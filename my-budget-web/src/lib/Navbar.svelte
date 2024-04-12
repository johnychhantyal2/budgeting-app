<script lang="ts">
	import { isAuthenticated, userProfile } from '$lib/store';
	import { goto } from '$app/navigation';
	import toast from 'svelte-french-toast';
	import { Button } from '$lib/components/ui/button';
	import Sun from 'lucide-svelte/icons/sun';
	import Moon from 'lucide-svelte/icons/moon';
	import { toggleMode } from 'mode-watcher';
	import Logo from '$lib/assets/day37-calculator.svg';

	function handleLogout(): void {
		localStorage.removeItem('access_token');
		localStorage.removeItem('refresh_token');
		localStorage.removeItem('username'); // Clear username
		isAuthenticated.set(false);
		userProfile.set({}); // Reset user profile
		goto('/login');
		toast.success('You have been signed out.');
	}
</script>

<nav
	class="sticky top-0 z-50 flex justify-between items-center p-4 glass-effect md:px-24 bottom-shadow"
>
	<div class="flex items-center">
		<a
			href="/"
			class="flex items-center text-lg font-bold"
			on:click|preventDefault={() => goto('/')}
		>
			<img src={Logo} alt="BudgetApp Logo" class="h-8 mr-2" /> BudgetApp
		</a>
		<Button on:click={toggleMode} variant="outline" size="icon" class="ml-4">
			<Sun
				class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"
			/>
			<Moon
				class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"
			/>
			<span class="sr-only">Toggle theme</span>
		</Button>
	</div>
	<div>
		{#if $isAuthenticated && $userProfile.username}
			<span class="mr-4">Hello, {$userProfile.username}</span>
			<Button variant="destructive" on:click={handleLogout}>Sign Out</Button>
		{:else if $isAuthenticated}
			<span class="mr-4">Hello, user</span>
			<!-- Fallback text -->
			<Button variant="destructive" on:click={handleLogout}>Sign Out</Button>
		{:else}
			<!-- Unauthenticated user UI -->
			<Button variant="default" on:click={() => goto('/login')}>Sign In</Button>
			<Button variant="ghost" on:click={() => goto('/register')}>Register</Button>
		{/if}
	</div>
</nav>

<style>
	.glass-effect {
		/* background-color: rgba(255, 255, 255, 0.2); */
		backdrop-filter: blur(10px);
		border-radius: 0px;
		border: 0px solid rgba(255, 255, 255, 0.18);
	}

	.bottom-shadow {
		box-shadow:
			0 4px 6px -1px rgba(0, 0, 0, 0.1),
			0 2px 4px -2px rgba(0, 0, 0, 0.1);
	}
</style>
