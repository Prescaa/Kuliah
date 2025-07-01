package com.presca.foodfacts.presentation.screens

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.bumptech.glide.integration.compose.ExperimentalGlideComposeApi
import com.bumptech.glide.integration.compose.GlideImage
import com.presca.foodfacts.data.mapper.FoodProductMapper
import com.presca.foodfacts.domain.model.ProductInfo
import androidx.compose.foundation.shape.RoundedCornerShape

@OptIn(ExperimentalMaterial3Api::class, ExperimentalGlideComposeApi::class)
@Composable
fun ProductDetailScreen(product: ProductInfo, navController: NavController) {
    val context = LocalContext.current

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(product.name, maxLines = 1, overflow = TextOverflow.Ellipsis) },
                navigationIcon = { IconButton(onClick = { navController.popBackStack() }) { Icon(Icons.Default.ArrowBack, contentDescription = "Kembali") } },
                colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    titleContentColor = MaterialTheme.colorScheme.onPrimary,
                    navigationIconContentColor = MaterialTheme.colorScheme.onPrimary
                )
            )
        }
    ) { padding ->
        Column(modifier = Modifier.padding(padding).verticalScroll(rememberScrollState()).fillMaxWidth()) {
            ProductTitleCard(product)
            NutriScoreCard(product.nutriscore)
            NutritionTableCard(product)
            CategoriesCard(product)
            LastUpdatedCard(product.lastUpdated)

            Button(
                onClick = {
                    try { context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(product.productUrl))) }
                    catch (e: Exception) { e.printStackTrace() }
                },
                modifier = Modifier.fillMaxWidth().padding(16.dp)
            ) {
                Text("Lihat di Open Food Facts")
            }
        }
    }
}

@OptIn(ExperimentalGlideComposeApi::class)
@Composable
private fun ProductTitleCard(product: ProductInfo) {
    Card(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp), shape = RoundedCornerShape(8.dp), elevation = CardDefaults.cardElevation(4.dp)) {
        Column(modifier = Modifier.padding(16.dp).fillMaxWidth(), horizontalAlignment = Alignment.CenterHorizontally) {
            GlideImage(model = product.imageUrl, contentDescription = product.name, modifier = Modifier.size(150.dp).padding(bottom = 16.dp))
            Text(text = product.name, style = MaterialTheme.typography.headlineMedium, textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth())
            Spacer(modifier = Modifier.height(8.dp))
            Text(text = "Merek: ${product.brand}", style = MaterialTheme.typography.bodyMedium, textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth())
            Text(text = "Kuantitas: ${product.quantity}", style = MaterialTheme.typography.bodyMedium, textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth())
            Text(
                text = "Negara: ${
                    product.country
                        .substringAfterLast(":")
                        .substringAfterLast(".")
                        .substringBefore(";")
                        .trim()
                        .replaceFirstChar { it.uppercase() }
                }",
                style = MaterialTheme.typography.bodyMedium, textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth()
            )
        }
    }
}

@Composable
private fun NutriScoreCard(score: String) {
    val color = when (score.uppercase()) {
        "A" -> Color(0xFF388E3C)
        "B" -> Color(0xFF689F38)
        "C" -> Color(0xFFFBC02D)
        "D" -> Color(0xFFF57C00)
        "E" -> Color(0xFFD32F2F)
        else -> MaterialTheme.colorScheme.onSurface
    }
    Card(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 4.dp), shape = RoundedCornerShape(8.dp)) {
        Column(modifier = Modifier.padding(16.dp).fillMaxWidth(), horizontalAlignment = Alignment.CenterHorizontally) {
            Text(text = "Nutri-Score: ${score.uppercase()}", style = MaterialTheme.typography.headlineMedium, color = color, fontWeight = FontWeight.Bold, textAlign = TextAlign.Center)
        }
    }
}

@Composable
private fun NutritionTableCard(product: ProductInfo) {
    val nutritionInfoLines = product.nutritionInfo.split("\n")
    val energy = nutritionInfoLines.find { it.startsWith("Energi:") }?.substringAfter("Energi:")?.trim() ?: "N/A"
    val fat = nutritionInfoLines.find { it.startsWith("Lemak:") }?.substringAfter("Lemak:")?.trim() ?: "N/A"
    val sugar = nutritionInfoLines.find { it.startsWith("Gula:") }?.substringAfter("Gula:")?.trim() ?: "N/A"
    val protein = nutritionInfoLines.find { it.startsWith("Protein:") }?.substringAfter("Protein:")?.trim() ?: "N/A"

    val nutritionItems = listOf(
        "Energi" to energy,
        "Lemak" to fat,
        "Gula" to sugar,
        "Protein" to protein
    )

    Card(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 4.dp), shape = RoundedCornerShape(8.dp), elevation = CardDefaults.cardElevation(2.dp)) {
        Column(modifier = Modifier.padding(16.dp).fillMaxWidth(), horizontalAlignment = Alignment.CenterHorizontally) {
            Text(text = "Informasi Gizi per 100g", style = MaterialTheme.typography.titleLarge, modifier = Modifier.padding(bottom = 8.dp), textAlign = TextAlign.Center)
            nutritionItems.forEachIndexed { index, (nutrient, value) ->
                Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text(text = nutrient, style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f), textAlign = TextAlign.Start)
                    Text(text = value, style = MaterialTheme.typography.bodyLarge, modifier = Modifier.weight(1f), textAlign = TextAlign.End)
                }
                if (index < nutritionItems.lastIndex) {
                    Divider(modifier = Modifier.padding(vertical = 4.dp))
                }
            }
        }
    }
}

@Composable
private fun CategoriesCard(product: ProductInfo) {
    Card(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 4.dp), shape = RoundedCornerShape(8.dp), elevation = CardDefaults.cardElevation(2.dp)) {
        Column(modifier = Modifier.padding(16.dp).fillMaxWidth(), horizontalAlignment = Alignment.CenterHorizontally) {
            Text(text = "Kategori Produk", style = MaterialTheme.typography.titleLarge, modifier = Modifier.padding(bottom = 8.dp), textAlign = TextAlign.Center)
            product.categories.forEach { category ->
                Text(text = "• ${category.replace("-", " ")}", modifier = Modifier.padding(vertical = 2.dp), textAlign = TextAlign.Center)
            }
        }
    }
}

@Composable
private fun LastUpdatedCard(timestamp: Long) {
    Card(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 4.dp), shape = RoundedCornerShape(8.dp)) {
        Row(modifier = Modifier.padding(16.dp).fillMaxWidth(), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.Center) {
            Icon(imageVector = Icons.Default.Update, contentDescription = "Terakhir Diperbarui", modifier = Modifier.size(20.dp))
            Spacer(modifier = Modifier.width(8.dp))
            Text(text = "Diperbarui: ${FoodProductMapper.formatLastUpdated(timestamp)}", style = MaterialTheme.typography.bodyMedium, textAlign = TextAlign.Center)
        }
    }
}