package com.presca.foodfacts.domain.model

data class ProductInfo(
    val code: String,
    val name: String,
    val brand: String,
    val imageUrl: String,
    val nutriscore: String,
    val ingredients: String,
    val country: String,
    val quantity: String,
    val productUrl: String,
    val lastUpdated: Long,
    val countriesTags: List<String> = emptyList(),
    val categories: List<String> = emptyList(),
    val nutritionInfo: String
) {
    fun isFromIndonesia(): Boolean {
        return countriesTags.contains("en:indonesia") ||
                country.contains("indonesia", ignoreCase = true)
    }

    fun getMainCategory(): String {
        return categories.firstOrNull() ?: "Unknown"
    }
}