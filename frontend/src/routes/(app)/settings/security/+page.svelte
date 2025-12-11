<script lang="ts">
    import { fade, slide } from 'svelte/transition';

    let currentPassword = $state('');
    let newPassword = $state('');
    let confirmPassword = $state('');
    
    let is2FAEnabled = $state(false);
    let isSettingUp2FA = $state(false);
    let verificationCode = $state('');
    let showSetupSuccess = $state(false);
    
    // Dummy Data for Sessions
    let sessions = $state([
        {
            id: 1,
            device: 'Windows PC (Chrome)',
            location: 'Jakarta, Indonesia',
            ip: '192.168.1.1',
            lastActive: 'Active now',
            isCurrent: true,
            icon: 'desktop'
        },
        {
            id: 2,
            device: 'iPhone 13 (Safari)',
            location: 'Bandung, Indonesia',
            ip: '10.0.0.5',
            lastActive: '2 hours ago',
            isCurrent: false,
            icon: 'mobile'
        },
        {
            id: 3,
            device: 'MacBook Pro (Firefox)',
            location: 'Surabaya, Indonesia',
            ip: '172.16.0.2',
            lastActive: '3 days ago',
            isCurrent: false,
            icon: 'laptop'
        }
    ]);

    let isSaving = $state(false);

    function handlePasswordUpdate() {
        isSaving = true;
        setTimeout(() => {
            isSaving = false;
            // Clear passwords
            currentPassword = '';
            newPassword = '';
            confirmPassword = '';
        }, 1500);
    }

    function toggle2FA() {
        if (is2FAEnabled) {
            // Disable immediately if currently enabled
            is2FAEnabled = false;
            showSetupSuccess = false;
        } else {
            // Start setup flow if enabling
            isSettingUp2FA = true;
            verificationCode = '';
        }
    }
    
    function cancel2FASetup() {
        isSettingUp2FA = false;
        verificationCode = '';
    }

    function verifyAndEnable2FA() {
        // Simulate verification
        isSaving = true;
        setTimeout(() => {
            isSaving = false;
            is2FAEnabled = true;
            isSettingUp2FA = false;
            showSetupSuccess = true;
            setTimeout(() => showSetupSuccess = false, 3000);
        }, 1000);
    }

    function revokeSession(id: number) {
        sessions = sessions.filter(s => s.id !== id);
    }

    function logoutAllOtherSessions() {
        sessions = sessions.filter(s => s.isCurrent);
    }
</script>

<div in:fade class="max-w-4xl space-y-8">
	<div>
		<h1 class="text-2xl font-bold text-gray-900 dark:text-white">Security Settings</h1>
		<p class="text-gray-500 dark:text-gray-400 mt-1">
			Protect your account with advanced security features.
		</p>
	</div>

	<!-- Two-Factor Authentication -->
	<div
		class="bg-white dark:bg-neutral-800 p-8 rounded-2xl border border-gray-200 dark:border-white/5 shadow-sm space-y-6"
	>
		<div class="flex items-center justify-between">
			<div>
				<h3 class="text-lg font-semibold text-gray-900 dark:text-white">
					Two-Factor Authentication
				</h3>
				<p class="text-sm text-gray-500 dark:text-gray-400 mt-1 max-w-xl">
					Add an extra layer of security to your account by requiring a code from your
					authentication app (e.g., Google Authenticator) in addition to your password.
				</p>
			</div>

			<!-- Toggle Button -->
			<button
				onclick={toggle2FA}
				class="relative inline-flex h-8 w-14 items-center rounded-full transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:ring-offset-2 dark:focus:ring-offset-neutral-800"
				class:bg-blue-600={is2FAEnabled}
				class:bg-gray-200={!is2FAEnabled}
				class:dark:bg-neutral-700={!is2FAEnabled}
			>
				<span class="sr-only">Enable 2FA</span>
				<span
					class="inline-block h-6 w-6 transform rounded-full bg-white shadow-sm ring-0 transition-transform duration-300"
					class:translate-x-7={is2FAEnabled}
					class:translate-x-1={!is2FAEnabled}
				></span>
			</button>
		</div>

		<!-- Setup Flow -->
		{#if isSettingUp2FA}
			<div transition:slide class="pt-6 border-t border-gray-100 dark:border-white/5 space-y-6">
				<div class="grid grid-cols-1 md:grid-cols-2 gap-8">
					<div class="space-y-4">
						<div class="space-y-2">
							<h4 class="font-medium text-gray-900 dark:text-white">1. Scan QR Code</h4>
							<p class="text-sm text-gray-500 dark:text-gray-400">
								Open your authentication app (Google Authenticator, Authy, etc.) and scan this QR
								code.
							</p>
						</div>
						<div class="bg-white p-4 rounded-xl border border-gray-200 inline-block">
							<!-- Dummy QR Code placeholder -->
							<div
								class="w-40 h-40 bg-gray-900 flex items-center justify-center text-white text-xs text-center p-2"
							>
								[ QR CODE ]<br />Valid for 5:00
							</div>
						</div>
						<div class="text-xs text-gray-500">
							Can't scan? <button class="text-blue-600 hover:underline">View setup key</button>
						</div>
					</div>

					<div class="space-y-4">
						<div class="space-y-2">
							<h4 class="font-medium text-gray-900 dark:text-white">2. Enter Verification Code</h4>
							<p class="text-sm text-gray-500 dark:text-gray-400">
								Enter the 6-digit code generated by your app to verify setup.
							</p>
						</div>

						<div class="space-y-3">
							<input
								bind:value={verificationCode}
								type="text"
								placeholder="000 000"
								maxlength="6"
								class="w-full text-center text-2xl tracking-[0.5em] font-mono bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all uppercase"
							/>

							<div class="flex gap-3">
								<button
									onclick={cancel2FASetup}
									class="flex-1 px-4 py-2.5 rounded-xl text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-neutral-700 font-medium transition-colors"
								>
									Cancel
								</button>
								<button
									onclick={verifyAndEnable2FA}
									disabled={verificationCode.length < 6 || isSaving}
									class="flex-1 px-4 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors shadow-lg shadow-blue-500/20 font-medium disabled:opacity-70 disabled:cursor-not-allowed flex justify-center items-center gap-2"
								>
									{#if isSaving}
										<div
											class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"
										></div>
									{:else}
										Verify & Enable
									{/if}
								</button>
							</div>
						</div>
					</div>
				</div>
			</div>
		{/if}

		<!-- Active State -->
		{#if is2FAEnabled}
			<div transition:slide class="pt-4 border-t border-gray-100 dark:border-white/5">
				<div
					class="flex items-center gap-4 p-4 bg-green-50 dark:bg-green-500/10 text-green-800 dark:text-green-300 rounded-xl border border-green-100 dark:border-green-500/20"
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="w-6 h-6 shrink-0"
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
					<div>
						<p class="font-medium">Two-Factor Authentication is enabled</p>
						<p class="text-sm opacity-90">
							Your account is secured. You will need a code to log in from new devices.
						</p>
					</div>
				</div>
			</div>
		{/if}
	</div>

	<!-- Change Password -->
	<div
		class="bg-white dark:bg-neutral-800 p-8 rounded-2xl border border-gray-200 dark:border-white/5 shadow-sm space-y-6"
	>
		<h3
			class="text-lg font-semibold text-gray-900 dark:text-white border-b border-gray-100 dark:border-white/5 pb-4"
		>
			Change Password
		</h3>

		<div class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl">
			<div class="space-y-4">
				<div class="space-y-2">
					<label for="currentPass" class="text-sm font-medium text-gray-700 dark:text-neutral-300"
						>Current Password</label
					>
					<input
						bind:value={currentPassword}
						type="password"
						id="currentPass"
						class="w-full bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all"
					/>
				</div>
				<div class="space-y-2">
					<label for="newPass" class="text-sm font-medium text-gray-700 dark:text-neutral-300"
						>New Password</label
					>
					<input
						bind:value={newPassword}
						type="password"
						id="newPass"
						class="w-full bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all"
					/>
				</div>
				<div class="space-y-2">
					<label for="confirmPass" class="text-sm font-medium text-gray-700 dark:text-neutral-300"
						>Confirm New Password</label
					>
					<input
						bind:value={confirmPassword}
						type="password"
						id="confirmPass"
						class="w-full bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all"
					/>
				</div>
			</div>

			<div class="bg-gray-50 dark:bg-neutral-900/30 p-6 rounded-xl space-y-4">
				<h4 class="text-sm font-semibold text-gray-900 dark:text-white">Password Requirements</h4>
				<ul class="space-y-2 text-sm text-gray-600 dark:text-gray-400 list-disc pl-4">
					<li>Minimum 8 characters long</li>
					<li>At least one uppercase character</li>
					<li>At least one number</li>
					<li>At least one special character</li>
				</ul>
			</div>
		</div>

		<div class="pt-2">
			<button
				onclick={handlePasswordUpdate}
				disabled={isSaving || !currentPassword || !newPassword}
				class="px-6 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors shadow-lg shadow-blue-500/20 font-medium text-sm disabled:opacity-70 disabled:cursor-not-allowed flex items-center gap-2"
			>
				{#if isSaving}
					<div
						class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"
					></div>
					Updating...
				{:else}
					Update Password
				{/if}
			</button>
		</div>
	</div>

	<!-- Active Sessions -->
	<div
		class="bg-white dark:bg-neutral-800 p-8 rounded-2xl border border-gray-200 dark:border-white/5 shadow-sm space-y-6"
	>
		<div
			class="flex items-center justify-between border-b border-gray-100 dark:border-white/5 pb-4"
		>
			<div>
				<h3 class="text-lg font-semibold text-gray-900 dark:text-white">Active Sessions</h3>
				<p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
					Manage devices signed in to your account.
				</p>
			</div>
			{#if sessions.length > 1}
				<button
					onclick={logoutAllOtherSessions}
					class="text-sm font-medium text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 transition-colors"
				>
					Log out all other sessions
				</button>
			{/if}
		</div>

		<div class="space-y-4">
			{#each sessions as session (session.id)}
				<div
					class="flex items-center justify-between p-4 rounded-xl border border-gray-100 dark:border-white/5 hover:bg-gray-50 dark:hover:bg-mixed transition-colors"
					transition:slide
				>
					<div class="flex items-center gap-4">
						<div
							class="w-10 h-10 rounded-full bg-gray-100 dark:bg-neutral-700 flex items-center justify-center text-gray-500 dark:text-gray-400"
						>
							{#if session.icon === 'desktop'}
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
										d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
									/>
								</svg>
							{:else if session.icon === 'mobile'}
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
										d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"
									/>
								</svg>
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
										d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
									/>
								</svg>
							{/if}
						</div>
						<div>
							<p class="text-sm font-medium text-gray-900 dark:text-white">
								{session.device}
								{#if session.isCurrent}
									<span
										class="ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 dark:bg-green-500/20 text-green-800 dark:text-green-300"
										>Current</span
									>
								{/if}
							</p>
							<p class="text-xs text-gray-500 dark:text-gray-400">
								{session.location} • {session.ip} •
								<span
									class:text-green-600={session.isCurrent}
									class:dark:text-green-400={session.isCurrent}>{session.lastActive}</span
								>
							</p>
						</div>
					</div>

					{#if !session.isCurrent}
						<button
							onclick={() => revokeSession(session.id)}
							class="px-3 py-1.5 text-sm font-medium text-gray-600 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-500/10 rounded-lg transition-colors"
						>
							Revoke
						</button>
					{/if}
				</div>
			{/each}
		</div>
	</div>
</div>
