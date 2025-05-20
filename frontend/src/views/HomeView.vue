<template>
  <div class="home">
    <h1>Welcome to Hotel Reservations System</h1>
    <div class="features">
      <div class="feature-card">
        <h2>📤 Upload Data</h2>
        <p>Upload your hotel reservations data in YAML format</p>
        <RouterLink to="/upload" class="feature-button">Go to Upload</RouterLink>
      </div>
      <div class="feature-card">
        <h2>📊 View Data</h2>
        <p>View and manage your hotel reservations data</p>
        <RouterLink to="/data" class="feature-button">View Data</RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  text-align: center;
  padding: 2rem;
}

h1 {
  color: #2c3e50;
  margin-bottom: 3rem;
}

.features {
  display: flex;
  gap: 2rem;
  justify-content: center;
  flex-wrap: wrap;
}

.feature-card {
  background-color: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  flex: 1;
  min-width: 300px;
  max-width: 400px;
}

.feature-card h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #666;
  margin-bottom: 1.5rem;
}

.feature-button {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background-color: #2c3e50;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.feature-button:hover {
  background-color: #1a252f;
}

@media (max-width: 768px) {
  .features {
    flex-direction: column;
    align-items: center;
  }

  .feature-card {
    width: 100%;
  }
}
</style> 