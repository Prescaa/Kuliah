package com.presca.foodfacts.domain.repository

import com.presca.foodfacts.domain.model.ProductInfo
import kotlinx.coroutines.flow.Flow

interface FoodProductRepository {
    fun fetchProducts(): Flow<List<ProductInfo>>
    suspend fun refreshProducts()
}