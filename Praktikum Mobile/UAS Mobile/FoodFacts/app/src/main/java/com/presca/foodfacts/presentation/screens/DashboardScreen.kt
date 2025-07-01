package com.presca.foodfacts.presentation.screens

import android.content.Intent
import android.net.Uri
import android.widget.Toast
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowForwardIos
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.presca.foodfacts.navigateToLogin
import com.presca.foodfacts.presentation.viewmodel.AuthViewModel
import com.presca.foodfacts.presentation.viewmodel.SettingsViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DashboardScreen(
    navController: NavController,
    authViewModel: AuthViewModel,
    settingsViewModel: SettingsViewModel
) {
    val context = LocalContext.current
    val settingsUiState by settingsViewModel.uiState.collectAsState()

    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(
                title = { Text("FoodFacts", fontWeight = FontWeight.Bold) },
                actions = {
                    IconButton(onClick = { settingsViewModel.toggleDarkMode(!settingsUiState.darkModeEnabled) }) {
                        Icon(imageVector = if (settingsUiState.darkModeEnabled) Icons.Default.LightMode else Icons.Default.DarkMode, contentDescription = if (settingsUiState.darkModeEnabled) "Mode Terang" else "Mode Gelap")
                    }
                    IconButton(onClick = {
                        run {
                            authViewModel.logout()
                        }
                        navController.navigateToLogin()
                    }) {
                        Icon(Icons.Default.Logout, contentDescription = "Keluar")
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
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(horizontal = 16.dp)
                .verticalScroll(rememberScrollState()),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 16.dp),
                shape = RoundedCornerShape(12.dp),
                elevation = CardDefaults.cardElevation(4.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer)
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    verticalAlignment = Alignment.Top,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Column(
                        modifier = Modifier.weight(1f)
                    ) {
                        Text(
                            text = "Tentang FoodFacts",
                            style = MaterialTheme.typography.headlineSmall,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onPrimaryContainer,
                            modifier = Modifier.padding(bottom = 8.dp)
                        )
                        Text(
                            text = "FoodFacts adalah aplikasi yang dirancang untuk memberikan informasi detail mengenai produk makanan.",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onPrimaryContainer.copy(alpha = 0.8f),
                            modifier = Modifier.padding(bottom = 8.dp)
                        )
                        Text(
                            text = "Telusuri informasi gizi, kandungan alergen, dan detail lainnya hanya dengan mencari nama produk.",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onPrimaryContainer.copy(alpha = 0.8f)
                        )
                    }

                    Spacer(modifier = Modifier.width(16.dp))

                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Default.Info,
                            contentDescription = "Informasi Produk",
                            tint = MaterialTheme.colorScheme.onPrimaryContainer,
                            modifier = Modifier.size(48.dp)
                        )
                        Icon(
                            imageVector = Icons.Default.Search,
                            contentDescription = "Cari Produk",
                            tint = MaterialTheme.colorScheme.onPrimaryContainer,
                            modifier = Modifier.size(48.dp)
                        )
                    }
                }
            }

            Text(
                text = "Menu Utama",
                style = MaterialTheme.typography.titleSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(bottom = 8.dp, top = 16.dp),
                textAlign = TextAlign.Start
            )

            Column(
                modifier = Modifier.fillMaxWidth(),
                verticalArrangement = Arrangement.spacedBy(8.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                DashboardMenuItemStyled(
                    icon = Icons.Default.ListAlt,
                    title = "Daftar Produk Terbaru",
                    description = "Cari produk & info gizi.",
                    onClick = { navController.navigate("product_list") }
                )
                DashboardMenuItemStyled(
                    icon = Icons.Default.Person,
                    title = "Profil Saya",
                    description = "Edit detail akun Anda.",
                    onClick = { navController.navigate("edit_profile") }
                )
                DashboardMenuItemStyled(
                    icon = Icons.Default.TravelExplore,
                    title = "Jelajahi Lebih Lanjut",
                    description = "Kunjungi Open Food Facts.",
                    onClick = {
                        try {
                            context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse("https://id.openfoodfacts.org/")))
                        } catch (e: Exception) {
                            Toast.makeText(context, "Tidak dapat membuka tautan.", Toast.LENGTH_SHORT).show()
                            e.printStackTrace()
                        }
                    }
                )
            }
        }
    }
}

@Composable
fun DashboardMenuItemStyled(icon: ImageVector, title: String, description: String, onClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        shape = RoundedCornerShape(12.dp),
        elevation = CardDefaults.cardElevation(4.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainer)
    ) {
        Row(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Icon(
                imageVector = icon,
                contentDescription = title,
                modifier = Modifier.size(30.dp),
                tint = MaterialTheme.colorScheme.primary
            )
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface
                )
                Text(
                    text = description,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }
    }
}