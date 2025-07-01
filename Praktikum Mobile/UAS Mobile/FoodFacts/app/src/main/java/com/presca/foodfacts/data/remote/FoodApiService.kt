package com.presca.foodfacts.data.remote

import com.presca.foodfacts.data.remote.response.FoodProductResponse
import retrofit2.http.GET
import retrofit2.http.Query
import retrofit2.http.Headers
import retrofit2.http.Path
import retrofit2.http.POST
import retrofit2.http.Body

import com.presca.foodfacts.data.remote.LoginRequest
import com.presca.foodfacts.data.remote.response.LoginResponse
import com.presca.foodfacts.data.remote.RegisterRequest
import com.presca.foodfacts.data.remote.response.RegisterResponse

interface FoodApiService {
    @Headers("User-Agent: FoodFactsApp - Android - 1.0.0 (your.email@example.com)")
    @GET("api/v2/search?json=1")
    suspend fun searchProducts(
        @Query("search_terms") searchTerm: String,
        @Query("page") page: Int,
        @Query("page_size") pageSize: Int,
        @Query("countries_tags") countries: String = "indonesia"
    ): FoodProductResponse

    @Headers("User-Agent: FoodFactsApp - Android - 1.0.0 (your.email@example.com)")
    @GET("api/v2/product/{barcode}.json")
    suspend fun getProductByBarcode(
        @Path("barcode") barcode: String
    ): FoodProductResponse

    @Headers("User-Agent: FoodFactsApp - Android - 1.0.0 (your.email@example.com)")
    @POST("api/login")
    suspend fun loginUser(@Body request: LoginRequest): LoginResponse

    @Headers("User-Agent: FoodFactsApp - Android - 1.0.0 (your.email@example.com)")
    @POST("api/register")
    suspend fun registerUser(@Body request: RegisterRequest): RegisterResponse
}