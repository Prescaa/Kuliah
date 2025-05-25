package com.presca.tugasbeeceptor

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET

data class ApiResponse(
    val Nama: String,
    val NIM: String,
    val Prodi: String
)

interface BeeceptorApiService {
    @GET("/")
    suspend fun getData(): ApiResponse
}

object RetrofitClient {
    private const val BASE_URL = "https://mobilebeeceptor.free.beeceptor.com"

    val apiService: BeeceptorApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(BeeceptorApiService::class.java)
    }
}
