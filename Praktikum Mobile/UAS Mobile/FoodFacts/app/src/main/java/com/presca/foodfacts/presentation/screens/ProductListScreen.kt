package com.presca.foodfacts.presentation.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.DarkMode
import androidx.compose.material.icons.filled.LightMode
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.bumptech.glide.integration.compose.ExperimentalGlideComposeApi
import com.bumptech.glide.integration.compose.GlideImage
import com.presca.foodfacts.domain.model.ProductInfo
import com.presca.foodfacts.data.mapper.FoodProductMapper
import com.presca.foodfacts.presentation.viewmodel.ProductViewModel
import com.presca.foodfacts.presentation.viewmodel.SettingsViewModel
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class, ExperimentalGlideComposeApi::class)
@Composable
fun ProductListScreen(
    state: ProductViewModel.ProductState,
    onRefresh: () -> Unit,
    onClickProduct: (ProductInfo) -> Unit,
    navController: NavController,
    settingsViewModel: SettingsViewModel
) {
    val settingsUiState by settingsViewModel.uiState.collectAsState()

    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(
                title = { Text("Daftar Produk") },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Kembali")
                    }
                },
                actions = {
                    IconButton(onClick = { settingsViewModel.toggleDarkMode(!settingsUiState.darkModeEnabled) }) {
                        Icon(imageVector = if (settingsUiState.darkModeEnabled) Icons.Default.LightMode else Icons.Default.DarkMode, contentDescription = if (settingsUiState.darkModeEnabled) "Mode Terang" else "Mode Gelap")
                    }
                },
                colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    titleContentColor = MaterialTheme.colorScheme.onPrimary,
                    actionIconContentColor = MaterialTheme.colorScheme.onPrimary,
                    navigationIconContentColor = MaterialTheme.colorScheme.onPrimary
                )
            )
        }
    ) { innerPadding ->
        Box(modifier = Modifier.padding(innerPadding).fillMaxSize()) {
            when (state) {
                is ProductViewModel.ProductState.Loading -> LoadingView()
                is ProductViewModel.ProductState.Error -> ErrorView(state.message, onRefresh)
                is ProductViewModel.ProductState.Success -> ProductContentView(products = state.products, onClickProduct = onClickProduct)
            }
        }
    }
}

@Composable
private fun LoadingView() {
    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        CircularProgressIndicator()
    }
}

@Composable
private fun ErrorView(message: String, onRefresh: () -> Unit) {
    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(message)
        Spacer(modifier = Modifier.height(16.dp))
        Button(onClick = onRefresh) {
            Text("Coba Lagi")
        }
    }
}

@OptIn(ExperimentalGlideComposeApi::class)
@Composable
private fun ProductContentView(products: List<ProductInfo>, onClickProduct: (ProductInfo) -> Unit) {
    if (products.isEmpty()) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            Text("Tidak ada produk ditemukan.")
        }
    } else {
        LazyColumn(
            modifier = Modifier.fillMaxSize().padding(horizontal = 8.dp),
            contentPadding = PaddingValues(vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(products) { product ->
                ProductCard(product = product, onClick = { onClickProduct(product) })
            }
        }
    }
}

@OptIn(ExperimentalGlideComposeApi::class)
@Composable
private fun ProductCard(product: ProductInfo, onClick: () -> Unit) {
    Card(modifier = Modifier.fillMaxWidth(), onClick = onClick, shape = RoundedCornerShape(8.dp)) {
        Row(
            modifier = Modifier.padding(12.dp).fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            GlideImage(
                model = product.imageUrl,
                contentDescription = product.name,
                modifier = Modifier.size(60.dp).clip(RoundedCornerShape(8.dp))
            )
            Spacer(modifier = Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1.5f)) {
                Text(text = product.name, fontSize = 16.sp)
                Text(text = product.brand, fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                val formattedCategory = product.getMainCategory()
                    .replace("-", " ")
                    .split(" ")
                    .joinToString(" ") { it.replaceFirstChar { if (it.isLowerCase()) it.titlecase(Locale.getDefault()) else it.toString() } }
                Text(text = formattedCategory, fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            Spacer(modifier = Modifier.width(16.dp))
            Column(horizontalAlignment = Alignment.End, modifier = Modifier.weight(1f)) {
                val nutriScoreColor = getNutriScoreColor(product.nutriscore)
                Text(text = FoodProductMapper.formatNutriScore(product.nutriscore), fontSize = 16.sp, color = nutriScoreColor, modifier = Modifier.fillMaxWidth(), textAlign = TextAlign.End)
            }
        }
    }
}

@Composable
fun getNutriScoreColor(nutriScore: String): Color {
    return when (nutriScore.uppercase(Locale.getDefault())) {
        "A" -> Color(0xFF388E3C)
        "B" -> Color(0xFF689F38)
        "C" -> Color(0xFFFBC02D)
        "D" -> Color(0xFFF57C00)
        "E" -> Color(0xFFD32F2F)
        else -> MaterialTheme.colorScheme.onSurface
    }
}