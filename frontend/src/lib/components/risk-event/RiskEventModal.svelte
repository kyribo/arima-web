<script lang="ts">
    import { fade, fly } from 'svelte/transition';
    import type { Incident, IncidentSeverity, IncidentStatus } from '$lib/types/risk-event';
    import { formatDateID } from '$lib/utils/risk-helpers';

    let {
        showModal = $bindable(),
        modalMode,
        formState = $bindable(),
        incidents,
        editingId,
        handleSubmit,
        handleDelete,
        handlePrint,
        onClose,
        onEdit,
        allowPrint = true
    } = $props<{
        showModal: boolean;
        modalMode: 'create' | 'edit' | 'view';
        formState: any; // Type strictly if possible
        incidents: Incident[];
        editingId: string | null;
        handleSubmit: (e: Event) => void;
        handleDelete: (id: string) => void;
        handlePrint: () => void;
        onClose: () => void;
        onEdit: (incident: Incident) => void;
        allowPrint?: boolean;
    }>();

    let previewImage = $state<string | null>(null);

    function closeModal() {
        onClose();
        previewImage = null;
    }

    function handleFileSelect(e: Event) {
		const target = e.target as HTMLInputElement;
		if (target.files) {
			Array.from(target.files).forEach((file) => {
				const reader = new FileReader();
				reader.onload = (e) => {
					if (e.target?.result) {
						formState.images = [...formState.images, e.target.result as string];
					}
				};
				reader.readAsDataURL(file);
			});
		}
	}

    function removeImage(index: number) {
		formState.images = formState.images.filter((_: string, i: number) => i !== index);
	}
</script>

{#if showModal}
	<div
		class="fixed inset-0 bg-black/60 backdrop-blur-md z-50 flex items-center justify-center p-4"
		onclick={(e) => {
			if (e.target === e.currentTarget) closeModal();
		}}
		onkeydown={(e) => {
			if (e.key === 'Escape') closeModal();
		}}
		role="button"
		tabindex="0"
		transition:fade={{ duration: 200 }}
	>
		<div
			class="bg-white dark:bg-neutral-900 rounded-3xl p-8 max-w-5xl w-full shadow-2xl border border-gray-200 dark:border-white/10 max-h-[90vh] overflow-y-auto custom-scrollbar"
			role="document"
			transition:fly={{ y: 20, duration: 300 }}
		>
			<h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-8">
				{#if modalMode === 'create'}
					New Entry
				{:else if modalMode === 'edit'}
					Edit Entry
				{:else}
					View Event Detail
				{/if}
			</h2>

			<form onsubmit={handleSubmit} class="space-y-6">
				<fieldset disabled={modalMode === 'view'} class="contents">
					<div class="space-y-8">
						<!-- Inputs -->
						<div class="space-y-6">
							<!-- Section: Details -->
							<div class="space-y-4">
								<h3
									class="text-lg font-bold text-gray-900 dark:text-white border-b border-gray-100 dark:border-white/5 pb-2"
								>
									Risk Event Detail
								</h3>
								<!-- Row 1: Date | Impacted Client | Severity -->
								<div class="grid grid-cols-1 md:grid-cols-4 gap-6">
									<div class="md:col-span-1">
										<label
											for="reportDate"
											class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
											>Date</label
										>
										{#if modalMode === 'view'}
											<div
												class="w-full bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white font-medium"
											>
												{formatDateID(formState.date)}
											</div>
										{:else}
											<input
												type="date"
												id="reportDate"
												bind:value={formState.date}
												class="w-full bg-gray-50 dark:bg-neutral-800 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white outline-none focus:ring-2 focus:ring-gray-900 dark:focus:ring-white transition-shadow disabled:opacity-75 disabled:cursor-not-allowed"
											/>
										{/if}
									</div>
									<div class="md:col-span-1">
										<label
											for="clientCode"
											class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
											>Impacted Client</label
										>
										{#if modalMode === 'view'}
											<div
												class="w-full bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white font-medium"
											>
												{formState.clientCode}
											</div>
										{:else}
											<input
												type="text"
												id="clientCode"
												bind:value={formState.clientCode}
												required
												placeholder="e.g. CLI-001"
												class="w-full bg-gray-50 dark:bg-neutral-800 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white outline-none focus:ring-2 focus:ring-gray-900 dark:focus:ring-white"
											/>
										{/if}
									</div>
									<div class="md:col-span-2">
										<fieldset>
											<legend
												class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
												>Severity Level</legend
											>
											{#if modalMode === 'view'}
												<div
													class="w-full py-2.5 px-4 bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded-xl font-bold uppercase tracking-wider text-sm {formState.severity ===
													'critical'
														? 'text-red-600'
														: formState.severity === 'high'
															? 'text-orange-600'
															: formState.severity === 'medium'
																? 'text-yellow-600'
																: 'text-blue-600'}"
												>
													{formState.severity}
												</div>
											{:else}
												<div class="flex gap-2 p-1 bg-gray-100 dark:bg-neutral-800 rounded-xl">
													{#each ['low', 'medium', 'high', 'critical'] as sev}
														<button
															type="button"
															onclick={() => (formState.severity = sev as IncidentSeverity)}
															class="flex-1 py-2 rounded-lg text-sm font-bold capitalize transition-all border-2
                                                                {formState.severity === sev
																? sev === 'low'
																	? 'border-green-500 bg-white dark:bg-neutral-700 text-green-600 shadow-sm'
																	: sev === 'medium'
																		? 'border-yellow-500 bg-white dark:bg-neutral-700 text-yellow-600 shadow-sm'
																		: sev === 'high'
																			? 'border-orange-500 bg-white dark:bg-neutral-700 text-orange-600 shadow-sm'
																			: 'border-red-500 bg-white dark:bg-neutral-700 text-red-600 shadow-sm'
																: 'border-transparent text-gray-500 hover:text-gray-900 dark:hover:text-gray-300'}"
														>
															{sev}
														</button>
													{/each}
												</div>
											{/if}
										</fieldset>
									</div>
								</div>

								<!-- Row 2: Title (Full Width) -->
								<div>
									<label
										for="reportTitle"
										class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
										>Report Title</label
									>
									{#if modalMode === 'view'}
										<div
											class="w-full bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white font-bold text-lg"
										>
											{formState.reportTitle}
										</div>
									{:else}
										<input
											type="text"
											id="reportTitle"
											bind:value={formState.reportTitle}
											required
											placeholder="E.g., System Latency"
											class="w-full bg-gray-50 dark:bg-neutral-800 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white outline-none focus:ring-2 focus:ring-gray-900 dark:focus:ring-white transition-shadow"
										/>
									{/if}
								</div>
							</div>

							<!-- Section: Analysis -->
							<div class="space-y-4 pt-4">
								<h3
									class="text-lg font-bold text-gray-900 dark:text-white border-b border-gray-100 dark:border-white/5 pb-2"
								>
									Analysis & Actions
								</h3>

								<div class="mt-6">
									<label
										for="riskDescription"
										class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
										>Risk Description</label
									>
									{#if modalMode === 'view'}
										<div
											class="w-full bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white leading-relaxed whitespace-pre-wrap"
										>
											{formState.riskDescription}
										</div>
									{:else}
										<textarea
											id="riskDescription"
											bind:value={formState.riskDescription}
											required
											rows="4"
											placeholder="Describe the risk..."
											class="w-full bg-gray-50 dark:bg-neutral-800 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white outline-none focus:ring-2 focus:ring-gray-900 dark:focus:ring-white transition-shadow"
										></textarea>
									{/if}
								</div>

								<div class="mt-6">
									<label
										for="impact"
										class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
										>Actual or Potential Impact</label
									>
									{#if modalMode === 'view'}
										<div
											class="w-full bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white leading-relaxed whitespace-pre-wrap"
										>
											{formState.impact || '-'}
										</div>
									{:else}
										<textarea
											id="impact"
											bind:value={formState.impact}
											rows="3"
											placeholder="Describe the impact..."
											class="w-full bg-gray-50 dark:bg-neutral-800 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white outline-none focus:ring-2 focus:ring-gray-900 dark:focus:ring-white transition-shadow"
										></textarea>
									{/if}
								</div>

								<div class="mt-6">
									<label
										for="actionTaken"
										class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
										>Controls or Actions Taken</label
									>
									{#if modalMode === 'view'}
										<div
											class="w-full bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white leading-relaxed whitespace-pre-wrap"
										>
											{formState.actionTaken}
										</div>
									{:else}
										<textarea
											id="actionTaken"
											bind:value={formState.actionTaken}
											required
											rows="4"
											placeholder="Proposed or implemented solution..."
											class="w-full bg-gray-50 dark:bg-neutral-800 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white outline-none focus:ring-2 focus:ring-gray-900 dark:focus:ring-white transition-shadow"
										></textarea>
									{/if}
								</div>

								<div class="mt-6">
									<label
										for="followUpPlan"
										class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
										>Follow-up Plan</label
									>
									{#if modalMode === 'view'}
										<div
											class="w-full bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white leading-relaxed whitespace-pre-wrap"
										>
											{formState.followUpPlan || '-'}
										</div>
									{:else}
										<textarea
											id="followUpPlan"
											bind:value={formState.followUpPlan}
											rows="3"
											placeholder="Future steps..."
											class="w-full bg-gray-50 dark:bg-neutral-800 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white outline-none focus:ring-2 focus:ring-gray-900 dark:focus:ring-white transition-shadow"
										></textarea>
									{/if}
								</div>

								<div class="mt-6">
									<label
										for="additionalNotes"
										class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
										>Additional Notes</label
									>
									{#if modalMode === 'view'}
										<div
											class="w-full bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white leading-relaxed whitespace-pre-wrap"
										>
											{formState.additionalNotes || '-'}
										</div>
									{:else}
										<textarea
											id="additionalNotes"
											bind:value={formState.additionalNotes}
											rows="3"
											placeholder="Any other details..."
											class="w-full bg-gray-50 dark:bg-neutral-800 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white outline-none focus:ring-2 focus:ring-gray-900 dark:focus:ring-white transition-shadow"
										></textarea>
									{/if}
								</div>
							</div>

							<!-- Image Upload (Moved Below) -->
							<div class="border-t border-gray-100 dark:border-white/5 pt-8">
								<div class="">
									<h3 class="font-bold text-gray-900 dark:text-white mb-4">Attachments</h3>
									{#if modalMode !== 'view'}
										<div
											class="border-2 border-dashed border-gray-300 dark:border-neutral-700 rounded-xl p-6 text-center hover:bg-gray-50 dark:hover:bg-neutral-800 transition-colors cursor-pointer relative aspect-[3/1] flex flex-col items-center justify-center"
										>
											<input
												type="file"
												multiple
												accept="image/*"
												onchange={handleFileSelect}
												class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
											/>
											<div class="pointer-events-none">
												<svg
													xmlns="http://www.w3.org/2000/svg"
													class="w-10 h-10 text-gray-400 mx-auto mb-2"
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
												<p class="text-sm text-gray-500">
													<span class="text-blue-600 font-medium">Click to upload</span> or drag and drop
												</p>
												<p class="text-xs text-gray-400 mt-1">PNG, JPG up to 5MB</p>
											</div>
										</div>
									{/if}

									{#if formState.images.length > 0}
										<div
											class="grid grid-cols-4 gap-4 mt-4 max-h-[300px] overflow-y-auto custom-scrollbar"
										>
											{#each formState.images as img, i}
												<div
													class="relative group aspect-square rounded-lg overflow-hidden border border-gray-200 dark:border-white/10"
												>
													<!-- Clickable Thumbnail -->
													<button
														type="button"
														onclick={() => (previewImage = img)}
														class="w-full h-full cursor-zoom-in focus:outline-none"
													>
														<img
															src={img}
															alt="Evidence"
															class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
														/>
													</button>

													<div
														class="absolute inset-x-0 bottom-0 p-2 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex justify-end"
													>
														{#if modalMode !== 'view'}
															<button
																type="button"
																onclick={(e) => {
																	e.stopPropagation();
																	removeImage(i);
																}}
																class="p-1.5 bg-red-500/80 hover:bg-red-600 rounded-lg text-white transition-colors"
																title="Remove image"
															>
																<svg
																	xmlns="http://www.w3.org/2000/svg"
																	class="w-4 h-4"
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
															</button>
														{/if}
													</div>
												</div>
											{/each}
										</div>
									{/if}

									{#if formState.images.length === 0 && modalMode === 'view'}
										<p class="text-sm text-gray-500 italic text-center py-4">No Attachment</p>
									{/if}
								</div>
							</div>
						</div>
					</div>
				</fieldset>

				{#if modalMode === 'view'}
					<div
						class="mt-8 pt-6 border-t border-gray-100 dark:border-white/5 grid grid-cols-2 gap-8"
					>
						<div>
							<h4 class="text-sm font-bold text-gray-900 dark:text-white mb-1">Maker</h4>
							<p class="text-gray-600 dark:text-gray-400 text-sm">
								{incidents.find((i: Incident) => i.id === editingId)?.maker || 'Current User'}
							</p>
						</div>
						<div>
							<h4 class="text-sm font-bold text-gray-900 dark:text-white mb-1">Approver</h4>
							<p class="text-gray-600 dark:text-gray-400 text-sm">
								{incidents.find((i: Incident) => i.id === editingId)?.approver || '-'}
							</p>
						</div>
					</div>
				{/if}

				<div
					class="flex items-center justify-between pt-6 border-t border-gray-100 dark:border-white/5"
				>
					<div class="flex gap-3">
						{#if modalMode === 'view'}
							<button
								type="button"
								onclick={() => {
									const incident = incidents.find((i: Incident) => i.id === editingId);
									if (incident) onEdit(incident);
								}}
								class="px-4 py-2.5 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-white/5 rounded-xl transition-colors font-medium flex items-center gap-2"
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="w-5 h-5"
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
								Edit
							</button>
							<button
								type="button"
								onclick={() => editingId && handleDelete(editingId)}
								class="px-4 py-2.5 text-red-600 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/20 rounded-xl transition-colors font-medium flex items-center gap-2"
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="w-5 h-5"
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
								Delete
							</button>
						{/if}
					</div>

					<div class="flex gap-3">
						{#if modalMode !== 'create' && allowPrint}
							<button
								type="button"
								onclick={handlePrint}
								class="px-6 py-2.5 bg-white dark:bg-neutral-800 text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-white/10 rounded-xl font-medium hover:bg-gray-50 dark:hover:bg-neutral-700 transition-colors flex items-center gap-2"
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="w-5 h-5"
									fill="none"
									viewBox="0 0 24 24"
									stroke="currentColor"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"
									/>
								</svg>
								Print
							</button>
						{/if}

						{#if modalMode === 'view'}
							<button
								type="button"
								onclick={closeModal}
								class="px-6 py-2.5 bg-gray-100 dark:bg-white/5 text-gray-700 dark:text-gray-300 rounded-xl font-medium hover:bg-gray-200 dark:hover:bg-white/10 transition-colors"
							>
								Close
							</button>
						{:else}
							<button
								type="button"
								onclick={closeModal}
								class="px-6 py-2.5 bg-gray-100 dark:bg-white/5 text-gray-700 dark:text-gray-300 rounded-xl font-medium hover:bg-gray-200 dark:hover:bg-white/10 transition-colors"
							>
								Cancel
							</button>
							<button
								type="submit"
								class="px-6 py-2.5 bg-gray-900 dark:bg-white text-white dark:text-gray-900 rounded-xl font-medium hover:bg-black dark:hover:bg-gray-100 transition-all shadow-lg hover:shadow-xl hover:-translate-y-0.5"
							>
								{modalMode === 'create' ? 'Submit Entry' : 'Save Changes'}
							</button>
						{/if}
					</div>
				</div>
			</form>
		</div>
	</div>

	<!-- Lightbox/Image Preview Overlay -->
	{#if previewImage}
		<div
			class="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4 backdrop-blur-sm"
			onclick={() => (previewImage = null)}
			transition:fade={{ duration: 200 }}
			role="button"
			tabindex="0"
			onkeydown={(e) => {
				if (e.key === 'Escape') previewImage = null;
			}}
		>
			<div class="relative max-w-4xl max-h-[90vh]">
				<img
					src={previewImage}
					alt="Full preview"
					class="max-w-full max-h-[90vh] object-contain rounded-lg"
				/>
				<button
					class="absolute -top-10 right-0 text-white hover:text-gray-300"
					onclick={() => (previewImage = null)}
					aria-label="Close preview"
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
							d="M6 18L18 6M6 6l12 12"
						/>
					</svg>
				</button>
			</div>
		</div>
	{/if}
{/if}
