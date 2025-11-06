<template>
  <div id="app">
    <header class="app-header">
      <div class="container">
        <div class="logo">
          <h1>🐅 Golden Tiger Shoes</h1>
          <p>Ancient Craftsmanship • Modern Performance</p>
        </div>
        <nav class="nav">
          <router-link to="/" class="nav-link">Home</router-link>
          <a href="#" class="nav-link">Collections</a>
          <a href="#" class="nav-link">About</a>
          <a href="#" class="nav-link">Contact</a>
        </nav>
      </div>
    </header>

    <main class="main-content">
      <router-view></router-view>
    </main>

    <footer class="app-footer">
      <div class="container">
        <p>&copy; 2024 Golden Tiger Shoes. Crafted with ancient wisdom.</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
  padding: 1rem 0;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo h1 {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.logo p {
  font-size: 0.9rem;
  opacity: 0.9;
}

.nav {
  display: flex;
  gap: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: opacity 0.3s;
}

.nav-link:hover {
  opacity: 0.8;
}

.main-content {
  min-height: calc(100vh - 140px);
  padding: 2rem 0;
}

.app-footer {
  background: #1f2937;
  color: white;
  text-align: center;
  padding: 1.5rem 0;
  margin-top: auto;
}
</style>