<script lang="ts">
    import { page } from '$app/stores';
    import { fade, fly } from 'svelte/transition';

    // Get category from URL params
    let category = $derived($page.params.category ?? '');
    
    // Map slug to display title
    const categoryTitles: Record<string, string> = {
        'statement': 'Statement',
        'stock-info': 'Stock Information',
        'other': 'Other'
    };

    let displayTitle = $derived(categoryTitles[category] || 'Broadcast');

    let title = $state('');
    let message = $state('');
    let target = $state('All Users');
    let channels = $state(['In-App']);
    let isSending = $state(false);
    let showSuccess = $state(false);

    // Mock History (Shared structure, filtered by category in real app)
    let history = $state([
        { id: 1, category: 'statement', title: 'Monthly Statement Available', target: 'All Users', date: '2023-10-25 14:00', status: 'Sent' },
        { id: 2, category: 'stock-info', title: 'Stock Market Update', target: 'Active Users', date: '2023-10-24 09:00', status: 'Sent' },
        { id: 3, category: 'other', title: 'System Maintenance', target: 'All Users', date: '2023-10-20 09:30', status: 'Sent' },
    ]);

    // Filter history for current category
    let filteredHistory = $derived(history.filter(h => h.category === category));

    function toggleChannel(channel: string) {
        if (channels.includes(channel)) {
            channels = channels.filter(c => c !== channel);
        } else {
            channels = [...channels, channel];
        }
    }

    function handleSend() {
        if (!title || !message || channels.length === 0) return;

        isSending = true;
        
        setTimeout(() => {
            isSending = false;
            showSuccess = true;
            
            // Add to history
            history = [{
                id: history.length + 1,
                category: category,
                title: title,
                target: target,
                date: new Date().toLocaleString(),
                status: 'Sent'
            }, ...history];

            // Reset form
            title = '';
            message = '';
            channels = ['In-App'];
            
            setTimeout(() => {
                showSuccess = false;
            }, 3000);
        }, 1500);
    }
</script>

<div in:fade class="max-w-4xl space-y-8">
	<div class="flex justify-between items-start">
		<div>
			<h1 class="text-2xl font-bold text-gray-900 dark:text-white">Broadcast: {displayTitle}</h1>
			<p class="text-gray-500 dark:text-gray-400 mt-1">
				Send {displayTitle.toLowerCase()} announcements to your users.
			</p>
		</div>
	</div>

	<!-- Compose Area -->
	<div
		class="bg-white dark:bg-neutral-800 p-8 rounded-2xl border border-gray-200 dark:border-white/5 shadow-sm space-y-6"
	>
		<h2
			class="text-lg font-semibold text-gray-900 dark:text-white border-b border-gray-100 dark:border-white/5 pb-4"
		>
			Compose {displayTitle}
		</h2>

		<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
			<!-- Target Audience -->
			<div class="space-y-2">
				<label for="target" class="text-sm font-medium text-gray-700 dark:text-neutral-300"
					>Target Audience</label
				>
				<select
					bind:value={target}
					id="target"
					class="w-full bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50"
				>
					<option value="All Users">All Users</option>
					<option value="Director">Directors</option>
					<option value="Manager">Managers</option>
					<option value="Admin">Admins</option>
					<option value="Staff">Staff</option>
					<option value="Active Users">Active Users Only</option>
				</select>
			</div>

			<!-- Channels -->
			<div class="space-y-2">
				<span class="text-sm font-medium text-gray-700 dark:text-neutral-300 block mb-2"
					>Channels</span
				>
				<div class="flex gap-3" role="group" aria-label="Select Channels">
					{#each ['Email', 'Push', 'In-App'] as channel}
						<button
							onclick={() => toggleChannel(channel)}
							class="px-4 py-2 rounded-xl text-sm font-medium border transition-colors flex items-center gap-2
                                {channels.includes(channel)
								? 'bg-blue-600 text-white border-blue-600'
								: 'bg-white dark:bg-neutral-900/50 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-white/10 hover:bg-gray-50 dark:hover:bg-neutral-800'}"
						>
							{#if channels.includes(channel)}
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="w-4 h-4"
									viewBox="0 0 20 20"
									fill="currentColor"
								>
									<path
										fill-rule="evenodd"
										d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
										clip-rule="evenodd"
									/>
								</svg>
							{/if}
							{channel}
						</button>
					{/each}
				</div>
			</div>

			<!-- Subject -->
			<div class="space-y-2 md:col-span-2">
				<label for="title" class="text-sm font-medium text-gray-700 dark:text-neutral-300"
					>Subject</label
				>
				<input
					bind:value={title}
					type="text"
					id="title"
					class="w-full bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50"
					placeholder="e.g., Important Update"
				/>
			</div>

			<!-- Message Body -->
			<div class="space-y-2 md:col-span-2">
				<label for="message" class="text-sm font-medium text-gray-700 dark:text-neutral-300"
					>Message</label
				>
				<textarea
					bind:value={message}
					id="message"
					rows="6"
					class="w-full bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 resize-none"
					placeholder="Write your message here..."
				></textarea>
			</div>
		</div>

		<!-- Action Bar -->
		<div class="flex justify-end pt-4 border-t border-gray-100 dark:border-white/5">
			<button
				onclick={handleSend}
				disabled={!title || !message || channels.length === 0 || isSending}
				class="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl shadow-lg shadow-blue-500/20 font-medium disabled:opacity-70 disabled:cursor-not-allowed flex items-center gap-2 transition-all"
			>
				{#if isSending}
					<div
						class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"
					></div>
					Sending...
				{:else}
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
							d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
						/>
					</svg>
					Send Broadcast
				{/if}
			</button>
		</div>
	</div>

	<!-- History -->
	<div
		class="bg-white dark:bg-neutral-800 p-8 rounded-2xl border border-gray-200 dark:border-white/5 shadow-sm space-y-6"
	>
		<div class="flex items-center justify-between">
			<h2 class="text-lg font-semibold text-gray-900 dark:text-white">
				Recent {displayTitle} Broadcasts
			</h2>
			<button class="text-sm text-blue-600 dark:text-blue-400 font-medium hover:underline"
				>View All</button
			>
		</div>

		<div class="overflow-x-auto">
			<table class="w-full text-left">
				<thead
					class="bg-gray-50 dark:bg-neutral-900/30 border-b border-gray-200 dark:border-white/5"
				>
					<tr>
						<th class="px-6 py-4 text-sm font-semibold text-gray-900 dark:text-white">Subject</th>
						<th class="px-6 py-4 text-sm font-semibold text-gray-900 dark:text-white">Target</th>
						<th class="px-6 py-4 text-sm font-semibold text-gray-900 dark:text-white">Date Sent</th>
						<th class="px-6 py-4 text-sm font-semibold text-gray-900 dark:text-white text-right"
							>Status</th
						>
					</tr>
				</thead>
				<tbody class="divide-y divide-gray-200 dark:divide-white/5">
					{#each filteredHistory as item}
						<tr class="hover:bg-gray-50 dark:hover:bg-neutral-700/30 transition-colors">
							<td class="px-6 py-4 text-gray-900 dark:text-white font-medium">{item.title}</td>
							<td class="px-6 py-4">
								<span
									class="px-2.5 py-1 rounded-lg text-xs font-medium bg-gray-100 dark:bg-gray-500/20 text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-500/20"
								>
									{item.target}
								</span>
							</td>
							<td class="px-6 py-4 text-gray-500 dark:text-gray-400 text-sm">{item.date}</td>
							<td class="px-6 py-4 text-right">
								<span
									class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-green-100 dark:bg-green-500/20 text-green-700 dark:text-green-300 border border-green-200 dark:border-green-500/20"
								>
									<span class="w-1.5 h-1.5 rounded-full bg-green-600 dark:bg-green-400"></span>
									{item.status}
								</span>
							</td>
						</tr>
					{/each}
					{#if filteredHistory.length === 0}
						<tr>
							<td colspan="4" class="px-6 py-8 text-center text-gray-500 dark:text-gray-400">
								No recent broadcasts in this category.
							</td>
						</tr>
					{/if}
				</tbody>
			</table>
		</div>
	</div>
</div>

{#if showSuccess}
	<div
		class="fixed bottom-6 right-6 bg-green-600 text-white px-6 py-3 rounded-xl shadow-lg flex items-center gap-3"
		in:fly={{ y: 20 }}
		out:fade
	>
		<svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
			<path
				fill-rule="evenodd"
				d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
				clip-rule="evenodd"
			/>
		</svg>
		<span class="font-medium">Broadcast message sent successfully!</span>
	</div>
{/if}
