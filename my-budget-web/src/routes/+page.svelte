<script>
	import { isAuthenticated } from '$lib/store';
	import { goto } from '$app/navigation';
	// If you have specific actions for the button
	function navigateToGetStarted() {
		// For example, navigate to a signup or feature page
	}

	// Function to handle button action
	function handleAction() {
		if ($isAuthenticated) {
			goto('/dashboard'); // Navigate to Dashboard if authenticated
		} else {
			// Assuming you have a specific route or action for "Learn More"
			goto('/learn-more'); // Navigate to a page where users can learn more about your app
		}
	}
</script>

<section class="text-gray-700 body-font">
	<div class="container mx-auto px-5 py-24 grid grid-cols-1 md:grid-cols-2 items-center gap-12">
		<img
			class="w-3/4 mx-auto mb-10 md:mb-0 object-cover object-center rounded"
			alt="hero"
			src="https://illlustrations.co/static/13fefd389e126b12f50282fc1f93b6df/ee604/day19-apple-watch.png"
		/>
		<div class="text-center md:text-left">
			<h1 class="title-font sm:text-4xl text-3xl mb-4 font-medium text-gray-900">
				Make Budgeting Simple
			</h1>
			<p class="mb-8 leading-relaxed">
				Our app provides intuitive and powerful tools to help you manage your finances with ease.
				Get started today and take control of your budget.
			</p>
			<div class="flex justify-center md:justify-start">
				<button on:click={handleAction} class="bg-black px-4 py-2 text-sm rounded text-white">
					{$isAuthenticated ? 'Go to Dashboard' : 'Learn More'}
				</button>
			</div>
		</div>
	</div>
</section>

<style>
	@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

	:global(body) {
		font-family: 'Inter', sans-serif;
	}
</style>
