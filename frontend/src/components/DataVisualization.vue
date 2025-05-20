<template>
  <div class="visualization-container">
    <h2>Hotel Data Visualization</h2>
    
    <div class="charts-grid">
      <div class="chart-container">
        <h3>Hotels by Location</h3>
        <canvas ref="locationChart"></canvas>
      </div>
      
      <div class="chart-container">
        <h3>Room Types Distribution</h3>
        <canvas ref="roomTypeChart"></canvas>
      </div>
      
      <div class="chart-container">
        <h3>Price Range Distribution</h3>
        <canvas ref="priceChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Chart from 'chart.js/auto'

const locationChart = ref(null)
const roomTypeChart = ref(null)
const priceChart = ref(null)

const fetchData = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/data')
    const data = response.data
    
    // Process data for charts
    processLocationData(data.hotels)
    processRoomTypeData(data.hotels)
    processPriceData(data.hotels)
  } catch (error) {
    console.error('Error fetching data:', error)
  }
}

const processLocationData = (hotels) => {
  const locationCount = {}
  hotels.forEach(hotel => {
    locationCount[hotel.location] = (locationCount[hotel.location] || 0) + 1
  })

  new Chart(locationChart.value, {
    type: 'bar',
    data: {
      labels: Object.keys(locationCount),
      datasets: [{
        label: 'Number of Hotels',
        data: Object.values(locationCount),
        backgroundColor: 'rgba(54, 162, 235, 0.5)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Hotels by Location',
          font: {
            size: 16,
            weight: 'bold'
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0
          }
        }
      }
    }
  })
}

const processRoomTypeData = (hotels) => {
  const roomTypeCount = {}
  hotels.forEach(hotel => {
    hotel.rooms.forEach(room => {
      roomTypeCount[room.type] = (roomTypeCount[room.type] || 0) + 1
    })
  })

  new Chart(roomTypeChart.value, {
    type: 'pie',
    data: {
      labels: Object.keys(roomTypeCount),
      datasets: [{
        data: Object.values(roomTypeCount),
        backgroundColor: [
          'rgba(255, 99, 132, 0.5)',
          'rgba(54, 162, 235, 0.5)',
          'rgba(255, 206, 86, 0.5)',
          'rgba(75, 192, 192, 0.5)',
          'rgba(153, 102, 255, 0.5)'
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: {
            padding: 20,
            font: {
              size: 12
            }
          }
        },
        title: {
          display: true,
          text: 'Room Types Distribution',
          font: {
            size: 16,
            weight: 'bold'
          }
        }
      }
    }
  })
}

const processPriceData = (hotels) => {
  const prices = []
  hotels.forEach(hotel => {
    hotel.rooms.forEach(room => {
      prices.push(room.price)
    })
  })

  // Create price ranges
  const ranges = {
    '0-300': 0,
    '301-500': 0,
    '501-800': 0,
    '801-1000': 0,
    '1000+': 0
  }

  prices.forEach(price => {
    if (price <= 300) ranges['0-300']++
    else if (price <= 500) ranges['301-500']++
    else if (price <= 800) ranges['501-800']++
    else if (price <= 1000) ranges['801-1000']++
    else ranges['1000+']++
  })

  new Chart(priceChart.value, {
    type: 'bar',
    data: {
      labels: Object.keys(ranges),
      datasets: [{
        label: 'Number of Rooms',
        data: Object.values(ranges),
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Price Range Distribution',
          font: {
            size: 16,
            weight: 'bold'
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Number of Rooms',
            font: {
              size: 12,
              weight: 'bold'
            }
          },
          ticks: {
            precision: 0
          }
        },
        x: {
          title: {
            display: true,
            text: 'Price Range (PLN)',
            font: {
              size: 12,
              weight: 'bold'
            }
          }
        }
      }
    }
  })
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.visualization-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

h2 {
  text-align: center;
  color: var(--color-heading);
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.chart-container {
  background: var(--color-background-soft);
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  height: 300px;
  position: relative;
}

h3 {
  text-align: center;
  color: var(--color-heading);
  margin-bottom: 0.8rem;
  font-size: 1.1rem;
}

canvas {
  width: 100% !important;
  height: 100% !important;
}

@media (max-width: 768px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .chart-container {
    height: 280px;
  }
}
</style> 