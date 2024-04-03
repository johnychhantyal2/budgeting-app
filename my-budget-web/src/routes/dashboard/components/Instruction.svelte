<script>
	export let visible = true;
</script>

{#if visible}
	<div class="bg-white shadow-lg rounded-lg p-4 mb-4">
		<h2 class="text-lg font-semibold mb-2">How to Use This App</h2>
		<p>Here are some instructions on how to get the most out of the app:</p>
		<ul class="list-disc pl-5 space-y-1">
			<li>Track your expenses and incomes by adding transactions.</li>
			<li>View your spending habits on the dashboard.</li>
			<li>Set budgets for different categories to manage your finances better.</li>
		</ul>
	</div>
{/if}
