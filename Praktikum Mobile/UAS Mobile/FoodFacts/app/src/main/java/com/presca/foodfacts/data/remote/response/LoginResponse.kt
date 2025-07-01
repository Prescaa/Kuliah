package com.presca.foodfacts.data.remote.response

import kotlinx.serialization.Serializable

@Serializable
data class LoginResponse(val token: String, val userId: String)