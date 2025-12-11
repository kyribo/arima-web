<script lang="ts">
	import { fade } from 'svelte/transition';
</script>

<svelte:head>
	<title>System Status | Arima</title>
</svelte:head>

<div in:fade={{ duration: 200 }} class="space-y-6">
	<!-- Page Header -->
	<div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
		<div>
			<h1 class="text-2xl font-bold text-gray-900 dark:text-white">System Status</h1>
			<p class="text-gray-500 dark:text-gray-400 mt-1">Monitor system health and connectivity</p>
		</div>
	</div>

	<!-- Status Content -->
	<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
		<div
			class="bg-white dark:bg-neutral-800 rounded-2xl p-6 border border-gray-200 dark:border-white/5 shadow-sm"
		>
			<div class="flex items-center gap-4 mb-4">
				<div class="p-3 bg-green-100 dark:bg-green-500/10 rounded-xl">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="w-6 h-6 text-green-600 dark:text-green-400"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
						/>
					</svg>
				</div>
				<div>
					<h3 class="text-lg font-semibold text-gray-900 dark:text-white">Backend Server</h3>
					<p class="text-sm text-gray-500 dark:text-gray-400">Connection Status</p>
				</div>
				<div class="ml-auto">
					<span
						class="px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700 dark:bg-green-500/10 dark:text-green-400"
					>
						Connected
					</span>
				</div>
			</div>
			<div class="space-y-3">
				<div class="flex justify-between text-sm">
					<span class="text-gray-500 dark:text-gray-400">Response Time</span>
					<span class="font-medium text-gray-900 dark:text-white">45ms</span>
				</div>
				<div class="flex justify-between text-sm">
					<span class="text-gray-500 dark:text-gray-400">Uptime</span>
					<span class="font-medium text-gray-900 dark:text-white">99.9%</span>
				</div>
			</div>
		</div>

		<div
			class="bg-white dark:bg-neutral-800 rounded-2xl p-6 border border-gray-200 dark:border-white/5 shadow-sm"
		>
			<div class="flex items-center gap-4 mb-4">
				<div class="p-3 bg-green-100 dark:bg-green-500/10 rounded-xl">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="w-6 h-6 text-green-600 dark:text-green-400"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"
						/>
					</svg>
				</div>
				<div>
					<h3 class="text-lg font-semibold text-gray-900 dark:text-white">Database</h3>
					<p class="text-sm text-gray-500 dark:text-gray-400">Connection Status</p>
				</div>
				<div class="ml-auto">
					<span
						class="px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700 dark:bg-green-500/10 dark:text-green-400"
					>
						Connected
					</span>
				</div>
			</div>
			<div class="space-y-3">
				<div class="flex justify-between text-sm">
					<span class="text-gray-500 dark:text-gray-400">Query Time</span>
					<span class="font-medium text-gray-900 dark:text-white">12ms</span>
				</div>
				<div class="flex justify-between text-sm">
					<span class="text-gray-500 dark:text-gray-400">Connections</span>
					<span class="font-medium text-gray-900 dark:text-white">4 Active</span>
				</div>
			</div>
		</div>
	</div>
</div>
