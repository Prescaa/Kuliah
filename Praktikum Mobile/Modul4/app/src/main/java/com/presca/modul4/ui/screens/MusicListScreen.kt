package com.presca.modul4.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.bumptech.glide.integration.compose.ExperimentalGlideComposeApi
import com.bumptech.glide.integration.compose.GlideImage
import com.presca.modul4.models.Music
import com.presca.modul4.viewmodel.MusicViewModel

@OptIn(ExperimentalGlideComposeApi::class, ExperimentalMaterial3Api::class)
@Composable
fun MusicListScreen(
    viewModel: MusicViewModel,
    onMusicClick: (Music) -> Unit,
    onExternalClick: (String) -> Unit
) {
    val musicList = viewModel.musicList.collectAsState().value

    Scaffold(
        topBar = { TopAppBar(title = { Text("List of Twice's Best Songs") }) }
    ) { padding ->
        LazyColumn(
            contentPadding = padding,
            modifier = Modifier.fillMaxSize().padding(8.dp)
        ) {
            items(musicList) { music ->
                Card(
                    modifier = Modifier.fillMaxWidth().padding(vertical = 10.dp),
                    shape = RoundedCornerShape(16.dp),
                    elevation = CardDefaults.cardElevation(6.dp)
                ) {
                    Row(modifier = Modifier.padding(12.dp)) {
                        GlideImage(
                            model = music.imageUrl,
                            contentDescription = music.title,
                            modifier = Modifier.size(120.dp).clip(RoundedCornerShape(12.dp))
                        )
                        Spacer(Modifier.width(16.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Text(music.title, fontSize = 18.sp, style = MaterialTheme.typography.titleMedium)
                            Text("Tanggal Rilis: ${music.year}", fontSize = 14.sp)
                            Spacer(Modifier.height(8.dp))
                            Text("Tentang Lagu Ini:", fontSize = 12.sp, fontWeight = FontWeight.Bold)
                            Text(music.description, fontSize = 12.sp, maxLines = 3)
                            Spacer(Modifier.height(12.dp))
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.spacedBy(8.dp)
                            ) {
                                Button(onClick = { onExternalClick(music.externalUrl) }, modifier = Modifier.weight(1f)) {
                                    Text("Info")
                                }
                                Button(onClick = { onMusicClick(music) }, modifier = Modifier.weight(1f)) {
                                    Text("Detail")
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}