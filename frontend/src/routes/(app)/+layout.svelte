<script lang="ts">
  import ThemeToggle from '$lib/components/ThemeToggle.svelte';
  import { menuItems, type MenuItem } from '$lib/config/navigation';
  import { user } from '$lib/stores/user';
  import { page } from '$app/stores';
  import { fade, slide } from 'svelte/transition';
  import { goto } from '$app/navigation';
  import { browser } from '$app/environment';

  let { children } = $props();
  
  // Sidebar state
  let isSidebarCollapsed = $state(false);
  let isMobileMenuOpen = $state(false);
  let expandedMenus = $state<string[]>([]);
  let isCheckingAuth = $state(true);

  $effect(() => {
    // 1. Basic Protection: Check if token exists
    if (browser) {
        const token = localStorage.getItem('access_token');
        if (!token) {
            goto('/');
            return;
        }
        isCheckingAuth = false;
    }
    // 2. Fetch user profile
    user.fetch();
  });

  function toggleSidebar() {
    isSidebarCollapsed = !isSidebarCollapsed;
  }

  function toggleMobileMenu() {
    isMobileMenuOpen = !isMobileMenuOpen;
  }

  function closeMobileMenu() {
    isMobileMenuOpen = false;
  }

  function toggleMenu(name: string) {
    if (isSidebarCollapsed) {
      isSidebarCollapsed = false;
      setTimeout(() => {
         if (!expandedMenus.includes(name)) expandedMenus = [...expandedMenus, name];
      }, 150);
      return;
    }
    
    if (expandedMenus.includes(name)) {
      expandedMenus = expandedMenus.filter(m => m !== name);
    } else {
      expandedMenus = [...expandedMenus, name];
    }
  }
  
  /* Automatically expand menu if child is active */
  $effect(() => {
    const currentPath = $page.url.pathname;
    
    // Close mobile menu on navigation
    isMobileMenuOpen = false;

    menuItems.forEach(item => {
      if (item.children && item.children.some(child => currentPath.startsWith(child.href))) {
         if (!expandedMenus.includes(item.name) && !isSidebarCollapsed) {
           expandedMenus = [...expandedMenus, item.name];
         }
      }
    });
  });
</script>

{#if isCheckingAuth}
	<!-- Full Screen Loader to prevent FOUC -->
	<div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-neutral-900">
		<!-- Optional: Add a logo or spinner here -->
	</div>
{:else}
	<div class="min-h-screen bg-gray-50 dark:bg-neutral-900 flex transition-colors duration-300">
		<!-- Mobile Menu Overlay -->
		{#if isMobileMenuOpen}
			<button
				class="fixed inset-0 bg-black/50 z-20 md:hidden backdrop-blur-sm"
				onclick={closeMobileMenu}
				transition:fade={{ duration: 200 }}
				aria-label="Close menu"
			></button>
		{/if}

		<!-- Sidebar -->
		<aside
			class="fixed inset-y-0 left-0 bg-white dark:bg-neutral-800 border-r border-gray-200 dark:border-white/5 z-30 flex flex-col transition-all duration-300 transform md:transform-none
    	{isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
    	{isSidebarCollapsed ? 'w-64 md:w-20' : 'w-64'}"
		>
			<!-- Logo -->
			<div
				class="h-16 flex items-center {isSidebarCollapsed
					? 'justify-center'
					: 'px-6'} border-b border-gray-200 dark:border-white/5 relative"
			>
				<div
					class="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-500 shrink-0"
				></div>
				{#if !isSidebarCollapsed}
					<span
						class="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent ml-3"
						transition:fade={{ duration: 100 }}
					>
						Arima
					</span>
				{/if}
				<!-- Close button for mobile -->
				<button
					class="md:hidden absolute right-4 text-gray-500"
					onclick={closeMobileMenu}
					aria-label="Close Mobile Menu"
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
							d="M6 18L18 6M6 6l12 12"
						/>
					</svg>
				</button>
			</div>

			<!-- Navigation -->
			<nav class="flex-1 px-3 py-6 space-y-1 overflow-y-auto custom-scrollbar">
				{#snippet menuItem(item: MenuItem, level = 0)}
					{@const visibleChildren = item.children?.filter((c) => !c.hidden) || []}
					{@const hasChildren = visibleChildren.length > 0}
					{@const isExpanded = expandedMenus.includes(item.name)}

					<!-- Check simplified active state - checking sub-items RECURSIVELY -->
					<!-- Note: In a real app we might want a recursive helper function for this check -->
					{@const isActive =
						$page.url.pathname === item.href ||
						(hasChildren &&
							(item.children!.some((c) => $page.url.pathname.startsWith(c.href)) ||
								item.children!.some(
									(c) =>
										c.children && c.children.some((gc) => $page.url.pathname.startsWith(gc.href))
								)))}

					<div>
						{#if hasChildren}
							<button
								onclick={() => toggleMenu(item.name)}
								class="w-full flex items-center {isSidebarCollapsed && level === 0 // Collapsed only affects top level centering
									? 'justify-center px-0'
									: 'px-4'} py-3 rounded-xl transition-all duration-200 group relative {isActive
									? 'bg-blue-50/50 dark:bg-blue-500/5 text-blue-600 dark:text-blue-400 font-medium'
									: 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-neutral-700/50 hover:text-gray-900 dark:hover:text-gray-200'}"
								title={isSidebarCollapsed ? item.name : ''}
							>
								{#if item.icon}
									<svg
										xmlns="http://www.w3.org/2000/svg"
										class="w-6 h-6 shrink-0 {isActive
											? 'text-blue-600 dark:text-blue-400'
											: 'text-gray-400 dark:text-gray-500 group-hover:text-gray-500 dark:group-hover:text-gray-300'}"
										fill="none"
										viewBox="0 0 24 24"
										stroke="currentColor"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d={item.icon}
										/>
									</svg>
								{/if}

								<!-- For sub-menus (level > 0), if no icon, maybe some indentation or dot? 
                                 Current design just implies text. But we moved items with icons INTO Trans Data.
                                 So we should probably render icons if they exist, even in submenus. 
                            -->

								{#if !isSidebarCollapsed}
									<span class="ml-3 truncate flex-1 text-left" transition:fade={{ duration: 100 }}
										>{item.name}</span
									>
									<svg
										xmlns="http://www.w3.org/2000/svg"
										class="w-4 h-4 ml-2 transition-transform duration-200 {isExpanded
											? 'rotate-180'
											: ''}"
										fill="none"
										viewBox="0 0 24 24"
										stroke="currentColor"
										transition:fade={{ duration: 100 }}
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M19 9l-7 7-7-7"
										/>
									</svg>
								{/if}
							</button>

							{#if isExpanded && !isSidebarCollapsed}
								<div
									class="ml-4 pl-4 border-l border-gray-200 dark:border-white/10 mt-1 space-y-1"
									transition:slide={{ duration: 200 }}
								>
									{#each visibleChildren as child}
										{@render menuItem(child, level + 1)}
									{/each}
								</div>
							{/if}
						{:else}
							<!-- Standard Menu Item -->
							<a
								href={item.href}
								class="flex items-center {isSidebarCollapsed && level === 0
									? 'justify-center px-0'
									: 'px-4'} py-3 rounded-xl transition-all duration-200 group relative {isActive
									? 'bg-blue-50 dark:bg-blue-500/10 text-blue-600 dark:text-blue-400 font-medium'
									: 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-neutral-700/50 hover:text-gray-900 dark:hover:text-gray-200'}"
								title={isSidebarCollapsed ? item.name : ''}
							>
								{#if item.icon}
									<svg
										xmlns="http://www.w3.org/2000/svg"
										class="w-6 h-6 shrink-0 {isActive
											? 'text-blue-600 dark:text-blue-400'
											: 'text-gray-400 dark:text-gray-500 group-hover:text-gray-500 dark:group-hover:text-gray-300'}"
										fill="none"
										viewBox="0 0 24 24"
										stroke="currentColor"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d={item.icon}
										/>
									</svg>
								{/if}
								{#if !isSidebarCollapsed}
									<span
										class="{item.icon ? 'ml-3' : ''} truncate"
										transition:fade={{ duration: 100 }}>{item.name}</span
									>
								{/if}
							</a>
						{/if}
					</div>
				{/snippet}

				{#each menuItems.filter((i) => !i.hidden) as item}
					{@render menuItem(item)}
				{/each}
			</nav>

			<!-- User Profile (Bottom) -->
			<div class="p-4 border-t border-gray-200 dark:border-white/5">
				<button
					onclick={user.logout}
					class="w-full flex items-center {isSidebarCollapsed
						? 'justify-center'
						: 'gap-3'} p-2 rounded-xl hover:bg-red-50 dark:hover:bg-red-500/10 transition-colors cursor-pointer group text-left relative"
					title="Sign Out"
				>
					<div
						class="w-9 h-9 rounded-full bg-gradient-to-tr from-yellow-400 to-orange-500 shrink-0"
					></div>
					{#if !isSidebarCollapsed}
						<div class="flex-1 min-w-0" transition:fade={{ duration: 100 }}>
							<p
								class="text-sm font-medium text-gray-900 dark:text-white group-hover:text-red-600 dark:group-hover:text-red-400 truncate"
							>
								{$user
									? $user.first_name
										? `${$user.first_name} ${$user.last_name || ''}`
										: $user.username
									: 'Loading...'}
							</p>
							<p
								class="text-xs text-gray-500 dark:text-gray-400 group-hover:text-red-500/70 dark:group-hover:text-red-400/70 truncate"
							>
								Sign Out
							</p>
						</div>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="w-5 h-5 text-gray-400 group-hover:text-red-500 transition-colors"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							transition:fade={{ duration: 100 }}
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
							/>
						</svg>
					{/if}
				</button>
			</div>
		</aside>

		<!-- Main Content -->
		<main
			class="flex-1 min-h-screen flex flex-col transition-all duration-300 {isSidebarCollapsed
				? 'md:ml-20'
				: 'md:ml-64'}"
		>
			<!-- Header -->
			<header
				class="h-16 bg-white/80 dark:bg-neutral-800/80 backdrop-blur-xl border-b border-gray-200 dark:border-white/5 sticky top-0 z-20 px-6 flex items-center justify-between transition-colors duration-300"
			>
				<div class="flex items-center gap-4">
					<!-- Desktop Sidebar Toggle -->
					<button
						onclick={toggleSidebar}
						aria-label="Toggle Sidebar"
						class="hidden md:flex p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-neutral-700/50 transition-colors"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="w-6 h-6 transition-transform duration-300 {isSidebarCollapsed
								? 'rotate-180'
								: ''}"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M4 6h16M4 12h16M4 18h16"
							/>
						</svg>
					</button>

					<!-- Mobile Sidebar Toggle -->
					<button
						onclick={toggleMobileMenu}
						aria-label="Toggle Mobile Menu"
						class="md:hidden p-2 text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-neutral-700/50 rounded-lg transition-colors"
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
								d="M4 6h16M4 12h16M4 18h16"
							/>
						</svg>
					</button>
				</div>

				<!-- Global Search -->
				<div class="flex-1 max-w-xl mx-4 hidden md:block">
					<div class="relative">
						<span class="absolute left-3 top-2.5 text-gray-400">
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
									d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
								/>
							</svg>
						</span>
						<input
							type="text"
							name="global-search"
							autocomplete="off"
							placeholder="Search anything..."
							class="w-full bg-gray-100 dark:bg-neutral-900/50 border-none rounded-xl pl-10 pr-4 py-2.5 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500/50 transition-all font-medium"
						/>
						<div class="absolute right-3 top-2.5 flex gap-1">
							<span
								class="text-xs font-semibold text-gray-400 bg-white dark:bg-neutral-800 border border-gray-200 dark:border-white/10 px-1.5 py-0.5 rounded"
								>Ctrl</span
							>
							<span
								class="text-xs font-semibold text-gray-400 bg-white dark:bg-neutral-800 border border-gray-200 dark:border-white/10 px-1.5 py-0.5 rounded"
								>K</span
							>
						</div>
					</div>
				</div>

				<div class="flex items-center gap-4">
					<!-- Theme Toggle -->
					<ThemeToggle />
				</div>
			</header>

			<!-- Page Content -->
			<div class="p-6 md:p-8 max-w-7xl mx-auto w-full">
				{@render children()}
			</div>
		</main>
	</div>
{/if}
