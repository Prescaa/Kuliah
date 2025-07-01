package com.presca.foodfacts.data.remote

import kotlinx.serialization.Serializable

@Serializable
data class LoginRequest(val email: String, val password: String)