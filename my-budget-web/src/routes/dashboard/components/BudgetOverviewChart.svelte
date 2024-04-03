<script lang="ts">
	import { onMount } from 'svelte';
	import Chart from 'chart.js/auto';
	import type { ChartTypeRegistry } from 'chart.js/auto';
	import { fetchBudgetOverview } from '$lib/api/reports';
	import type { BudgetOverviewReport } from '../../../types/types';
	import { Button } from '$lib/components/ui/button';
	import toast from 'svelte-french-toast';

	let canvasElement: HTMLCanvasElement;
	let chartInstance: Chart<'doughnut', number[], string> | null = null;
	const currentYear = new Date().getFullYear();
	const currentMonth = new Date().getMonth() + 1; // JavaScript months are 0-based

	let selectedYear = currentYear;
	let selectedMonth = currentMonth;

	let budgetOverview: BudgetOverviewReport | null = null;

	const updateChart = async () => {
		const apiUrl = import.meta.env.VITE_API_URL;
		const token = localStorage.getItem('access_token');

		if (token) {
			try {
				budgetOverview = await fetchBudgetOverview(apiUrl, token, selectedYear, selectedMonth);
				if (budgetOverview && canvasElement) {
					if (chartInstance) {
						chartInstance.destroy(); // Destroy the previous instance of the chart before creating a new one
					}
					createChart();
					toast.success('Successfully fetched budget overview');
				}
			} catch (error) {
				console.error('Error fetching budget overview:', error);
				toast.error('Error fetching budget overview');
			}
		} else {
			console.error('No token found');
		}
	};

	onMount(() => {
		updateChart(); // Initial chart creation
	});

	function createChart() {
		// Ensure budgetOverview is not null
		if (!budgetOverview || !canvasElement.getContext) return;

		const ctx = canvasElement.getContext('2d');
		if (!ctx) return;

		// Destroy the previous chart instance if it exists
		if (chartInstance) {
			chartInstance.destroy();
		}

		// Create a new pie chart instance
		chartInstance = new Chart<'doughnut', number[], string>(ctx, {
			type: 'doughnut', // Change the chart type to 'doughnut'
			data: {
				labels: ['Total Income', 'Total Expenses'],
				datasets: [
					{
						label: 'Budget Overview',
						data: [budgetOverview.total_income, budgetOverview.total_expenses],
						backgroundColor: ['rgba(54, 162, 235, 0.5)', 'rgba(255, 99, 132, 0.5)'],
						borderColor: ['rgba(54, 162, 235, 1)', 'rgba(255, 99, 132, 1)'],
						borderWidth: 1
					}
				]
			},
			options: {
				responsive: true,
				plugins: {
					legend: {
						position: 'bottom'
					}
				}
			}
		});
	}

	// Months array for the dropdown
	const months = Array.from({ length: 12 }, (_, i) => i + 1);

	// Generate some years for the dropdown
	const years = Array.from({ length: 10 }, (_, i) => currentYear - i);
</script>

<div class="mb-4">
	<div class="flex gap-4 mb-4">
		<select
			bind:value={selectedYear}
			class="block w-full py-2 px-3 border rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
		>
			{#each years as year}
				<option value={year}>{year}</option>
			{/each}
		</select>

		<select
			bind:value={selectedMonth}
			class="block w-full py-2 px-3 border rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
		>
			{#each months as month}
				<option value={month}>{month.toString().padStart(2, '0')}</option>
			{/each}
		</select>

		<Button on:click={updateChart}>Update Chart</Button>
	</div>

	<div class="text-xl font-semibold text-center mb-4">Budget Overview</div>
	<div class="flex justify-center items-center h-full w-full">
		<canvas bind:this={canvasElement} class="max-w-xs sm:max-w-lg md:max-w-xl lg:max-w-3xl"
		></canvas>
	</div>
</div>
