<script lang="ts">
    import { fade, fly } from 'svelte/transition';
    import type { ApprovalRequest } from '$lib/types/risk-event';

    let { 
        showInbox = $bindable(), 
        pendingRequests, 
        handleApprove, 
        handleReject 
    } = $props<{
        showInbox: boolean;
        pendingRequests: ApprovalRequest[];
        handleApprove: (req: ApprovalRequest) => void;
        handleReject: (id: string) => void;
    }>();
</script>

<div in:fade={{ duration: 200 }} class="max-w-3xl mx-auto space-y-6 pt-6">
	<!-- Back Navigation -->
	<button
		onclick={() => (showInbox = false)}
		class="flex items-center gap-2 text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white transition-colors font-medium mb-2 group"
	>
		<svg
			xmlns="http://www.w3.org/2000/svg"
			class="w-5 h-5 group-hover:-translate-x-1 transition-transform"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
		>
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				d="M10 19l-7-7m0 0l7-7m-7 7h18"
			/>
		</svg>
		Back to Reports
	</button>

	{#each pendingRequests as req (req.id)}
		<div
			in:fly={{ y: 20 }}
			class="bg-white dark:bg-neutral-800 rounded-2xl border border-gray-200 dark:border-white/5 overflow-hidden shadow-sm"
		>
			<!-- Header -->
			<div
				class="px-6 py-4 bg-gray-50/50 dark:bg-neutral-900/50 border-b border-gray-100 dark:border-white/5 flex justify-between items-center"
			>
				<div class="flex items-center gap-3">
					<span
						class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold
                        {req.action === 'create' ? 'bg-green-100 text-green-700' : ''}
                        {req.action === 'edit' ? 'bg-blue-100 text-blue-700' : ''}
                        {req.action === 'delete' ? 'bg-red-100 text-red-700' : ''}
                    "
					>
						{req.action[0].toUpperCase()}
					</span>
					<div>
						<h3 class="text-sm font-bold text-gray-900 dark:text-white capitalize">
							{req.action} Request
						</h3>
						<p class="text-xs text-gray-500">ID: {req.id}</p>
					</div>
				</div>
				<div class="text-xs text-gray-400 font-mono">
					{new Date(req.timestamp).toLocaleTimeString()}
				</div>
			</div>

			<!-- Content -->
			<div class="p-6">
				{#if req.action === 'edit' && req.payload}
					<div class="grid gap-4">
						{#each Object.entries(req.payload) as [key, value]}
							<div class="grid grid-cols-12 gap-4 text-sm">
								<div class="col-span-3 text-gray-500 capitalize">
									{key.replace(/([A-Z])/g, ' $1').trim()}
								</div>
								<div
									class="col-span-9 font-medium text-gray-900 dark:text-white bg-blue-50 dark:bg-blue-900/20 px-2 py-1 rounded"
								>
									{#if key === 'images' && Array.isArray(value)}
										<div class="flex gap-2 flex-wrap">
											{#each value as img}
												<img
													src={img as string}
													alt="Diff"
													class="w-16 h-16 object-cover rounded border border-gray-200"
												/>
											{/each}
										</div>
									{:else}
										{value}
									{/if}
								</div>
							</div>
						{/each}
					</div>
				{:else if req.action === 'create'}
					<div class="space-y-2">
						<h4 class="text-lg font-bold text-gray-900 dark:text-white">
							{req.payload.reportTitle}
						</h4>
						<div class="grid grid-cols-2 gap-4 text-xs">
							<span class="px-2 py-1 bg-gray-100 dark:bg-neutral-700 rounded"
								>Code: {req.payload.clientCode}</span
							>
						</div>
						<p class="text-gray-600 dark:text-gray-400 text-sm mt-2">
							<strong>Risk Description:</strong>
							{req.payload.riskDescription}
						</p>
						<div class="flex gap-2 mt-2">
							<span
								class="text-xs bg-gray-100 dark:bg-neutral-700 px-2 py-1 rounded text-gray-600 dark:text-gray-300"
							>
								Severity: {req.payload.severity}
							</span>
							{#if (req.payload.images?.length ?? 0) > 0}
								<div
									class="text-xs bg-gray-100 dark:bg-neutral-700 px-2 py-1 rounded text-gray-600 dark:text-gray-300 flex items-center gap-1"
								>
									<svg
										xmlns="http://www.w3.org/2000/svg"
										class="w-3 h-3"
										fill="none"
										viewBox="0 0 24 24"
										stroke="currentColor"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
										/>
									</svg>
									{req.payload.images?.length ?? 0}
								</div>
							{/if}
						</div>
					</div>
				{:else}
					<div
						class="flex items-center gap-4 text-red-600 bg-red-50 dark:bg-red-900/10 p-4 rounded-xl"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="w-6 h-6"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
							/>
						</svg>
						<div>
							<p class="font-bold text-sm">Deletion Requested</p>
							<p class="text-xs opacity-80">
								This will permanently remove Incident {req.targetIncidentId}
							</p>
						</div>
					</div>
				{/if}

				<!-- Footer -->
				<div
					class="mt-6 flex items-center justify-between pt-4 border-t border-gray-100 dark:border-white/5"
				>
					<div class="flex items-center gap-2 text-xs text-gray-500">
						<div class="w-5 h-5 rounded-full bg-gradient-to-tr from-blue-400 to-indigo-500"></div>
						<span>Requested by <strong>{req.requestedBy}</strong></span>
					</div>

					<div class="flex gap-3">
						<button
							onclick={() => handleReject(req.id)}
							class="px-4 py-2 text-sm font-semibold text-gray-600 hover:text-red-600 hover:bg-red-50 dark:text-gray-400 dark:hover:text-red-400 dark:hover:bg-red-900/20 rounded-lg transition-colors"
						>
							Reject
						</button>
						<button
							onclick={() => handleApprove(req)}
							class="px-6 py-2 text-sm font-semibold text-white bg-gray-900 dark:bg-white dark:text-gray-900 hover:bg-black hover:scale-105 active:scale-95 transition-all rounded-lg shadow-lg"
						>
							Approve
						</button>
					</div>
				</div>
			</div>
		</div>
	{/each}

	{#if pendingRequests.length === 0}
		<div class="text-center py-20">
			<div
				class="w-20 h-20 bg-gray-50 dark:bg-neutral-800 rounded-full flex items-center justify-center mx-auto mb-6"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="w-10 h-10 text-gray-300"
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
			<h3 class="text-xl font-bold text-gray-900 dark:text-white">All Caught Up!</h3>
			<p class="text-gray-500 dark:text-gray-400 mt-2">
				No pending approval requests at the moment.
			</p>
		</div>
	{/if}
</div>
