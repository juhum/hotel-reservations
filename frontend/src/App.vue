<script setup>
import { RouterView, RouterLink } from 'vue-router'
</script>

<template>
  <div class="app">
    <header>
      <div class="logo">🏨</div>
      <nav>
        <RouterLink to="/" class="nav-link">Home</RouterLink>
        <RouterLink to="/upload" class="nav-link">Upload Data</RouterLink>
        <RouterLink to="/data" class="nav-link">View Data</RouterLink>
        <RouterLink to="/visualization" class="nav-link">Data Visualization</RouterLink>
      </nav>
    </header>

    <main>
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

header {
  padding: 1rem 2rem;
  background-color: var(--color-background-soft);
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo {
  font-size: 2.5rem;
  margin-right: 2rem;
}

nav {
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  text-decoration: none;
  color: var(--color-text);
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.nav-link:hover {
  background-color: var(--color-background-mute);
}

.nav-link.router-link-active {
  background-color: var(--color-text);
  color: white;
}

main {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

@media (max-width: 768px) {
  header {
    flex-direction: column;
    padding: 1rem;
  }

  .logo {
    margin: 0 0 1rem 0;
  }

  nav {
    width: 100%;
    justify-content: center;
  }
}
</style>
