<script lang="ts">
    import { fade, fly, slide } from 'svelte/transition';
    import type { ApprovalRequest, IncidentSeverity } from '$lib/types/risk-event';

    let { 
        showInbox = $bindable(), 
        pendingRequests, 
        handleApprove, 
        handleReject,
        handleViewDetails
    } = $props<{
        showInbox: boolean;
        pendingRequests: ApprovalRequest[];
        handleApprove: (req: ApprovalRequest) => void;
        handleReject: (id: string) => void;
        handleViewDetails: (req: ApprovalRequest) => void;
    }>();

    function getSeverityColor(severity: string) {
        switch (severity?.toLowerCase()) {
            case 'critical': return 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400 border-red-200 dark:border-red-800';
            case 'high': return 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400 border-orange-200 dark:border-orange-800';
            case 'medium': return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400 border-yellow-200 dark:border-yellow-800';
            case 'low': return 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400 border-green-200 dark:border-green-800';
            default: return 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400 border-gray-200 dark:border-gray-700';
        }
    }

    function getActionColor(action: string) {
        switch (action) {
            case 'create': return 'bg-emerald-500 shadow-emerald-500/20';
            case 'edit': return 'bg-blue-500 shadow-blue-500/20';
            case 'delete': return 'bg-red-500 shadow-red-500/20';
            default: return 'bg-gray-500';
        }
    }
</script>

<div in:fade={{ duration: 200 }} class="max-w-5xl mx-auto space-y-8 pt-6 pb-20">
	<!-- Header & Navigation -->
	<div class="flex items-center justify-between">
		<div>
			<h2 class="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
				Needs Approval
				<span
					class="px-3 py-1 bg-gray-100 dark:bg-white/10 text-gray-600 dark:text-gray-300 text-sm rounded-full font-medium"
				>
					{pendingRequests.length}
				</span>
			</h2>
			<p class="text-gray-500 dark:text-gray-400 mt-1">
				Review and action pending risk event requests
			</p>
		</div>
		<button
			onclick={() => (showInbox = false)}
			class="px-4 py-2 bg-white dark:bg-neutral-800 border border-gray-200 dark:border-white/10 text-gray-700 dark:text-gray-300 rounded-xl text-sm font-medium hover:bg-gray-50 dark:hover:bg-neutral-700 transition-colors"
		>
			Close Inbox
		</button>
	</div>

	{#if pendingRequests.length === 0}
		<div in:fade class="text-center py-32">
			<div
				class="w-24 h-24 bg-gradient-to-tr from-gray-100 to-gray-50 dark:from-neutral-800 dark:to-neutral-900 rounded-full flex items-center justify-center mx-auto mb-6 shadow-inner"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="w-10 h-10 text-gray-400 dark:text-gray-500"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="1.5"
						d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
					/>
				</svg>
			</div>
			<h3 class="text-xl font-bold text-gray-900 dark:text-white">All Caught Up!</h3>
			<p class="text-gray-500 dark:text-gray-400 mt-2 max-w-sm mx-auto">
				Great job! There are no pending requests requiring your attention right now.
			</p>
		</div>
	{:else}
		<div class="grid grid-cols-1 gap-6">
			{#each pendingRequests as req (req.id)}
				<div
					in:fly={{ y: 20, duration: 400 }}
					class="bg-white dark:bg-neutral-800 rounded-2xl border border-gray-200 dark:border-white/5 shadow-sm hover:shadow-md transition-shadow overflow-hidden group"
				>
					<!-- Status Strip -->
					<div class="h-1.5 w-full {getActionColor(req.action)}"></div>

					<div class="p-6">
						<!-- Card Header -->
						<div class="flex justify-between items-start mb-6">
							<div class="flex gap-4">
								<!-- Type Icon -->
								<div
									class="w-12 h-12 rounded-xl flex items-center justify-center shrink-0 {getActionColor(
										req.action
									)} text-white shadow-lg"
								>
									{#if req.action === 'create'}
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
												d="M12 4v16m8-8H4"
											/>
										</svg>
									{:else if req.action === 'edit'}
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
												d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"
											/>
										</svg>
									{:else}
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
									{/if}
								</div>

								<div>
									<h3
										class="text-lg font-bold text-gray-900 dark:text-white capitalize leading-tight"
									>
										{req.action} Request
									</h3>
									<div
										class="flex items-center gap-2 mt-1 text-xs text-gray-500 dark:text-gray-400"
									>
										<span class="font-mono">{req.id}</span>
										<span>•</span>
										<span>{new Date(req.timestamp).toLocaleString()}</span>
									</div>
								</div>
							</div>

							<!-- Severity Badge (if applicable) -->
							{#if req.payload?.severity || req.action === 'delete'}
								<div
									class="px-3 py-1 rounded-lg text-xs font-bold border capitalize {getSeverityColor(
										req.payload?.severity || 'critical'
									)}"
								>
									{req.payload?.severity || 'Critical Action'}
								</div>
							{/if}
						</div>

						<!-- Card Content -->
						<div class="pl-16">
							{#if req.action === 'create'}
								<div
									class="bg-gray-50 dark:bg-neutral-900/50 rounded-xl p-5 border border-gray-100 dark:border-white/5 space-y-3"
								>
									<div>
										<h4 class="text-base font-semibold text-gray-900 dark:text-white">
											{req.payload.reportTitle}
										</h4>
										<p class="text-sm text-gray-600 dark:text-gray-400 mt-1 line-clamp-2">
											{req.payload.riskDescription}
										</p>
									</div>
									<div class="flex flex-wrap gap-4 text-xs">
										{#if req.payload.clientCode}
											<div class="flex items-center gap-1.5 text-gray-600 dark:text-gray-300">
												<svg
													xmlns="http://www.w3.org/2000/svg"
													class="w-4 h-4 text-gray-400"
													fill="none"
													viewBox="0 0 24 24"
													stroke="currentColor"
												>
													<path
														stroke-linecap="round"
														stroke-linejoin="round"
														stroke-width="2"
														d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
													/>
												</svg>
												{req.payload.clientCode}
											</div>
										{/if}
										{#if req.payload.impact}
											<div class="flex items-center gap-1.5 text-gray-600 dark:text-gray-300">
												<svg
													xmlns="http://www.w3.org/2000/svg"
													class="w-4 h-4 text-gray-400"
													fill="none"
													viewBox="0 0 24 24"
													stroke="currentColor"
												>
													<path
														stroke-linecap="round"
														stroke-linejoin="round"
														stroke-width="2"
														d="M13 10V3L4 14h7v7l9-11h-7z"
													/>
												</svg>
												Has Impact
											</div>
										{/if}
									</div>
								</div>
							{:else if req.action === 'edit' && req.payload}
								<div class="space-y-3">
									<h4 class="text-sm font-semibold text-gray-700 dark:text-gray-300">
										Changes Proposed:
									</h4>
									<div class="grid gap-3">
										{#each Object.entries(req.payload) as [key, value]}
											{#if key !== 'date' && value}
												<!-- Show meaningful changes -->
												<div
													class="flex items-center gap-3 text-sm p-3 rounded-lg bg-gray-50 dark:bg-neutral-900/30 border border-gray-100 dark:border-white/5 transition-colors hover:border-blue-200 dark:hover:border-blue-500/30"
												>
													<span class="w-1/3 text-gray-500 capitalize"
														>{key.replace(/([A-Z])/g, ' $1')}</span
													>
													<span class="w-2/3 font-medium text-gray-900 dark:text-white truncate">
														{#if key === 'images'}
															{Array.isArray(value) ? `${value.length} images` : value}
														{:else}
															{value}
														{/if}
													</span>
												</div>
											{/if}
										{/each}
									</div>
								</div>
							{:else}
								<div
									class="bg-red-50 dark:bg-red-900/10 p-4 rounded-xl border border-red-100 dark:border-red-900/20 flex gap-4"
								>
									<div class="shrink-0 p-2 bg-red-100 dark:bg-red-900/30 rounded-lg text-red-600">
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
									</div>
									<div>
										<p class="font-bold text-red-900 dark:text-red-200">
											Permanent Deletion Request
										</p>
										<p class="text-sm text-red-700 dark:text-red-300/80 mt-1">
											This action cannot be undone. Please ensure the incident <strong
												>{req.targetIncidentId}</strong
											> is valid to delete.
										</p>
									</div>
								</div>
							{/if}

							<!-- Footer Actions -->
							<div
								class="mt-8 flex items-center justify-between pt-6 border-t border-gray-100 dark:border-white/5"
							>
								<div class="flex items-center gap-3">
									<div
										class="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white text-xs font-bold ring-2 ring-white dark:ring-neutral-800"
									>
										{req.requestedBy.charAt(0)}
									</div>
									<div class="text-sm">
										<p class="font-bold text-gray-900 dark:text-white">{req.requestedBy}</p>
										<p class="text-xs text-gray-500">{req.note || 'No notes provided'}</p>
									</div>
								</div>

								<div class="flex gap-3">
									<button
										onclick={() => handleViewDetails(req)}
										class="px-4 py-2 bg-gray-100 dark:bg-neutral-700 text-gray-700 dark:text-gray-300 rounded-lg text-sm font-semibold hover:bg-gray-200 dark:hover:bg-neutral-600 transition-colors"
									>
										View Details
									</button>
									<div class="h-8 w-px bg-gray-200 dark:bg-neutral-700 mx-1"></div>
									<button
										onclick={() => handleReject(req.id)}
										class="px-4 py-2 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg text-sm font-semibold transition-colors"
									>
										Reject
									</button>
									<button
										onclick={() => handleApprove(req)}
										class="px-6 py-2 bg-gray-900 dark:bg-white text-white dark:text-gray-900 rounded-lg text-sm font-bold shadow-lg hover:shadow-xl hover:-translate-y-0.5 transition-all"
									>
										Approve
									</button>
								</div>
							</div>
						</div>
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>
