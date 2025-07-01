package com.presca.foodfacts.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "food_products")
data class ProductEntity(
    @PrimaryKey val code: String,
    val name: String,
    val brand: String,
    val imageUrl: String,
    val nutriscore: String,
    val ingredients: String,
    val country: String,
    val quantity: String,
    val productUrl: String,
    val lastUpdated: Long = System.currentTimeMillis(),
    val countriesTags: String = "",
    val nutritionInfo: String,
    val categories: String = "",
    val categoriesTags: String = ""
) {
    fun getCountriesTagsList(): List<String> {
        return countriesTags.split(",")
            .map { it.trim() }
            .filter { it.isNotEmpty() }
    }

    fun getCategoriesList(): List<String> {
        return categoriesTags.split(",")
            .map { it.trim() }
            .filter { it.isNotEmpty() }
            .map { it.substringAfter(":") }
    }
}