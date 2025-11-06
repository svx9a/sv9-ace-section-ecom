<template>
  <div class="product-catalog">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">GOLDEN TIGER</h1>
        <p class="hero-subtitle">Where Ancient Legends Meet Modern Performance</p>
        <div class="hero-features">
          <span class="feature">🔥 Premium Materials</span>
          <span class="feature">🎯 Elite Performance</span>
          <span class="feature">🐅 Legendary Design</span>
        </div>
      </div>
    </div>

    <div class="container">
      <!-- Category Filters -->
      <div class="filters-section">
        <h2 class="section-title">LEGENDARY COLLECTION</h2>
        <div class="filters">
          <button 
            v-for="category in categories" 
            :key="category"
            @click="filterByCategory(category)"
            :class="['filter-btn', { active: selectedCategory === category }]"
          >
            {{ getCategoryEmoji(category) }} {{ category.toUpperCase() }}
          </button>
        </div>
      </div>

      <!-- Products Grid -->
      <div v-if="loading" class="loading">
        <div class="loading-spinner"></div>
        <p>Summoning legendary footwear...</p>
      </div>
      
      <div v-else class="products-grid">
        <div 
          v-for="product in filteredProducts" 
          :key="product.id"
          class="product-card"
          @click="$router.push(`/product/${product.id}`)"
        >
          <div class="product-badge" :class="product.category">
            {{ getCategoryBadge(product.category) }}
          </div>
          <div class="product-image">
            <img 
              :src="getProductImage(product)" 
              :alt="product.name"
              @error="handleImageError"
            />
            <div class="image-overlay">
              <button class="quick-view-btn">QUICK VIEW</button>
            </div>
          </div>
          <div class="product-info">
            <h3 class="product-name">{{ product.name }}</h3>
            <p class="product-category">{{ getCategoryName(product.category) }}</p>
            <p class="product-description">{{ product.description }}</p>
            <div class="product-features">
              <span v-for="feature in product.features.slice(0, 2)" :key="feature" class="feature-tag">
                {{ feature }}
              </span>
            </div>
            <div class="product-footer">
              <div class="product-price">${{ product.price }}</div>
              <div class="product-colors">
                <span 
                  v-for="color in getUniqueColors(product.variants)" 
                  :key="color"
                  class="color-dot"
                  :style="{ backgroundColor: getColorCode(color) }"
                  :title="color"
                ></span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ProductCatalog',
  data() {
    return {
      products: [],
      loading: true,
      selectedCategory: 'all',
      categories: ['all', 'basketball', 'lifestyle', 'running']
    }
  },
  computed: {
    filteredProducts() {
      if (this.selectedCategory === 'all') {
        return this.products
      }
      return this.products.filter(product => product.category === this.selectedCategory)
    }
  },
  async mounted() {
    await this.fetchProducts()
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await axios.get('/api/products')
        this.products = response.data
      } catch (error) {
        console.error('Error fetching products:', error)
        // Fallback data
        this.products = this.getFallbackProducts()
      } finally {
        this.loading = false
      }
    },
    getFallbackProducts() {
      return [
        {
          id: 1,
          name: "PHOENIX ASCENDANT",
          category: "basketball",
          price: 199.99,
          description: "Rise above the competition with celestial design and ultimate comfort",
          features: ["Phoenix Feather Cushioning", "Golden Thread Embroidery", "Cloud-Step Soles"],
          variants: [
            { color: "gold" }, { color: "black" }, { color: "red" },
            { color: "gold" }, { color: "black" }, { color: "red" }
          ]
        },
        {
          id: 2,
          name: "DRAGON SOVEREIGN",
          category: "lifestyle", 
          price: 179.99,
          description: "Command respect with ancient dragon motifs and imperial craftsmanship",
          features: ["Dragon Scale Texture", "Imperial Gold Accents", "Royal Comfort Lining"],
          variants: [
            { color: "green" }, { color: "brown" }, { color: "black" },
            { color: "green" }, { color: "brown" }, { color: "black" }
          ]
        },
        {
          id: 3,
          name: "TIGER WARRIOR",
          category: "running",
          price: 159.99,
          description: "Unleash your inner strength with tiger-stripe dynamics and warrior spirit",
          features: ["Tiger Stripe Traction", "Warrior Agility Flex", "Spirit Animal Cushioning"],
          variants: [
            { color: "orange" }, { color: "white" }, { color: "blue" },
            { color: "orange" }, { color: "white" }, { color: "blue" }
          ]
        }
      ]
    },
    filterByCategory(category) {
      this.selectedCategory = category
    },
    getProductImage(product) {
      const productSlug = product.name.toLowerCase().replace(' ', '_')
      const firstColor = this.getUniqueColors(product.variants)[0]
      return `/src/assets/shoes/${productSlug}/${firstColor}/img01.jpg`
    },
    getUniqueColors(variants) {
      const colors = [...new Set(variants.map(v => v.color))]
      return colors.slice(0, 3)
    },
    handleImageError(event) {
      event.target.src = '/src/assets/placeholder.jpg'
    },
    getCategoryEmoji(category) {
      const emojis = {
        'all': '⚡',
        'basketball': '🏀',
        'lifestyle': '👑',
        'running': '🎯'
      }
      return emojis[category] || '👟'
    },
    getCategoryBadge(category) {
      const badges = {
        'basketball': 'ELITE',
        'lifestyle': 'PREMIUM', 
        'running': 'PERFORMANCE'
      }
      return badges[category] || 'NEW'
    },
    getCategoryName(category) {
      const names = {
        'basketball': 'BASKETBALL ELITE',
        'lifestyle': 'LIFESTYLE PREMIUM',
        'running': 'RUNNING PERFORMANCE'
      }
      return names[category] || category.toUpperCase()
    },
    getColorCode(color) {
      const colors = {
        'gold': '#f59e0b',
        'black': '#1f2937',
        'red': '#dc2626',
        'green': '#16a34a',
        'brown': '#92400e',
        'orange': '#ea580c',
        'white': '#f8fafc',
        'blue': '#2563eb'
      }
      return colors[color] || '#6b7280'
    }
  }
}
</script>

<style scoped>
.hero-section {
  background: linear-gradient(135deg, #000000 0%, #1f2937 50%, #f59e0b 100%);
  color: white;
  padding: 4rem 0;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text x="50" y="50" font-family="Arial" font-size="8" fill="rgba(245,158,11,0.1)" text-anchor="middle" dominant-baseline="middle">🐅</text></svg>');
  opacity: 0.3;
}

.hero-content {
  position: relative;
  z-index: 2;
}

.hero-title {
  font-size: 4rem;
  font-weight: 900;
  margin-bottom: 1rem;
  background: linear-gradient(45deg, #f59e0b, #fbbf24, #f59e0b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 30px rgba(245, 158, 11, 0.5);
}

.hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.hero-features {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.feature {
  background: rgba(245, 158, 11, 0.2);
  padding: 0.5rem 1rem;
  border-radius: 25px;
  border: 1px solid rgba(245, 158, 11, 0.5);
}

.filters-section {
  text-align: center;
  margin: 3rem 0;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 2rem;
  position: relative;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 3px;
  background: linear-gradient(45deg, #f59e0b, #d97706);
  border-radius: 2px;
}

.filters {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 1rem 2rem;
  border: 2px solid #e5e7eb;
  background: white;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  font-size: 1.1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.filter-btn.active {
  background: linear-gradient(45deg, #f59e0b, #d97706);
  border-color: #f59e0b;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -5px rgba(245, 158, 11, 0.4);
}

.filter-btn:hover:not(.active) {
  border-color: #f59e0b;
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.15);
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  padding: 2rem 0;
}

.product-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
}

.product-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.product-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 25px;
  font-size: 0.8rem;
  font-weight: 700;
  color: white;
  z-index: 2;
}

.product-badge.basketball {
  background: linear-gradient(45deg, #dc2626, #ef4444);
}

.product-badge.lifestyle {
  background: linear-gradient(45deg, #f59e0b, #d97706);
}

.product-badge.running {
  background: linear-gradient(45deg, #2563eb, #3b82f6);
}

.product-image {
  height: 250px;
  overflow: hidden;
  position: relative;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.product-card:hover .product-image img {
  transform: scale(1.1);
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.product-card:hover .image-overlay {
  opacity: 1;
}

.quick-view-btn {
  background: #f59e0b;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s ease;
}

.quick-view-btn:hover {
  background: #d97706;
}

.product-info {
  padding: 1.5rem;
}

.product-name {
  font-size: 1.4rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.product-category {
  color: #f59e0b;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.product-description {
  color: #6b7280;
  font-size: 0.95rem;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.product-features {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.feature-tag {
  background: #fef3c7;
  color: #92400e;
  padding: 0.4rem 0.8rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
}

.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.product-price {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
}

.product-colors {
  display: flex;
  gap: 0.5rem;
}

.color-dot {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid #e5e7eb;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.loading {
  text-align: center;
  padding: 4rem;
  color: #6b7280;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f4f6;
  border-top: 4px solid #f59e0b;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .products-grid {
    grid-template-columns: 1fr;
  }
  
  .filters {
    gap: 0.5rem;
  }
  
  .filter-btn {
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
  }
}
</style>