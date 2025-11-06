<template>
  <div class="product-detail">
    <div class="container" v-if="product">
      <div class="product-layout">
        <!-- Product Images -->
        <div class="image-gallery">
          <div class="main-image">
            <img :src="currentImage" :alt="product.name" />
          </div>
        </div>

        <!-- Product Info -->
        <div class="product-info">
          <h1>{{ product.name }}</h1>
          <p class="category">{{ product.category }}</p>
          <p class="price">${{ product.price }}</p>
          <p class="description">{{ product.description }}</p>

          <!-- Color Selection -->
          <div class="selection-section">
            <h3>Color</h3>
            <div class="color-options">
              <div 
                v-for="color in availableColors" 
                :key="color"
                class="color-option"
                :class="{ active: selectedColor === color }"
                @click="selectColor(color)"
              >
                <div class="color-swatch" :style="{ backgroundColor: color }"></div>
                <span>{{ color }}</span>
              </div>
            </div>
          </div>

          <!-- Size Selection -->
          <div class="selection-section">
            <h3>Size</h3>
            <div class="size-options">
              <div 
                v-for="size in availableSizes" 
                :key="size"
                class="size-option"
                :class="{ active: selectedSize === size }"
                @click="selectSize(size)"
              >
                {{ size }}
              </div>
            </div>
          </div>

          <!-- Features -->
          <div class="features-section">
            <h3>Legendary Features</h3>
            <ul class="features-list">
              <li v-for="feature in product.features" :key="feature">
                {{ feature }}
              </li>
            </ul>
          </div>

          <!-- Add to Cart -->
          <div class="action-section">
            <button class="add-to-cart-btn" @click="addToCart">
              Add to Cart - ${{ product.price }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-else-if="loading" class="loading">Loading product details...</div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ProductDetail',
  props: ['id'],
  data() {
    return {
      product: null,
      loading: true,
      selectedColor: null,
      selectedSize: null,
      currentImageIndex: 0
    }
  },
  computed: {
    availableColors() {
      if (!this.product?.variants) return []
      return [...new Set(this.product.variants.map(v => v.color))]
    },
    availableSizes() {
      if (!this.selectedColor || !this.product?.variants) return []
      return this.product.variants
        .filter(v => v.color === this.selectedColor)
        .map(v => v.size)
        .sort()
    },
    currentVariant() {
      if (!this.selectedColor || !this.selectedSize) return null
      return this.product.variants.find(
        v => v.color === this.selectedColor && v.size === this.selectedSize
      )
    },
    currentImage() {
      return '/src/assets/placeholder.jpg'
    }
  },
  async mounted() {
    await this.fetchProduct()
  },
  methods: {
    async fetchProduct() {
      try {
        const response = await axios.get(`/api/products/${this.id}`)
        this.product = response.data
        // Set initial selections
        if (this.availableColors.length > 0) {
          this.selectedColor = this.availableColors[0]
        }
        if (this.availableSizes.length > 0) {
          this.selectedSize = this.availableSizes[0]
        }
      } catch (error) {
        console.error('Error fetching product:', error)
        // Fallback data
        this.product = {
          id: this.id,
          name: "Golden Phoenix Ascendant",
          category: "basketball",
          price: 199.99,
          description: "Rise above the competition with celestial design and ultimate comfort",
          features: ["Phoenix feather cushioning", "Golden thread embroidery", "Cloud-step soles"],
          variants: [
            { color: "gold", size: "US 9" },
            { color: "black", size: "US 9" },
            { color: "red", size: "US 9" }
          ]
        }
      } finally {
        this.loading = false
      }
    },
    selectColor(color) {
      this.selectedColor = color
      this.selectedSize = this.availableSizes[0]
    },
    selectSize(size) {
      this.selectedSize = size
    },
    addToCart() {
      if (!this.currentVariant) {
        alert('Please select color and size')
        return
      }
      alert(`Added ${this.product.name} (${this.selectedColor}, ${this.selectedSize}) to cart!`)
    }
  }
}
</script>

<style scoped>
.product-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: start;
}

.image-gallery {
  position: sticky;
  top: 2rem;
}

.main-image {
  border-radius: 12px;
  overflow: hidden;
}

.main-image img {
  width: 100%;
  height: 500px;
  object-fit: cover;
}

.product-info h1 {
  font-size: 2.5rem;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.category {
  color: #f59e0b;
  font-weight: 600;
  text-transform: uppercase;
  margin-bottom: 1rem;
}

.price {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.description {
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.selection-section {
  margin-bottom: 2rem;
}

.selection-section h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #1f2937;
}

.color-options, .size-options {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.color-option, .size-option {
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.color-option.active, .size-option.active {
  border-color: #f59e0b;
  background: #fef3c7;
}

.color-swatch {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  border: 1px solid #e5e7eb;
}

.features-section {
  margin-bottom: 2rem;
}

.features-list {
  list-style: none;
  padding: 0;
}

.features-list li {
  padding: 0.5rem 0;
  color: #6b7280;
  position: relative;
  padding-left: 1.5rem;
}

.features-list li:before {
  content: '✓';
  color: #f59e0b;
  font-weight: bold;
  position: absolute;
  left: 0;
}

.add-to-cart-btn {
  width: 100%;
  padding: 1rem 2rem;
  background: #f59e0b;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.add-to-cart-btn:hover {
  background: #d97706;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .product-layout {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .image-gallery {
    position: static;
  }
}
</style>