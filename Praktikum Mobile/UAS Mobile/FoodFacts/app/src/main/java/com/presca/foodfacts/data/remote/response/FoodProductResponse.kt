package com.presca.foodfacts.data.remote.response

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class FoodProductResponse(
    val products: List<ProductItem>?,
    val count: Int?,
    val page: Int?,
    @SerialName("page_size")
    val pageSize: Int?,
    @SerialName("skip")
    val skipCount: Int?
)

@Serializable
data class ProductItem(
    val code: String?,
    val product_name: String?,
    @SerialName("product_name_id")
    val productNameId: String? = null,
    val brands: String?,
    val image_front_url: String?,
    val nutriscore_score: Int? = null,
    val nutriscore_grade: String? = null,
    val ingredients_text: String? = null,
    @SerialName("ingredients_text_id")
    val ingredientsTextId: String? = null,
    val countries: String? = null,
    val quantity: String? = null,
    val url: String? = null,
    @SerialName("countries_tags")
    val countriesTags: List<String>? = null,
    val categories: String? = null,
    @SerialName("categories_tags")
    val categoriesTags: List<String>? = null,
    @SerialName("nutriments")
    val nutriments: Nutriments? = null,
    @SerialName("labels_tags")
    val labelsTags: List<String>? = null,
    @SerialName("selected_images")
    val selectedImages: SelectedImages? = null
)

@Serializable
data class Nutriments(
    @SerialName("energy-kcal_100g") val energyKcal100g: Double? = null,
    @SerialName("fat_100g") val fat100g: Double? = null,
    @SerialName("saturated-fat_100g") val saturatedFat100g: Double? = null,
    @SerialName("carbohydrates_100g") val carbohydrates100g: Double? = null,
    @SerialName("sugars_100g") val sugars100g: Double? = null,
    @SerialName("proteins_100g") val proteins100g: Double? = null,
    @SerialName("salt_100g") val salt100g: Double? = null
)

@Serializable
data class SelectedImages(
    @SerialName("front") val front: Map<String, Map<String, String>>? = null,
    @SerialName("nutrition") val nutrition: Map<String, Map<String, String>>? = null,
    @SerialName("ingredients") val ingredients: Map<String, Map<String, String>>? = null,
    @SerialName("labels") val labels: Map<String, Map<String, String>>? = null
)

@Serializable
data class ImageSizes(
    @SerialName("small") val small: String? = null,
    @SerialName("display") val display: String? = null,
    @SerialName("thumb") val thumb: String? = null
)

@Serializable
data class ImageDetail(
    @SerialName("display") val display: String? = null,
    @SerialName("small") val small: String? = null,
    @SerialName("thumb") val thumb: String? = null,
    @SerialName("original") val original: String? = null,
    @SerialName("sizes") val sizes: ImageSizes? = null,
    @SerialName("urls") val urls: ImageUrls? = null
)

@Serializable
data class ImageUrls(
    @SerialName("en") val en: String? = null,
    @SerialName("fr") val fr: String? = null,
    @SerialName("id") val id: String? = null,
    @SerialName("400") val size400: String? = null,
    @SerialName("full") val full: String? = null
)