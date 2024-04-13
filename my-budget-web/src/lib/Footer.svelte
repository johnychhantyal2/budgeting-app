<script lang="ts">
	import footerInfo from './FooterInfo.json';
	import { fetchBuildInfo } from './api/version';

	async function getBuildInfo() {
		const buildInfo = await fetchBuildInfo(import.meta.env.VITE_API_URL);
		footerInfo.version = buildInfo.version;
		footerInfo.backend_commit_id = buildInfo.commit_id;
	}

	getBuildInfo();
</script>

<footer class="py-8 px-4">
	<div class="container mx-auto">
		<div class="flex flex-wrap justify-between">
			<div>
				<h3 class="text-lg font-semibold">{footerInfo.title}</h3>
				<p class="mt-2 text-sm">{footerInfo.description}</p>
				<p class="mt-2 text-sm">Backend Commit: {footerInfo.backend_commit_id}</p>
				<p class="mt-2 text-sm">Build Version: {footerInfo.version}</p>
			</div>
			<div>
				<h3 class="text-lg">Links</h3>
				<ul class="mt-2 space-y-2">
					{#each footerInfo.links as link (link.id)}
						<li>
							<a href={link.url} class="text-blue-400 text-sm hover:underline">{link.name}</a>
						</li>
					{/each}
				</ul>
			</div>
		</div>
		<div class="mt-8 text-center">
			<p>{footerInfo.copyRight}</p>
		</div>
	</div>
</footer>
