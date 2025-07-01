package com.presca.foodfacts.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.presca.foodfacts.data.local.entity.ProductEntity

@Dao
interface FoodProductDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(products: List<ProductEntity>)

    @Query("SELECT * FROM food_products WHERE country LIKE '%indonesia%' OR countriesTags LIKE '%indonesia%' ORDER BY lastUpdated DESC")
    suspend fun getAllProducts(): List<ProductEntity>

    @Query("DELETE FROM food_products")
    suspend fun clearAll()

    @Query("SELECT COUNT(*) FROM food_products")
    suspend fun count(): Int
}