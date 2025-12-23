<script lang="ts">
	import { onMount } from 'svelte';
	import { theme } from '$lib/stores/theme';
	import { fade } from 'svelte/transition';
	import ThemeToggle from '$lib/components/ThemeToggle.svelte';

	let isLoading = $state(false);

	async function handleLogin(event: Event) {
		event.preventDefault();
		isLoading = true;

		try {
            // Get form data
            const email = (document.getElementById('email') as HTMLInputElement).value;
            const password = (document.getElementById('password') as HTMLInputElement).value;

            const formData = new FormData();
            formData.append('username', email); // OAuth2 expects 'username' field
            formData.append('password', password);

			const response = await fetch('http://localhost:8000/api/v1/auth/login', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                alert(errorData.detail || 'Login failed');
                isLoading = false;
                return;
            }

            const data = await response.json();
            // Store token
            localStorage.setItem('access_token', data.access_token);
            
			isLoading = false;
			// Redirect
			window.location.href = '/dashboard';
		} catch (error) {
            console.error(error);
            alert('An error occurred during login');
			isLoading = false;
		}
	}
</script>

<div
	class="min-h-screen bg-gray-50 dark:bg-neutral-900 flex items-center justify-center p-4 transition-colors duration-300"
>
	<!-- Theme Toggle -->
	<div class="absolute top-6 right-6 z-50">
		<ThemeToggle />
	</div>

	<!-- Interactive Background Elements -->
	<div class="absolute inset-0 overflow-hidden pointer-events-none">
		<div
			class="absolute -top-[20%] -left-[10%] w-[50%] h-[50%] bg-blue-500/10 rounded-full blur-3xl animate-pulse dark:bg-blue-500/10 bg-blue-600/5"
		></div>
		<div
			class="absolute top-[40%] right-[10%] w-[40%] h-[40%] bg-purple-500/10 rounded-full blur-3xl animate-pulse delay-1000 dark:bg-purple-500/10 bg-purple-600/5"
		></div>
	</div>

	<div
		class="w-full max-w-md bg-white/70 dark:bg-neutral-800/50 backdrop-blur-xl border border-gray-200 dark:border-white/10 rounded-2xl shadow-2xl dark:shadow-none p-8 relative z-10 transition-colors duration-300"
	>
		<div class="text-center mb-10">
			<h1
				class="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent mb-2"
			>
				Welcome Back
			</h1>
			<p class="text-gray-500 dark:text-neutral-400">Sign in to access your dashboard</p>
		</div>

		<form onsubmit={handleLogin} class="space-y-6">
			<div class="space-y-2">
				<label for="email" class="text-sm font-medium text-gray-700 dark:text-neutral-300 ml-1"
					>Email Address</label
				>
				<div class="relative">
					<input
						type="email"
						id="email"
						placeholder="name@company.com"
						class="w-full bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white placeholder:text-gray-400 dark:placeholder:text-neutral-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-200"
						required
					/>
				</div>
			</div>

			<div class="space-y-2">
				<div class="flex justify-between items-center ml-1">
					<label for="password" class="text-sm font-medium text-gray-700 dark:text-neutral-300"
						>Password</label
					>
					<a
						href="/forgot-password"
						class="text-xs text-blue-600 dark:text-blue-400 hover:text-blue-500 dark:hover:text-blue-300 transition-colors"
						>Forgot password?</a
					>
				</div>
				<div class="relative">
					<input
						type="password"
						id="password"
						placeholder="••••••••"
						class="w-full bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white placeholder:text-gray-400 dark:placeholder:text-neutral-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-200"
						required
					/>
				</div>
			</div>

			<button
				type="submit"
				disabled={isLoading}
				class="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 dark:hover:from-blue-500 dark:hover:to-purple-500 text-white font-semibold py-3.5 rounded-xl shadow-lg shadow-blue-500/20 active:scale-[0.98] transition-all duration-200 disabled:opacity-70 disabled:cursor-not-allowed flex justify-center items-center group"
			>
				{#if isLoading}
					<div
						class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"
					></div>
				{:else}
					Sign In
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-5 w-5 ml-2 group-hover:translate-x-1 transition-transform"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M14 5l7 7m0 0l-7 7m7-7H3"
						/>
					</svg>
				{/if}
			</button>
		</form>

		<div class="mt-8 pt-6 border-t border-gray-200 dark:border-white/10 text-center">
			<p class="text-gray-500 dark:text-neutral-400 text-sm">
				Don't have an account?
				<a
					href="/register"
					class="text-gray-900 dark:text-white hover:underline decoration-blue-500 underline-offset-4"
					>Create account</a
				>
			</p>
		</div>
	</div>
</div>
