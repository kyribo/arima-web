<script lang="ts">
	import { fade } from 'svelte/transition';
</script>

<svelte:head>
	<title>Users | Arima</title>
</svelte:head>

<div in:fade={{ duration: 200 }} class="space-y-6">
	<!-- Page Header -->
	<div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
		<div>
			<h1 class="text-2xl font-bold text-gray-900 dark:text-white">Users</h1>
			<p class="text-gray-500 dark:text-gray-400 mt-1">Manage users and permissions</p>
		</div>
	</div>

	<!-- Content Placeholder -->
	<div
		class="bg-white dark:bg-neutral-800 rounded-2xl p-12 border border-gray-200 dark:border-white/5 text-center"
	>
		<p class="text-gray-500 dark:text-gray-400">Users management content coming soon...</p>
	</div>
</div>
