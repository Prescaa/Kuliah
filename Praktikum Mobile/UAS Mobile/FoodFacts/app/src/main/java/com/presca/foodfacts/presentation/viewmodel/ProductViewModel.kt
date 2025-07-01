package com.presca.foodfacts.presentation.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.presca.foodfacts.domain.model.ProductInfo
import com.presca.foodfacts.domain.repository.FoodProductRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class ProductViewModel(private val repository: FoodProductRepository) : ViewModel() {
    sealed class ProductState {
        object Loading : ProductState()
        data class Success(val products: List<ProductInfo>) : ProductState()
        data class Error(val message: String) : ProductState()
    }

    private val _state = MutableStateFlow<ProductState>(ProductState.Loading)
    val state: StateFlow<ProductState> = _state.asStateFlow()

    init {
        fetchProducts()
    }

    fun fetchProducts() {
        viewModelScope.launch {
            _state.value = ProductState.Loading
            try {
                repository.fetchProducts().collect { products ->
                    if (products.isEmpty()) {
                        _state.value = ProductState.Error("Tidak ada produk ditemukan")
                    } else {
                        _state.value = ProductState.Success(products)
                    }
                }
            } catch (e: Exception) {
                _state.value = ProductState.Error(
                    "Gagal memuat data: ${e.message ?: "Format data tidak valid"}"
                )
            }
        }
    }

    fun refreshProducts() {
        viewModelScope.launch {
            _state.value = ProductState.Loading
            try {
                repository.refreshProducts()
                fetchProducts()
            } catch (e: Exception) {
                _state.value = ProductState.Error(
                    "Gagal menyegarkan data: ${e.message ?: "Terjadi kesalahan"}"
                )
            }
        }
    }
}










