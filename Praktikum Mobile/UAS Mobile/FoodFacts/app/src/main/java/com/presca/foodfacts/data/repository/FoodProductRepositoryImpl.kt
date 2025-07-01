package com.presca.foodfacts.data.repository

import android.util.Log
import com.presca.foodfacts.data.local.AppDatabase
import com.presca.foodfacts.data.local.entity.ProductEntity
import com.presca.foodfacts.data.mapper.FoodProductMapper
import com.presca.foodfacts.data.remote.FoodApiService
import com.presca.foodfacts.domain.model.ProductInfo
import com.presca.foodfacts.domain.repository.FoodProductRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.flowOn
import kotlinx.coroutines.withContext

class FoodProductRepositoryImpl(
    private val api: FoodApiService,
    private val db: AppDatabase
) : FoodProductRepository {

    companion object {
        private const val TAG = "FoodProductRepository"
        private const val DEFAULT_SEARCH_TERM = "indonesia"
        private const val DEFAULT_COUNTRY_FILTER = "indonesia"
        private const val CACHE_DURATION_HOURS = 6
    }

    private val cacheDurationMillis = CACHE_DURATION_HOURS * 60 * 60 * 1000L

    override fun fetchProducts(): Flow<List<ProductInfo>> = flow {
        try {
            Log.d(TAG, "Starting product data fetch...")

            val cachedProducts = withContext(Dispatchers.IO) {
                db.foodProductDao().getAllProducts()
            }

            if (cachedProducts.isNotEmpty() &&
                (System.currentTimeMillis() - cachedProducts[0].lastUpdated < cacheDurationMillis)) {
                Log.d(TAG, "Using cached data")
                emit(cachedProducts.map { productEntity ->
                    FoodProductMapper.mapEntityToDomain(productEntity)
                })
                return@flow
            }

            Log.d(TAG, "Fetching from API...")

            val productResponse = try {
                api.searchProducts(
                    searchTerm = DEFAULT_SEARCH_TERM,
                    page = 1,
                    pageSize = 50,
                    countries = DEFAULT_COUNTRY_FILTER
                )
            } catch (e: Exception) {
                Log.e(TAG, "API fetch failed: ${e.message}", e)
                throw Exception("Failed to connect to server. Please check your internet connection.")
            }

            val entities = try {
                FoodProductMapper.mapResponseToEntities(productResponse)
            } catch (e: Exception) {
                Log.e(TAG, "Mapping failed: ${e.message}", e)
                throw Exception("Invalid product data. Please try again.")
            }

            if (entities.isNotEmpty()) {
                try {
                    withContext(Dispatchers.IO) {
                        db.foodProductDao().clearAll()
                        db.foodProductDao().insertAll(entities)
                        Log.d(TAG, "Data saved to local database")
                    }
                } catch (e: Exception) {
                    Log.e(TAG, "Failed to save to local DB: ${e.message}", e)
                }

                emit(entities.map { productEntity ->
                    FoodProductMapper.mapEntityToDomain(productEntity)
                })
            } else if (cachedProducts.isNotEmpty()) {
                Log.d(TAG, "No new data, using existing cache")
                emit(cachedProducts.map { productEntity ->
                    FoodProductMapper.mapEntityToDomain(productEntity)
                })
            } else {
                Log.d(TAG, "No products found")
                emit(emptyList())
            }

        } catch (e: Exception) {
            Log.e(TAG, "Error in fetchProducts: ${e.message}", e)

            val cachedProducts = withContext(Dispatchers.IO) {
                db.foodProductDao().getAllProducts()
            }

            if (cachedProducts.isNotEmpty()) {
                Log.d(TAG, "Using cache as fallback")
                emit(cachedProducts.map { productEntity ->
                    FoodProductMapper.mapEntityToDomain(productEntity)
                })
            } else {
                throw e
            }
        }
    }.flowOn(Dispatchers.IO)

    override suspend fun refreshProducts() {
        try {
            Log.d(TAG, "Refreshing product data...")

            val productResponse = api.searchProducts(
                searchTerm = DEFAULT_SEARCH_TERM,
                page = 1,
                pageSize = 50,
                countries = DEFAULT_COUNTRY_FILTER
            )

            val entities = FoodProductMapper.mapResponseToEntities(productResponse)

            if (entities.isNotEmpty()) {
                withContext(Dispatchers.IO) {
                    db.foodProductDao().clearAll()
                    db.foodProductDao().insertAll(entities)
                    Log.d(TAG, "Data refreshed successfully")
                }
            } else {
                Log.d(TAG, "No new data found during refresh")
            }
        } catch (e: Exception) {
            Log.e(TAG, "Refresh failed: ${e.message}", e)
            throw Exception("Failed to refresh data: ${e.message ?: "Unknown error"}")
        }
    }
}