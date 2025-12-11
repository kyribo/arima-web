<script lang="ts">
	import { fade } from 'svelte/transition';
</script>

<svelte:head>
	<title>Trans Data | Arima</title>
</svelte:head>

<div in:fade class="space-y-6">
	<div class="flex justify-between items-start">
		<div>
			<h1 class="text-2xl font-bold text-gray-900 dark:text-white">Trans Data</h1>
			<p class="text-gray-500 dark:text-gray-400 mt-1">Transaction Data Management</p>
		</div>
	</div>

	<div
		class="bg-white dark:bg-neutral-800 rounded-2xl border border-gray-200 dark:border-white/5 p-12 text-center"
	>
		<div
			class="w-16 h-16 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-2xl flex items-center justify-center mx-auto mb-4"
		>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				class="w-8 h-8"
				fill="none"
				viewBox="0 0 24 24"
				stroke="currentColor"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"
				/>
			</svg>
		</div>
		<h3 class="text-lg font-semibold text-gray-900 dark:text-white">Under Construction</h3>
		<p class="text-gray-500 dark:text-gray-400 mt-2 max-w-sm mx-auto">
			This feature is currently being developed. Check back later for updates.
		</p>
	</div>
</div>
