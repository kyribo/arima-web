<script lang="ts">
    import { fade } from 'svelte/transition';

    let emailNotifications = $state({
        news: true,
        account: true,
        marketing: false,
        security: true
    });

    let pushNotifications = $state({
        newComments: true,
        mentions: true,
        directMessages: true
    });

    let isSaving = $state(false);

    function handleSave() {
        isSaving = true;
        setTimeout(() => {
            isSaving = false;
        }, 1000);
    }
</script>

<div in:fade class="max-w-4xl space-y-8">
	<div>
		<h1 class="text-2xl font-bold text-gray-900 dark:text-white">Notification Settings</h1>
		<p class="text-gray-500 dark:text-gray-400 mt-1">
			Manage how and when you receive notifications.
		</p>
	</div>

	<!-- Email Notifications -->
	<div
		class="bg-white dark:bg-neutral-800 p-8 rounded-2xl border border-gray-200 dark:border-white/5 shadow-sm space-y-6"
	>
		<div class="border-b border-gray-100 dark:border-white/5 pb-4">
			<h3 class="text-lg font-semibold text-gray-900 dark:text-white">Email Notifications</h3>
			<p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
				Select which emails you'd like to receive.
			</p>
		</div>

		<div class="space-y-4">
			<label
				class="flex items-center justify-between p-3 rounded-xl hover:bg-gray-50 dark:hover:bg-neutral-700/50 transition-colors cursor-pointer group"
			>
				<div>
					<p class="font-medium text-gray-900 dark:text-white">Account Activity</p>
					<p class="text-sm text-gray-500 dark:text-gray-400">
						Get notified about changes to your account settings.
					</p>
				</div>
				<div
					class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:ring-offset-2 dark:focus:ring-offset-neutral-800"
					class:bg-blue-600={emailNotifications.account}
					class:bg-gray-200={!emailNotifications.account}
					class:dark:bg-neutral-700={!emailNotifications.account}
				>
					<input type="checkbox" bind:checked={emailNotifications.account} class="sr-only" />
					<span
						class="inline-block h-4 w-4 transform rounded-full bg-white transition-transform"
						class:translate-x-6={emailNotifications.account}
						class:translate-x-1={!emailNotifications.account}
					></span>
				</div>
			</label>

			<label
				class="flex items-center justify-between p-3 rounded-xl hover:bg-gray-50 dark:hover:bg-neutral-700/50 transition-colors cursor-pointer group"
			>
				<div>
					<p class="font-medium text-gray-900 dark:text-white">Security Alerts</p>
					<p class="text-sm text-gray-500 dark:text-gray-400">
						Receive emails about suspicious activity (Recommended).
					</p>
				</div>
				<div
					class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:ring-offset-2 dark:focus:ring-offset-neutral-800"
					class:bg-blue-600={emailNotifications.security}
					class:bg-gray-200={!emailNotifications.security}
					class:dark:bg-neutral-700={!emailNotifications.security}
				>
					<input type="checkbox" bind:checked={emailNotifications.security} class="sr-only" />
					<span
						class="inline-block h-4 w-4 transform rounded-full bg-white transition-transform"
						class:translate-x-6={emailNotifications.security}
						class:translate-x-1={!emailNotifications.security}
					></span>
				</div>
			</label>

			<label
				class="flex items-center justify-between p-3 rounded-xl hover:bg-gray-50 dark:hover:bg-neutral-700/50 transition-colors cursor-pointer group"
			>
				<div>
					<p class="font-medium text-gray-900 dark:text-white">Product Updates</p>
					<p class="text-sm text-gray-500 dark:text-gray-400">
						Be the first to know about new features and improvements.
					</p>
				</div>
				<div
					class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:ring-offset-2 dark:focus:ring-offset-neutral-800"
					class:bg-blue-600={emailNotifications.news}
					class:bg-gray-200={!emailNotifications.news}
					class:dark:bg-neutral-700={!emailNotifications.news}
				>
					<input type="checkbox" bind:checked={emailNotifications.news} class="sr-only" />
					<span
						class="inline-block h-4 w-4 transform rounded-full bg-white transition-transform"
						class:translate-x-6={emailNotifications.news}
						class:translate-x-1={!emailNotifications.news}
					></span>
				</div>
			</label>
		</div>
	</div>

	<!-- Push Notifications -->
	<div
		class="bg-white dark:bg-neutral-800 p-8 rounded-2xl border border-gray-200 dark:border-white/5 shadow-sm space-y-6"
	>
		<div class="border-b border-gray-100 dark:border-white/5 pb-4">
			<h3 class="text-lg font-semibold text-gray-900 dark:text-white">Push Notifications</h3>
			<p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
				Get real-time updates in your browser.
			</p>
		</div>

		<div class="space-y-4">
			<label
				class="flex items-center justify-between p-3 rounded-xl hover:bg-gray-50 dark:hover:bg-neutral-700/50 transition-colors cursor-pointer group"
			>
				<div>
					<p class="font-medium text-gray-900 dark:text-white">New Comments</p>
					<p class="text-sm text-gray-500 dark:text-gray-400">
						Notify me when someone comments on my posts.
					</p>
				</div>
				<div
					class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:ring-offset-2 dark:focus:ring-offset-neutral-800"
					class:bg-blue-600={pushNotifications.newComments}
					class:bg-gray-200={!pushNotifications.newComments}
					class:dark:bg-neutral-700={!pushNotifications.newComments}
				>
					<input type="checkbox" bind:checked={pushNotifications.newComments} class="sr-only" />
					<span
						class="inline-block h-4 w-4 transform rounded-full bg-white transition-transform"
						class:translate-x-6={pushNotifications.newComments}
						class:translate-x-1={!pushNotifications.newComments}
					></span>
				</div>
			</label>

			<label
				class="flex items-center justify-between p-3 rounded-xl hover:bg-gray-50 dark:hover:bg-neutral-700/50 transition-colors cursor-pointer group"
			>
				<div>
					<p class="font-medium text-gray-900 dark:text-white">Mentions</p>
					<p class="text-sm text-gray-500 dark:text-gray-400">Notify me when I am mentioned.</p>
				</div>
				<div
					class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:ring-offset-2 dark:focus:ring-offset-neutral-800"
					class:bg-blue-600={pushNotifications.mentions}
					class:bg-gray-200={!pushNotifications.mentions}
					class:dark:bg-neutral-700={!pushNotifications.mentions}
				>
					<input type="checkbox" bind:checked={pushNotifications.mentions} class="sr-only" />
					<span
						class="inline-block h-4 w-4 transform rounded-full bg-white transition-transform"
						class:translate-x-6={pushNotifications.mentions}
						class:translate-x-1={!pushNotifications.mentions}
					></span>
				</div>
			</label>
		</div>

		<div class="pt-4 border-t border-gray-100 dark:border-white/5 flex justify-end">
			<button
				onclick={handleSave}
				disabled={isSaving}
				class="px-6 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors shadow-lg shadow-blue-500/20 font-medium text-sm disabled:opacity-70 disabled:cursor-not-allowed flex items-center gap-2"
			>
				{#if isSaving}
					<div
						class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"
					></div>
					Saving...
				{:else}
					Save Preferences
				{/if}
			</button>
		</div>
	</div>
</div>
