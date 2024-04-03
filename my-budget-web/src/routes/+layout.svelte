<script>
	import '../app.css';
	import Navbar from '../lib/Navbar.svelte';
	import { onMount } from 'svelte';
	import { initializeAuth } from '$lib/store';
	import { Toaster } from 'svelte-french-toast';
	import { ModeWatcher } from 'mode-watcher';

	// On component mount, initialize the authentication state based on localStorage
	onMount(() => {
		initializeAuth();
	});
</script>

<Navbar />

<!-- Toast notifications will be available on every page that uses this layout -->
<Toaster />
<ModeWatcher />
<slot />
