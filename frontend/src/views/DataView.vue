<template>
  <div class="data-view">
    <h1>Hotel Reservations Data</h1>
    
    <div v-if="loading" class="loading">
      Loading data...
    </div>
    
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    
    <div v-else class="data-container">
      <div class="data-section">
        <h2>Hotels ({{ data.counts?.hotels || 0 }})</h2>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Location</th>
                <th>Stars</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="hotel in data.hotels" :key="hotel.name">
                <td>{{ hotel.name }}</td>
                <td>{{ hotel.location }}</td>
                <td>{{ hotel.stars }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="data-section">
        <h2>Guests ({{ data.counts?.guests || 0 }})</h2>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="guest in data.guests" :key="guest.email">
                <td>{{ guest.name }}</td>
                <td>{{ guest.email }}</td>
                <td>{{ guest.phone }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="data-section">
        <h2>Reservations ({{ data.counts?.reservations || 0 }})</h2>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Hotel</th>
                <th>Guest</th>
                <th>Check In</th>
                <th>Check Out</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="reservation in data.reservations" :key="reservation._id">
                <td>{{ reservation.hotel_name }}</td>
                <td>{{ reservation.guest_email }}</td>
                <td>{{ reservation.check_in }}</td>
                <td>{{ reservation.check_out }}</td>
                <td>{{ reservation.status }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const data = ref({})
const loading = ref(true)
const error = ref(null)

const fetchData = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await axios.get('http://localhost:8000/api/data')
    data.value = response.data
  } catch (err) {
    error.value = 'Failed to load data. Please try again later.'
    console.error('Error fetching data:', err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)
</script>

<style scoped>
.data-view {
  padding: 2rem;
}

h1 {
  color: #2c3e50;
  text-align: center;
  margin-bottom: 2rem;
}

.data-section {
  margin-bottom: 3rem;
}

h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.table-container {
  overflow-x: auto;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
  min-width: 600px;
}

th, td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #2c3e50;
}

tr:hover {
  background-color: #f8f9fa;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  text-align: center;
  padding: 2rem;
  color: #dc3545;
  background-color: #f8d7da;
  border-radius: 8px;
  margin: 2rem 0;
}

@media (max-width: 768px) {
  .data-view {
    padding: 1rem;
  }
  
  .table-container {
    margin: 0 -1rem;
    border-radius: 0;
  }
}
</style> 