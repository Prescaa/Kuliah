package com.presca.modul5.presentation.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Info
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.bumptech.glide.integration.compose.ExperimentalGlideComposeApi
import com.bumptech.glide.integration.compose.GlideImage
import com.presca.modul5.domain.model.CountryInfo

@OptIn(ExperimentalGlideComposeApi::class, ExperimentalMaterial3Api::class)
@Composable
fun CountryDetailScreen(
    country: CountryInfo,
    navController: NavController,
    onClickInfo: () -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(country.name) },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Kembali")
                    }
                },
                actions = {
                    IconButton(onClick = onClickInfo) {
                        Icon(Icons.Default.Info, contentDescription = "Info")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .padding(padding)
                .padding(16.dp)
                .verticalScroll(rememberScrollState())
        ) {
            GlideImage(
                model = country.flagUrl,
                contentDescription = "Bendera ${country.name}",
                modifier = Modifier
                    .fillMaxWidth()
                    .height(200.dp)
                    .clip(MaterialTheme.shapes.medium)
            )

            Spacer(modifier = Modifier.height(24.dp))

            Text(
                text = "Nama Resmi:",
                style = MaterialTheme.typography.labelLarge
            )
            Text(
                text = country.officialName,
                style = MaterialTheme.typography.bodyLarge,
                modifier = Modifier.padding(bottom = 16.dp)
            )

            Text(
                text = "Informasi:",
                style = MaterialTheme.typography.labelLarge
            )
            Text(
                text = country.description,
                style = MaterialTheme.typography.bodyLarge,
                modifier = Modifier.padding(bottom = 16.dp)
            )

            Button(
                onClick = onClickInfo,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Buka Info Lengkap")
            }
        }
    }
}