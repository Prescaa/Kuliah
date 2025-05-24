package com.presca.modul4.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.bumptech.glide.integration.compose.ExperimentalGlideComposeApi
import com.bumptech.glide.integration.compose.GlideImage
import com.presca.modul4.models.Music
import androidx.compose.foundation.shape.RoundedCornerShape

@OptIn(ExperimentalGlideComposeApi::class, ExperimentalMaterial3Api::class)
@Composable
fun MusicDetailScreen(music: Music, navController: NavController) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(music.title, color = MaterialTheme.colorScheme.onPrimary) },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface)
            )
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier.padding(padding).padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            item {
                GlideImage(
                    model = music.imageUrl,
                    contentDescription = music.title,
                    modifier = Modifier.fillMaxWidth().height(400.dp).clip(RoundedCornerShape(16.dp))
                )
            }
            item {
                Text("Judul: ${music.title}", style = MaterialTheme.typography.titleLarge)
            }
            item {
                Text("Tanggal Rilis: ${music.year}")
            }
            item {
                Text("Tentang Lagu Ini:", style = MaterialTheme.typography.titleMedium)
            }
            item {
                Text(music.description, style = MaterialTheme.typography.bodyMedium)
            }
        }
    }
}