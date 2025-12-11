<script lang="ts">
    import { fade } from 'svelte/transition';

    const defaults = {
        firstName: 'Rizky',
        lastName: 'Hasan',
        username: 'rizky.hasan',
        email: 'rizky@example.com',
        role: 'Director',
        phone: '+62 812 3456 7890',
        bio: 'Software Engineer based in Jakarta. Loves coding and coffee.',
        location: 'Jakarta, Indonesia'
    };

    let firstName = $state(defaults.firstName);
    let lastName = $state(defaults.lastName);
    let username = $state(defaults.username);
    let email = $state(defaults.email);
    let role = $state(defaults.role);
    let phone = $state(defaults.phone);
    let bio = $state(defaults.bio);
    let location = $state(defaults.location);

    let isEditing = $state(false);
    let isSaving = $state(false);

    // Backup state for cancelling edits
    let originalState = { ...defaults };

    function toggleEdit() {
        if (!isEditing) {
            // Enter edit mode: backup current state
            originalState = { firstName, lastName, username, email, phone, bio, location, role };
        } else {
            // Cancel edit: restore original state
            ({ firstName, lastName, username, email, phone, bio, location, role } = originalState);
        }
        isEditing = !isEditing;
    }

    function handleSave() {
        isSaving = true;
        // Simulate API call
        setTimeout(() => {
            isSaving = false;
            isEditing = false;
            // Update backup state to new values
            originalState = { firstName, lastName, username, email, phone, bio, location, role };
        }, 1500);
    }
</script>

<div in:fade class="max-w-4xl space-y-8">
	<div class="flex justify-between items-start">
		<div>
			<h1 class="text-2xl font-bold text-gray-900 dark:text-white">Profile Settings</h1>
			<p class="text-gray-500 dark:text-gray-400 mt-1">Manage your account information.</p>
		</div>
		{#if !isEditing}
			<button
				onclick={toggleEdit}
				class="px-5 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors shadow-lg shadow-blue-500/20 font-medium text-sm flex items-center gap-2"
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
						d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"
					/>
				</svg>
				Edit Profile
			</button>
		{/if}
	</div>

	<!-- Profile Header & Avatar -->
	<div
		class="bg-white dark:bg-neutral-800 p-8 rounded-2xl border border-gray-200 dark:border-white/5 shadow-sm flex flex-col md:flex-row items-start md:items-center gap-6"
	>
		<div class="relative group">
			<div
				class="w-24 h-24 rounded-full bg-gradient-to-tr from-blue-500 to-purple-600 flex items-center justify-center text-white text-3xl font-bold shadow-lg"
			>
				{firstName[0]}{lastName[0]}
			</div>
			{#if isEditing}
				<button
					class="absolute bottom-0 right-0 p-2 bg-white dark:bg-neutral-700 rounded-full border border-gray-200 dark:border-white/10 shadow-sm hover:bg-gray-50 dark:hover:bg-neutral-600 transition-colors"
					title="Change Avatar"
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="w-4 h-4 text-gray-600 dark:text-gray-300"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"
						/>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"
						/>
					</svg>
				</button>
			{/if}
		</div>
		<div class="flex-1">
			<h3 class="text-lg font-semibold text-gray-900 dark:text-white">{firstName} {lastName}</h3>
			<p class="text-sm text-gray-500 dark:text-gray-400">{role} • {location}</p>
		</div>
		{#if isEditing}
			<div class="flex gap-3">
				<button
					class="px-4 py-2 bg-white dark:bg-neutral-700 border border-gray-200 dark:border-white/10 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-50 dark:hover:bg-neutral-600 transition-colors text-sm font-medium"
				>
					Remove
				</button>
				<button
					class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-lg shadow-blue-500/20 font-medium text-sm"
				>
					Change Photo
				</button>
			</div>
		{/if}
	</div>

	<!-- Personal Information -->
	<div
		class="bg-white dark:bg-neutral-800 p-8 rounded-2xl border border-gray-200 dark:border-white/5 shadow-sm space-y-6"
	>
		<h2
			class="text-lg font-semibold text-gray-900 dark:text-white border-b border-gray-100 dark:border-white/5 pb-4"
		>
			Personal Information
		</h2>

		<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
			<!-- First Name -->
			<div class="space-y-2">
				<p class="text-sm font-medium text-gray-500 dark:text-gray-400">First Name</p>
				{#if isEditing}
					<input
						bind:value={firstName}
						type="text"
						class="w-full bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all"
					/>
				{:else}
					<p class="text-gray-900 dark:text-white font-medium">{firstName}</p>
				{/if}
			</div>

			<!-- Last Name -->
			<div class="space-y-2">
				<p class="text-sm font-medium text-gray-500 dark:text-gray-400">Last Name</p>
				{#if isEditing}
					<input
						bind:value={lastName}
						type="text"
						class="w-full bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all"
					/>
				{:else}
					<p class="text-gray-900 dark:text-white font-medium">{lastName}</p>
				{/if}
			</div>

			<!-- Email -->
			<div class="space-y-2">
				<p class="text-sm font-medium text-gray-500 dark:text-gray-400">Email Address</p>
				{#if isEditing}
					<div class="relative">
						<span class="absolute left-4 top-3 text-gray-400">
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
									d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
								/>
							</svg>
						</span>
						<input
							bind:value={email}
							type="email"
							class="w-full pl-11 bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all"
						/>
					</div>
				{:else}
					<p class="text-gray-900 dark:text-white font-medium">{email}</p>
				{/if}
			</div>

			<!-- Phone -->
			<div class="space-y-2">
				<p class="text-sm font-medium text-gray-500 dark:text-gray-400">Phone Number</p>
				{#if isEditing}
					<input
						bind:value={phone}
						type="tel"
						class="w-full bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all"
					/>
				{:else}
					<p class="text-gray-900 dark:text-white font-medium">{phone}</p>
				{/if}
			</div>

			<!-- Username -->
			<div class="space-y-2">
				<p class="text-sm font-medium text-gray-500 dark:text-gray-400">Username</p>
				{#if isEditing}
					<div class="relative">
						<span class="absolute left-4 top-2.5 text-gray-400 select-none">@</span>
						<input
							bind:value={username}
							type="text"
							class="w-full pl-9 bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all"
						/>
					</div>
				{:else}
					<p class="text-gray-900 dark:text-white font-medium">@{username}</p>
				{/if}
			</div>

			<!-- Role (Read Only) -->
			<div class="space-y-2">
				<p class="text-sm font-medium text-gray-500 dark:text-gray-400">Role</p>
				<div class="flex items-center">
					<span
						class="px-3 py-1 bg-blue-100 dark:bg-blue-500/20 text-blue-700 dark:text-blue-300 rounded-lg text-sm font-medium"
					>
						{role}
					</span>
				</div>
			</div>

			<!-- Location -->
			<div class="space-y-2 md:col-span-2">
				<p class="text-sm font-medium text-gray-500 dark:text-gray-400">Location</p>
				{#if isEditing}
					<input
						bind:value={location}
						type="text"
						class="w-full bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all"
						placeholder="City, Country"
					/>
				{:else}
					<p class="text-gray-900 dark:text-white font-medium">{location}</p>
				{/if}
			</div>

			<!-- Bio -->
			<div class="space-y-2 md:col-span-2">
				<p class="text-sm font-medium text-gray-500 dark:text-gray-400">Bio</p>
				{#if isEditing}
					<textarea
						bind:value={bio}
						rows="3"
						class="w-full bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all resize-none"
						placeholder="Tell us a little about yourself..."
					></textarea>
					<p class="text-xs text-gray-400 text-right">Brief description for your profile.</p>
				{:else}
					<p class="text-gray-900 dark:text-white leading-relaxed">{bio}</p>
				{/if}
			</div>
		</div>

		<!-- Action Buttons -->
		{#if isEditing}
			<div
				class="flex justify-end gap-3 pt-4 border-t border-gray-100 dark:border-white/5 mt-4"
				transition:fade
			>
				<button
					onclick={toggleEdit}
					class="px-6 py-2.5 rounded-xl text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-neutral-700 font-medium transition-colors"
				>
					Cancel
				</button>
				<button
					onclick={handleSave}
					disabled={isSaving}
					class="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-medium shadow-lg shadow-blue-500/20 active:scale-95 transition-all flex items-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
				>
					{#if isSaving}
						<div
							class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"
						></div>
						Saving...
					{:else}
						Save Changes
					{/if}
				</button>
			</div>
		{/if}
	</div>
</div>
