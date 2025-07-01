package com.presca.foodfacts.data.mapper

import com.presca.foodfacts.data.local.entity.ProductEntity
import com.presca.foodfacts.data.remote.response.FoodProductResponse
import com.presca.foodfacts.domain.model.ProductInfo
import java.time.Instant
import java.time.format.DateTimeFormatter
import java.util.Locale

object FoodProductMapper {

    fun mapResponseToEntities(response: FoodProductResponse): List<ProductEntity> {
        return response.products?.mapNotNull { productItem ->
            if (productItem.code != null && productItem.product_name != null) {
                val nutritionSummary = productItem.nutriments?.let { nutriments ->
                    buildString {
                        nutriments.energyKcal100g?.let { append("Energi: ${it}kcal/100g\n") }
                        nutriments.fat100g?.let { append("Lemak: ${it}g/100g\n") }
                        nutriments.sugars100g?.let { append("Gula: ${it}g/100g\n") }
                        nutriments.proteins100g?.let { append("Protein: ${it}g/100g\n") }
                    }.trim().takeIf { it.isNotEmpty() } ?: "Informasi gizi tidak tersedia"
                } ?: "Informasi gizi tidak tersedia"

                ProductEntity(
                    code = productItem.code!!,
                    name = productItem.productNameId ?: productItem.product_name!!,
                    brand = productItem.brands ?: "Unknown Brand",
                    imageUrl = productItem.image_front_url ?: "",
                    nutriscore = productItem.nutriscore_grade?.uppercase(Locale.getDefault()) ?: "N/A",
                    ingredients = productItem.ingredientsTextId ?:
                    productItem.ingredients_text ?: "Ingredients not available",
                    country = productItem.countries ?: "Unknown",
                    quantity = productItem.quantity ?: "N/A",
                    productUrl = productItem.url ?: "https://world.openfoodfacts.org/product/${productItem.code}",
                    lastUpdated = System.currentTimeMillis(),
                    countriesTags = productItem.countriesTags
                        ?.filterNotNull()
                        ?.joinToString(",") ?: "",
                    nutritionInfo = nutritionSummary,
                    categories = productItem.categories ?: "",
                    categoriesTags = productItem.categoriesTags
                        ?.filterNotNull()
                        ?.joinToString(",") ?: ""
                )
            } else {
                null
            }
        } ?: emptyList()
    }

    fun mapEntityToDomain(entity: ProductEntity): ProductInfo {
        return ProductInfo(
            code = entity.code,
            name = entity.name,
            brand = entity.brand,
            imageUrl = entity.imageUrl,
            nutriscore = entity.nutriscore,
            ingredients = entity.ingredients,
            country = entity.country,
            quantity = entity.quantity,
            productUrl = entity.productUrl,
            lastUpdated = entity.lastUpdated,
            countriesTags = entity.getCountriesTagsList(),
            categories = entity.getCategoriesList(),
            nutritionInfo = entity.nutritionInfo
        )
    }

    fun formatNutriScore(score: String): String {
        return "Nutri-Score: $score"
    }

    fun formatLastUpdated(timestamp: Long): String {
        return Instant.ofEpochMilli(timestamp)
            .atZone(java.time.ZoneId.systemDefault())
            .format(DateTimeFormatter.ofPattern("dd MMM, HH:mm", Locale("id", "ID")))
    }
}