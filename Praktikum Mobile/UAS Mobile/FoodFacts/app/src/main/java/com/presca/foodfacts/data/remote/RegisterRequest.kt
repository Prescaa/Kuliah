package com.presca.foodfacts.data.remote

import kotlinx.serialization.Serializable

@Serializable
data class RegisterRequest(val username: String, val email: String, val password: String)