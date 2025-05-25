package com.presca.tugasbeeceptor

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow

class MainViewModel : ViewModel() {
    private val _response = MutableStateFlow("Loading...")
    val response = _response.asStateFlow()

    init {
        fetchData()
    }

    private fun fetchData() {
        viewModelScope.launch {
            try {
                val result = RetrofitClient.apiService.getData()
                _response.value = """
                    Nama: ${result.Nama}
                    NIM: ${result.NIM}
                    Prodi: ${result.Prodi}
                """.trimIndent()
            } catch (e: Exception) {
                _response.value = "Error: ${e.localizedMessage}"
            }
        }
    }
}
