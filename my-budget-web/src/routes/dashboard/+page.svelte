<script lang="ts">
	import { onMount } from 'svelte';
	import { userProfile } from '$lib/store';
	import { goto } from '$app/navigation';
	import { fetchTransactions } from '$lib/api/transaction';
	import { fetchUserProfile } from '$lib/api/users';
	import TransactionTable from './components/TransactionTable.svelte';
	import type { Transaction } from '../../types/types';
	import Categories from './components/Categories.svelte';
	import BudgetOverviewChart from './components/BudgetOverviewChart.svelte';
	import * as Alert from '$lib/components/ui/alert';
	import Rocket from 'svelte-radix/Rocket.svelte';

	let transactions: Transaction[] = [];
	const apiUrl = import.meta.env.VITE_API_URL || '';

	onMount(async () => {
		const token = localStorage.getItem('access_token');
		if (token) {
			try {
				const profileData = await fetchUserProfile(apiUrl, token);
				userProfile.set(profileData);

				const transactionsData = await fetchTransactions(apiUrl, token);
				transactions = transactionsData;
			} catch (error) {
				console.error(error);
				goto('/login');
			}
		} else {
			goto('/login');
		}
	});
</script>

<section class="min-h-screen">
	<div class="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
		<!-- Adjusted padding for different screen sizes -->
		<!-- Separate Container for Data Table -->
		<div class="shadow-lg rounded-lg p-4 sm:p-6 lg:p-6 mb-6">
			<!-- Adjusted padding and margin for different screen sizes -->
			<Alert.Root>
				<Rocket class="h-4 w-4" />
				<Alert.Title>Heads up!</Alert.Title>
				<Alert.Description
					>API endpoints are rate limited. To ensure smooth experience, avoid quick requests.</Alert.Description
				>
			</Alert.Root>
		</div>
		<div class="shadow-lg rounded-lg p-4 sm:p-6 lg:p-6 mb-6">
			<!-- Adjusted padding and margin for different screen sizes -->
			<TransactionTable {transactions} />
		</div>
		<!-- Top Row for Main Component and Data Visualization -->
		<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-12 gap-6 items-center">
			<!-- Adjusted grid columns for different screen sizes -->
			<!-- Main Component -->
			<div class="col-span-1 sm:col-span-2 lg:col-span-7 shadow-lg rounded-lg p-4 sm:p-6 lg:p-6">
				<!-- Adjusted padding for different screen sizes -->
				<Categories />
			</div>

			<!-- Data Visualization (Graph) with Fixed Height -->
			<div class="col-span-1 sm:col-span-2 lg:col-span-5 shadow-lg rounded-lg p-4 sm:p-6 lg:p-6">
				<!-- Adjusted padding for different screen sizes -->
				<BudgetOverviewChart />
			</div>
		</div>
	</div>
</section>

<svelte:head>
	<title>Budget Overview</title>
</svelte:head>
