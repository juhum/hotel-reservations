<template>
  <div class="upload-view">
    <h1>Upload Reservations Data</h1>
    <WelcomeItem>
      <template #icon>📤</template>
      <template #heading>Upload YAML File</template>
      <p>Drag and drop your YAML file here or click to select a file.</p>
      <p class="hint">The file should contain hotels, guests, and reservations data.</p>
    </WelcomeItem>
  </div>
</template>

<script setup>
import WelcomeItem from '../components/WelcomeItem.vue'
</script>

<style scoped>
.upload-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  color: #2c3e50;
  text-align: center;
  margin-bottom: 2rem;
}

.hint {
  color: #666;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}
</style> 